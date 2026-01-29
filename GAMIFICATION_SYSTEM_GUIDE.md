# COHORT GAMIFICATION SYSTEM - IMPLEMENTATION GUIDE

## 🎮 System Overview

**System Name:** COHORT GAMIFICATION SYSTEM  
**Type:** Level-Based, Episode-Driven Quest System  
**Scoring:** 1500 Point System per Season

---

## 📋 INSTALLATION & SETUP

### 1. Backend Setup (Django)

#### Step 1: Run Migrations
```bash
cd backend
python manage.py makemigrations gamification
python manage.py migrate
```

#### Step 2: Create Sample Titles
```bash
python manage.py create_sample_titles
```

#### Step 3: Setup LeetCode Sync Cron Job
Add to your crontab (runs daily at midnight):
```bash
0 0 * * * cd /path/to/backend && python manage.py sync_leetcode_streaks
```

Or use Windows Task Scheduler:
```powershell
# Run daily
python manage.py sync_leetcode_streaks
```

#### Step 4: Create First Season (Django Admin)
1. Go to `http://localhost:8000/admin/`
2. Navigate to **Gamification → Seasons**
3. Click "Add Season"
4. Fill in:
   - Name: "Season 1 - January 2025"
   - Season Number: 1
   - Start Date: 2025-01-01
   - End Date: 2025-01-31
   - Is Active: ✓
5. Save

**Note:** Episodes are auto-created when season is saved (4 episodes, 7 days each)

---

## 🏗️ ARCHITECTURE

### Core Structure

```
Season (1 Month)
  ├── Episode 1 (Week 1 - Kickoff)
  ├── Episode 2 (Week 2 - Build)
  ├── Episode 3 (Week 3 - Intensity)
  └── Episode 4 (Week 4 - Finale)
```

### Five Mandatory Pillars

1. **CLT** - Continuous Learning Track (100 points)
2. **CFC** - Career, Future & Competency (800 points)
3. **IIPC** - Industry Interaction & Professional Connect (200 points)
4. **SRI** - Social Responsibility Initiative (300 points in outcome)
5. **SCD** - Self-Code Development (100 points - LeetCode streak only)

---

## 📅 EPISODE & TASK DISTRIBUTION

### Episode 1 (Week 1 – Kickoff)
- **CLT:** 1 task (course completion)
- **SCD:** Start daily LeetCode streak

### Episode 2 (Week 2 – Build)
- **CFC:** Task 1 (e.g., BMC Video)
- **IIPC:** Task 1 (e.g., LinkedIn Connect)
- **SCD:** Continue streak

### Episode 3 (Week 3 – Intensity)
- **CFC:** Task 2 (e.g., GenAI Project)
- **IIPC:** Task 2 (e.g., LinkedIn Post)
- **SCD:** Continue streak

### Episode 4 (Week 4 – Finale)
- **CFC:** Task 3 (e.g., Hackathon)
- **SRI:** 1 task (social responsibility)
- **SCD:** Full-month streak completion

### Rules
- Episode N unlocks ONLY after Episode N-1 is completed
- Episode completion requires mentor approval of ALL tasks
- Partial season completion = NO score, NO leaderboard, NO vault credits

---

## ⭐ SEASON SCORE SYSTEM (1500 Points)

### Pillar Breakdown

| Pillar | Max Points | Components |
|--------|-----------|------------|
| CLT | 100 | AI Certification |
| IIPC | 200 | LinkedIn Connect (100) + Post/Article (100) |
| SCD | 100 | Daily LeetCode streak (full month) |
| CFC | 800 | BMC (200) + GenAI (200) + Hackathon (200) + Patent/Journal (200) |
| Outcome | 300 | Internship/Placement >= 10 LPA |

**Total:** 1500 points

### SCD CRITICAL OVERRIDE

⚠️ **IMPORTANT:** SCD is based ONLY on daily streak verification, NOT problem count.

Implementation:
- Student links LeetCode username (stored in profile)
- Daily cron job syncs streak data via LeetCode GraphQL API
- Full uninterrupted streak = 100 points
- Partial streaks = reduced points
- Breaks in streak reduce score but don't fail season

---

## 🏆 SCORING NAMES

### 1. Season Score
- Monthly performance (max 1500)
- Resets every season
- Calculated ONLY after full season completion

### 2. Legacy Score
- Lifetime cumulative score
- NEVER resets
- Includes: Season Scores + Ascension Bonus + Achievements

### 3. Vault Credits
- Redeemable currency
- Earned ONLY after full season completion
- Formula: `Season Score ÷ 10` = Credits
- Used for: Titles, OD/WFH, Tech tools
- Spending does NOT reduce Legacy Score

---

## 📈 ASCENSION BONUS

