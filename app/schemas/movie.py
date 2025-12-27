from pydantic import BaseModel , Field
from typing import List

class Movie(BaseModel):
    id: int
    title: str
    release_year: int | None = None
    rating: float | None = None
    poster_url: str | None = None
    genre: List[str] = Field(default_factory=list)


class MovieDetails(Movie):
    overview: str | None = None
    cast: List[str] = Field(default_factory=list)
    directors: str | None = None
    trailer_url: str | None = None
