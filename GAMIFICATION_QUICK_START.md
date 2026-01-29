# 🚀 GAMIFICATION SYSTEM - QUICK START COMMANDS

## Initial Setup (Run Once)

```bash
# 1. Navigate to backend
cd backend

# 2. Create migrations
python manage.py makemigrations gamification

# 3. Apply migrations
python manage.py migrate

# 4. Run setup script
python setup_gamification.py

# 5. Create sample titles
python manage.py create_sample_titles

# 6. Create superuser (if not already)
python manage.py createsuperuser

# 7. Start server
python manage.py runserver
```

## Access Points

```
Django Admin: http://localhost:8000/admin/
API Documentation: http://localhost:8000/api/docs/
Gamification Admin: http://localhost:8000/admin/gamification/
```

## Create First Season (Django Admin)

1. Go to: http://localhost:8000/admin/gamification/season/
2. Click "Add Season"
3. Fill in:
   - Name: `Season 1 - January 2025`
   - Season Number: `1`
   - Start Date: `2025-01-01`
   - End Date: `2025-01-31`
   - Is Active: ✓
4. Save (Episodes auto-create)

## Daily Operations

```bash
# Sync LeetCode streaks (run daily at midnight)
python manage.py sync_leetcode_streaks

# Check current season
python manage.py shell
>>> from apps.gamification.models import Season
>>> Season.objects.filter(is_active=True).first()
```

## Testing APIs (cURL)

```bash
# Get JWT token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"student@test.com","password":"password"}'

# Get student dashboard
curl http://localhost:8000/api/gamification/dashboard/student_overview/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get current leaderboard
curl http://localhost:8000/api/gamification/leaderboard/current_season/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Mentor approve task
curl -X POST http://localhost:8000/api/gamification/mentor/approve-task/ \
  -H "Authorization: Bearer MENTOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"student_id":1,"episode_id":1,"task_type":"clt"}'
```

## Frontend Integration

```bash
# 1. Component is already created at: src/components/GamificationCard.jsx

# 2. Add to student dashboard (src/pages/student/Home.jsx):

import GamificationCard from '../../components/GamificationCard';

// Inside your component JSX:
<GamificationCard />
```

## Setup Cron Job

### Linux/Mac
```bash
# Edit crontab
crontab -e

# Add this line (runs daily at midnight)
0 0 * * * cd /path/to/backend && /path/to/python manage.py sync_leetcode_streaks
```

### Windows (Task Scheduler)
```powershell
# Open Task Scheduler
# Create Basic Task
# Name: "LeetCode Streak Sync"
# Trigger: Daily at 12:00 AM
# Action: Start a program
# Program: C:\Path\To\python.exe
# Arguments: manage.py sync_leetcode_streaks
# Start in: C:\Path\To\backend
```

### Using Windows Command
```powershell
# Run this in PowerShell as Administrator
$action = New-ScheduledTaskAction -Execute "python" -Argument "manage.py sync_leetcode_streaks" -WorkingDirectory "C:\Python310\cohort_webapp\cohort\backend"
$trigger = New-ScheduledTaskTrigger -Daily -At 12:00AM
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "LeetCodeSync" -Description "Daily LeetCode streak sync"
```

## Verification Commands

```bash
# Check tables created
python manage.py dbshell
> .tables
> SELECT * FROM gamification_season;
> .exit

# Check migrations
python manage.py showmigrations gamification

# Verify episodes auto-created
python manage.py shell
>>> from apps.gamification.models import Season, Episode
>>> season = Season.objects.first()
>>> season.episodes.count()  # Should be 4
```

## Common Admin Tasks

```bash
# Create a new season (Django shell)
python manage.py shell

>>> from apps.gamification.models import Season
>>> from datetime import date
>>> Season.objects.create(
...     name="Season 2 - February 2025",
...     season_number=2,
...     start_date=date(2025, 2, 1),
...     end_date=date(2025, 2, 28),
...     is_active=True
... )

# Check student progress
>>> from apps.gamification.models import EpisodeProgress
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> student = User.objects.get(username='student@test.com')
>>> EpisodeProgress.objects.filter(student=student)

# Manually finalize a season
>>> from apps.gamification.services import SeasonScoringService
>>> season = Season.objects.get(season_number=1)
>>> result, msg = SeasonScoringService.finalize_season(student, season)
>>> print(msg)
```

## Monitoring

