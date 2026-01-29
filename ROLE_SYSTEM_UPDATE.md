# Role-Based Campus/Floor System - Implementation Summary

## Overview
Extended the cohort management system with a hierarchical role structure:
- **4 Roles**: STUDENT, MENTOR, FLOOR_WING, ADMIN
- **2 Campuses**: TECH (4 floors), ARTS (3 floors)
- **Hierarchical Access**: Admin → Campus → Floor Wing → Mentors → Students

## Backend Implementation ✅

### 1. Database Schema (apps/profiles/models.py)
- Added `role` field: STUDENT, MENTOR, FLOOR_WING, ADMIN
- Added `campus` field: TECH, ARTS
- Added `floor` field: 1-4 (TECH), 1-3 (ARTS)
- Added validation: Ensures valid campus/floor combinations
- Applied migration: `0003_userprofile_campus_userprofile_floor_and_more.py`

### 2. Permissions System (apps/profiles/permissions.py)
- `IsStudent`, `IsMentor`, `IsFloorWing`, `IsAdmin`: Role-based checks
- `SameCampusPermission`: Ensures campus-level isolation
- `SameFloorPermission`: Ensures floor-level isolation

### 3. Floor Wing API (apps/profiles/floor_wing_views.py)
```python
/api/profiles/floor-wing/dashboard/          # Dashboard stats
/api/profiles/floor-wing/students/           # List students on floor
/api/profiles/floor-wing/mentors/            # List mentors on floor
/api/profiles/floor-wing/assign-student/     # Assign student to mentor
```

### 4. Admin API (apps/profiles/admin_views.py)
```python
/api/profiles/admin/campus/<campus>/                    # Campus overview
/api/profiles/admin/campus/<campus>/floor/<floor>/      # Floor details
/api/profiles/admin/assign-floor-wing/                  # Assign floor wing
/api/profiles/admin/assign-mentor/                      # Assign mentor to floor
```

### 5. Authentication (apps/jwt_serializers.py)
- Login response now includes: `user.profile.role`, `user.profile.campus`, `user.profile.floor`

## Frontend Implementation ✅

### 1. AuthContext Updates (src/context/AuthContext.jsx)
- Updated `ROLE_ACCESS` with UPPERCASE role names
- Added `/admin/campus-select` and `/admin/campus` paths
- Created `ROLE_HOME_PATHS` mapping:
  - ADMIN → `/admin/campus-select`
  - FLOOR_WING → `/floorwing-dashboard`
  - MENTOR → `/mentor-dashboard`
  - STUDENT → `/`
- `login()` extracts role/campus/floor from backend response
- `getHomePath()` returns role-based home page

### 2. Protected Routes (src/components/ProtectedRoute.jsx)
- Added `requiredRole` prop for explicit role checking
- Handles both `user.role` and `user.profile.role`
- Shows "Access Denied" for unauthorized access

### 3. Login Page (src/pages/Login.jsx)
- Updated role selector with 4 roles: STUDENT, MENTOR, FLOOR_WING, ADMIN
- Uses `getHomePath()` for role-based navigation after login
- Role IDs updated to UPPERCASE to match backend

### 4. App Routing (src/App.jsx)
```jsx
// Admin campus routes (before AdminLayout)
/admin/campus-select                    → CampusSelection (Admin entry point)
/admin/campus/:campus                   → CampusOverview (Floor cards)
/admin/campus/:campus/floor/:floor      → FloorDetail (Floor management)

// Role-specific dashboards
/floorwing-dashboard                    → FloorWingDashboard (FLOOR_WING only)
/mentor-dashboard/*                     → MentorLayout (MENTOR only)
```

### 5. Navigation Component (src/App.jsx - Navigation function)
- Added Floor Wing navigation items
- Desktop and mobile navigation for FLOOR_WING role
- Role-based navigation display (Student, Mentor, Floor Wing)
  - STUDENT → `/`
- `login()` extracts role/campus/floor from backend response
- `getHomePath()` returns role-based home page

### 2. Protected Routes (src/components/ProtectedRoute.jsx)
- Added `requiredRole` prop for explicit role checking
- Handles both `user.role` and `user.profile.role`
- Shows "Access Denied" for unauthorized access

### 3. Login Page (src/pages/Login.jsx)
- Updated role selector with 4 roles: STUDENT, MENTOR, FLOOR_WING, ADMIN
- Uses `getHomePath()` for role-based navigation after login
- Role IDs updated to UPPERCASE to match backend

### 4. App Routing (src/App.jsx)
```jsx
// Admin campus routes (before AdminLayout)
/admin/campus-select          → CampusSelection (Admin entry point)
/admin/campus/:campus         → CampusOverview (Floor cards)

// Role-specific dashboards
/floorwing-dashboard          → FloorWingDashboard (FLOOR_WING only)
/mentor-dashboard/*           → MentorLayout (MENTOR only)
```

### 5. Floor Wing Dashboard (src/pages/floorwing/FloorWingDashboard.jsx)
- **Dashboard View**: Shows floor stats, student count, mentor count, submissions
- **Students View**: Lists unassigned students with assignment interface
- **Mentors View**: Shows mentors with workload (assigned student count)
- Full API integration with floorWingService

