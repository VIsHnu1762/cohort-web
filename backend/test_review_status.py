"""
Test review submission and check if status updates correctly
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

# Login as mentor
print("1. Logging in as mentor...")
login_response = requests.post(
    f"{BASE_URL}/auth/token/",
    json={"username": "mentor", "password": "mentor123"}
)

if login_response.status_code != 200:
    print(f"❌ Login failed: {login_response.status_code}")
    print(login_response.text)
    exit(1)

token = login_response.json()['access']
print(f"✅ Logged in. Token: {token[:30]}...")

headers = {"Authorization": f"Bearer {token}"}

# Get CLT submissions before review
print("\n2. Fetching CLT submissions...")
subs_response = requests.get(
    f"{BASE_URL}/mentor/pillar/clt/submissions/?status=all",
    headers=headers
)

if subs_response.status_code != 200:
    print(f"❌ Failed to get submissions: {subs_response.status_code}")
    print(subs_response.text)
    exit(1)

submissions = subs_response.json()['submissions']
print(f"✅ Found {len(submissions)} submissions")

if not submissions:
    print("❌ No submissions found to test")
    exit(1)

# Get first pending submission
test_sub = None
for sub in submissions:
    if sub['status'] == 'pending':
        test_sub = sub
        break

if not test_sub:
    print("❌ No pending submissions found")
    print(f"Available submissions: {[s['status'] for s in submissions]}")
    exit(1)

print(f"\n📋 Test submission:")
print(f"   ID: {test_sub['id']}")
print(f"   DB ID: {test_sub['dbId']}")
print(f"   Title: {test_sub['title']}")
print(f"   Status: {test_sub['status']}")
print(f"   Model Type: {test_sub['modelType']}")

# Approve the submission
print("\n3. Approving submission...")
review_data = {
    'pillar': 'clt',
    'submission_id': test_sub['dbId'],
    'submission_type': test_sub['modelType'],
    'action': 'approve',
    'comment': 'Great work! Approved for testing.'
}

print(f"Review data: {json.dumps(review_data, indent=2)}")

review_response = requests.post(
    f"{BASE_URL}/mentor/review/",
    headers=headers,
    json=review_data
)

print(f"\nReview response status: {review_response.status_code}")
print(f"Review response: {json.dumps(review_response.json(), indent=2)}")

if review_response.status_code != 200:
    print("❌ Review failed")
    exit(1)

print("✅ Review successful!")

# Fetch submissions again to verify status changed
print("\n4. Fetching submissions again to verify status...")
subs_response2 = requests.get(
    f"{BASE_URL}/mentor/pillar/clt/submissions/?status=all",
    headers=headers
)

if subs_response2.status_code != 200:
    print(f"❌ Failed to get submissions: {subs_response2.status_code}")
    exit(1)

submissions2 = subs_response2.json()['submissions']
updated_sub = next((s for s in submissions2 if s['dbId'] == test_sub['dbId']), None)

if updated_sub:
    print(f"\n📋 Updated submission:")
    print(f"   ID: {updated_sub['id']}")
    print(f"   Title: {updated_sub['title']}")
    print(f"   OLD Status: {test_sub['status']}")
    print(f"   NEW Status: {updated_sub['status']}")
    
    if updated_sub['status'] == 'approved':
        print("\n✅ SUCCESS! Status updated to 'approved'")
    else:
        print(f"\n❌ FAILED! Status is still '{updated_sub['status']}' instead of 'approved'")
else:
    print("\n❌ Could not find updated submission")

# Check stats
print("\n5. Checking stats...")
stats_response = requests.get(
    f"{BASE_URL}/mentor/pillar/clt/stats/",
    headers=headers
)

if stats_response.status_code == 200:
    stats = stats_response.json()
    print(f"Stats: {json.dumps(stats, indent=2)}")
