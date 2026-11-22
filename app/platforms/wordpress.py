
from datetime import datetime, timezone

import httpx

from app.config import (
    WORDPRESS_SITE_URL,
    WORDPRESS_USERNAME,
    WORDPRESS_APP_PASSWORD,
)
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult


class WordPressPlatform(BasePlatform):
    name = "WordPress"

    async def publish(self, message: str, cta_url: str) -> PlatformResult:
        if not all([
            WORDPRESS_SITE_URL,
            WORDPRESS_USERNAME,
            WORDPRESS_APP_PASSWORD,
        ]):
            raise RuntimeError("WordPress credentials are not configured")

        endpoint = f"{WORDPRESS_SITE_URL}/wp-json/wp/v2/posts"

        payload = {
            "title": message,
            "content": (
                f"<p>{message}</p>"
                f'<p><a href="{cta_url}">Learn more</a></p>'
            ),
            "status": "publish",
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                endpoint,
                json=payload,
                auth=(WORDPRESS_USERNAME, WORDPRESS_APP_PASSWORD),
            )
            response.raise_for_status()
            data = response.json()

        post_url = data.get("link")
        post_status = data.get("status")

        if not post_url:
            raise RuntimeError("WordPress did not return a post URL")

        return PlatformResult(
            platform=self.name,
            status="success",
            posted_url=post_url,
            public_access=(post_status == "publish"),
            datetime=datetime.now(timezone.utc),
            error=None,
        )
