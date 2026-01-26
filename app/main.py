from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.movies import router as movies_router
from app.api.routes.search import router as search_router

app = FastAPI(title="Movie Query Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(movies_router)
app.include_router(search_router)
