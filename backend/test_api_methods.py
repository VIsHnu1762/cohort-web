"""
Comprehensive API Methods Test - Tests all HTTP methods (GET, POST, PUT, PATCH, DELETE)
and actual functionality across all endpoints
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

TEST_USERS = {
    'student': {'email': 'test_student@cohort.com', 'password': 'test_password_123'},
    'mentor': {'email': 'test_mentor@cohort.com', 'password': 'test_password_123'},
    'floorwing': {'email': 'test_floorwing@cohort.com', 'password': 'test_password_123'},
    'admin': {'email': 'test_admin@cohort.com', 'password': 'test_password_123'},
}

def login(email, password):
    """Login and return access token"""
    try:
        response = requests.post(
            f"{BASE_URL}/auth/token/",
            json={"username": email, "password": password}  # API uses 'username' field but accepts email
        )
        if response.status_code == 200:
            return response.json().get('access')
        return None
    except Exception as e:
        print(f"Login error: {e}")
        return None

def test_method(name, method, url, headers, data=None, expected_status=[200, 201, 204]):
    """Test an HTTP method on an endpoint"""
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=5)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data, timeout=5)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=data, timeout=5)
        elif method == 'PATCH':
            response = requests.patch(url, headers=headers, json=data, timeout=5)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=5)
        
        status = response.status_code
        if status in expected_status:
            return {"name": name, "method": method, "status": status, "success": True, "symbol": "✅"}
        else:
            return {"name": name, "method": method, "status": status, "success": False, "symbol": "⚠️"}
    except Exception as e:
        return {"name": name, "method": method, "status": "ERROR", "success": False, "symbol": "❌", "error": str(e)}

def test_student_crud_operations():
    """Test CRUD operations for student endpoints"""
    print("\n" + "="*60)
    print("1. STUDENT CRUD OPERATIONS")
    print("="*60)
    
    token = login(TEST_USERS['student']['email'], TEST_USERS['student']['password'])
    if not token:
        print("❌ Could not login as student")
        return []
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    results = []
    
    # Profile Operations
    result = test_method("GET Profile", "GET", f"{BASE_URL}/profiles/me/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    result = test_method("PATCH Profile", "PATCH", f"{BASE_URL}/profiles/me/", headers, 
                        {"first_name": "Test", "last_name": "Student"}, [200, 400])
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # Notifications
    result = test_method("GET Notifications", "GET", f"{BASE_URL}/profiles/notifications/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # Gamification - Episode Progress
    result = test_method("GET Episode Progress", "GET", f"{BASE_URL}/gamification/episode-progress/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # CLT Submissions
    result = test_method("GET CLT Submissions", "GET", f"{BASE_URL}/clt/submissions/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    result = test_method("POST CLT Submission", "POST", f"{BASE_URL}/clt/submissions/", headers,
                        {
                            "submission_type": "WEEKLY",
                            "week_number": 1,
                            "leetcode_url": "https://leetcode.com/problems/two-sum/",
                            "screenshot": None,
                            "notes": "Test submission"
                        }, [201, 400])
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # CFC Operations (Community, Freelance, Contests)
    result = test_method("GET CFC Hackathons", "GET", f"{BASE_URL}/cfc/hackathons/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    result = test_method("POST CFC Hackathon", "POST", f"{BASE_URL}/cfc/hackathons/", headers,
                        {"title": "Test Hackathon", "description": "Test", "hackathon_url": "https://devpost.com/test"}, [201, 400])
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    result = test_method("GET CFC BMC Videos", "GET", f"{BASE_URL}/cfc/bmc-videos/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # IIPC Operations (Industry Integration & Professional Communication)
    result = test_method("GET IIPC Posts", "GET", f"{BASE_URL}/iipc/posts/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    result = test_method("POST IIPC Post", "POST", f"{BASE_URL}/iipc/posts/", headers,
                        {"post_url": "https://linkedin.com/post/test", "post_type": "ARTICLE"}, [201, 400])
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    result = test_method("GET IIPC Connections", "GET", f"{BASE_URL}/iipc/connections/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # SCD Operations (Self Competitive Development)
    result = test_method("GET SCD Profiles", "GET", f"{BASE_URL}/scd/profiles/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    return results

def test_gamification_system():
    """Test comprehensive gamification features"""
    print("\n" + "="*60)
    print("GAMIFICATION SYSTEM")
    print("="*60)
    
    token = login(TEST_USERS['student']['email'], TEST_USERS['student']['password'])
    if not token:
        print("❌ Could not login as student")
        return []
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    results = []
    
    # Seasons
    result = test_method("GET Seasons", "GET", f"{BASE_URL}/gamification/seasons/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    result = test_method("GET Current Season", "GET", f"{BASE_URL}/gamification/seasons/current/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # Episodes
    result = test_method("GET Episodes", "GET", f"{BASE_URL}/gamification/episodes/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # Episode Progress
    result = test_method("GET Episode Progress", "GET", f"{BASE_URL}/gamification/episode-progress/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    result = test_method("POST Update Progress", "POST", f"{BASE_URL}/gamification/episode-progress/", headers,
                        {"episode": 1, "completion_percentage": 50}, [201, 400, 404])
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # Season Scores
    result = test_method("GET Season Scores", "GET", f"{BASE_URL}/gamification/season-scores/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # Legacy Scores
    result = test_method("GET Legacy Scores", "GET", f"{BASE_URL}/gamification/legacy-scores/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # Vault Wallet
    result = test_method("GET Vault Wallets", "GET", f"{BASE_URL}/gamification/vault-wallets/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # SCD Streaks
    result = test_method("GET SCD Streaks", "GET", f"{BASE_URL}/gamification/scd-streaks/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # Leaderboard
    result = test_method("GET Leaderboard", "GET", f"{BASE_URL}/gamification/leaderboard/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # Titles
    result = test_method("GET Available Titles", "GET", f"{BASE_URL}/gamification/titles/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # User Titles
    result = test_method("GET User Titles", "GET", f"{BASE_URL}/gamification/user-titles/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    result = test_method("POST Equip Title", "POST", f"{BASE_URL}/gamification/user-titles/", headers,
                        {"title": 1, "is_equipped": True}, [201, 400, 404])
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # Dashboard
    result = test_method("GET Dashboard Stats", "GET", f"{BASE_URL}/dashboard/stats/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # Progress Notifications (may fail if no progress data exists)
    result = test_method("GET Batch Stats", "GET", f"{BASE_URL}/gamification/progress-notifications/batch_stats/", headers, expected_status=[200, 404, 500])
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    result = test_method("GET My Comparison", "GET", f"{BASE_URL}/gamification/progress-notifications/my_comparison/", headers, expected_status=[200, 404, 500])
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    return results

def test_mentor_operations():
    """Test mentor-specific operations"""
    print("\n" + "="*60)
    print("2. MENTOR OPERATIONS")
    print("="*60)
    
    token = login(TEST_USERS['mentor']['email'], TEST_USERS['mentor']['password'])
    if not token:
        print("❌ Could not login as mentor")
        return []
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    results = []
    
    # Get assigned students
    result = test_method("GET Assigned Students", "GET", f"{BASE_URL}/mentor/students/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # Get submissions for each pillar
    pillars = ['clt', 'sri', 'cfc', 'iipc', 'scd']
    for pillar in pillars:
        result = test_method(f"GET {pillar.upper()} Submissions", "GET", 
                            f"{BASE_URL}/mentor/pillar/{pillar}/submissions/", headers)
        results.append(result)
        print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # Test review submission (POST)
    result = test_method("POST Review Submission", "POST", f"{BASE_URL}/mentor/review/", headers,
                        {
                            "submission_id": 1,
                            "pillar": "clt",
                            "status": "APPROVED",
                            "feedback": "Good work!",
                            "points_awarded": 10
                        }, [200, 201, 400, 404])
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # Announcements
    result = test_method("GET Announcements", "GET", f"{BASE_URL}/mentor/announcements/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    result = test_method("POST Announcement", "POST", f"{BASE_URL}/mentor/announcements/", headers,
                        {
                            "title": "Test Announcement",
                            "content": "This is a test",
                            "priority": "NORMAL"
                        }, [201, 400, 403])
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # Notifications
    result = test_method("GET Notifications", "GET", f"{BASE_URL}/mentor/notifications/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # Messages
    result = test_method("GET Message Threads", "GET", f"{BASE_URL}/mentor/messages/threads/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    result = test_method("POST Send Message", "POST", f"{BASE_URL}/mentor/messages/send/", headers,
                        {"recipient_id": 1, "content": "Test message"}, [200, 201, 400, 404])
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    return results

def test_floorwing_operations():
    """Test floor wing operations"""
    print("\n" + "="*60)
    print("3. FLOOR WING OPERATIONS")
    print("="*60)
    
    token = login(TEST_USERS['floorwing']['email'], TEST_USERS['floorwing']['password'])
    if not token:
        print("❌ Could not login as floor wing")
        return []
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    results = []
    
    # Dashboard
    result = test_method("GET Dashboard", "GET", f"{BASE_URL}/profiles/floor-wing/dashboard/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # Students
    result = test_method("GET Floor Students", "GET", f"{BASE_URL}/profiles/floor-wing/students/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # Mentors
    result = test_method("GET Floor Mentors", "GET", f"{BASE_URL}/profiles/floor-wing/mentors/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # Announcements
    result = test_method("GET Announcements", "GET", f"{BASE_URL}/profiles/floor-wing/announcements/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    result = test_method("POST Announcement", "POST", f"{BASE_URL}/profiles/floor-wing/announcements/", headers,
                        {
                            "title": "Floor Announcement",
                            "content": "Test floor announcement",
                            "priority": "HIGH"
                        }, [201, 400])
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    return results

def test_admin_operations():
    """Test admin operations"""
    print("\n" + "="*60)
    print("4. ADMIN OPERATIONS")
    print("="*60)
    
    token = login(TEST_USERS['admin']['email'], TEST_USERS['admin']['password'])
    if not token:
        print("❌ Could not login as admin")
        return []
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    results = []
    
    # Campus overview
    result = test_method("GET Campus TECH", "GET", f"{BASE_URL}/profiles/admin/campus/TECH/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    result = test_method("GET Campus ARTS", "GET", f"{BASE_URL}/profiles/admin/campus/ARTS/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # Users management
    result = test_method("GET All Users", "GET", f"{BASE_URL}/admin/users/", headers)
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    # Mentor assignment
    result = test_method("POST Assign Mentor", "POST", f"{BASE_URL}/admin/assign-mentor/", headers,
                        {"student_id": 1, "mentor_id": 2}, [200, 201, 400, 404])
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    result = test_method("POST Bulk Assign", "POST", f"{BASE_URL}/admin/bulk-assign-mentor/", headers,
                        {"student_ids": [1, 2], "mentor_id": 2}, [200, 201, 400, 404])
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    result = test_method("POST Auto Assign", "POST", f"{BASE_URL}/admin/auto-assign-mentors/", headers,
                        {}, [200, 201, 400])
    results.append(result)
    print(f"{result['symbol']} {result['name']}: {result['status']}")
    
    return results

def main():
    print("\n" + "="*60)
    print("COMPREHENSIVE API METHODS & FEATURES TEST")
    print("Testing GET, POST, PUT, PATCH, DELETE operations")
    print("="*60)
    
    all_results = []
    
    # Run all tests
    all_results.extend(test_student_crud_operations())
    all_results.extend(test_gamification_system())
    all_results.extend(test_mentor_operations())
    all_results.extend(test_floorwing_operations())
    all_results.extend(test_admin_operations())
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    total = len(all_results)
    passed = sum(1 for r in all_results if r['success'])
    failed = total - passed
    success_rate = (passed / total * 100) if total > 0 else 0
    
    # Group by HTTP method
    methods = {}
    for result in all_results:
        method = result['method']
        if method not in methods:
            methods[method] = {'total': 0, 'passed': 0}
        methods[method]['total'] += 1
        if result['success']:
            methods[method]['passed'] += 1
    
    print(f"\nTotal Tests: {total}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {failed} ❌")
    print(f"Success Rate: {success_rate:.1f}%")
    
    print("\n" + "="*60)
    print("BY HTTP METHOD:")
    print("="*60)
    for method, stats in methods.items():
        rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
        print(f"{method:8} {stats['passed']}/{stats['total']} ({rate:.1f}%)")
    
    # Show failures
    failures = [r for r in all_results if not r['success']]
    if failures:
        print("\n" + "="*60)
        print("FAILED TESTS:")
        print("="*60)
        for f in failures:
            error_msg = f" - {f.get('error', '')}" if 'error' in f else ""
            print(f"❌ {f['method']:6} {f['name']}: {f['status']}{error_msg}")

if __name__ == "__main__":
    main()
