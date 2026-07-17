from backend.services.data_loader import load_and_clean_data, get_locations, get_cuisines

def test_pipeline():
    df = load_and_clean_data()
    print(f"Data shape after cleaning: {df.shape}")
    
    locs = get_locations()
    print(f"Total unique locations returned: {len(locs)}")
    print(f"First 5 locations: {locs[:5]}")
    
    cuisines = get_cuisines()
    print(f"Total unique cuisines: {len(cuisines)}")
    print(f"First 5 cuisines: {cuisines[:5]}")
    
    print("\nSample row:")
    print(df.iloc[0].to_dict())
    print("\n✅ Phase 2 Data Pipeline tests passed!")

if __name__ == "__main__":
    test_pipeline()
