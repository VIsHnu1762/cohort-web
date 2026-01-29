import requests
import json

# Test full leaderboard endpoint
BASE_URL = "http://localhost:8000/api"

# Get token
login_response = requests.post(
    f"{BASE_URL}/auth/token/",
    json={
        "username": "test_mentor",
        "password": "test_password_123"
    }
)

if login_response.status_code == 200:
    token = login_response.json()['access']
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test full leaderboard
    print("Testing full leaderboard endpoint...")
    response = requests.get(
        f"{BASE_URL}/gamification/leaderboard/full_leaderboard/",
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("\n✅ SUCCESS!")
        print(f"Total Students: {data.get('total_students')}")
        print(f"Top Ranks: {len(data.get('top_ranks', []))}")
        print(f"Percentiles: {len(data.get('percentiles', []))}")
        print("\nFull Response:")
        print(json.dumps(data, indent=2))
    else:
        print(f"\n❌ ERROR: {response.text}")
else:
    print(f"Login failed: {login_response.status_code}")
    print(login_response.text)
