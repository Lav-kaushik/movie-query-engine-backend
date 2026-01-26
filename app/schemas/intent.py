from typing import List

from pydantic import BaseModel, Field


class SearchIntent(BaseModel):
    titles: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    actors: List[str] = Field(default_factory=list)
    directors: List[str] = Field(default_factory=list)
    genres: List[str] = Field(default_factory=list)
