# 🎬 Movie Query Engine – Backend

This is the backend service for the **Movie Query Engine**, built using **FastAPI**.  
It allows users to search movies using natural language queries and fetch detailed movie information using the **TMDB API**, with optional **LLM-based intent extraction**.

---

## 🚀 Features

- 🔍 Search movies using natural language queries
- 🤖 LLM-based intent extraction (movie titles / keywords)
- 🎞️ Fetch detailed movie information:
  - Poster
  - Overview
  - Genres
  - Cast
  - Directors
  - Trailer (YouTube)
- ⚡ In-memory caching for performance
- 🚦 Basic rate limiting
- 🌐 CORS enabled (frontend-ready)
- 📄 Auto-generated Swagger docs

---

## 🛠 Tech Stack

- **FastAPI**
- **Python 3.10+**
- **TMDB API**
- **Groq LLM API**
- **Pydantic v2**
- **Requests**
- **Uvicorn**

---

## 📁 Project Structure  

backend/
├── app/
│ ├── api/
│ │ └── routes/
│ │ ├── search.py
│ │ └── movies.py
│ ├── services/
│ │ ├── tmdb_service.py
│ │ ├── movie_service.py
│ │ ├── search_service.py
│ │ └── llm_service.py
│ ├── schemas/
│ │ └── movie.py
│ ├── utils/
│ │ ├── cache.py
│ │ └── rate_limiter.py
│ └── main.py
├── requirements.txt
└── README.md


---

## 🔑 API Keys Required

You need the following API keys:

1. **TMDB API Key**
   - Get it from: https://www.themoviedb.org/settings/api

2. **Groq API Key**
   - Get it from: https://console.groq.com

---

## ▶️ Run Locally (Step-by-Step)

### 1 Clone the repository

```bash
git clone https://github.com/Lav-kaushik/movie-query-engine-backend.git
cd backend
```
---

### 2 Create virtual environment
python -m venv .venv

source .venv/bin/activate   # Linux / macOS

.venv\Scripts\activate    # Windows

---

### 3 Install Dependencies
pip install -r requirements.txt

---

### 4 Set Environment variables in .env
TMDB_API_KEY=your_tmdb_api_key_here

GROQ_API_KEY=your_groq_api_key_here

---

### 5 Run the server
uvicorn app.main:app --reload
#### the backend will be available at
http://127.0.0.1:8000/docs

---

## Available endpoints

GET /api/search

GET /api/movies/{movie_id}

---








