from pydantic import BaseModel , Field
from typing import List
from app.schemas.movie import Movie

class SearchRequest(BaseModel):
    query: str = Field(
        ... , 
        min_length=3 , 
        description="Natural language movie search query" , 
        example="A mind bending sci-fi movie like inception.",
    )

class SearchResponse(BaseModel):
    result: List[Movie]
    
