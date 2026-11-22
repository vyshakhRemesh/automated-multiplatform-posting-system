
from datetime import datetime, timezone

import httpx

from app.config import MASTODON_BASE_URL, MASTODON_ACCESS_TOKEN
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult


class MastodonPlatform(BasePlatform):

    name = "Mastodon"

    async def publish(
        self,
        message: str,
        cta_url: str
    ) -> PlatformResult:

        if not MASTODON_BASE_URL or not MASTODON_ACCESS_TOKEN:
            raise RuntimeError("Mastodon credentials are not configured")

        endpoint = f"{MASTODON_BASE_URL}/api/v1/statuses"

        payload = {
            "status": f"{message}\n\n{cta_url}",
            "visibility": "public"
        }

        headers = {
            "Authorization": f"Bearer {MASTODON_ACCESS_TOKEN}"
        }

        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(
                endpoint,
                json=payload,
                headers=headers
            )

            response.raise_for_status()
            data = response.json()

        return PlatformResult(
            platform=self.name,
            status="success",
            posted_url=data.get("url"),
            public_access=(
                data.get("visibility") == "public"
                if data.get("visibility") is not None
                else None
            ),
            datetime=datetime.now(timezone.utc),
            error=None
        )
