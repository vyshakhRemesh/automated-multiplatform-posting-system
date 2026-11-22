
from fastapi import FastAPI

from app.schemas import PostingRequest, PostingResponse
from app.services.posting_service import PostingService

from app.platforms.mastodon import MastodonPlatform
from app.platforms.bluesky import BlueskyPlatform
from app.platforms.reddit import RedditPlatform
from app.platforms.wordpress import WordPressPlatform
from app.platforms.linkedin import LinkedInPlatform


app = FastAPI(
    title="Automated Multi-Platform Posting System",
    description="Publish content across multiple platforms using their APIs",
    version="1.0.0"
)

platforms = [
    MastodonPlatform(),
    BlueskyPlatform(),
    RedditPlatform(),
    WordPressPlatform(),
    LinkedInPlatform(),
]

posting_service = PostingService(platforms)


@app.post("/posting", response_model=PostingResponse)
async def create_post(request: PostingRequest):

    results = await posting_service.publish_to_all(
        message=request.message,
        cta_url=request.cta_url
    )

    successful_posts = any(
        result.status == "success"
        for result in results
    )

    return PostingResponse(
        success=successful_posts,
        results=results
    )
