"""
Comprehensive Backend API Endpoint Tests
Tests all major endpoints for each role with test users
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

# Test credentials
TEST_USERS = {
    'student': {
        'email': 'test_student@cohort.com',
        'password': 'test_password_123',
        'role': 'STUDENT'
    },
    'mentor': {
        'email': 'test_mentor@cohort.com',
        'password': 'test_password_123',
        'role': 'MENTOR'
    },
    'floorwing': {
        'email': 'test_floorwing@cohort.com',
        'password': 'test_password_123',
        'role': 'FLOOR_WING'
    },
    'admin': {
        'email': 'test_admin@cohort.com',
        'password': 'test_password_123',
        'role': 'ADMIN'
    }
}

def login(username, password):
    """Login and get access token"""
    url = f"{BASE_URL}/auth/token/"
    response = requests.post(url, json={"username": username, "password": password})
    if response.status_code == 200:
        return response.json().get('access')
    return None

def test_endpoint(name, url, headers=None, method='GET', data=None):
    """Test an endpoint and return result"""
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers)
        
        status = "✅" if response.status_code in [200, 201] else "❌"
        return {
            'name': name,
            'status': response.status_code,
            'success': response.status_code in [200, 201],
            'symbol': status
        }
    except Exception as e:
        return {
            'name': name,
            'status': 'ERROR',
            'success': False,
            'symbol': '❌',
            'error': str(e)
        }

def test_authentication():
    """Test authentication endpoints"""
    print("\n" + "="*60)
    print("1. AUTHENTICATION TESTS")
    print("="*60)
    
    results = []
    for role, creds in TEST_USERS.items():
        token = login(creds['email'], creds['password'])
        if token:
            print(f"✅ {role.upper()}: Login successful")
            results.append({'role': role, 'success': True})
            
            # Test user endpoint
            headers = {"Authorization": f"Bearer {token}"}
            user_response = requests.get(f"{BASE_URL}/auth/user/", headers=headers)
            if user_response.status_code == 200:
                user_data = user_response.json()
                print(f"   ✅ User profile retrieved: {user_data.get('email', 'N/A')}")
                if 'profile' in user_data:
                    print(f"   ✅ Profile role: {user_data['profile'].get('role', 'N/A')}")
            else:
                print(f"   ❌ User profile failed: {user_response.status_code}")
        else:
            print(f"❌ {role.upper()}: Login failed")
            results.append({'role': role, 'success': False})
    
    return results

def test_student_endpoints():
    """Test student-specific endpoints"""
    print("\n" + "="*60)
    print("2. STUDENT ENDPOINTS")
    print("="*60)
    
    token = login(TEST_USERS['student']['email'], TEST_USERS['student']['password'])
    if not token:
        print("❌ Could not login as student")
        return []
    
    headers = {"Authorization": f"Bearer {token}"}
    endpoints = [
        ("User Profile", f"{BASE_URL}/profiles/me/"),
        ("Notifications", f"{BASE_URL}/profiles/notifications/"),
        ("Seasons", f"{BASE_URL}/gamification/seasons/"),
        ("Episodes", f"{BASE_URL}/gamification/episodes/"),
        ("Episode Progress", f"{BASE_URL}/gamification/episode-progress/"),
        ("Leaderboard", f"{BASE_URL}/gamification/leaderboard/"),
        ("Dashboard Stats", f"{BASE_URL}/dashboard/stats/"),
        ("CLT", f"{BASE_URL}/clt/"),
        ("SRI", f"{BASE_URL}/sri/"),
        ("CFC", f"{BASE_URL}/cfc/"),
        ("IIPC", f"{BASE_URL}/iipc/"),
        ("SCD", f"{BASE_URL}/scd/"),
    ]
    
    results = []
    for name, url in endpoints:
        result = test_endpoint(name, url, headers)
        results.append(result)
        print(f"{result['symbol']} {name}: {result['status']}")
    
    return results

def test_mentor_endpoints():
    """Test mentor-specific endpoints"""
    print("\n" + "="*60)
    print("3. MENTOR ENDPOINTS")
    print("="*60)
    
    token = login(TEST_USERS['mentor']['email'], TEST_USERS['mentor']['password'])
    if not token:
        print("❌ Could not login as mentor")
        return []
    
    headers = {"Authorization": f"Bearer {token}"}
    endpoints = [
        ("User Profile", f"{BASE_URL}/profiles/me/"),
        ("Assigned Students", f"{BASE_URL}/mentor/students/"),
        ("CLT Submissions", f"{BASE_URL}/mentor/pillar/clt/submissions/"),
        ("Announcements", f"{BASE_URL}/mentor/announcements/"),
    ]
    
    results = []
    for name, url in endpoints:
        result = test_endpoint(name, url, headers)
        results.append(result)
        print(f"{result['symbol']} {name}: {result['status']}")
    
    return results

def test_floorwing_endpoints():
    """Test floor wing-specific endpoints"""
    print("\n" + "="*60)
    print("4. FLOOR WING ENDPOINTS")
    print("="*60)
    
    token = login(TEST_USERS['floorwing']['email'], TEST_USERS['floorwing']['password'])
    if not token:
        print("❌ Could not login as floor wing")
        return []
    
    headers = {"Authorization": f"Bearer {token}"}
    endpoints = [
        ("User Profile", f"{BASE_URL}/profiles/me/"),
        ("Dashboard", f"{BASE_URL}/profiles/floor-wing/dashboard/"),
        ("Floor Students", f"{BASE_URL}/profiles/floor-wing/students/"),
        ("Floor Mentors", f"{BASE_URL}/profiles/floor-wing/mentors/"),
        ("Announcements", f"{BASE_URL}/profiles/floor-wing/announcements/"),
    ]
    
    results = []
    for name, url in endpoints:
        result = test_endpoint(name, url, headers)
        results.append(result)
        print(f"{result['symbol']} {name}: {result['status']}")
    
    return results

def test_admin_endpoints():
    """Test admin-specific endpoints"""
    print("\n" + "="*60)
    print("5. ADMIN ENDPOINTS")
    print("="*60)
    
    token = login(TEST_USERS['admin']['email'], TEST_USERS['admin']['password'])
    if not token:
        print("❌ Could not login as admin")
        return []
    
    headers = {"Authorization": f"Bearer {token}"}
    endpoints = [
        ("User Profile", f"{BASE_URL}/profiles/me/"),
        ("Campus Overview TECH", f"{BASE_URL}/profiles/admin/campus/TECH/"),
        ("Campus Overview ARTS", f"{BASE_URL}/profiles/admin/campus/ARTS/"),
        ("All Users", f"{BASE_URL}/admin/users/"),
    ]
    
    results = []
    for name, url in endpoints:
        result = test_endpoint(name, url, headers)
        results.append(result)
        print(f"{result['symbol']} {name}: {result['status']}")
    
    return results

def print_summary(all_results):
    """Print test summary"""
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    total = 0
    passed = 0
    
    for category, results in all_results.items():
        if isinstance(results, list):
            for result in results:
                total += 1
                if result.get('success', False):
                    passed += 1
    
    print(f"\nTotal Tests: {total}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {total - passed} ❌")
    print(f"Success Rate: {(passed/total*100):.1f}%")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("BACKEND API ENDPOINT TESTS")
    print("="*60)
    
    results = {
        'auth': test_authentication(),
        'student': test_student_endpoints(),
        'mentor': test_mentor_endpoints(),
        'floorwing': test_floorwing_endpoints(),
        'admin': test_admin_endpoints()
    }
    
    print_summary(results)
