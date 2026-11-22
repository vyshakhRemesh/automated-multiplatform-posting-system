
from datetime import datetime, timezone

import httpx

from app.config import (
    BLUESKY_IDENTIFIER,
    BLUESKY_APP_PASSWORD,
    BLUESKY_HANDLE,
)
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult


class BlueskyPlatform(BasePlatform):
    name = "Bluesky"

    async def publish(self, message: str, cta_url: str) -> PlatformResult:
        if not BLUESKY_IDENTIFIER or not BLUESKY_APP_PASSWORD:
            raise RuntimeError("Bluesky credentials are not configured")

        base_url = "https://bsky.social/xrpc"

        async with httpx.AsyncClient(timeout=20.0) as client:

            # Authenticate with Bluesky
            login_response = await client.post(
                f"{base_url}/com.atproto.server.createSession",
                json={
                    "identifier": BLUESKY_IDENTIFIER,
                    "password": BLUESKY_APP_PASSWORD,
                },
            )
            login_response.raise_for_status()

            session = login_response.json()
            access_token = session["accessJwt"]
            did = session["did"]

            # Create the post
            post_text = f"{message}\n\n{cta_url}"

            post_response = await client.post(
                f"{base_url}/com.atproto.repo.createRecord",
                headers={
                    "Authorization": f"Bearer {access_token}"
                },
                json={
                    "repo": did,
                    "collection": "app.bsky.feed.post",
                    "record": {
                        "text": post_text,
                        "createdAt": datetime.now(
                            timezone.utc
                        ).isoformat(),
                    },
                },
            )
            post_response.raise_for_status()

            post_data = post_response.json()

        uri = post_data.get("uri", "")
        rkey = uri.rsplit("/", 1)[-1] if uri else None

        posted_url = None
        if rkey and BLUESKY_HANDLE:
            posted_url = (
                f"https://bsky.app/profile/"
                f"{BLUESKY_HANDLE}/post/{rkey}"
            )

        return PlatformResult(
            platform=self.name,
            status="success",
            posted_url=posted_url,
            public_access=True,
            datetime=datetime.now(timezone.utc),
            error=None,
        )
