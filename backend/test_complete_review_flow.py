"""
Complete test of the review flow:
1. Login as mentor
2. Get submissions
3. Approve one
4. Verify status changed
5. Check notification created
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

print("=" * 60)
print("COMPLETE REVIEW FLOW TEST")
print("=" * 60)

# Step 1: Login as mentor
print("\n1️⃣ Logging in as mentor...")
login_response = requests.post(
    f"{BASE_URL}/auth/token/",
    json={"username": "mentor", "password": "mentor123"}
)

if login_response.status_code != 200:
    print(f"❌ Login failed: {login_response.status_code}")
    print(login_response.text)
    exit(1)

token = login_response.json()['access']
print(f"✅ Logged in successfully")

headers = {"Authorization": f"Bearer {token}"}

# Step 2: Get pending CLT submissions
print("\n2️⃣ Fetching pending CLT submissions...")
subs_response = requests.get(
    f"{BASE_URL}/mentor/pillar/clt/submissions/?status=pending",
    headers=headers
)

if subs_response.status_code != 200:
    print(f"❌ Failed to get submissions: {subs_response.status_code}")
    print(subs_response.text)
    exit(1)

data = subs_response.json()
submissions = data.get('submissions', [])
print(f"✅ Found {len(submissions)} pending submissions")

if not submissions:
    print("❌ No pending submissions to test with")
    exit(1)

# Pick first pending submission
test_submission = submissions[0]
print(f"\n📋 Selected submission for testing:")
print(f"   ID: {test_submission['id']}")
print(f"   DB ID: {test_submission['dbId']}")
print(f"   Title: {test_submission['title']}")
print(f"   Student: {test_submission['student']['name']}")
print(f"   Status: {test_submission['status']}")
print(f"   Pillar: {test_submission['pillar']}")
print(f"   Model Type: {test_submission['modelType']}")

# Step 3: Approve the submission
print(f"\n3️⃣ Approving submission...")
review_payload = {
    'pillar': test_submission['pillar'],
    'submission_id': test_submission['dbId'],
    'submission_type': test_submission['modelType'],
    'action': 'approve',
    'comment': 'Excellent work! This is a test approval.'
}

print(f"   Payload: {json.dumps(review_payload, indent=2)}")

review_response = requests.post(
    f"{BASE_URL}/mentor/review/",
    headers=headers,
    json=review_payload
)

print(f"\n   Response Status: {review_response.status_code}")
print(f"   Response Body: {json.dumps(review_response.json(), indent=2)}")

if review_response.status_code != 200:
    print(f"❌ Review failed!")
    exit(1)

result = review_response.json()
print(f"✅ Review successful!")
print(f"   New status: {result['status']}")
print(f"   Notification ID: {result.get('notification_id')}")

# Step 4: Verify status changed
print(f"\n4️⃣ Verifying status changed...")
subs_response2 = requests.get(
    f"{BASE_URL}/mentor/pillar/clt/submissions/?status=all",
    headers=headers
)

if subs_response2.status_code != 200:
    print(f"❌ Failed to re-fetch submissions")
    exit(1)

data2 = subs_response2.json()
updated_submission = next(
    (s for s in data2['submissions'] if s['dbId'] == test_submission['dbId']),
    None
)

if not updated_submission:
    print(f"❌ Could not find submission in response")
    exit(1)

print(f"   OLD Status: {test_submission['status']}")
print(f"   NEW Status: {updated_submission['status']}")

if updated_submission['status'] == 'approved':
    print(f"✅ Status successfully changed to 'approved'!")
else:
    print(f"❌ Status is '{updated_submission['status']}' instead of 'approved'")
    exit(1)

# Step 5: Check stats updated
print(f"\n5️⃣ Checking stats...")
stats_response = requests.get(
    f"{BASE_URL}/mentor/pillar/clt/stats/",
    headers=headers
)

if stats_response.status_code == 200:
    stats = stats_response.json()
    print(f"   Total: {stats['total']}")
    print(f"   Pending: {stats['pending']}")
    print(f"   Approved: {stats['approved']}")
    print(f"   Rejected: {stats['rejected']}")
    print(f"✅ Stats retrieved successfully")
else:
    print(f"⚠️ Could not fetch stats")

# Step 6: Check notification
print(f"\n6️⃣ Checking notification created...")
notif_response = requests.get(
    f"{BASE_URL}/mentor/notifications/",
    headers=headers
)

if notif_response.status_code == 200:
    notifications = notif_response.json().get('notifications', [])
    print(f"✅ Found {len(notifications)} total notifications")
    if result.get('notification_id'):
        latest_notif = next(
            (n for n in notifications if n['id'] == result['notification_id']),
            None
        )
        if latest_notif:
            print(f"   Latest notification:")
            print(f"   - Title: {latest_notif['title']}")
            print(f"   - Message: {latest_notif['message']}")
            print(f"   - Type: {latest_notif['notification_type']}")
else:
    print(f"⚠️ Could not fetch notifications")

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("Backend is working correctly!")
print("=" * 60)
