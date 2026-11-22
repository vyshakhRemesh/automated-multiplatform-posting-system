from fastapi import FastAPI
from app.schemas import PostingRequest, PostingResponse
from app.services.posting_service import PostingService

app = FastAPI(
    title="Automated Multi-Platform Posting System",
    description="API for publishing posts across multiple platforms",
    version="1.0.0"
)

platforms = []

posting_service = PostingService(platforms)


@app.post("/posting", response_model=PostingResponse)
async def create_post(request: PostingRequest):

    results = await posting_service.publish_to_all(
        message=request.message,
        cta_url=str(request.cta_url)
    )


    return PostingResponse(results=results)