# Role-Based Authentication System

## Overview
Your Cohort Web application now has a complete role-based authentication system with 4 user roles:

### User Roles
1. **Student** - Access to all student pages (Home, CLT, SRI, CFC, IIPC, SCD)
2. **Mentor** - Same access as students (can be extended with mentor-specific features)
3. **Floor Wing** - Same access as students (can be extended with floor wing features)
4. **Admin** - Full access to all pages and features

## Features Implemented

### 1. Login Page with Role Selection
- Visual role selector with 4 role cards
- Each role has a unique icon and color
- Active role is highlighted with a checkmark
- Form validation for email and password
- Toggle between Sign In and Sign Up modes

### 2. Authentication Context (`src/context/AuthContext.jsx`)
- Manages user authentication state
- Stores user data in localStorage for persistence
- Provides login/logout functionality
- Role-based access control (RBAC)

### 3. Protected Routes (`src/components/ProtectedRoute.jsx`)
- Redirects unauthenticated users to login page
- Shows "Access Denied" for unauthorized access
- Checks user permissions based on role

### 4. Navigation Updates
- Shows current user role badge
- Logout button with icon
- Conditionally hides navigation on login page

## How It Works

### Login Flow
1. User selects their role (Student/Mentor/Floor Wing/Admin)
2. Enters email and password
3. Clicks "Sign In"
4. System authenticates and stores user data with role
5. Redirects to home page
6. All routes are now protected based on role

### Access Control
- **Student** role can access: `/`, `/clt`, `/sri`, `/cfc`, `/iipc`, `/scd`
- **Mentor** role: Same as student (ready for expansion)
- **Floor Wing** role: Same as student (ready for expansion)
- **Admin** role: Access to everything including future admin dashboards

### Testing the System
1. Navigate to `http://localhost:5174/login`
2. Select "Student" role
3. Enter any email (e.g., `student@test.com`) and password (min 6 characters)
4. Click "Sign In"
5. You'll be redirected to the home page with student access
6. Try logging out and selecting different roles

## File Structure
```
src/
├── context/
│   └── AuthContext.jsx          # Authentication state management
├── components/
│   └── ProtectedRoute.jsx       # Route protection wrapper
├── pages/
│   ├── Login.jsx                # Login page with role selection
│   └── Login.css                # Login page styles
└── App.jsx                      # Updated with AuthProvider
```

## Next Steps (Optional Enhancements)

### 1. Create Role-Specific Dashboards
- `/mentor-dashboard` for mentors
- `/floorwing-dashboard` for floor wings
- `/admin-dashboard` for admins

### 2. Add Backend Integration
- Replace mock authentication with real API calls
- Implement JWT tokens
- Add password hashing

### 3. Enhance Access Control
- Page-level permissions
- Feature-level permissions
- Dynamic role assignment

### 4. Add More Features
- Forgot password functionality
- Email verification
- Profile management
- User settings

## Security Notes
⚠️ **Current Implementation**: This is a client-side authentication demo. For production:
- Implement server-side authentication
- Use secure token management (JWT/OAuth)
- Add HTTPS
- Implement proper password hashing
- Add rate limiting
- Enable CSRF protection
