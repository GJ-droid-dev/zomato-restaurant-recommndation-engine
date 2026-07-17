from fastapi import APIRouter, HTTPException
from backend.services.data_loader import get_locations, get_cuisines
from backend.models.request import RecommendRequest
from backend.models.response import RecommendResponse
from backend.services.filter import filter_restaurants
from backend.services.llm import get_recommendations
from backend.utils.cache import llm_cache

router = APIRouter(prefix="/api")

@router.get("/locations")
async def api_locations():
    """Returns a list of available locations."""
    locations = get_locations()
    return {"success": True, "locations": locations}

@router.get("/cuisines")
async def api_cuisines():
    """Returns a list of available cuisines."""
    cuisines = get_cuisines()
    return {"success": True, "cuisines": cuisines}

@router.post("/recommend", response_model=RecommendResponse)
async def get_recommendation(request: RecommendRequest):
    """Fetches AI-powered restaurant recommendations based on preferences."""
    prefs = request.model_dump()
    
    # 1. Check cache
    cached_response = llm_cache.get(prefs)
    if cached_response is not None:
        return RecommendResponse(
            success=True,
            query=prefs,
            candidates_found=len(cached_response),
            recommendations=cached_response
        )

    # 2. Filter candidates
    try:
        candidates_df = filter_restaurants(
            location=request.location,
            budget=request.budget,
            cuisine=request.cuisine,
            min_rating=request.min_rating
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Filtering failed: {e}")

    if candidates_df.empty:
        return RecommendResponse(
            success=True,
            query=prefs,
            candidates_found=0,
            recommendations=[]
        )

    # 3. Get LLM recommendations
    recommendations = get_recommendations(prefs, candidates_df)

    # 4. Cache and return
    llm_cache.set(prefs, recommendations)
    
    return RecommendResponse(
        success=True,
        query=prefs,
        candidates_found=len(candidates_df),
        recommendations=recommendations
    )
