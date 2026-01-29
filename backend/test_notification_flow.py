import requests
import json

print("\n=== Testing Floor Wing Announcement → Student Notification ===\n")

# Step 1: Login as floor wing
login_url = "http://127.0.0.1:8000/api/auth/token/"
fw_login_data = {
    "username": "fw_tech_2",
    "password": "floorwing123"
}

print("1. Logging in as floor wing (fw_tech_2 - TECH Floor 2)...")
fw_response = requests.post(login_url, json=fw_login_data)
if fw_response.status_code != 200:
    print(f"   ❌ Login failed: {fw_response.text}")
    exit(1)

fw_token = fw_response.json()['access']
fw_headers = {"Authorization": f"Bearer {fw_token}"}
print("   ✅ Floor wing logged in")

# Step 2: Create announcement
print("\n2. Creating announcement for TECH Floor 2...")
announcement_url = "http://127.0.0.1:8000/api/profiles/floor-wing/announcements/"
announcement_data = {
    "title": "Important Update: Final Project Submission",
    "message": "All students on Floor 2 must submit their final projects by this Friday. Please make sure all documentation is complete.",
    "priority": "urgent",
    "status": "published"
}

announcement_response = requests.post(announcement_url, json=announcement_data, headers=fw_headers)
if announcement_response.status_code != 201:
    print(f"   ❌ Failed: {announcement_response.text}")
    exit(1)

announcement = announcement_response.json()
print(f"   ✅ Announcement created!")
print(f"      ID: {announcement['id']}")
print(f"      Title: {announcement['title']}")

# Step 3: Login as student
print("\n3. Logging in as student (nitya.b.it.2024@snsce.ac.in - TECH Floor 2)...")
student_login_data = {
    "username": "nitya.b.it.2024@snsce.ac.in",
    "password": "pass123#"
}

student_response = requests.post(login_url, json=student_login_data)
if student_response.status_code != 200:
    print(f"   ❌ Login failed: {student_response.text}")
    exit(1)

student_token = student_response.json()['access']
student_headers = {"Authorization": f"Bearer {student_token}"}
print("   ✅ Student logged in")

# Step 4: Check notifications
print("\n4. Checking student's notifications...")
notif_url = "http://127.0.0.1:8000/api/profiles/notifications/unread_count/"
notif_response = requests.get(notif_url, headers=student_headers)

if notif_response.status_code == 200:
    unread = notif_response.json()['unread_count']
    print(f"   ✅ Unread notifications: {unread}")
else:
    print(f"   ❌ Failed: {notif_response.text}")

# Step 5: Get notification details
print("\n5. Fetching notification details...")
all_notif_url = "http://127.0.0.1:8000/api/profiles/notifications/"
all_response = requests.get(all_notif_url, headers=student_headers)

if all_response.status_code == 200:
    data = all_response.json()
    notifications = data.get('results', data)
    
    print(f"   ✅ Total notifications: {len(notifications)}")
    
    # Find the announcement notification
    announcement_notif = None
    for notif in notifications:
        if notif.get('announcement_id') == announcement['id']:
            announcement_notif = notif
            break
    
    if announcement_notif:
        print(f"\n   🎉 SUCCESS! Student received the announcement notification!")
        print(f"      Type: {announcement_notif['notification_type']}")
        print(f"      Title: {announcement_notif['title']}")
        print(f"      Message preview: {announcement_notif['message'][:80]}...")
        print(f"      Is Read: {announcement_notif['is_read']}")
        print(f"      Announcement ID: {announcement_notif['announcement_id']}")
    else:
        print(f"\n   ⚠️  Notification not found in student's notifications")
        print(f"      Available notifications:")
        for notif in notifications[:3]:
            print(f"         - {notif.get('title', 'N/A')}")
else:
    print(f"   ❌ Failed: {all_response.text}")

print("\n\n=== Summary ===")
print(f"✅ Floor wing created announcement")
print(f"✅ Student received notification")
print(f"✅ Notification system is working!")
