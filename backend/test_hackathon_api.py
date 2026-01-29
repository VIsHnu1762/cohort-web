import requests
import json

# Test the hackathon list API
url = 'http://127.0.0.1:8000/api/hackathons/list/'

try:
    print("Fetching hackathons from API...")
    response = requests.get(url, timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Success! Found {data.get('count', 0)} hackathons\n")
        
        hackathons = data.get('hackathons', [])
        
        if hackathons:
            print("=" * 80)
            for i, hack in enumerate(hackathons[:10], 1):  # Show first 10
                print(f"\n{i}. {hack.get('name', 'N/A')}")
                print(f"   📅 Date: {hack.get('start_date', 'TBA')}")
                print(f"   📍 Location: {hack.get('location', 'N/A')}")
                print(f"   🌐 Mode: {'Online' if hack.get('is_online') else 'In-Person'}")
                print(f"   🔗 URL: {hack.get('url', 'N/A')}")
                print(f"   📝 Source: {hack.get('source', 'N/A')}")
                print("-" * 80)
        else:
            print("⚠️ No hackathons found. Check if APIs are accessible.")
    else:
        print(f"❌ Error: Status code {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error: {e}")
