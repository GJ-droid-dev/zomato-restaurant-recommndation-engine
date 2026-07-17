from pydantic import BaseModel, Field
from typing import Literal

class RecommendRequest(BaseModel):
    location: str = Field(..., description="City or locality")
    budget: Literal["low", "medium", "high"] = Field(..., description="Budget bracket")
    cuisine: str = Field(..., description="Preferred cuisine")
    min_rating: float = Field(0.0, ge=0.0, le=5.0, description="Minimum rating out of 5")
    additional_preferences: str = Field("", description="Any other preferences, e.g., family-friendly")
