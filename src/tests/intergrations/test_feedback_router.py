import json

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.mark.parametrize("data", [
    {
        "movie_id": 0,
        "model_type": "tmdb-sim",
        "like": True
    },
    {
        "movie_id": 1,
        "model_type": "glove-sim",
        "like": False
    }
])
def test_like_similar_movie_200(data):

    url = "/v1/user/feedback/like/similar/movie"
    response = client.post(url=url, data=json.dumps(data))
    assert response.status_code == 200


@pytest.mark.parametrize("data", [
    {
        "movie_id": "str",
        "model_type": "tmdb-sim",
        "like": True
    },
    {
        "movie_id": "1",
        "model_type": "diff-sim",
        "like": False
    },
    {
        "movie_id": "1",
        "model_type": "tmdb-sim",
        "like": "like"
    }
])
def test_like_similar_movie_422(data):

    url = "/v1/user/feedback/like/similar/movie"
    response = client.post(url=url, data=json.dumps(data))
    assert response.status_code == 422