**Name:** Ascension Bonus  
**Value:** +5 Legacy Score points

**Rule:** If Current Season Score > Previous Season Score → Add +5 to Legacy Score

- No penalty for score decrease
- Applies ONLY after full season completion
- Encourages self-improvement over peer competition

---

## 🥇 LEADERBOARD (CHAMPIONS PODIUM)

### Public Display (Top 3 Only)
- **Rank 1:** Season Champion 👑
- **Rank 2 & 3:** Elite Runners 🥇

### Private View (For Others)
Shows:
- Season Score
- Legacy Score
- Vault Credits
- Percentile Bracket (Top 10%, 25%, 50%, Below 50%)

**Note:** Only students who completed full season are ranked

---

## 👔 TITLE SYSTEM

Students redeem Vault Credits to unlock titles displayed next to their name.

### Sample Titles

| Title | Cost | Rarity | Description |
|-------|------|--------|-------------|
| The Consistent 🔥 | 50 | Rare | Completed all episodes without breaking streak |
| The Ascender 📈 | 100 | Epic | Ascension Bonus in 3 consecutive seasons |
| The Finisher ✅ | 30 | Common | First season 100% completion |
| The Quality Champion 👑 | 150 | Legendary | Season Score above 1400 |
| Code Warrior ⚔️ | 80 | Epic | Perfect LeetCode streak |
| Season Champion 🏆 | 200 | Legendary | Achieved Rank 1 |

---

## 👨‍🏫 MENTOR GOVERNANCE

Mentors are the ONLY controlling role:

### Mentor Actions
1. **Approve Task Submissions** → Marks task complete in gamification
2. **Assign Quality Scores** → Influences final scoring
3. **Control Episode Completion** → Unlocks next episode
4. **Finalize Season** → Triggers score calculation
5. **All actions are auditable**

### API Endpoints for Mentors

```javascript
// Approve a task
POST /api/gamification/mentor/approve-task/
{
  "student_id": 123,
  "episode_id": 1,
  "task_type": "clt"  // or "cfc_task1", "iipc_task1", etc.
}

// View student progress
GET /api/gamification/mentor/student-progress/123/

// Finalize student's season
POST /api/gamification/mentor/finalize-season/123/
```

---

## 🔧 API ENDPOINTS (Students - Read-Only)

### Dashboard
```javascript
GET /api/gamification/dashboard/student_overview/
// Returns: Complete gamification dashboard data
```

### Seasons & Episodes
```javascript
GET /api/gamification/seasons/current/
GET /api/gamification/episode-progress/current/
GET /api/gamification/episodes/?season=1
```

### Scores
```javascript
GET /api/gamification/season-scores/current/
GET /api/gamification/legacy-scores/my_score/
```

### Vault & Streak
```javascript
GET /api/gamification/vault-wallets/my_wallet/
GET /api/gamification/scd-streaks/current/
POST /api/gamification/scd-streaks/sync/  // Manual sync
```

### Leaderboard
```javascript
GET /api/gamification/leaderboard/current_season/  // Top 3
GET /api/gamification/leaderboard/my_position/     // Personal position
```

### Titles
```javascript
GET /api/gamification/titles/              // All available titles
GET /api/gamification/user-titles/         // My owned titles
POST /api/gamification/titles/1/redeem/    // Redeem title
POST /api/gamification/titles/1/equip/     // Equip title
```

---

## 💻 FRONTEND INTEGRATION

### Step 1: Import GamificationCard Component

In your student home page (`src/pages/student/Home.jsx`):

```javascript
import GamificationCard from '../../components/GamificationCard';

// Add to your component
<GamificationCard />
```

### Step 2: The Component Shows

- Current Season & Episode
- Episode lock/unlock state
- Task completion status
- Season Score (live)
- Legacy Score (lifetime)
- Vault Credits
- LeetCode Streak
- Leaderboard Position
- Equipped Title

### Integration Guidelines

✅ **DO:**
- Add GamificationCard where you want to display gamification data
- Style to match your existing UI theme
- Show notifications when episodes unlock

❌ **DON'T:**
- Redesign existing pillar submission pages
- Change existing submission workflows
- Break existing APIs

---

## 🔄 WORKFLOW EXAMPLE

### Student Journey

1. **Season Starts** → Episode 1 unlocks automatically
2. **Student submits CLT course** → Mentor reviews
3. **Mentor approves** → Calls API to mark `clt_completed = True`
4. **Student maintains LeetCode streak** → Daily cron syncs
5. **All Episode 1 tasks done** → Episode 1 auto-completes
6. **Episode 2 unlocks** → Student sees new tasks
7. **Repeat for Episodes 2-4**
8. **Episode 4 completes** → Season auto-finalizes
9. **Season Score calculated** (1500 point system)
10. **Legacy Score updated** (+ Ascension Bonus if improved)
11. **Vault Credits allocated** (Score ÷ 10)
12. **Leaderboard updated** (Top 3 shown)

