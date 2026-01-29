import requests
import json

API_URL = 'http://127.0.0.1:8000/api'

print("=" * 60)
print("Testing Student Detail Endpoint")
print("=" * 60)

# Step 1: Login
print("\n1. Logging in as admin...")
login_response = requests.post(f'{API_URL}/auth/token/', json={
    'username': 'testuser',
    'password': 'testpass123'
})

if login_response.status_code != 200:
    print(f"❌ Login failed: {login_response.status_code}")
    print(login_response.text)
    exit(1)

token = login_response.json()['access']
print("✅ Login successful")

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# Step 2: Get floor data to find a student
print("\n2. Getting floor data (TECH, Floor 1)...")
floor_response = requests.get(
    f'{API_URL}/profiles/admin/campus/TECH/floor/1/',
    headers=headers
)

if floor_response.status_code != 200:
    print(f"❌ Failed to get floor data: {floor_response.status_code}")
    print(floor_response.text)
    exit(1)

floor_data = floor_response.json()
print(f"✅ Found {len(floor_data['students'])} students")

if not floor_data['students']:
    print("❌ No students found on this floor")
    exit(1)

student = floor_data['students'][0]
student_id = student['id']
print(f"\n📋 Testing with student: {student['name']} (ID: {student_id})")

# Step 3: Test student detail endpoint
print(f"\n3. Getting detailed info for student {student_id}...")
detail_response = requests.get(
    f'{API_URL}/profiles/admin/student/{student_id}/',
    headers=headers
)

if detail_response.status_code != 200:
    print(f"❌ Failed to get student details: {detail_response.status_code}")
    print(detail_response.text)
    exit(1)

student_detail = detail_response.json()
print("✅ Student details retrieved successfully!\n")

# Display the results
print("=" * 60)
print("STUDENT DETAILS")
print("=" * 60)
print(f"Name: {student_detail['name']}")
print(f"Email: {student_detail['email']}")
print(f"Roll No: {student_detail['roll_no']}")
print(f"Campus: {student_detail['campus_name']}")
print(f"Floor: {student_detail['floor']}")
print(f"XP Points: {student_detail['xp_points']}")
print(f"Status: {student_detail['status']}")
print(f"Overall Progress: {student_detail['pillar_progress']}%")

if student_detail.get('assigned_mentor'):
    print(f"\nMentor: {student_detail['assigned_mentor']['name']}")
    print(f"Mentor Email: {student_detail['assigned_mentor']['email']}")
else:
    print("\nMentor: Not assigned")

print("\nPillar Progress:")
for pillar, progress in student_detail['pillar_details'].items():
    print(f"  {pillar}: {progress}%")

print("\nSubmission Stats:")
stats = student_detail['submission_stats']
print(f"  Total: {stats['total']}")
print(f"  Approved: {stats['approved']}")
print(f"  Pending: {stats['pending']}")
print(f"  Rejected: {stats['rejected']}")

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print("\n📝 The endpoint is working correctly and ready for frontend use.")
