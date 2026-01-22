def test_search_movies_with_natural_language_query(client):
    query = "movies like interstellar with space travel"

    response = client.get("/api/search", params={"query": query})

    assert response.status_code == 200

    movies = response.json()
    assert isinstance(movies, list)

    for movie in movies:
        assert "title" in movie