---

## 🛠️ ADMIN TASKS

### Creating New Season

1. Go to Django Admin
2. Add new Season
3. Set start/end dates
4. Mark as active
5. Episodes auto-create

### Monitoring

Check these models in admin:
- `EpisodeProgress` → Track student progress
- `SeasonScore` → View season scores
- `LegacyScore` → Lifetime scores
- `LeaderboardEntry` → Top 3 rankings
- `VaultWallet` → Credit balances

---

## 📊 DATABASE MODELS

### Core Models
1. **Season** - Monthly seasons
2. **Episode** - 4 episodes per season (weekly)
3. **EpisodeProgress** - Student progress through episodes
4. **SeasonScore** - 1500 point breakdown
5. **LegacyScore** - Lifetime cumulative
6. **VaultWallet** - Redeemable credits
7. **SCDStreak** - LeetCode streak tracking
8. **LeaderboardEntry** - Top 3 champions
9. **Title** - Available titles
10. **UserTitle** - Owned/equipped titles
11. **PercentileBracket** - Percentile rankings

---

## 🚀 DAILY OPERATIONS

### Cron Jobs Required

1. **LeetCode Sync** (Daily at midnight)
   ```bash
   python manage.py sync_leetcode_streaks
   ```

2. **Season Auto-Finalization** (End of month)
   - Manually trigger OR
   - Auto-triggers when Episode 4 completes

---

## 🔐 SECURITY & PERMISSIONS

### Student Permissions
- ✅ View own gamification data
- ✅ Sync own LeetCode streak
- ✅ Redeem/equip titles
- ❌ Modify scores
- ❌ Unlock episodes manually
- ❌ View other students' data

### Mentor Permissions
- ✅ View assigned students' progress
- ✅ Approve task submissions
- ✅ Finalize student seasons
- ❌ Modify scores directly
- ❌ Create/delete seasons

### Admin Permissions
- ✅ Full access to all data
- ✅ Create/manage seasons
- ✅ Manage titles
- ✅ Override any data

---

## 📝 TESTING CHECKLIST

### Backend Tests
- [ ] Create season → Episodes auto-create
- [ ] Mark task complete → Episode progress updates
- [ ] Complete Episode 1 → Episode 2 unlocks
- [ ] Complete all 4 episodes → Season finalizes
- [ ] Season finalization → Score calculated
- [ ] Ascension Bonus → Applied correctly
- [ ] Vault Credits → Allocated correctly
- [ ] Leaderboard → Top 3 displayed

### Frontend Tests
- [ ] GamificationCard loads data
- [ ] Episode status displays correctly
- [ ] Tasks show completed/pending
- [ ] Scores update in real-time
- [ ] Leaderboard position shows
- [ ] Title redemption works

### Integration Tests
- [ ] Mentor approves CLT → Gamification updates
- [ ] LeetCode sync → Streak updates
- [ ] Season completes → All calculations correct

---

## 🐛 TROUBLESHOOTING

### Issue: Episodes Not Auto-Creating
**Solution:** Check signals.py is loaded. Season must trigger post_save signal.

### Issue: LeetCode Sync Failing
**Solutions:**
- Check internet connection
- Verify LeetCode username is correct
- LeetCode API may be rate-limited (try again later)

### Issue: Season Not Finalizing
**Check:**
- All 4 episodes completed? Use admin to verify EpisodeProgress
- Manually trigger: `/api/gamification/mentor/finalize-season/{student_id}/`

### Issue: Scores Not Calculating
**Check:**
- Season completed? (all 4 episodes done)
- Submissions approved by mentor?
- Check Django logs for calculation errors

---

## 📞 SUPPORT

For issues or questions:
1. Check Django admin logs
2. Review API responses in browser console
3. Check backend logs: `python manage.py runserver --noreload`

---

## ✅ COMPLETION CRITERIA

System is fully operational when:

- [x] Django models created and migrated
- [x] Service layer logic implemented
- [x] API endpoints functional
- [x] Frontend component created
- [x] Admin interface configured
- [x] Cron job for LeetCode sync
- [x] Documentation complete

---

**System Status:** ✅ READY FOR DEPLOYMENT

**Next Steps:**
1. Run migrations: `python manage.py migrate`
2. Create first season in admin
3. Create sample titles: `python manage.py create_sample_titles`
4. Setup LeetCode sync cron job
5. Integrate GamificationCard into student dashboard
6. Train mentors on approval workflow

**Implementation Date:** December 20, 2025  
**Version:** 1.0.0
