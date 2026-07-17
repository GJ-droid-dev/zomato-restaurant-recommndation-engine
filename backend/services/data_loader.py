import pandas as pd
import numpy as np
import re
from backend.config import DATA_PATH
import logging

logger = logging.getLogger(__name__)

# Module-level cache for the dataset
_df_cache = None

def load_and_clean_data() -> pd.DataFrame:
    """Loads and preprocesses the Zomato dataset."""
    global _df_cache
    if _df_cache is not None:
        return _df_cache

    logger.info(f"Loading dataset from {DATA_PATH}...")
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        logger.error(f"FATAL: zomato.csv not found at {DATA_PATH}")
        raise

    if len(df) == 0:
        raise ValueError("Dataset is empty.")

    # 1. Keep only relevant columns and rename them
    cols_to_keep = ['name', 'location', 'cuisines', 'approx_cost(for two people)', 'rate', 'votes']
    # Check if expected columns exist
    missing_cols = [c for c in cols_to_keep if c not in df.columns]
    if missing_cols:
        raise KeyError(f"Missing expected columns in dataset: {missing_cols}")

    df = df[cols_to_keep].copy()
    df.rename(columns={
        'approx_cost(for two people)': 'cost_for_two',
        'rate': 'rating'
    }, inplace=True)

    # 2. Drop duplicates based on name and location
    df.drop_duplicates(subset=['name', 'location'], inplace=True)

    # 3. Handle nulls
    df.dropna(subset=['name', 'location'], inplace=True)
    df['cuisines'] = df['cuisines'].fillna('unknown')

    # 4. Clean 'rating' column (e.g., '4.1/5', 'NEW', '-') -> float
    def clean_rating(r):
        if pd.isna(r) or r in ('NEW', '-'):
            return 0.0
        r = str(r).replace('/5', '').strip()
        try:
            return float(r)
        except ValueError:
            return 0.0

    df['rating'] = df['rating'].apply(clean_rating)

    # 5. Clean 'cost_for_two' column (e.g., '1,200', '800') -> float
    def clean_cost(c):
        if pd.isna(c):
            return 0.0
        c = str(c)
        c = re.sub(r'[^\d.]', '', c)
        try:
            return float(c)
        except ValueError:
            return 0.0

    df['cost_for_two'] = df['cost_for_two'].apply(clean_cost)

    # 6. Normalise 'location'
    df['location'] = df['location'].astype(str).str.strip().str.title()

    # 7. Normalise 'cuisines' into a list of lowercase strings
    def parse_cuisines(c):
        return [x.strip().lower() for x in str(c).split(',') if x.strip()]
    
    df['cuisines'] = df['cuisines'].apply(parse_cuisines)

    # 8. Map cost to budget brackets
    def get_budget_bracket(cost):
        if cost <= 500:
            return 'low'
        elif cost <= 1500:
            return 'medium'
        else:
            return 'high'
            
    df['budget_bracket'] = df['cost_for_two'].apply(get_budget_bracket)

    _df_cache = df
    logger.info(f"Dataset successfully loaded and preprocessed. Total rows: {len(df)}")
    return df

def get_locations() -> list[str]:
    """Returns a sorted list of unique locations."""
    df = load_and_clean_data()
    # To avoid overwhelming UI, return top 100 locations by count if too many
    location_counts = df['location'].value_counts()
    top_locations = location_counts.head(100).index.tolist()
    return sorted(top_locations)

def get_cuisines() -> list[str]:
    """Returns a sorted list of unique cuisines."""
    df = load_and_clean_data()
    all_cuisines = set()
    for cuisines_list in df['cuisines']:
        all_cuisines.update(cuisines_list)
    return sorted(list(all_cuisines))
