import json
import logging
import pandas as pd
from groq import Groq, GroqError
from backend.config import GROQ_API_KEY, GROQ_MODEL
from backend.models.response import Recommendation

logger = logging.getLogger(__name__)

# Initialize client; handles missing API key gracefully at call time if needed
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

def get_recommendations(user_prefs: dict, candidates_df: pd.DataFrame) -> list[Recommendation]:
    """Calls Groq API to rank and explain restaurant recommendations."""
    if candidates_df.empty:
        return []

    if not client:
        logger.error("Groq API key not configured. Returning top filters without AI explanations.")
        return _fallback_recommendations(candidates_df)

    # Prepare candidate JSON
    candidates = []
    for _, row in candidates_df.iterrows():
        candidates.append({
            "name": row['name'],
            "location": row['location'],
            "cuisines": ", ".join(row['cuisines']).title(),
            "rating": row['rating'],
            "cost_for_two": row['cost_for_two']
        })
    candidate_json_str = json.dumps(candidates, indent=2)

    system_prompt = """You are an expert restaurant recommendation engine. 
Given the user's preferences and a list of candidate restaurants, rank the best matches and explain why each one is a good fit.

Instructions:
1. Select the top 5 restaurants that best match the preferences.
2. Rank them from 1 to 5 (1 being the best match).
3. For each, provide: rank, name, cuisine, rating, cost_for_two, and a 2-3 sentence explanation of why it is recommended based on the user's specific inputs.
4. You MUST return a JSON object with a single key "recommendations" that contains a list of these objects.

Example expected output format:
{
  "recommendations": [
    {
      "rank": 1,
      "name": "Restaurant Name",
      "cuisine": "Italian, Cafe",
      "rating": 4.5,
      "cost_for_two": 1200.0,
      "explanation": "This restaurant perfectly matches your budget and location. It offers..."
    }
  ]
}"""

    user_prompt = f"""User Preferences:
- Location: {user_prefs.get('location')}
- Budget: {user_prefs.get('budget')}
- Cuisine: {user_prefs.get('cuisine')}
- Minimum Rating: {user_prefs.get('min_rating')}
- Other: {user_prefs.get('additional_preferences', '')}

Candidate Restaurants:
{candidate_json_str}"""

    try:
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        response_text = completion.choices[0].message.content
        data = json.loads(response_text)
        recs_data = data.get("recommendations", [])
        
        recommendations = []
        for rec in recs_data:
            try:
                # Validate with Pydantic model
                recommendation = Recommendation(**rec)
                recommendations.append(recommendation)
            except Exception as e:
                logger.warning(f"Skipping invalid recommendation entry from LLM: {rec}. Error: {e}")
                
        return recommendations[:5]
        
    except Exception as e:
        logger.error(f"LLM API Error: {e}")
        return _fallback_recommendations(candidates_df)

def _fallback_recommendations(candidates_df: pd.DataFrame) -> list[Recommendation]:
    """Fallback if LLM fails: returns top 5 based on pure filtering."""
    recs = []
    for idx, (_, row) in enumerate(candidates_df.head(5).iterrows()):
        recs.append(Recommendation(
            rank=idx + 1,
            name=row['name'],
            cuisine=", ".join(row['cuisines']).title(),
            rating=row['rating'],
            cost_for_two=row['cost_for_two'],
            explanation="AI explanation temporarily unavailable. Recommended based on rating and popularity."
        ))
    return recs
