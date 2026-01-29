import requests
import json

# Configuration
API_URL = 'http://127.0.0.1:8000/api'

# First, login to get token (replace with actual admin credentials)
def get_admin_token():
    """Login and get admin token"""
    login_url = f'{API_URL}/auth/token/'
    # Replace with your admin credentials
    credentials = {
        'username': 'testuser',  # or email
        'password': 'testpass123'
    }
    
    try:
        response = requests.post(login_url, json=credentials)
        response.raise_for_status()
        data = response.json()
        return data.get('access')
    except requests.exceptions.RequestException as e:
        print(f"Login failed: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return None

def test_student_detail(student_id, token):
    """Test the student detail endpoint"""
    url = f'{API_URL}/profiles/admin/student/{student_id}/'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        print("\n=== Student Detail Response ===")
        print(json.dumps(data, indent=2))
        print("\n✅ Student detail endpoint working!")
        
        return data
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error testing student detail: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status: {e.response.status_code}")
            print(f"Response: {e.response.text}")
        return None

def main():
    print("Testing Admin Student Detail Endpoint...")
    
    # Get admin token
    print("\n1. Getting admin token...")
    token = get_admin_token()
    
    if not token:
        print("Failed to get admin token. Please check credentials.")
        return
    
    print("✅ Token obtained successfully")
    
    # Test with a student ID (you may need to adjust this)
    # First, let's get a list of students to find a valid ID
    print("\n2. Getting floor data to find a student...")
    floor_url = f'{API_URL}/profiles/admin/campus/TECH/floor/1/'
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(floor_url, headers=headers)
        response.raise_for_status()
        floor_data = response.json()
        
        if floor_data.get('students'):
            student = floor_data['students'][0]
            student_id = student['id']
            print(f"Found student: {student['name']} (ID: {student_id})")
            
            # Test the student detail endpoint
            print(f"\n3. Testing student detail for ID {student_id}...")
            test_student_detail(student_id, token)
        else:
            print("No students found on floor")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
