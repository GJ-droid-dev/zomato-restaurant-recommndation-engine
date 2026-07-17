import os
from fastapi.testclient import TestClient
from backend.main import app

# Ensure .env is loaded to pick up the user's API key
from dotenv import load_dotenv
load_dotenv(override=True)

client = TestClient(app)

def test_recommendation():
    print(f"GROQ_API_KEY available: {bool(os.getenv('GROQ_API_KEY'))}")
    
    payload = {
        "location": "Bellandur",
        "budget": "medium",  # 1500 maps to 'medium' in our data loader logic
        "cuisine": "",       # Unspecified
        "min_rating": 4.2,
        "additional_preferences": ""
    }
    
    print(f"\nSending request with preferences: {payload}")
    resp = client.post("/api/recommend", json=payload)
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"\nCandidates found: {data.get('candidates_found')}")
        print("-" * 50)
        recs = data.get('recommendations', [])
        for rec in recs:
            print(f"Rank {rec['rank']}: {rec['name']}")
            print(f"Cuisine: {rec['cuisine']}")
            print(f"Rating: {rec['rating']} | Cost for Two: Rs. {rec['cost_for_two']}")
            print(f"Explanation: {rec['explanation']}")
            print("-" * 50)
    else:
        print(f"Error: {resp.status_code}")
        print(resp.text)

if __name__ == "__main__":
    test_recommendation()
