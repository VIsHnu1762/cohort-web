"""
Quick setup script for Gamification System
Run this after migrations are complete
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone
from datetime import timedelta
from apps.gamification.models import Season, Title

def create_first_season():
    """Create the first active season"""
    print("Creating first season...")
    
    # Check if season already exists
    if Season.objects.exists():
        print("✓ Season already exists")
        return
    
    # Create season starting from next month
    today = timezone.now().date()
    start_date = today.replace(day=1) + timedelta(days=32)
    start_date = start_date.replace(day=1)  # First day of next month
    end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)  # Last day of month
    
    season = Season.objects.create(
        name=f"Season 1 - {start_date.strftime('%B %Y')}",
        season_number=1,
        start_date=start_date,
        end_date=end_date,
        is_active=True
    )
    
    print(f"✓ Created Season 1: {season.name}")
    print(f"  Start: {start_date}")
    print(f"  End: {end_date}")
    print(f"  Episodes will be auto-created")

def create_titles():
    """Create sample titles"""
    print("\nCreating titles...")
    
    titles_data = [
        {
            'name': 'The Consistent',
            'description': 'Completed all episodes without breaking streak',
            'vault_credit_cost': 50,
            'icon': '🔥',
            'rarity': 'rare'
        },
        {
            'name': 'The Ascender',
            'description': 'Achieved Ascension Bonus in 3 consecutive seasons',
            'vault_credit_cost': 100,
            'icon': '📈',
            'rarity': 'epic'
        },
        {
            'name': 'The Finisher',
            'description': 'Completed first season with 100% episode completion',
            'vault_credit_cost': 30,
            'icon': '✅',
            'rarity': 'common'
        },
        {
            'name': 'The Quality Champion',
            'description': 'Achieved Season Score above 1400',
            'vault_credit_cost': 150,
            'icon': '👑',
            'rarity': 'legendary'
        },
        {
            'name': 'Code Warrior',
            'description': 'Maintained perfect LeetCode streak for entire season',
            'vault_credit_cost': 80,
            'icon': '⚔️',
            'rarity': 'epic'
        },
    ]
    
    created = 0
    for title_data in titles_data:
        title, created_new = Title.objects.get_or_create(
            name=title_data['name'],
            defaults=title_data
        )
        if created_new:
            created += 1
            print(f"✓ Created: {title.name}")
    
    print(f"\n✓ {created} titles created ({Title.objects.count()} total)")

def main():
    print("=" * 60)
    print("GAMIFICATION SYSTEM SETUP")
    print("=" * 60)
    
    try:
        create_first_season()
        create_titles()
        
        print("\n" + "=" * 60)
        print("✓ SETUP COMPLETE!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Check Django admin: http://localhost:8000/admin/")
        print("2. Navigate to Gamification → Seasons")
        print("3. Verify Season 1 and Episodes are created")
        print("4. Setup daily cron: python manage.py sync_leetcode_streaks")
        print("5. Integrate GamificationCard into frontend")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
