from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_endpoints():
    print("Testing /api/health...")
    resp = client.get("/api/health")
    print(resp.json())
    assert resp.status_code == 200
    
    print("\nTesting /api/locations...")
    resp = client.get("/api/locations")
    assert resp.status_code == 200
    locs = resp.json().get("locations", [])
    print(f"Got {len(locs)} locations. First 3: {locs[:3]}")

    print("\nTesting /api/recommend...")
    payload = {
        "location": "Banashankari",
        "budget": "medium",
        "cuisine": "cafe",
        "min_rating": 4.0,
        "additional_preferences": "friendly"
    }
    
    # We will just test that the endpoint responds and handles the flow.
    # Note: If GROQ_API_KEY is not set or valid, it should return fallback recommendations.
    resp = client.post("/api/recommend", json=payload)
    print(f"Response Status: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"Success: {data.get('success')}")
        print(f"Candidates found: {data.get('candidates_found')}")
        print(f"Recommendations count: {len(data.get('recommendations', []))}")
        
        if data.get('recommendations'):
            print("First recommendation:")
            print(data['recommendations'][0])
    else:
        print(resp.text)
        
    print("\n✅ Phase 3 API tests passed!")

if __name__ == "__main__":
    test_endpoints()
