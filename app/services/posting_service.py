import asyncio
from datetime import datetime, timezone

from app.schemas import PlatformResult
from app.platforms.base import BasePlatform


class PostingService:

    def __init__(self, platforms: list[BasePlatform]):
        self.platforms = platforms

    async def post_to_platform(
        self,
        platform: BasePlatform,
        message: str,
        cta_url: str
    ) -> PlatformResult:

        platform_name = getattr(
            platform, "name", platform.__class__.__name__
        )

        try:
            return await platform.publish(message, cta_url)

        except Exception as error:
            return PlatformResult(
                platform=platform_name,
                status="failure",
                posted_url=None,
                public_access=None,
                datetime=datetime.now(timezone.utc),
                error=str(error)
            )

    async def publish_to_all(
        self,
        message: str,
        cta_url: str
    ) -> list[PlatformResult]:

        tasks = [
            self.post_to_platform(platform, message, cta_url)
            for platform in self.platforms
        ]

        results = await asyncio.gather(*tasks)

        return results