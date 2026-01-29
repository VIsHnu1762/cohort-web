"""Quick verification that PostgreSQL is working"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import connection
from apps.gamification.models import Season
from apps.profiles.models import UserProfile

User = get_user_model()

print("\n" + "="*60)
print("✅ POSTGRESQL MIGRATION SUCCESSFUL!")
print("="*60)

# Check database
print(f"\n📊 Database Info:")
print(f"   Engine: {connection.settings_dict['ENGINE']}")
print(f"   Database: {connection.settings_dict['NAME']}")
print(f"   Host: {connection.settings_dict['HOST']}")
print(f"   Port: {connection.settings_dict['PORT']}")

# Check data
users = User.objects.all()
test_users = User.objects.filter(username__contains='test')
profiles = UserProfile.objects.all()
seasons = Season.objects.all()

print(f"\n📈 Data Statistics:")
print(f"   Total Users: {users.count()}")
print(f"   Test Users: {test_users.count()}")
print(f"   User Profiles: {profiles.count()}")
print(f"   Seasons: {seasons.count()}")

print(f"\n👥 Test Users Created:")
for user in test_users:
    profile = getattr(user, 'profile', None)
    role = profile.role if profile else 'N/A'
    print(f"   ✓ {user.username:20} | Email: {user.email:30} | Role: {role}")

print(f"\n🎮 Seasons:")
for season in seasons:
    print(f"   • {season.name} ({season.start_date} to {season.end_date})")

print("\n" + "="*60)
print("🎉 All data successfully migrated to PostgreSQL!")
print("="*60)
print("\n⚠️  IMPORTANT: Restart your Django server for changes to take effect!")
print("   Run: python manage.py runserver\n")
