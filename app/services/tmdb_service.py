from fastapi import HTTPException
import requests
from typing import List , Optional
from schemas.movie import Movie , MovieDetails
from services.llm_service import extract_intent
from api.utils.cache import LocalCache
from api.utils.cache_keys import build_movie_cache_key , build_search_cache_key


TMDB_BASE_URL="https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p"
TMDB_API_KEY="d52329235f9dfa990eeda588623cf88e"

TMDB_GENRE_MAP = {
    28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy",
    80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family",
    14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music",
    9648: "Mystery", 10749: "Romance", 878: "Science Fiction",
    10770: "TV Movie", 53: "Thriller", 10752: "War", 37: "Western"
}

cache = LocalCache()
SEARCH_CACHE_TTL = 300

def fetch_from_tmdb(search_query: str) -> List[dict]:
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": search_query,
        "language": "en-US",
        "page": 1,
        "include_adult": False
    }

    try:
        response = requests.get(url , params=params , timeout=10)
        response.raise_for_status()

        data = response.json()
        return data.get("results")
    except requests.RequestException as e:
        print(f"Error fetching the data form tmdb: {e}")
        return []
    

def build_poster_url(poster_path: str | None, size: str = "w500") -> str | None:
    if not poster_path:
        return None

    return f"{TMDB_IMAGE_BASE_URL}/{size}{poster_path}"


def convert_tmdb_results(raw_result: List[dict]) -> List[Movie]:
    movies = []

    for item in raw_result:
        release_date = item.get("release_date", "")
        year = int(release_date.split("-")[0]) if release_date else None 

        genre_ids = item.get("genre_ids", [])
        genre_names = [TMDB_GENRE_MAP.get(g_id, "Unknown") for g_id in genre_ids]

        movie = Movie(
            id=item.get("id"),
            title=item.get("title"),
            release_year=year,
            rating=item.get("vote_average"),
            poster_url=build_poster_url(item.get("poster_path")),
            genre=genre_names
        )

        movies.append(movie)
    
    return movies


def search_by_intent(query: str) -> List[Movie]:
    intent = extract_intent(query=query)

    titles = intent.titles
    title: str
    if titles:
        # take the first title
        title = titles[0]
    else:
        title = query.strip()

    cache_key = build_search_cache_key(title)

    # search in cache
    result = cache.get(cache_key)

    if result:
        return result
    
    print(f"Cache miss. Fetching '{title}' from TMDB...")

    # search using tmdb api
    raw_result = fetch_from_tmdb(title)

    movies = convert_tmdb_results(raw_result)

    cache.set(
        key=cache_key,
        value=movies,
        ttl_seconds=SEARCH_CACHE_TTL
    )

    return movies

def fetch_movie_details(movie_id: int , retries:int = 2) -> Optional[dict]:
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "append_to_response": "credits,videos",
        "language": "en-US"
    }

    for attempt in range(retries + 1):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()

        except requests.RequestException:
            if attempt == retries:
                return None
    

def get_movie_by_id(movie_id: int) -> MovieDetails | None:
    cache_key = build_movie_cache_key(movie_id=movie_id)
    
    result = cache.get(cache_key)

    if result:
        return result

    raw_data = fetch_movie_details(movie_id)
    
    if not raw_data:
        return None
    
    # convert to Movie object

    # release date
    release_date = raw_data.get("release_date", "")
    year = int(release_date.split("-")[0]) if release_date else None

    # top 10 cast
    cast = [
        c["name"] for c in raw_data.get("credits" , {}).get("cast" , [])[:10]
    ]

    # directors
    directors = [
        c["name"] for c in raw_data.get("credits" , {}).get("crew" , []) if c.get("job")=="Director"
    ]

    trailer_url = None
    for video in raw_data.get("videos", {}).get("results", []):
        if video.get("type") == "Trailer" and video.get("site") == "YouTube":
            trailer_url = f"https://www.youtube.com/watch?v={video['key']}"
            break


    movie = MovieDetails(
        id=raw_data.get("id"),
        title=raw_data.get("title"),
        release_year=year,
        rating=raw_data.get("vote_average"),
        poster_url=build_poster_url(raw_data.get("poster_path")),
        genre=[g["name"] for g in raw_data.get("genres", [])],
        cast=cast,
        directors=directors,
        overview=raw_data.get("overview"),
        trailer_url=trailer_url,
    )

    # cache the result
    cache.set(
        key=cache_key,
        value=movie,
        ttl_seconds=600
    )

    return movie
    

