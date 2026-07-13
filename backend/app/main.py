from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from core.config import get_settings
from services.influencer_service import InfluencerService

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Influencer Finder API is running", "docs": "/docs"}

@app.get("/influencers")
async def get_influencers(
    topic: str = Query(..., description="Topic to search for"),
    top_n: int = Query(10, description="Number of top influencers"),
    platform: str = Query(None, description="Filter by platform")
):
    service = InfluencerService()
    results = service.find_influencers(topic, top_n, platform)
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
