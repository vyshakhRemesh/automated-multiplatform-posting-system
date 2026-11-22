
from fastapi.testclient import TestClient

import app.main as main
from app.schemas import PlatformResult


client = TestClient(main.app)


class FakePostingService:
    async def publish_to_all(self, message, cta_url):
        return [
            PlatformResult(
                platform="TestPlatform",
                status="success",
                posted_url="https://example.com/post/1",
                public_access=True,
                datetime=None,
                error=None
            )
        ]


def test_posting_endpoint_success(monkeypatch):
    monkeypatch.setattr(
        main,
        "posting_service",
        FakePostingService()
    )

    response = client.post(
        "/posting",
        json={
            "message": "Check this out https://example.com"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert len(data["results"]) == 1
    assert data["results"][0]["platform"] == "TestPlatform"
    assert data["results"][0]["status"] == "success"


def test_posting_endpoint_invalid_request():
    response = client.post(
        "/posting",
        json={
            "message": "Hello without a URL"
        }
    )

    assert response.status_code == 422
