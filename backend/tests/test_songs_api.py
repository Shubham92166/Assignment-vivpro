API_PREFIX = "/api/v1"

def test_list_songs_api(client):
    response = client.get(f"{API_PREFIX}/songs?skip=0&limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_search_song_not_found(client):
    response = client.get(f"{API_PREFIX}/songs/search?title=unknownsong")
    assert response.status_code == 404


def test_rate_song_api_success(client):
    response= client.post("/api/v1/songs/1/rate", json={"rating": 4})
    assert response.status_code == 200
    assert response.json()["rating"] == 4


def test_rate_song_invalid_rating(client):
    response = client.post(
    "/api/v1/songs/1/rate",
    json={"rating": 10}
    )
    assert response.status_code == 422



def test_rate_song_missing_rating(client):
    response = client.post(f"{API_PREFIX}/songs/1/rate")
    assert response.status_code == 422


def test_rate_song_not_found(client):
    response = client.post(
    "/api/v1/songs/999/rate",
    json={"rating": 4}
    )
    assert response.status_code == 404
