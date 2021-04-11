from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_invalidate_cache_200():

    url = "/v1/cache/invalidate"
    response = client.post(url=url)
    assert response.status_code == 200
