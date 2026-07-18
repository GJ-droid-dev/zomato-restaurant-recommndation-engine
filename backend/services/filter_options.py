import pandas as pd
from backend.services.data_loader import load_and_clean_data
import logging

logger = logging.getLogger(__name__)

# Budget bracket labels for the UI
BUDGET_LABELS = {
    "low": "Low (<= 500)",
    "medium": "Medium (<= 1500)",
    "high": "High (> 1500)",
}

def get_available_options(location: str = "", budget: str = "", cuisine: str = "") -> dict:
    """
    Given the user's current selections, returns the valid options
    for ALL fields plus a match count.
    """
    df = load_and_clean_data()
    filtered = df.copy()

    # Apply whichever filters are already set
    if location:
        filtered = filtered[filtered['location'].str.contains(location, case=False, na=False)]

    if budget and not filtered.empty:
        filtered = filtered[filtered['budget_bracket'] == budget.lower()]

    if cuisine and not filtered.empty:
        cuisine_lower = cuisine.lower().strip()
        filtered = filtered[filtered['cuisines'].apply(
            lambda c_list: any(cuisine_lower in c for c in c_list)
        )]

    match_count = len(filtered)
    highest_rating = round(float(filtered['rating'].max()), 1) if not filtered.empty else 0.0

    # --- Derive available options from filtered data ---

    # Locations: derived from data filtered by budget + cuisine only (not location itself)
    loc_base = df.copy()
    if budget:
        loc_base = loc_base[loc_base['budget_bracket'] == budget.lower()]
    if cuisine and not loc_base.empty:
        cuisine_lower = cuisine.lower().strip()
        loc_base = loc_base[loc_base['cuisines'].apply(
            lambda c_list: any(cuisine_lower in c for c in c_list)
        )]
    location_counts = loc_base['location'].value_counts()
    available_locations = sorted(location_counts.head(100).index.tolist())

    # Cuisines: derived from data filtered by location + budget only (not cuisine itself)
    cui_base = df.copy()
    if location:
        cui_base = cui_base[cui_base['location'].str.contains(location, case=False, na=False)]
    if budget and not cui_base.empty:
        cui_base = cui_base[cui_base['budget_bracket'] == budget.lower()]
    available_cuisines_set = set()
    if not cui_base.empty:
        for cuisines_list in cui_base['cuisines']:
            available_cuisines_set.update(cuisines_list)
    available_cuisines = sorted(list(available_cuisines_set))

    # Budgets: derived from data filtered by location + cuisine only (not budget itself)
    bud_base = df.copy()
    if location:
        bud_base = bud_base[bud_base['location'].str.contains(location, case=False, na=False)]
    if cuisine and not bud_base.empty:
        cuisine_lower = cuisine.lower().strip()
        bud_base = bud_base[bud_base['cuisines'].apply(
            lambda c_list: any(cuisine_lower in c for c in c_list)
        )]
    available_budget_keys = bud_base['budget_bracket'].unique().tolist() if not bud_base.empty else []
    # Preserve order: low, medium, high
    ordered_budgets = [k for k in ["low", "medium", "high"] if k in available_budget_keys]
    available_budgets = [{"value": k, "label": BUDGET_LABELS[k]} for k in ordered_budgets]

    return {
        "locations": available_locations,
        "cuisines": available_cuisines,
        "budgets": available_budgets,
        "match_count": match_count,
        "highest_rating": highest_rating,
    }
