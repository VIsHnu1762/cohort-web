"""
Test CLT submission with file upload
"""
import requests
import io

BASE_URL = "http://127.0.0.1:8000/api"

# First get token
print("1. Getting auth token...")
auth_response = requests.post(
    f"{BASE_URL}/auth/token/",
    json={"username": "testuser", "password": "testpass123"}
)
token = auth_response.json()['access']
print(f"✓ Token: {token[:50]}...")

headers = {"Authorization": f"Bearer {token}"}

# Create submission with file
print("\n2. Creating submission with file...")

# Create a fake file
fake_file = io.BytesIO(b"This is a test certificate file content")
fake_file.name = "certificate.txt"

files = {
    'files': ('certificate.txt', fake_file, 'text/plain')
}

data = {
    'title': 'Test Course with File',
    'description': 'This is a test submission with file upload',
    'platform': 'Udemy',
    'completion_date': '2025-12-01'
}

response = requests.post(
    f"{BASE_URL}/clt/submissions/",
    headers=headers,
    data=data,
    files=files
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json() if response.text else 'Empty'}")

if response.status_code == 201:
    submission = response.json()
    submission_id = submission['id']
    print(f"\n✓ Submission created: ID={submission_id}")
    print(f"  Files count: {len(submission.get('files', []))}")
    
    # Try to submit it
    print(f"\n3. Submitting for review...")
    submit_response = requests.post(
        f"{BASE_URL}/clt/submissions/{submission_id}/submit/",
        headers=headers
    )
    print(f"Submit Status: {submit_response.status_code}")
    print(f"Submit Response: {submit_response.json()}")
    
    if submit_response.status_code == 200:
        print("\n✅ SUCCESS! Submission completed.")
    else:
        print("\n❌ Submit failed")
else:
    print("\n❌ Create failed")
    print(f"Error details: {response.text}")
