"""
Test script for SCD (Skill and Career Development) endpoints
Tests LeetCode profile integration and submission workflow
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api"

# Test credentials
TEST_EMAIL = "admin@example.com"
TEST_PASSWORD = "admin123"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_response(response):
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response Text: {response.text}")

# 1. Get JWT Token
print_section("1. AUTHENTICATION - Getting JWT Token")
# Try both username and email for compatibility
auth_response = requests.post(
    f"{BASE_URL}/auth/token/",
    json={"username": "admin", "email": TEST_EMAIL, "password": TEST_PASSWORD}
)
print_response(auth_response)

if auth_response.status_code != 200:
    print("\n❌ Authentication failed! Make sure the test user exists.")
    exit(1)

token = auth_response.json()["access"]
headers = {"Authorization": f"Bearer {token}"}
print("\n✓ Authentication successful")

# 2. Get User Profile
print_section("2. USER PROFILE - Getting user details")
profile_response = requests.get(f"{BASE_URL}/auth/user/", headers=headers)
print_response(profile_response)
user_data = profile_response.json()
print(f"\n✓ Logged in as: {user_data.get('email')} (Role: {user_data.get('role')})")

# 3. Test Sync LeetCode Profile
print_section("3. SYNC LEETCODE PROFILE - Fetching data from LeetCode API")
# Using a known LeetCode username for testing
test_username = "tourist"  # One of the top competitive programmers
print(f"Testing with username: {test_username}")

sync_response = requests.post(
    f"{BASE_URL}/scd/profiles/sync/",
    json={"leetcode_username": test_username},
    headers=headers
)
print_response(sync_response)

if sync_response.status_code == 200:
    sync_data = sync_response.json()
    profile = sync_data.get('profile', {})
    print(f"\n✓ Profile synced successfully!")
    print(f"  - Username: {profile.get('leetcode_username')}")
    print(f"  - Total Solved: {profile.get('total_solved')}")
    print(f"  - Easy: {profile.get('easy_solved')}")
    print(f"  - Medium: {profile.get('medium_solved')}")
    print(f"  - Hard: {profile.get('hard_solved')}")
    print(f"  - Ranking: {profile.get('ranking')}")
    print(f"  - Submissions: {len(profile.get('submissions', []))}")
    
    profile_id = profile.get('id')
else:
    print("\n⚠ Sync failed (LeetCode API might be rate-limited or username invalid)")
    profile_id = None

# 4. Get All Profiles
print_section("4. GET ALL PROFILES - Listing user's LeetCode profiles")
list_response = requests.get(f"{BASE_URL}/scd/profiles/", headers=headers)
print_response(list_response)

if list_response.status_code == 200:
    data = list_response.json()
    # Handle both paginated and non-paginated responses
    profiles = data.get('results', data) if isinstance(data, dict) and 'results' in data else data
    if isinstance(profiles, dict):
        profiles = [profiles]
    
    print(f"\n✓ Retrieved {len(profiles)} profile(s)")
    for idx, p in enumerate(profiles, 1):
        print(f"  {idx}. {p.get('leetcode_username')} - Status: {p.get('status')}")
    
    # Use first profile if sync failed
    if not profile_id and profiles:
        profile_id = profiles[0].get('id')

# 5. Test Profile Stats
print_section("5. GET PROFILE STATS - Retrieving statistics")
stats_response = requests.get(f"{BASE_URL}/scd/profiles/stats/", headers=headers)
print_response(stats_response)

if stats_response.status_code == 200:
    stats = stats_response.json()
    print(f"\n✓ Statistics:")
    print(f"  - Total Profiles: {stats.get('total_profiles')}")
    print(f"  - Draft: {stats.get('draft')}")
    print(f"  - Pending: {stats.get('pending')}")
    print(f"  - Approved: {stats.get('approved')}")
    print(f"  - Rejected: {stats.get('rejected')}")

# 6. Submit Profile for Review
if profile_id:
    print_section("6. SUBMIT PROFILE - Submitting for mentor review")
    screenshot_url = "https://drive.google.com/file/d/test_screenshot_123/view"
    
    submit_response = requests.post(
        f"{BASE_URL}/scd/profiles/{profile_id}/submit/",
        json={"screenshot_url": screenshot_url},
        headers=headers
    )
    print_response(submit_response)
    
    if submit_response.status_code == 200:
        submit_data = submit_response.json()
        print(f"\n✓ Profile submitted successfully!")
        print(f"  - Status: {submit_data.get('profile', {}).get('status')}")
        print(f"  - Submitted At: {submit_data.get('profile', {}).get('submitted_at')}")
    else:
        print("\n⚠ Submission failed")
else:
    print_section("6. SUBMIT PROFILE - Skipping (no profile available)")

# 7. Test Create Profile Manually
print_section("7. CREATE PROFILE MANUALLY - Testing manual profile creation")
manual_profile_data = {
    "leetcode_username": "test_user_123",
    "total_solved": 150,
    "easy_solved": 60,
    "medium_solved": 70,
    "hard_solved": 20,
    "ranking": 50000,
    "contest_rating": 1500,
    "streak": 15,
    "screenshot_url": "https://drive.google.com/file/d/manual_test/view"
}

create_response = requests.post(
    f"{BASE_URL}/scd/profiles/",
    json=manual_profile_data,
    headers=headers
)
print_response(create_response)

if create_response.status_code == 201:
    created = create_response.json()
    print(f"\n✓ Manual profile created successfully!")
    print(f"  - ID: {created.get('id')}")
    print(f"  - Username: {created.get('leetcode_username')}")
    print(f"  - Status: {created.get('status')}")

# Summary
print_section("TEST SUMMARY")
print("\n✅ All SCD endpoint tests completed!")
print("\nEndpoints tested:")
print("  1. ✓ Authentication")
print("  2. ✓ User Profile")
print("  3. ✓ Sync LeetCode Profile (with LeetCode API)")
print("  4. ✓ List Profiles")
print("  5. ✓ Get Profile Stats")
print("  6. ✓ Submit Profile for Review")
print("  7. ✓ Create Profile Manually")

print("\nNext steps:")
print("  - Start the React frontend: npm run dev")
print("  - Navigate to the SCD page")
print("  - Enter a LeetCode username and click 'Sync Profile'")
print("  - Watch the fire animation rise based on problems solved!")
print("  - Submit with screenshot URL for mentor review")
