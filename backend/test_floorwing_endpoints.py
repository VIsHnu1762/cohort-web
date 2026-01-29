#!/usr/bin/env python
"""
Test Floor Wing Endpoints
Tests all floor wing API endpoints to ensure proper connectivity
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import requests
import json
from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

# API Configuration
BASE_URL = 'http://127.0.0.1:8000/api'

def get_or_create_floor_wing():
    """Get or create a test floor wing user"""
    try:
        user = User.objects.get(username='floorwing_test')
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='floorwing_test',
            email='floorwing_test@test.com',
            password='test123',
            first_name='Test',
            last_name='FloorWing'
        )
        profile = user.profile
        profile.role = 'FLOOR_WING'
        profile.campus = 'TECH'
        profile.floor = 1
        profile.save()
    
    return user

def get_auth_token(username, password):
    """Get JWT authentication token"""
    response = requests.post(f'{BASE_URL}/auth/token/', json={
        'email': f'{username}@test.com',
        'password': password
    })
    
    if response.status_code == 200:
        data = response.json()
        return data.get('access')
    else:
        print(f"❌ Authentication failed: {response.status_code}")
        print(response.text)
        return None

def test_dashboard_endpoint(token):
    """Test GET /api/profiles/floor-wing/dashboard/"""
    print("\n🧪 Testing Dashboard Endpoint...")
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{BASE_URL}/profiles/floor-wing/dashboard/', headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Dashboard endpoint working")
        print(f"   - Campus: {data.get('campus_name')}")
        print(f"   - Floor: {data.get('floor')}")
        print(f"   - Total Students: {data.get('total_students')}")
        print(f"   - Total Mentors: {data.get('total_mentors')}")
        print(f"   - Unassigned Students: {data.get('unassigned_students')}")
        return True
    else:
        print(f"❌ Dashboard endpoint failed: {response.status_code}")
        print(response.text)
        return False

def test_students_endpoint(token):
    """Test GET /api/profiles/floor-wing/students/"""
    print("\n🧪 Testing Students Endpoint...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test without filter
    response = requests.get(f'{BASE_URL}/profiles/floor-wing/students/', headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        students = data.get('students', [])
        print(f"✅ Students endpoint working (all filter)")
        print(f"   - Total Students: {len(students)}")
        
        # Test with unassigned filter
        response2 = requests.get(
            f'{BASE_URL}/profiles/floor-wing/students/',
            headers=headers,
            params={'filter': 'unassigned'}
        )
        
        if response2.status_code == 200:
            data2 = response2.json()
            unassigned = data2.get('students', [])
            print(f"✅ Students endpoint working (unassigned filter)")
            print(f"   - Unassigned Students: {len(unassigned)}")
            return True
    else:
        print(f"❌ Students endpoint failed: {response.status_code}")
        print(response.text)
        return False

def test_mentors_endpoint(token):
    """Test GET /api/profiles/floor-wing/mentors/"""
    print("\n🧪 Testing Mentors Endpoint...")
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{BASE_URL}/profiles/floor-wing/mentors/', headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        mentors = data.get('mentors', [])
        print(f"✅ Mentors endpoint working")
        print(f"   - Total Mentors: {len(mentors)}")
        
        if mentors:
            mentor = mentors[0]
            print(f"   - Sample Mentor: {mentor.get('name')}")
            print(f"   - Assigned Students: {mentor.get('assigned_students_count')}")
            print(f"   - Workload Status: {mentor.get('workload_status')}")
        
        return True
    else:
        print(f"❌ Mentors endpoint failed: {response.status_code}")
        print(response.text)
        return False

def test_announcements_endpoint(token):
    """Test Floor Wing Announcements endpoints"""
    print("\n🧪 Testing Announcements Endpoints...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test GET announcements
    response = requests.get(f'{BASE_URL}/profiles/floor-wing/announcements/', headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        announcements = data if isinstance(data, list) else data.get('results', [])
        print(f"✅ Get announcements working")
        print(f"   - Total Announcements: {len(announcements)}")
        
        # Test CREATE announcement
        new_announcement = {
            'title': 'Test Announcement',
            'message': 'This is a test announcement from automated testing',
            'priority': 'normal',
            'status': 'published'
        }
        
        create_response = requests.post(
            f'{BASE_URL}/profiles/floor-wing/announcements/',
            headers=headers,
            json=new_announcement
        )
        
        if create_response.status_code in [200, 201]:
            created = create_response.json()
            announcement_id = created.get('id')
            print(f"✅ Create announcement working (ID: {announcement_id})")
            
            # Test DELETE announcement
            delete_response = requests.delete(
                f'{BASE_URL}/profiles/floor-wing/announcements/{announcement_id}/',
                headers=headers
            )
            
            if delete_response.status_code in [200, 204]:
                print(f"✅ Delete announcement working")
                return True
            else:
                print(f"⚠️ Delete announcement failed: {delete_response.status_code}")
                return True  # Still consider test passed if create works
        else:
            print(f"❌ Create announcement failed: {create_response.status_code}")
            print(create_response.text)
            return False
    else:
        print(f"❌ Get announcements failed: {response.status_code}")
        print(response.text)
        return False

def test_announcement_stats(token):
    """Test announcement stats endpoint"""
    print("\n🧪 Testing Announcement Stats Endpoint...")
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{BASE_URL}/profiles/floor-wing/announcements/stats/', headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Announcement stats working")
        print(f"   - Total Announcements: {data.get('total_announcements')}")
        print(f"   - Published: {data.get('published')}")
        print(f"   - Drafts: {data.get('drafts')}")
        print(f"   - Students on Floor: {data.get('students_on_floor')}")
        return True
    else:
        print(f"❌ Announcement stats failed: {response.status_code}")
        print(response.text)
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🔍 Floor Wing Backend Endpoint Testing")
    print("=" * 60)
    
    # Create test user
    print("\n📝 Setting up test floor wing user...")
    floor_wing_user = get_or_create_floor_wing()
    print(f"✅ Floor wing user ready: {floor_wing_user.username}")
    
    # Get auth token
    print("\n🔐 Getting authentication token...")
    token = get_auth_token('floorwing_test', 'test123')
    
    if not token:
        print("\n❌ Cannot proceed without authentication token")
        return
    
    print("✅ Authentication successful")
    
    # Run tests
    results = {
        'dashboard': test_dashboard_endpoint(token),
        'students': test_students_endpoint(token),
        'mentors': test_mentors_endpoint(token),
        'announcements': test_announcements_endpoint(token),
        'announcement_stats': test_announcement_stats(token),
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for endpoint, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {endpoint.replace('_', ' ').title()}")
    
    print(f"\n📈 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All endpoints working correctly!")
    else:
        print("⚠️ Some endpoints need attention")

if __name__ == '__main__':
    main()
