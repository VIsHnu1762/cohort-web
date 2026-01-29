"""
CFC Module Test Script
Tests all CFC endpoints and functionality
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

# Test credentials
TEST_USER = {
    "username": "admin@example.com",
    "password": "admin123"
}

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_authentication():
    print_section("TESTING AUTHENTICATION")
    
    # Test login
    print("\n1. Testing Login Endpoint...")
    response = requests.post(f"{BASE_URL}/auth/token/", json=TEST_USER)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Login successful")
        print(f"   Access Token: {data['access'][:50]}...")
        print(f"   Refresh Token: {data['refresh'][:50]}...")
        return data['access']
    else:
        print(f"   ✗ Login failed: {response.text}")
        return None

def test_user_profile(token):
    print_section("TESTING USER PROFILE")
    
    print("\n2. Testing User Profile Endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/user/", headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        user = response.json()
        print(f"   ✓ Profile fetched successfully")
        print(f"   Username: {user['username']}")
        print(f"   Email: {user['email']}")
        print(f"   Role: {user.get('role', 'N/A')}")
        print(f"   Is Superuser: {user.get('is_superuser', False)}")
        return True
    else:
        print(f"   ✗ Profile fetch failed: {response.text}")
        return False

def test_cfc_hackathon(token):
    print_section("TESTING CFC - HACKATHON ENDPOINTS")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test GET submissions
    print("\n3. Testing GET Hackathon Submissions...")
    response = requests.get(f"{BASE_URL}/cfc/hackathons/", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ GET successful - Found {len(response.json())} submissions")
    else:
        print(f"   ✗ GET failed: {response.text}")
    
    # Test GET stats
    print("\n4. Testing GET Hackathon Stats...")
    response = requests.get(f"{BASE_URL}/cfc/hackathons/stats/", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print(f"   ✓ Stats fetched: {json.dumps(stats, indent=2)}")
    else:
        print(f"   ✗ Stats failed: {response.text}")
    
    # Test POST submission
    print("\n5. Testing POST Hackathon Submission...")
    test_data = {
        "hackathon_name": "Test Hackathon 2025",
        "mode": "online",
        "registration_date": "2025-12-01",
        "participation_date": "2025-12-10",
        "certificate_link": "https://drive.google.com/file/d/test123"
    }
    response = requests.post(f"{BASE_URL}/cfc/hackathons/", json=test_data, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        submission = response.json()
        print(f"   ✓ Submission created - ID: {submission.get('id')}")
        return submission.get('id')
    else:
        print(f"   ✗ POST failed: {response.text}")
        return None

def test_cfc_bmc_video(token):
    print_section("TESTING CFC - BMC VIDEO ENDPOINTS")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test GET submissions
    print("\n6. Testing GET BMC Video Submissions...")
    response = requests.get(f"{BASE_URL}/cfc/bmc-videos/", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ GET successful - Found {len(response.json())} submissions")
    else:
        print(f"   ✗ GET failed: {response.text}")
    
    # Test POST submission
    print("\n7. Testing POST BMC Video Submission...")
    test_data = {
        "video_url": "https://youtube.com/watch?v=test123",
        "description": "Test BMC Video Description"
    }
    response = requests.post(f"{BASE_URL}/cfc/bmc-videos/", json=test_data, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        print(f"   ✓ Submission created")
        return True
    else:
        print(f"   ✗ POST failed: {response.text}")
        return False

def test_cfc_internship(token):
    print_section("TESTING CFC - INTERNSHIP ENDPOINTS")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test GET submissions
    print("\n8. Testing GET Internship Submissions...")
    response = requests.get(f"{BASE_URL}/cfc/internships/", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ GET successful - Found {len(response.json())} submissions")
    else:
        print(f"   ✗ GET failed: {response.text}")
    
    # Test POST submission
    print("\n9. Testing POST Internship Submission...")
    test_data = {
        "company": "Test Company Inc",
        "mode": "remote",
        "role": "Software Development Intern",
        "duration": "3 months",
        "internship_status": 1,
        "completion_certificate_link": "",
        "lor_link": ""
    }
    response = requests.post(f"{BASE_URL}/cfc/internships/", json=test_data, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        print(f"   ✓ Submission created")
        return True
    else:
        print(f"   ✗ POST failed: {response.text}")
        return False

def test_cfc_genai(token):
    print_section("TESTING CFC - GENAI PROJECT ENDPOINTS")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test GET submissions
    print("\n10. Testing GET GenAI Project Submissions...")
    response = requests.get(f"{BASE_URL}/cfc/genai-projects/", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ GET successful - Found {len(response.json())} submissions")
    else:
        print(f"   ✗ GET failed: {response.text}")
    
    # Test POST submission
    print("\n11. Testing POST GenAI Project Submission...")
    test_data = {
        "problem_statement": "Test problem statement for GenAI project",
        "solution_type": "chatbot",
        "innovation_technology": "Natural Language Processing",
        "innovation_industry": "education",
        "github_repo": "https://github.com/test/repo",
        "demo_link": "https://demo.test.com"
    }
    response = requests.post(f"{BASE_URL}/cfc/genai-projects/", json=test_data, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        print(f"   ✓ Submission created")
        return True
    else:
        print(f"   ✗ POST failed: {response.text}")
        return False

def main():
    print("\n" + "="*60)
    print("  CFC MODULE - COMPREHENSIVE ENDPOINT TEST")
    print("="*60)
    print(f"\n  Base URL: {BASE_URL}")
    print(f"  Test User: {TEST_USER['username']}")
    
    # Test authentication
    token = test_authentication()
    if not token:
        print("\n❌ FAILED: Cannot proceed without authentication")
        return
    
    # Test user profile
    test_user_profile(token)
    
    # Test all CFC modules
    test_cfc_hackathon(token)
    test_cfc_bmc_video(token)
    test_cfc_internship(token)
    test_cfc_genai(token)
    
    print_section("TEST SUMMARY")
    print("\n✓ All endpoint tests completed!")
    print("\nNext steps:")
    print("  1. Check backend terminal for any errors")
    print("  2. Test the UI buttons manually at http://localhost:5173")
    print("  3. Verify form submissions work correctly")
    print("\n")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to backend server")
        print("   Make sure Django is running on http://localhost:8000")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
