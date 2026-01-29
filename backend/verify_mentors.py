"""
Verify mentor assignments in production database
"""
import requests
import json

# API endpoints
BASE_URL = "https://wholesome-cat-production.up.railway.app/api"
LOGIN_URL = f"{BASE_URL}/auth/token/"

# Admin credentials
ADMIN_EMAIL = "admin@test.com"
ADMIN_PASSWORD = "admin123"

def verify_mentors():
    print("\n" + "="*60)
    print("VERIFYING MENTOR ASSIGNMENTS")
    print("="*60 + "\n")
    
    # Login
    print("1️⃣ Logging in...")
    login_response = requests.post(
        LOGIN_URL,
        json={"username": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
    )
    
    if login_response.status_code != 200:
        print(f"   ❌ Login failed: {login_response.text}")
        return
    
    token = login_response.json().get('access')
    print("   ✅ Login successful\n")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Check Floor 1 (Mentor 1)
    print("2️⃣ Checking Floor 1 (Mentor 1 - Rajesh Kumar)...")
    floor1_url = f"{BASE_URL}/profiles/admin/campus/TECH/floor/1/"
    floor1_response = requests.get(floor1_url, headers=headers)
    
    if floor1_response.status_code == 200:
        floor1_data = floor1_response.json()
        print(f"   Floor: {floor1_data.get('floor')}")
        print(f"   Total Students: {len(floor1_data.get('students', []))}")
        print(f"   Total Mentors: {len(floor1_data.get('mentors', []))}")
        
        print("\n   Students:")
        for student in floor1_data.get('students', [])[:5]:
            mentor_name = student.get('mentor_name') or 'Not assigned'
            print(f"      • {student['email']} - Mentor: {mentor_name}")
        
        print("\n   Mentors:")
        for mentor in floor1_data.get('mentors', []):
            print(f"      • {mentor['email']} (ID: {mentor['id']})")
    else:
        print(f"   ❌ Failed to get floor 1 data: {floor1_response.status_code}")
    
    # Check Floor 2 (Mentor 2)
    print("\n3️⃣ Checking Floor 2 (Mentor 2 - Priya Sharma)...")
    floor2_url = f"{BASE_URL}/profiles/admin/campus/TECH/floor/2/"
    floor2_response = requests.get(floor2_url, headers=headers)
    
    if floor2_response.status_code == 200:
        floor2_data = floor2_response.json()
        print(f"   Floor: {floor2_data.get('floor')}")
        print(f"   Total Students: {len(floor2_data.get('students', []))}")
        print(f"   Total Mentors: {len(floor2_data.get('mentors', []))}")
        
        print("\n   Students:")
        for student in floor2_data.get('students', [])[:10]:
            mentor_name = student.get('mentor') or 'Not assigned'
            mentor_id = student.get('mentor_id', 'N/A')
            print(f"      • {student['email']} - Mentor: {mentor_name} (ID: {mentor_id})")
        
        print("\n   Mentors:")
        for mentor in floor2_data.get('mentors', []):
            print(f"      • {mentor['email']} (ID: {mentor['id']})")
    else:
        print(f"   ❌ Failed to get floor 2 data: {floor2_response.status_code}")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    verify_mentors()
