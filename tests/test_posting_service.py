
import pytest

from app.schemas import PlatformResult
from app.services.posting_service import PostingService


class SuccessfulPlatform:
    name = "TestSuccess"

    async def publish(self, message, cta_url):
        return PlatformResult(
            platform=self.name,
            status="success",
            posted_url="https://example.com/post/1",
            public_access=True,
            datetime=None,
            error=None
        )


class FailedPlatform:
    name = "TestFailure"

    async def publish(self, message, cta_url):
        raise RuntimeError("Test API failure")


@pytest.mark.asyncio
async def test_platforms_are_handled_independently():
    service = PostingService([
        SuccessfulPlatform(),
        FailedPlatform()
    ])

    results = await service.publish_to_all(
        message="Check this out https://example.com",
        cta_url="https://example.com"
    )

    assert len(results) == 2

    assert results[0].platform == "TestSuccess"
    assert results[0].status == "success"

    assert results[1].platform == "TestFailure"
    assert results[1].status == "failed"
    assert results[1].error == "Test API failure"