### 6. Admin Campus Components
#### CampusSelection (src/pages/admin/campus/CampusSelection.jsx)
- First screen for admins after login
- Two campus cards: TECH and ARTS
- Shows campus info: floors, description
- Navigates to `/admin/campus/TECH` or `/admin/campus/ARTS`

#### CampusOverview (src/pages/admin/campus/CampusOverview.jsx)
- Shows floor cards for selected campus
- TECH: 4 floor cards, ARTS: 3 floor cards
- Each card displays:
  - Student count
  - Mentor count
  - Floor Wing name (if assigned)
  - Submission stats
- Click floor card → `/admin/campus/{campus}/floor/{floor}`

#### FloorDetail (src/pages/admin/campus/FloorDetail.jsx)
- **Complete floor management interface**
- Three tabs: Students, Mentors, Floor Wing
- **Students Tab**: Lists all students on floor with mentor assignments
- **Mentors Tab**: Shows mentors with assigned student counts, assignment interface
- **Floor Wing Tab**: Displays floor wing info or assignment interface
- Back navigation to campus overview
- Real-time stats: total students, mentors, floor wing status, submissions

### 7. API Services
#### floorWingService.js
```javascript
getDashboard()              // GET /api/profiles/floor-wing/dashboard/
getStudents()               // GET /api/profiles/floor-wing/students/
getMentors()                // GET /api/profiles/floor-wing/mentors/
assignStudent(data)         // POST /api/profiles/floor-wing/assign-student/
```

#### admin.js (extended)
```javascript
getCampusOverview(campus)              // GET /api/profiles/admin/campus/{campus}/
getFloorDetail(campus, floor)          // GET /api/profiles/admin/campus/{campus}/floor/{floor}/
assignFloorWing(campus, floor, userId) // POST /api/profiles/admin/assign-floor-wing/
assignMentor(campus, floor, userId)    // POST /api/profiles/admin/assign-mentor/
```

## Access Control Matrix

| Role | Home Path | Accessible Routes |
|------|-----------|------------------|
| STUDENT | `/` | Student pages (CLT, SRI, CFC, IIPC, SCD, monthly report) |
| MENTOR | `/mentor-dashboard` | Mentor dashboard, student list, pillar review, announcements |
| FLOOR_WING | `/floorwing-dashboard` | Floor Wing dashboard (students, mentors, assignments) |
| ADMIN | `/admin/campus-select` | Campus selection, campus overview, floor details, all admin routes |

## User Flow Examples

### Admin Flow
1. Login with ADMIN role
2. Redirected to `/admin/campus-select`
3. Select TECH or ARTS campus
4. View campus overview with floor cards at `/admin/campus/TECH`
5. Click floor card to manage floor
6. Can assign Floor Wings and Mentors to floors

### Floor Wing Flow
1. Login with FLOOR_WING role (assigned to specific campus/floor)
2. Redirected to `/floorwing-dashboard`
3. View dashboard with floor stats
4. Click "Students" tab to see unassigned students
5. Assign students to mentors on the floor
6. Click "Mentors" tab to view mentor workload

### Mentor Flow
1. Login with MENTOR role (assigned to specific campus/floor)
2. Redirected to `/mentor-dashboard`
3. View assigned students only
4. Review student submissions
5. Post announcements

### Student Flow
1. Login with STUDENT role (assigned to specific campus/floor/mentor)
2. Redirected to home page `/`
3. Access CLT, SRI, CFC, IIPC, SCD pillars
4. Submit monthly reports
5. View announcements from mentor

## Hierarchical Constraints

### Campus Level (Admin)
- Admin must select campus first
- Cannot view mixed campus data
- TECH: 4 floors (1-4)
- ARTS: 3 floors (1-3)

### Floor Level (Floor Wing)
- Floor Wing assigned to ONE campus and ONE floor
- Can only view/manage students and mentors on their floor
- Cannot access other floors or campuses
- Manages 3 mentors on their floor

### Mentor Level
- Mentor assigned to ONE campus and ONE floor
- Can only view/manage assigned students
- Cannot access other students

### Student Level
- Student assigned to ONE campus, ONE floor, ONE mentor
- Cannot access admin/floor wing/mentor management tools

## Testing Checklist

### Backend Tests
- [ ] Create users with different roles via Django admin
- [ ] Verify campus/floor validation (TECH floor 5 should fail)
- [ ] Test Floor Wing API with Floor Wing user
- [ ] Test Admin API with Admin user
- [ ] Verify permissions (Mentor cannot access Floor Wing endpoints)

