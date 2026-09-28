from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_shorten_and_redirect():
    response = client.post("/shorten", json={"url": "https://www.tru.ca"})
    assert response.status_code == 201
    code = response.json()["code"]

    redirect = client.get(f"/{code}", follow_redirects=False)
    assert redirect.status_code == 307
    assert redirect.headers["location"] == "https://www.tru.ca/"


def test_unknown_code_returns_404():
    response = client.get("/doesnotexist", follow_redirects=False)
    assert response.status_code == 404


def test_invalid_url_rejected():
    response = client.post("/shorten", json={"url": "not a url"})
    assert response.status_code == 422
    