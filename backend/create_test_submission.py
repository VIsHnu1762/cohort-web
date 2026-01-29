"""
Create a test CLT submission for review testing
"""
import requests

BASE_URL = "http://127.0.0.1:8000/api"

# Login as student
print("1. Logging in as student...")
login_response = requests.post(
    f"{BASE_URL}/auth/token/",
    json={"username": "testuser", "password": "testpass123"}
)

if login_response.status_code != 200:
    print(f"❌ Login failed: {login_response.status_code}")
    print(login_response.text)
    exit(1)

token = login_response.json()['access']
print(f"✅ Logged in. Token: {token[:30]}...")

headers = {"Authorization": f"Bearer {token}"}

# Create CLT submission
print("\n2. Creating CLT submission...")
submission_data = {
    'title': 'Python for Data Science',
    'description': 'Comprehensive Python course covering data analysis and visualization',
    'platform': 'Coursera',
    'completion_date': '2025-12-01',
    'duration': 40,
    'drive_link': 'https://drive.google.com/file/d/test123/view'
}

create_response = requests.post(
    f"{BASE_URL}/clt/submissions/",
    headers=headers,
    json=submission_data
)

if create_response.status_code not in [200, 201]:
    print(f"❌ Create failed: {create_response.status_code}")
    print(create_response.text)
    exit(1)

submission = create_response.json()
submission_id = submission['id']
print(f"✅ Submission created with ID: {submission_id}")
print(f"   Status: {submission['status']}")

# Submit it for review
print("\n3. Submitting for review...")
submit_response = requests.post(
    f"{BASE_URL}/clt/submissions/{submission_id}/submit/",
    headers=headers
)

if submit_response.status_code != 200:
    print(f"❌ Submit failed: {submit_response.status_code}")
    print(submit_response.text)
    exit(1)

print(f"✅ Submitted successfully!")
print(f"   Response: {submit_response.json()}")

print(f"\n✅ Test submission ready for review!")
print(f"   Submission ID: {submission_id}")
