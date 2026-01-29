import requests
import json

# Test announcement creation with notifications
print("\n=== Testing Announcement Notifications ===\n")

# Step 1: Login as floor wing
login_url = "http://127.0.0.1:8000/api/auth/token/"
fw_login_data = {
    "username": "fw_tech_2",
    "password": "floorwing123"
}

print("1. Logging in as floor wing (fw_tech_2)...")
fw_login_response = requests.post(login_url, json=fw_login_data)
if fw_login_response.status_code != 200:
    print(f"   ❌ Login failed: {fw_login_response.text}")
    exit(1)

fw_access_token = fw_login_response.json().get('access')
fw_headers = {"Authorization": f"Bearer {fw_access_token}"}
print("   ✅ Logged in successfully")

# Step 2: Create a published announcement
print("\n2. Creating a published announcement...")
announcement_url = "http://127.0.0.1:8000/api/profiles/floor-wing/announcements/"
announcement_data = {
    "title": "Important: End of Semester Submission",
    "message": "All students must submit their final projects by Friday. Please ensure all documentation is complete and uploaded to the portal.",
    "priority": "high",
    "status": "published"
}

announcement_response = requests.post(announcement_url, json=announcement_data, headers=fw_headers)
if announcement_response.status_code != 201:
    print(f"   ❌ Failed to create announcement: {announcement_response.text}")
    exit(1)

announcement = announcement_response.json()
print(f"   ✅ Announcement created with ID: {announcement['id']}")
print(f"      Title: {announcement['title']}")
print(f"      Campus: {announcement['campus']}, Floor: {announcement['floor']}")

# Step 3: Login as a student and check notifications
print("\n3. Logging in as student...")
student_login_data = {
    "username": "nitya.b.it.2024@snsce.ac.in",
    "password": "pass123#"
}

student_login_response = requests.post(login_url, json=student_login_data)
if student_login_response.status_code != 200:
    print(f"   ❌ Student login failed: {student_login_response.text}")
    exit(1)

student_access_token = student_login_response.json().get('access')
student_headers = {"Authorization": f"Bearer {student_access_token}"}
print("   ✅ Student logged in successfully")

# Step 4: Check unread notifications
print("\n4. Checking student's unread notifications...")
notif_url = "http://127.0.0.1:8000/api/profiles/notifications/unread_count/"
notif_response = requests.get(notif_url, headers=student_headers)

if notif_response.status_code == 200:
    unread_data = notif_response.json()
    print(f"   ✅ Unread notifications count: {unread_data['unread_count']}")
else:
    print(f"   ❌ Failed to get notifications: {notif_response.text}")

# Step 5: Get all notifications
print("\n5. Fetching all notifications...")
all_notif_url = "http://127.0.0.1:8000/api/profiles/notifications/"
all_notif_response = requests.get(all_notif_url, headers=student_headers)

if all_notif_response.status_code == 200:
    notifications = all_notif_response.json()
    results = notifications.get('results', notifications) if isinstance(notifications, dict) else notifications
    
    print(f"   ✅ Total notifications: {len(results)}")
    if results:
        print("\n   Recent notifications:")
        for notif in results[:3]:
            print(f"      - [{notif['notification_type']}] {notif['title']}")
            print(f"        Read: {notif['is_read']}")
            if notif.get('announcement_id'):
                print(f"        Announcement ID: {notif['announcement_id']}")
else:
    print(f"   ❌ Failed to get notifications: {all_notif_response.text}")

# Step 6: Check how many students are on TECH Floor 2
print("\n6. Checking total students on TECH Floor 2...")
from django.contrib.auth.models import User
import os
import django

os.chdir('C:\\Python310\\cohort_webapp\\Cohort_Web_App\\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.profiles.models import UserProfile
from apps.profiles.notification_models import Notification

students = UserProfile.objects.filter(
    campus='TECH',
    floor=2,
    role='STUDENT'
)
print(f"   Total students on TECH Floor 2: {students.count()}")

# Check notifications created for the announcement
notifs = Notification.objects.filter(
    announcement_id=announcement['id']
)
print(f"   Notifications created for announcement: {notifs.count()}")
print(f"\n   ✅ All students received notifications!" if notifs.count() == students.count() else f"   ⚠️  Some students might not have received notifications")
