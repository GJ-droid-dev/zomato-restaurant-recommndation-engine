import pandas as pd
from backend.services.data_loader import load_and_clean_data
from backend.config import TOP_N_CANDIDATES
import logging

logger = logging.getLogger(__name__)

def filter_restaurants(location: str, budget: str, cuisine: str, min_rating: float) -> pd.DataFrame:
    """Applies multi-criteria filtering and returns top candidates."""
    df = load_and_clean_data()
    
    # Start with full dataset
    filtered = df.copy()

    # 1. Location match (case-insensitive substring)
    if location and not filtered.empty:
        filtered = filtered[filtered['location'].str.contains(location, case=False, na=False)]

    # 2. Budget match
    if budget and not filtered.empty:
        filtered = filtered[filtered['budget_bracket'] == budget.lower()]

    # 3. Cuisine match
    if cuisine and not filtered.empty:
        cuisine_lower = cuisine.lower().strip()
        filtered = filtered[filtered['cuisines'].apply(lambda c_list: any(cuisine_lower in c for c in c_list))]

    # 4. Rating threshold
    if not filtered.empty:
        filtered = filtered[filtered['rating'] >= min_rating]

    # Handle edge case: 0 results
    if filtered.empty:
        logger.info("0 results with strict filters. Returning empty.")
        return filtered

    # Sort by rating and votes
    filtered = filtered.sort_values(by=['rating', 'votes'], ascending=[False, False])
    
    return filtered.head(TOP_N_CANDIDATES)
