import requests
import json

# Test student login
print("\n=== Testing Student Login ===\n")

# Step 1: Login
login_url = "http://127.0.0.1:8000/api/auth/token/"
login_data = {
    "username": "nitya.b.it.2024@snsce.ac.in",
    "password": "pass123#"
}

print("1. Logging in...")
login_response = requests.post(login_url, json=login_data)
print(f"   Status: {login_response.status_code}")

if login_response.status_code == 200:
    tokens = login_response.json()
    access_token = tokens.get('access')
    print(f"   ✅ Got access token: {access_token[:20]}...")
    
    # Step 2: Get user profile
    user_url = "http://127.0.0.1:8000/api/auth/user/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    print("\n2. Getting user profile...")
    user_response = requests.get(user_url, headers=headers)
    print(f"   Status: {user_response.status_code}")
    
    if user_response.status_code == 200:
        user_data = user_response.json()
        print(f"   ✅ User data:")
        print(json.dumps(user_data, indent=4))
        
        # Check if profile has role
        if 'profile' in user_data and 'role' in user_data['profile']:
            print(f"\n   ✅ Profile role: {user_data['profile']['role']}")
        else:
            print("\n   ❌ Profile or role not found in response!")
    else:
        print(f"   ❌ Failed to get user profile: {user_response.text}")
        
    # Step 3: Test notifications endpoint
    print("\n3. Testing notifications endpoint...")
    notif_url = "http://127.0.0.1:8000/api/profiles/notifications/unread_count/"
    notif_response = requests.get(notif_url, headers=headers)
    print(f"   Status: {notif_response.status_code}")
    
    if notif_response.status_code == 200:
        print(f"   ✅ Notifications response: {notif_response.json()}")
    else:
        print(f"   ❌ Failed: {notif_response.text}")
        
else:
    print(f"   ❌ Login failed: {login_response.text}")

# Test floor wing login and announcement creation
print("\n\n=== Testing Floor Wing Login ===\n")

fw_login_data = {
    "username": "fw_tech_2",
    "password": "floorwing123"
}

print("1. Logging in as floor wing...")
fw_login_response = requests.post(login_url, json=fw_login_data)
print(f"   Status: {fw_login_response.status_code}")

if fw_login_response.status_code == 200:
    fw_tokens = fw_login_response.json()
    fw_access_token = fw_tokens.get('access')
    print(f"   ✅ Got access token")
    
    # Get user profile
    fw_headers = {
        "Authorization": f"Bearer {fw_access_token}"
    }
    
    print("\n2. Getting floor wing user profile...")
    fw_user_response = requests.get(user_url, headers=fw_headers)
    print(f"   Status: {fw_user_response.status_code}")
    
    if fw_user_response.status_code == 200:
        fw_user_data = fw_user_response.json()
        print(f"   ✅ Floor wing user data:")
        print(json.dumps(fw_user_data, indent=4))
    
    # Test creating announcement
    print("\n3. Testing announcement creation...")
    announcement_url = "http://127.0.0.1:8000/api/profiles/floor-wing/announcements/"
    announcement_data = {
        "title": "Test Announcement",
        "message": "This is a test announcement",
        "priority": "normal",
        "status": "published"
    }
    
    announcement_response = requests.post(announcement_url, json=announcement_data, headers=fw_headers)
    print(f"   Status: {announcement_response.status_code}")
    
    if announcement_response.status_code == 201:
        print(f"   ✅ Announcement created: {announcement_response.json()}")
    else:
        print(f"   ❌ Failed: {announcement_response.text}")
else:
    print(f"   ❌ Login failed: {fw_login_response.text}")
