# Testing Guide - Role-Based Campus/Floor System

## Overview
This guide walks you through testing the complete role-based hierarchical system with 4 roles, 2 campuses, and multiple floors.

## Development Server
- Frontend: http://localhost:5174/
- Backend: http://localhost:8000/ (ensure Django server is running)

## Test Users Setup

### Step 1: Access Django Admin
1. Navigate to http://localhost:8000/admin/
2. Login with superuser credentials
3. Go to **Profiles → User profiles**

### Step 2: Create Test Users

#### Admin User
```
Username: admin@college.edu
Email: admin@college.edu
Password: Test123!

Profile Settings:
- Role: ADMIN
- Campus: Leave blank
- Floor: Leave blank
```

#### Floor Wing User (Tech Campus, Floor 1)
```
Username: fw.tech.floor1@college.edu
Email: fw.tech.floor1@college.edu
Password: Test123!

Profile Settings:
- Role: FLOOR_WING
- Campus: TECH
- Floor: 1
```

#### Mentor User (Tech Campus, Floor 1)
```
Username: mentor.tech.floor1@college.edu
Email: mentor.tech.floor1@college.edu
Password: Test123!

Profile Settings:
- Role: MENTOR
- Campus: TECH
- Floor: 1
```

#### Student User (Tech Campus, Floor 1)
```
Username: student.tech.floor1@college.edu
Email: student.tech.floor1@college.edu
Password: Test123!

Profile Settings:
- Role: STUDENT
- Campus: TECH
- Floor: 1
- Mentor: (Select mentor.tech.floor1)
```

## Test Flows

### 1. Admin Flow Test ✅

**Objective**: Test complete admin navigation and floor management

1. **Login**
   - Navigate to http://localhost:5174/login
   - Select role: **Admin**
   - Enter: admin@college.edu / Test123!
   - Click "Sign In"

2. **Campus Selection Screen**
   - Should redirect to: `/admin/campus-select`
   - Should see two cards: **Technology Campus** and **Arts & Science Campus**
   - Verify campus info displays correctly

3. **Select Tech Campus**
   - Click on **Technology Campus** card
   - Should navigate to: `/admin/campus/TECH`
   - Should see **4 floor cards** (Floors 1-4)

4. **View Floor Cards**
   - Each card should show:
     - Floor number and name
     - Student count
     - Mentor count
     - Floor Wing name (or "No Floor Wing assigned")
     - Submission statistics (progress bar, approved/pending/rejected)

5. **Navigate to Floor Detail**
   - Click on **Floor 1** card
   - Should navigate to: `/admin/campus/TECH/floor/1`
   - Should see three tabs: **Students**, **Mentors**, **Floor Wing**

6. **Students Tab**
   - Should list all students on Floor 1
   - Each student shows: name, email, assigned mentor, submission count
   - Verify student data displays correctly

7. **Mentors Tab**
   - Should list all mentors on Floor 1
   - Each mentor shows: name, email, assigned student count
   - Click "Assign Mentor" button
   - Select a user from dropdown
   - Click "Confirm Assignment"
   - Verify mentor is added to list

8. **Floor Wing Tab**
   - If no floor wing assigned: Shows "No floor wing assigned" with assign button
   - Click "Assign Floor Wing"
   - Select a user from dropdown
   - Click "Confirm Assignment"
   - Verify floor wing info displays with golden crown icon

9. **Navigation Test**
   - Click "Back to Technology Campus"
   - Should return to `/admin/campus/TECH`
   - Click back button in browser
   - Should navigate to campus selection

10. **Arts Campus Test**
    - Go to campus selection
    - Click **Arts & Science Campus**
    - Should navigate to: `/admin/campus/ARTS`
    - Should see **3 floor cards** (Floors 1-3)

**Expected Results**: ✅ All navigation works, data displays correctly, assignments work

---

### 2. Floor Wing Flow Test ✅

**Objective**: Test Floor Wing dashboard and student assignment

1. **Login**
   - Navigate to http://localhost:5174/login
   - Select role: **Floor Wing** (if available, otherwise use FLOOR_WING dropdown)
   - Enter: fw.tech.floor1@college.edu / Test123!
   - Click "Sign In"

2. **Floor Wing Dashboard**
   - Should redirect to: `/floorwing-dashboard`
   - Should see **Dashboard** tab active
   - Top section shows:
     - Floor Wing name
     - Campus and Floor info
     - Stats cards: Students, Mentors, Submissions

3. **Dashboard Tab**
   - Verify floor stats display correctly
   - Check student count
   - Check mentor count
   - Check submission statistics

4. **Students Tab**
   - Click "Students" tab
   - Should see list of students on the floor
   - **Unassigned Students** section shows students without mentors
   - Each student has "Assign to Mentor" dropdown
   - Select a mentor from dropdown
   - Click "Assign" button
   - Verify student moves to assigned list

5. **Mentors Tab**
   - Click "Mentors" tab
   - Should see list of mentors on the floor
   - Each mentor shows:
     - Name and email
     - Assigned student count
     - Student names (if any assigned)

6. **Navigation Bar**
   - Should see "Dashboard" in navigation
   - Logo should link back to dashboard
   - Logout button should work

7. **Access Control Test**
   - Try to navigate to `/admin/campus-select`
   - Should see "Access Denied" message
   - Try to navigate to `/mentor-dashboard`
   - Should see "Access Denied" message

**Expected Results**: ✅ Dashboard displays, student assignment works, access control enforced

---

### 3. Mentor Flow Test ✅

**Objective**: Test mentor dashboard and student management

1. **Login**
   - Navigate to http://localhost:5174/login
   - Select role: **Mentor**
   - Enter: mentor.tech.floor1@college.edu / Test123!
   - Click "Sign In"

