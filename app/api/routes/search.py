from fastapi import APIRouter , Query , Depends , Request
from typing import List
from app.schemas.movie import Movie
from app.services.llm_service import extract_intent
from app.services.tmdb_service import search_by_intent
from app.api.utils.rate_limiter import RateLimiter

router = APIRouter(prefix="/api/search" , tags=["Search"])

rate_limiter = RateLimiter(max_requests=30 , window_time=60)

def rate_limit(req: Request):
    rate_limiter.is_valid(request=req)

@router.get("" , response_model=List[Movie])
def search_movies(request: Request , query: str = Query(..., min_length=3) , _:None = Depends(rate_limit)):
    print("Called search_movie endpoint...")
    result = search_by_intent(query)
    return result