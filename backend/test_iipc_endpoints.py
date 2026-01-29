"""
IIPC Endpoints Testing Script
Tests all LinkedIn Post and Connection Verification endpoints
"""

import requests
import json
from datetime import date, timedelta

BASE_URL = "http://127.0.0.1:8000"
EMAIL = "admin@example.com"
PASSWORD = "admin123"

def test_authentication():
    """Test authentication and get access token"""
    print("\n" + "="*60)
    print("1. TESTING AUTHENTICATION")
    print("="*60)
    
    response = requests.post(f"{BASE_URL}/api/auth/token/", json={
        "username": EMAIL,
        "password": PASSWORD
    })
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Authentication successful")
        print(f"  Access Token: {data['access'][:50]}...")
        return data['access']
    else:
        print(f"✗ Authentication failed: {response.text}")
        return None


def test_user_profile(token):
    """Test user profile endpoint"""
    print("\n" + "="*60)
    print("2. TESTING USER PROFILE")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/auth/user/", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ User Profile retrieved")
        print(f"  Username: {data['username']}")
        print(f"  Email: {data['email']}")
        print(f"  Role: {data['role']}")
        return True
    else:
        print(f"✗ Failed: {response.text}")
        return False


def test_linkedin_posts(token):
    """Test LinkedIn Post Verification endpoints"""
    print("\n" + "="*60)
    print("3. TESTING LINKEDIN POST VERIFICATION")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # GET - List all posts
    print("\n3.1. GET /api/iipc/posts/ - List all posts")
    response = requests.get(f"{BASE_URL}/api/iipc/posts/", headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        posts = response.json()
        print(f"✓ Retrieved {len(posts)} post(s)")
    else:
        print(f"✗ Failed: {response.text}")
        return False
    
    # POST - Create new post verification
    print("\n3.2. POST /api/iipc/posts/ - Create new post")
    post_data = {
        "post_url": "https://www.linkedin.com/posts/test-user_innovation-technology-ai-activity-123456789",
        "post_date": str(date.today() - timedelta(days=5)),
        "character_count": 487,
        "hashtag_count": 5
    }
    response = requests.post(f"{BASE_URL}/api/iipc/posts/", headers=headers, json=post_data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 201:
        post = response.json()
        post_id = post['id']
        print(f"✓ Post created successfully")
        print(f"  ID: {post_id}")
        print(f"  Post URL: {post['post_url']}")
        print(f"  Character Count: {post['character_count']}")
        print(f"  Hashtag Count: {post['hashtag_count']}")
        print(f"  Status: {post['status']}")
    else:
        print(f"✗ Failed: {response.text}")
        return False
    
    # GET - Stats endpoint
    print("\n3.3. GET /api/iipc/posts/stats/ - Get statistics")
    response = requests.get(f"{BASE_URL}/api/iipc/posts/stats/", headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print(f"✓ Stats retrieved:")
        print(f"  Total: {stats['total']}")
        print(f"  Draft: {stats['draft']}")
        print(f"  Pending: {stats['pending']}")
        print(f"  Approved: {stats['approved']}")
    else:
        print(f"✗ Failed: {response.text}")
        return False
    
    # POST - Submit for review
    print(f"\n3.4. POST /api/iipc/posts/{post_id}/submit/ - Submit for review")
    response = requests.post(f"{BASE_URL}/api/iipc/posts/{post_id}/submit/", headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        post = response.json()
        print(f"✓ Post submitted for review")
        print(f"  Status: {post['status']}")
    else:
        print(f"✗ Failed: {response.text}")
    
    return True


def test_linkedin_connections(token):
    """Test LinkedIn Connection Verification endpoints"""
    print("\n" + "="*60)
    print("4. TESTING LINKEDIN CONNECTION VERIFICATION")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # GET - List all connections
    print("\n4.1. GET /api/iipc/connections/ - List all verifications")
    response = requests.get(f"{BASE_URL}/api/iipc/connections/", headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        connections = response.json()
        print(f"✓ Retrieved {len(connections)} verification(s)")
    else:
        print(f"✗ Failed: {response.text}")
        return False
    
    # POST - Create connection verification with screenshots
    print("\n4.2. POST /api/iipc/connections/ - Create with screenshots")
    connection_data = {
        "verification_method": "screenshot",
        "total_connections": 0,
        "screenshot_urls": [
            "https://drive.google.com/file/d/1234567890abcdef/view",
            "https://drive.google.com/file/d/abcdef1234567890/view"
        ],
        "verified_connections": [
            {
                "name": "John Smith",
                "company": "Google",
                "designation": "Senior Software Engineer",
                "profile_url": "https://www.linkedin.com/in/john-smith",
                "is_verified": True
            },
            {
                "name": "Sarah Johnson",
                "company": "Microsoft",
                "designation": "Product Manager",
                "profile_url": "https://www.linkedin.com/in/sarah-johnson",
                "is_verified": True
            },
            {
                "name": "Mike Chen",
                "company": "Amazon",
                "designation": "Tech Lead",
                "profile_url": "https://www.linkedin.com/in/mike-chen",
                "is_verified": True
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/api/iipc/connections/", headers=headers, json=connection_data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 201:
        connection = response.json()
        connection_id = connection['id']
        print(f"✓ Connection verification created")
        print(f"  ID: {connection_id}")
        print(f"  Total Connections: {connection['total_connections']}")
        print(f"  Verified Count: {connection['verified_connections_count']}")
        print(f"  Screenshots: {len(connection['screenshots'])}")
    else:
        print(f"✗ Failed: {response.text}")
        return False
    
    # GET - Stats endpoint
    print("\n4.3. GET /api/iipc/connections/stats/ - Get statistics")
    response = requests.get(f"{BASE_URL}/api/iipc/connections/stats/", headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print(f"✓ Stats retrieved:")
        print(f"  Total: {stats['total']}")
        print(f"  Draft: {stats['draft']}")
        print(f"  Pending: {stats['pending']}")
        print(f"  Approved: {stats['approved']}")
    else:
        print(f"✗ Failed: {response.text}")
        return False
    
    # GET - Combined stats
    print("\n4.4. GET /api/iipc/connections/all_stats/ - Get combined IIPC stats")
    response = requests.get(f"{BASE_URL}/api/iipc/connections/all_stats/", headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print(f"✓ Combined stats retrieved:")
        print(f"  Total Posts: {stats['total_posts']}")
        print(f"  Total Connections: {stats['total_connections']}")
        print(f"  Approved Posts: {stats['approved_posts']}")
        print(f"  Approved Connections: {stats['approved_connections']}")
    else:
        print(f"✗ Failed: {response.text}")
        return False
    
    # POST - Submit for review
    print(f"\n4.5. POST /api/iipc/connections/{connection_id}/submit/ - Submit for review")
    response = requests.post(f"{BASE_URL}/api/iipc/connections/{connection_id}/submit/", headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        connection = response.json()
        print(f"✓ Connection verification submitted")
        print(f"  Status: {connection['status']}")
    else:
        print(f"✗ Failed: {response.text}")
    
    # POST - Create with profile method
    print("\n4.6. POST /api/iipc/connections/ - Create with profile link")
    profile_data = {
        "verification_method": "profile",
        "profile_url": "https://www.linkedin.com/in/test-user-profile",
        "total_connections": 0
    }
    response = requests.post(f"{BASE_URL}/api/iipc/connections/", headers=headers, json=profile_data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 201:
        connection = response.json()
        print(f"✓ Profile-based verification created")
        print(f"  ID: {connection['id']}")
        print(f"  Method: {connection['verification_method']}")
        print(f"  Profile URL: {connection['profile_url']}")
    else:
        print(f"✗ Failed: {response.text}")
    
    # POST - Connect LinkedIn Profile
    print("\n4.7. POST /api/iipc/connections/connect_profile/ - Connect profile")
    connect_data = {
        "profile_url": "https://www.linkedin.com/in/jane-smith",
        "total_connections": 0
    }
    response = requests.post(f"{BASE_URL}/api/iipc/connections/connect_profile/", headers=headers, json=connect_data)
    print(f"Status Code: {response.status_code}")
    if response.status_code in [200, 201]:
        data = response.json()
        print(f"✓ {data['message']}")
        print(f"  Created: {data['created']}")
        print(f"  Verification ID: {data['verification']['id']}")
        print(f"  Total Connections: {data['verification']['total_connections']}")
    else:
        print(f"✗ Failed: {response.text}")
    
    return True


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("IIPC ENDPOINTS TESTING")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    print(f"Test User: {EMAIL}")
    
    # Test authentication
    token = test_authentication()
    if not token:
        print("\n✗ Authentication failed. Cannot proceed with tests.")
        return
    
    # Test user profile
    test_user_profile(token)
    
    # Test LinkedIn posts
    test_linkedin_posts(token)
    
    # Test LinkedIn connections
    test_linkedin_connections(token)
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print("="*60)


if __name__ == "__main__":
    main()
