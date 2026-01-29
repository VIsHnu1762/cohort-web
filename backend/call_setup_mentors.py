"""
Call the setup mentors endpoint on Railway production
"""
import requests
import json

# API endpoints
BASE_URL = "https://wholesome-cat-production.up.railway.app/api"
LOGIN_URL = f"{BASE_URL}/auth/token/"
SETUP_MENTORS_URL = f"{BASE_URL}/profiles/admin/setup-mentors/"

# Admin credentials
ADMIN_EMAIL = "admin@test.com"
ADMIN_PASSWORD = "admin123"

def setup_mentors():
    print("\n" + "="*60)
    print("SETTING UP MENTORS IN RAILWAY PRODUCTION")
    print("="*60 + "\n")
    
    # Step 1: Login as admin to get token
    print("1️⃣ Logging in as admin...")
    try:
        login_response = requests.post(
            LOGIN_URL,
            json={
                "username": ADMIN_EMAIL,  # Field name is 'username' but accepts email
                "password": ADMIN_PASSWORD
            },
            headers={"Content-Type": "application/json"}
        )
        
        if login_response.status_code != 200:
            print(f"   ❌ Login failed: {login_response.status_code}")
            print(f"   Response: {login_response.text}")
            return
        
        token = login_response.json().get('access')
        print(f"   ✅ Login successful! Token received.")
    
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return
    
    # Step 2: Call setup mentors endpoint
    print("\n2️⃣ Creating mentors and assigning students...")
    try:
        setup_response = requests.post(
            SETUP_MENTORS_URL,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        
        if setup_response.status_code != 200:
            print(f"   ❌ Setup failed: {setup_response.status_code}")
            print(f"   Response: {setup_response.text}")
            return
        
        result = setup_response.json()
        print("   ✅ Setup successful!\n")
        
        # Print results
        print("="*60)
        print("MENTORS CREATED:")
        print("="*60)
        for mentor in result.get('mentors_created', []):
            print(f"\n📧 {mentor['email']}")
            print(f"   Name: {mentor['name']}")
            print(f"   ID: {mentor['id']}")
            print(f"   Campus: {mentor['campus']} | Floor: {mentor['floor']}")
            print(f"   Status: {mentor['status']}")
        
        print("\n" + "="*60)
        print("STUDENTS ASSIGNED:")
        print("="*60)
        
        mentor1_students = [s for s in result.get('students_assigned', []) if 'mentor1' in s['mentor_email']]
        mentor2_students = [s for s in result.get('students_assigned', []) if 'mentor2' in s['mentor_email']]
        
        print(f"\nMentor 1 ({result['mentors_created'][0]['email']}) - {len(mentor1_students)} students:")
        for student in mentor1_students:
            print(f"   • {student['student_email']} ({student['student_name']})")
        
        print(f"\nMentor 2 ({result['mentors_created'][1]['email']}) - {len(mentor2_students)} students:")
        for student in mentor2_students:
            print(f"   • {student['student_email']} ({student['student_name']})")
        
        print("\n" + "="*60)
        print("CREDENTIALS:")
        print("="*60)
        credentials = result.get('credentials', {})
        print(f"Mentor 1: {credentials.get('mentor1')}")
        print(f"Mentor 2: {credentials.get('mentor2')}")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"   ❌ Setup error: {e}")
        return

if __name__ == '__main__':
    setup_mentors()
