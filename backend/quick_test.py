import requests
import json

token = requests.post('http://127.0.0.1:8000/api/auth/token/', json={'username':'testuser','password':'testpass123'}).json()['access']
floor_data = requests.get('http://127.0.0.1:8000/api/profiles/admin/campus/TECH/floor/1/', headers={'Authorization': f'Bearer {token}'}).json()
student_id = floor_data['students'][0]['id']
print(f'Testing with student ID: {student_id}')

detail = requests.get(f'http://127.0.0.1:8000/api/profiles/admin/student/{student_id}/', headers={'Authorization': f'Bearer {token}'})
print(f'Status: {detail.status_code}')

if detail.status_code == 200:
    data = detail.json()
    print(f"\nStudent Name: {data['name']}")
    print(f"Email: {data['email']}")
    print(f"Campus: {data['campus_name']}")
    print(f"Floor: {data['floor']}")
    print(f"Mentor: {data['assigned_mentor']['name'] if data.get('assigned_mentor') else 'None'}")
    print(f"Progress: {data['pillar_progress']}%")
    print(f"XP Points: {data['xp_points']}")
    print(f"Status: {data['status']}")
    print("\n** TEST PASSED **")
else:
    print(f"Error: {detail.text[:500]}")
