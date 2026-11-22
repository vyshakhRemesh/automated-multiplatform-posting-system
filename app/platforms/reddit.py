
from datetime import datetime, timezone

import httpx

from app.config import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USERNAME,
    REDDIT_PASSWORD,
    REDDIT_SUBREDDIT,
    REDDIT_USER_AGENT,
)
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult


class RedditPlatform(BasePlatform):
    name = "Reddit"

    async def publish(self, message: str, cta_url: str) -> PlatformResult:
        credentials = [
            REDDIT_CLIENT_ID,
            REDDIT_CLIENT_SECRET,
            REDDIT_USERNAME,
            REDDIT_PASSWORD,
            REDDIT_SUBREDDIT,
        ]

        if not all(credentials):
            raise RuntimeError("Reddit credentials are not configured")

        async with httpx.AsyncClient(timeout=30.0) as client:

            # Authenticate with Reddit
            auth_response = await client.post(
                "https://www.reddit.com/api/v1/access_token",
                auth=(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET),
                data={
                    "grant_type": "password",
                    "username": REDDIT_USERNAME,
                    "password": REDDIT_PASSWORD,
                },
                headers={
                    "User-Agent": REDDIT_USER_AGENT
                },
            )
            auth_response.raise_for_status()

            auth_data = auth_response.json()
            access_token = auth_data.get("access_token")

            if not access_token:
                raise RuntimeError(
                    f"Reddit authentication failed: {auth_data}"
                )

            # Submit a link post
            post_response = await client.post(
                "https://oauth.reddit.com/api/submit",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "User-Agent": REDDIT_USER_AGENT,
                },
                data={
                    "sr": REDDIT_SUBREDDIT,
                    "kind": "link",
                    "title": message,
                    "url": cta_url,
                    "resubmit": False,
                    "api_type": "json",
                },
            )
            post_response.raise_for_status()

            post_data = post_response.json()

            errors = post_data.get("json", {}).get("errors", [])
            if errors:
                raise RuntimeError(f"Reddit submission failed: {errors}")

            result = post_data.get("json", {}).get("data", {})
            post_url = result.get("url")

            if not post_url:
                raise RuntimeError(
                    "Reddit did not return a URL for the submitted post"
                )

        if post_url.startswith("/"):
            post_url = f"https://www.reddit.com{post_url}"

        return PlatformResult(
            platform=self.name,
            status="success",
            posted_url=post_url,
            public_access=True,
            datetime=datetime.now(timezone.utc),
            error=None,
        )