```bash
# Check vault balances
python manage.py shell
>>> from apps.gamification.models import VaultWallet
>>> VaultWallet.objects.values('student__username', 'available_credits')

# View leaderboard
>>> from apps.gamification.models import LeaderboardEntry
>>> LeaderboardEntry.objects.filter(season__is_active=True)

# Check streak data
>>> from apps.gamification.models import SCDStreak
>>> SCDStreak.objects.values('student__username', 'current_streak', 'streak_score')
```

## Troubleshooting Commands

```bash
# Reset a student's episode progress
python manage.py shell
>>> from apps.gamification.models import EpisodeProgress
>>> EpisodeProgress.objects.filter(student_id=1).delete()

# Recalculate season score
>>> from apps.gamification.services import SeasonScoringService
>>> from apps.gamification.models import Season
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> student = User.objects.get(id=1)
>>> season = Season.objects.filter(is_active=True).first()
>>> SeasonScoringService.finalize_season(student, season)

# Manual LeetCode sync for one student
>>> from apps.gamification.services import LeetCodeSyncService
>>> result, msg = LeetCodeSyncService.sync_student_streak(student, season)
>>> print(msg)
```

## File Locations Reference

```
Backend:
- Models: backend/apps/gamification/models.py
- Services: backend/apps/gamification/services.py
- Views: backend/apps/gamification/views.py
- URLs: backend/apps/gamification/urls.py
- Admin: backend/apps/gamification/admin.py

Frontend:
- Component: src/components/GamificationCard.jsx
- Styles: src/components/GamificationCard.css
- API Service: src/services/gamification.js

Documentation:
- Main Guide: GAMIFICATION_SYSTEM_GUIDE.md
- Implementation: GAMIFICATION_IMPLEMENTATION_COMPLETE.md
- Quick Start: GAMIFICATION_QUICK_START.md (this file)
- Mentor Guide: MENTOR_GAMIFICATION_INTEGRATION.js
```

## API Endpoint Quick Reference

```
Student (Read-Only):
GET /api/gamification/dashboard/student_overview/
GET /api/gamification/seasons/current/
GET /api/gamification/episode-progress/current/
GET /api/gamification/season-scores/current/
GET /api/gamification/legacy-scores/my_score/
GET /api/gamification/vault-wallets/my_wallet/
GET /api/gamification/scd-streaks/current/
POST /api/gamification/scd-streaks/sync/
GET /api/gamification/leaderboard/current_season/
GET /api/gamification/leaderboard/my_position/
GET /api/gamification/titles/
POST /api/gamification/titles/{id}/redeem/
POST /api/gamification/titles/{id}/equip/

Mentor (Control):
POST /api/gamification/mentor/approve-task/
GET /api/gamification/mentor/student-progress/{student_id}/
POST /api/gamification/mentor/finalize-season/{student_id}/
```

## Task Type Reference

```javascript
Episode 1: 'clt', 'scd_streak'
Episode 2: 'cfc_task1', 'iipc_task1', 'scd_streak'
Episode 3: 'cfc_task2', 'iipc_task2', 'scd_streak'
Episode 4: 'cfc_task3', 'sri', 'scd_streak'
```

## Status Checks

```bash
# Is system ready?
python -c "
from apps.gamification.models import Season, Episode, Title
print(f'Seasons: {Season.objects.count()}')
print(f'Episodes: {Episode.objects.count()}')
print(f'Titles: {Title.objects.count()}')
print('✓ System Ready' if all([Season.objects.exists(), Episode.objects.exists(), Title.objects.exists()]) else '✗ Setup incomplete')
"
```

## Production Deployment

```bash
# 1. Set environment variables
export DEBUG=False
export SECRET_KEY=your-production-secret-key

# 2. Collect static files
python manage.py collectstatic --noinput

# 3. Run with gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000

# 4. Setup cron job on production server
# 5. Configure reverse proxy (nginx)
# 6. Enable HTTPS
```

## Testing Checklist

```bash
# Test 1: Create season
# ✓ 4 episodes auto-created

# Test 2: Approve CLT task
curl -X POST http://localhost:8000/api/gamification/mentor/approve-task/ \
  -H "Authorization: Bearer TOKEN" \
  -d '{"student_id":1,"episode_id":1,"task_type":"clt"}'

# Test 3: Check episode progress
curl http://localhost:8000/api/gamification/episode-progress/current/ \
  -H "Authorization: Bearer STUDENT_TOKEN"

# Test 4: Complete all episodes and verify season finalization
# Test 5: Check leaderboard updates
# Test 6: Test title redemption
```

---

**Quick Start Complete!** 🚀

For detailed information, see:
- `GAMIFICATION_SYSTEM_GUIDE.md` - Complete guide
- `GAMIFICATION_IMPLEMENTATION_COMPLETE.md` - Implementation summary
