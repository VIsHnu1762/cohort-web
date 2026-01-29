"""
Call the setup floor wings endpoint on Railway production
"""
import requests
import json

# API endpoints  
BASE_URL = "https://wholesome-cat-production.up.railway.app/api"
LOGIN_URL = f"{BASE_URL}/auth/token/"
SETUP_FLOORWINGS_URL = f"{BASE_URL}/profiles/admin/setup-floorwings/"

# Admin credentials
ADMIN_EMAIL = "admin@test.com"
ADMIN_PASSWORD = "admin123"

def setup_floorwings():
    print("\n" + "="*80)
    print("SETTING UP FLOOR WING USERS IN RAILWAY PRODUCTION")
    print("="*80 + "\n")
    
    # Step 1: Login as admin to get token
    print("1️⃣  Logging in as admin...")
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
    
    # Step 2: Call setup floor wings endpoint
    print("\n2️⃣  Creating floor wing users...")
    try:
        setup_response = requests.post(
            SETUP_FLOORWINGS_URL,
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
        print(f"   ✅ Setup successful!")
        
        # Display summary
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        summary = result.get('summary', {})
        print(f"✅ Created: {summary.get('created', 0)}")
        print(f"🔄 Updated: {summary.get('updated', 0)}")
        print(f"❌ Errors: {summary.get('errors', 0)}")
        print(f"📊 Total Floor Wings: {summary.get('total_in_db', 0)}")
        print(f"🔑 Default Password: {result.get('default_password', 'N/A')}")
        
        # Display created floor wings
        if result.get('floorwings_created'):
            print("\n" + "="*80)
            print("CREATED FLOOR WINGS")
            print("="*80)
            for fw in result.get('floorwings_created', []):
                print(f"✅ {fw['username']}")
                print(f"   Email: {fw['email']}")
                print(f"   Campus: {fw['campus']}, Floor: {fw['floor']}")
                print()
        
        # Display updated floor wings
        if result.get('floorwings_updated'):
            print("\n" + "="*80)
            print("UPDATED FLOOR WINGS")
            print("="*80)
            for fw in result.get('floorwings_updated', []):
                print(f"🔄 {fw['username']}")
                print(f"   Email: {fw['email']}")
                print(f"   Campus: {fw['campus']}, Floor: {fw['floor']}")
                print()
        
        # Display errors
        if result.get('errors'):
            print("\n" + "="*80)
            print("ERRORS")
            print("="*80)
            for error in result.get('errors', []):
                print(f"❌ {error['username']}: {error['error']}")
        
        # Display all floor wings
        print("\n" + "="*80)
        print("ALL FLOOR WING USERS IN DATABASE")
        print("="*80)
        for fw in result.get('all_floor_wings', []):
            print(f"👤 {fw['username']}")
            print(f"   Email: {fw['email']}")
            print(f"   Campus: {fw['campus_display']}, Floor: {fw['floor']}")
            print()
        
        print("="*80)
        print("✅ FLOOR WING SETUP COMPLETE!")
        print("="*80)
        print("\nNEXT STEPS:")
        print("1. Test login with a floor wing user:")
        print(f"   Username: floorwing_tech_1")
        print(f"   Password: {result.get('default_password', 'floorwing123')}")
        print()
        print("2. Floor wings can access their dashboard at:")
        print("   https://wholesome-cat-production.up.railway.app/floor-wing-dashboard")
        print()
        print("="*80 + "\n")
    
    except Exception as e:
        print(f"   ❌ Setup error: {e}")
        import traceback
        traceback.print_exc()
        return

if __name__ == '__main__':
    setup_floorwings()