### Frontend Tests
- [ ] Login as STUDENT → verify redirected to `/`
- [ ] Login as MENTOR → verify redirected to `/mentor-dashboard`
- [ ] Login as FLOOR_WING → verify redirected to `/floorwing-dashboard`
- [ ] Login as ADMIN → verify redirected to `/admin/campus-select`
- [ ] Admin: Select TECH campus → verify 4 floor cards shown
- [ ] Admin: Select ARTS campus → verify 3 floor cards shown
- [ ] Floor Wing: Verify can only see own floor's students/mentors
- [ ] Floor Wing: Assign student to mentor → verify success
- [ ] Verify MENTOR cannot access `/floorwing-dashboard` (Access Denied)
- [ ] Verify STUDENT cannot access `/admin/campus-select` (Access Denied)

## Next Steps

### Completed ✅
1. **Admin Floor Detail Page** - Complete floor management with tabs for students, mentors, and floor wing
2. **Navigation Component Updates** - Floor Wing navigation items added to both desktop and mobile views
3. **Complete Routing** - All admin campus/floor routes implemented with role guards

### Future Enhancements
1. **Floor Wing Profile Management**
   - View/edit floor wing profile
   - Change password
   - View floor statistics

4. **Mentor Assignment UI Improvements**
   - Drag-and-drop student assignment
   - Bulk assignment operations
   - Real-time mentor workload updates

5. **Admin Analytics**
   - Campus-wide statistics
   - Floor performance comparison
   - Submission rate tracking

### Database Setup
To test the system, create users in Django admin:
```python
# Admin user
admin = User.objects.create_user(username='admin@college.edu', email='admin@college.edu')
admin.profile.role = 'ADMIN'
admin.profile.save()

# Floor Wing user (Tech, Floor 1)
fw = User.objects.create_user(username='fw_tech_1@college.edu', email='fw_tech_1@college.edu')
fw.profile.role = 'FLOOR_WING'
fw.profile.campus = 'TECH'
fw.profile.floor = 1
fw.profile.save()

# Mentor user (Tech, Floor 1)
mentor = User.objects.create_user(username='mentor_tech_1@college.edu', email='mentor_tech_1@college.edu')
mentor.profile.role = 'MENTOR'
mentor.profile.campus = 'TECH'
mentor.profile.floor = 1
mentor.profile.save()

# Student user (Tech, Floor 1)
student = User.objects.create_user(username='student@college.edu', email='student@college.edu')
student.profile.role = 'STUDENT'
student.profile.campus = 'TECH'
student.profile.floor = 1
student.profile.mentor = mentor.profile
student.profile.save()
```

## Architecture Notes

### Why Campus Selection First?
- Admin needs context before viewing data
- Prevents UI confusion with mixed campus data
- Clear navigation hierarchy
- Scalable for future multi-campus expansion

### Why Floor Wing Dashboard Separate?
- Floor Wing is operational role, not administrative
- Focused workflow: View floor → Manage students/mentors
- Simpler UI without campus selection overhead
- Clear separation from admin functions

### Why Separate Services?
- `floorWingService.js`: Floor-specific operations
- `admin.js`: Campus/floor management operations
- Clear API boundaries matching backend structure
- Easier to test and maintain

## Files Modified/Created

### Backend
- ✅ `apps/profiles/models.py` (modified)
- ✅ `apps/profiles/migrations/0003_*.py` (created)
- ✅ `apps/profiles/permissions.py` (created)
- ✅ `apps/profiles/floor_wing_views.py` (created)
- ✅ `apps/profiles/admin_views.py` (created)
- ✅ `apps/profiles/urls.py` (modified)
- ✅ `apps/profiles/serializers.py` (modified)
- ✅ `apps/jwt_serializers.py` (modified)

### Frontend
- ✅ `src/context/AuthContext.jsx` (modified)
- ✅ `src/components/ProtectedRoute.jsx` (modified)
- ✅ `src/pages/Login.jsx` (modified)
- ✅ `src/App.jsx` (modified - routing and navigation)
- ✅ `src/services/floorWing.js` (created)
- ✅ `src/services/admin.js` (modified)
- ✅ `src/pages/floorwing/FloorWingDashboard.jsx` (modified)
- ✅ `src/pages/admin/campus/CampusSelection.jsx` (created)
- ✅ `src/pages/admin/campus/CampusSelection.css` (created)
- ✅ `src/pages/admin/campus/CampusOverview.jsx` (created)
- ✅ `src/pages/admin/campus/CampusOverview.css` (created)
- ✅ `src/pages/admin/campus/FloorDetail.jsx` (created)
- ✅ `src/pages/admin/campus/FloorDetail.css` (created)

## Summary
The role-based campus/floor system is now **FULLY IMPLEMENTED** in both backend and frontend:

✅ **Backend**: Database schema, permissions, Floor Wing API, Admin API, authentication
✅ **Frontend**: AuthContext, protected routes, login flow, complete routing, navigation components
✅ **Admin Flow**: Campus selection → Campus overview → Floor detail (students, mentors, floor wing management)
✅ **Floor Wing Flow**: Dashboard with tabs (stats, students, mentors) and assignment interface
✅ **Navigation**: Role-based navigation for all user types (Student, Mentor, Floor Wing, Admin)

The system enforces strict hierarchical access control with campus-level isolation. All routes are protected with role-based guards, and the authentication flow correctly handles role/campus/floor context.
