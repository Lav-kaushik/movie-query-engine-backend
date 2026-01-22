def test_get_movie_by_id_success(client):
    movie_id = 155

    response = client.get(f"/api/movies/{movie_id}")

    assert response.status_code == 200

    movie = response.json()
    assert movie["id"] == movie_id
    assert "title" in movie
    assert "release_year" in movie