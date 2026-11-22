from fastapi import FastAPI
from app.schemas import PostingRequest, PostingResponse

app = FastAPI(
    title="Automated Multi-Platform Posting System",
    description="API for publishing posts across multiple platforms",
    version="1.0.0"
)


@app.post("/posting", response_model=PostingResponse)
async def create_post(request: PostingRequest):

    return PostingResponse(results=[])