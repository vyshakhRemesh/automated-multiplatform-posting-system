
from datetime import datetime, timezone

import httpx

from app.config import (
    LINKEDIN_ACCESS_TOKEN,
    LINKEDIN_PERSON_ID,
    LINKEDIN_VERSION,
)
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult


class LinkedInPlatform(BasePlatform):
    name = "LinkedIn"

    async def publish(self, message: str, cta_url: str) -> PlatformResult:
        if not LINKEDIN_ACCESS_TOKEN or not LINKEDIN_PERSON_ID:
            raise RuntimeError("LinkedIn credentials are not configured")

        endpoint = "https://api.linkedin.com/rest/posts"

        headers = {
            "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
            "Content-Type": "application/json",
            "LinkedIn-Version": LINKEDIN_VERSION,
            "X-Restli-Protocol-Version": "2.0.0",
        }

        payload = {
            "author": f"urn:li:person:{LINKEDIN_PERSON_ID}",
            "commentary": f"{message}\n\n{cta_url}",
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": [],
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                endpoint,
                headers=headers,
                json=payload,
            )
            response.raise_for_status()

        post_id = response.headers.get("x-restli-id")

        if not post_id:
            raise RuntimeError(
                "LinkedIn did not return a post identifier"
            )

        posted_url = (
            "https://www.linkedin.com/feed/update/"
            f"{post_id}/"
        )

        return PlatformResult(
            platform=self.name,
            status="success",
            posted_url=posted_url,
            public_access=True,
            datetime=datetime.now(timezone.utc),
            error=None,
        )