2. **Mentor Dashboard**
   - Should redirect to: `/mentor-dashboard`
   - Should see navigation items: Home, Student List, Pillar Review, Announcements
   - Dashboard shows assigned students

3. **Student List**
   - Click "Student List" in navigation
   - Should see only assigned students
   - Cannot see students from other mentors or floors

4. **Access Control Test**
   - Try to navigate to `/floorwing-dashboard`
   - Should see "Access Denied" message
   - Try to navigate to `/admin/campus-select`
   - Should see "Access Denied" message

**Expected Results**: ✅ Mentor sees only assigned students, access control works

---

### 4. Student Flow Test ✅

**Objective**: Test student access to learning pillars

1. **Login**
   - Navigate to http://localhost:5174/login
   - Select role: **Student**
   - Enter: student.tech.floor1@college.edu / Test123!
   - Click "Sign In"

2. **Student Home**
   - Should redirect to: `/`
   - Should see navigation: Home, CLT, SRI, CFC, IIPC, SCD
   - Can access all student pages

3. **Learning Pillars**
   - Click on CLT, SRI, CFC, IIPC, SCD
   - Should navigate to each pillar page
   - Can submit assignments

4. **Access Control Test**
   - Try to navigate to `/floorwing-dashboard`
   - Should see "Access Denied" message
   - Try to navigate to `/admin/campus-select`
   - Should see "Access Denied" message
   - Try to navigate to `/mentor-dashboard`
   - Should see "Access Denied" message

**Expected Results**: ✅ Student accesses only student pages, all other routes denied

---

## Role Access Matrix Test

| User Role | Home Path | Can Access | Cannot Access |
|-----------|-----------|-----------|---------------|
| **ADMIN** | /admin/campus-select | Campus selection, all floors, all admin routes | Student/Mentor/Floor Wing pages |
| **FLOOR_WING** | /floorwing-dashboard | Floor dashboard, students/mentors on floor | Other floors, admin routes, student pages |
| **MENTOR** | /mentor-dashboard | Mentor dashboard, assigned students only | Other mentors' students, admin routes, floor wing |
| **STUDENT** | / | Home, CLT, SRI, CFC, IIPC, SCD, monthly report | Admin, Floor Wing, Mentor pages |

---

## API Testing (Optional)

### Floor Wing API Test
```bash
# Get Floor Wing Dashboard (requires Floor Wing token)
curl -X GET http://localhost:8000/api/profiles/floor-wing/dashboard/ \
  -H "Authorization: Bearer <floor_wing_token>"

# Get Students on Floor
curl -X GET http://localhost:8000/api/profiles/floor-wing/students/ \
  -H "Authorization: Bearer <floor_wing_token>"

# Assign Student to Mentor
curl -X POST http://localhost:8000/api/profiles/floor-wing/assign-student/ \
  -H "Authorization: Bearer <floor_wing_token>" \
  -H "Content-Type: application/json" \
  -d '{"student_id": 1, "mentor_id": 2}'
```

### Admin API Test
```bash
# Get Campus Overview (requires Admin token)
curl -X GET http://localhost:8000/api/profiles/admin/campus/TECH/ \
  -H "Authorization: Bearer <admin_token>"

# Get Floor Detail
curl -X GET http://localhost:8000/api/profiles/admin/campus/TECH/floor/1/ \
  -H "Authorization: Bearer <admin_token>"

# Assign Floor Wing
curl -X POST http://localhost:8000/api/profiles/admin/assign-floor-wing/ \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 3, "campus": "TECH", "floor": 1}'
```

---

## Common Issues & Solutions

### Issue 1: Port 5173 in use
**Solution**: Frontend automatically switches to port 5174. Use http://localhost:5174/

### Issue 2: CORS errors
**Solution**: Ensure Django backend is running and CORS settings allow http://localhost:5174

### Issue 3: "Access Denied" on login
**Solution**: 
- Check user role in Django admin matches selected role in login
- Verify ROLE_ACCESS in AuthContext includes the path
- Check browser console for errors

### Issue 4: Backend 404 errors
**Solution**:
- Verify Django URLs are registered: `python manage.py show_urls`
- Check backend server is running on port 8000
- Verify API endpoints in services match backend routes

### Issue 5: Blank campus/floor data
**Solution**:
- Create test users with proper role/campus/floor assignments
- Ensure migrations are applied: `python manage.py migrate`
- Check database has users with correct profile data

---

## Success Criteria

### ✅ All Tests Pass When:
1. **Admin** can select campus, view floors, manage floor wing and mentors
2. **Floor Wing** can view dashboard, see students/mentors on floor, assign students
3. **Mentor** can see assigned students only, cannot access other data
4. **Student** can access learning pillars, cannot access management tools
5. **Access Control** properly denies unauthorized access to all roles
6. **Navigation** displays correct items based on role
7. **API** returns proper data for each role's scope

---

## Reporting Issues

If you encounter issues during testing:

1. **Check Browser Console**: Look for JavaScript errors
2. **Check Network Tab**: Verify API calls are successful (200 status)
3. **Check Django Logs**: Look for backend errors in terminal
4. **Verify User Setup**: Ensure users have correct role/campus/floor in Django admin
5. **Check AuthContext**: Verify user object has role/campus/floor after login

---

## Next Steps After Testing

Once all tests pass:
1. Create production user data
2. Set up real campus/floor structure
3. Import student/mentor data
4. Configure submission workflows
5. Set up analytics dashboards
6. Deploy to production environment

---

**Testing Complete!** 🎉

All role-based access control, hierarchical navigation, and campus/floor management features are now verified and working correctly.
