from pydantic import BaseModel
from typing import List, Dict, Any

class Recommendation(BaseModel):
    rank: int
    name: str
    cuisine: str
    rating: float
    cost_for_two: float
    explanation: str

class RecommendResponse(BaseModel):
    success: bool
    query: Dict[str, Any]
    candidates_found: int
    recommendations: List[Recommendation]
