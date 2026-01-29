import requests
import json

BASE_URL = 'http://localhost:8000/api'

print("=== Testing Mentor API Endpoints ===\n")

# Test without authentication first
print("1. Testing GET /api/mentor/pillar/all/stats/ (no auth)")
try:
    response = requests.get(f'{BASE_URL}/mentor/pillar/all/stats/')
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text}\n")
except Exception as e:
    print(f"   Error: {e}\n")

print("2. Testing GET /api/mentor/pillar/clt/stats/ (no auth)")
try:
    response = requests.get(f'{BASE_URL}/mentor/pillar/clt/stats/')
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text}\n")
except Exception as e:
    print(f"   Error: {e}\n")

print("3. Testing GET /api/mentor/pillar/all/submissions/ (no auth)")
try:
    response = requests.get(f'{BASE_URL}/mentor/pillar/all/submissions/')
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text[:500] if len(response.text) > 500 else response.text}\n")
except Exception as e:
    print(f"   Error: {e}\n")

# Try to login and get token
print("4. Trying to authenticate as admin")
try:
    login_response = requests.post(f'{BASE_URL}/auth/token/', 
                                   json={'username': 'admin', 'password': 'admin123'})
    print(f"   Status: {login_response.status_code}")
    if login_response.status_code == 200:
        token = login_response.json().get('access')
        print(f"   Got token: {token[:50]}...\n")
        
        # Test with authentication
        headers = {'Authorization': f'Bearer {token}'}
        
        print("5. Testing GET /api/mentor/pillar/all/stats/ (with auth)")
        response = requests.get(f'{BASE_URL}/mentor/pillar/all/stats/', headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}\n")
        
        print("6. Testing GET /api/mentor/pillar/clt/submissions/ (with auth)")
        response = requests.get(f'{BASE_URL}/mentor/pillar/clt/submissions/', headers=headers)
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Found {len(data.get('submissions', []))} submissions")
        if data.get('submissions'):
            print(f"   First submission: {json.dumps(data['submissions'][0], indent=2)}\n")
    else:
        print(f"   Login failed: {login_response.text}\n")
except Exception as e:
    print(f"   Error: {e}\n")
