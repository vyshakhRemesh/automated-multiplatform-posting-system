
import asyncio

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
            platform,
            "name",
            platform.__class__.__name__
        )

        try:
            result = await asyncio.wait_for(
                platform.publish(message, cta_url),
                timeout=30.0
            )
            return result

        except asyncio.TimeoutError:
            error_message = "Platform request timed out"

        except Exception as error:
            error_message = str(error)

        return PlatformResult(
            platform=platform_name,
            status="failed",
            posted_url=None,
            public_access=False,
            datetime=None,
            error=error_message
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

        return await asyncio.gather(*tasks)
