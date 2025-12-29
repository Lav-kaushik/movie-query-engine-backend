from fastapi import APIRouter , HTTPException , Depends , Request
from typing import List
from app.schemas.movie import MovieDetails
from app.services.llm_service import extract_intent
from app.services.tmdb_service import get_movie_by_id
from app.api.utils.rate_limiter import RateLimiter

router = APIRouter(prefix="/api/movies" , tags=["Movies"])

rate_limiter = RateLimiter(max_requests=30 , window_time=60)

def rate_limit(req: Request):
    rate_limiter.is_valid(req)

@router.get("/{movie_id}" , response_model=MovieDetails)
def search_movie_by_id(request: Request , movie_id: int , _:None = Depends(rate_limit)):
    movie = get_movie_by_id(movie_id=movie_id)
    if not movie:
        raise HTTPException(status_code=404 , detail="Movie Not Found.")
    return movie