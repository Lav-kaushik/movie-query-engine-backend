def normalize_query(query: str) -> str:
    return query.lower().strip()


# building caching key for title , movies
def build_search_cache_key(query: str) -> str:
    return f"search:{normalize_query(query)}"


# building caching key for movie_id , movies
def build_movie_cache_key(movie_id: int) -> str:
    return f"movie:{movie_id}"
