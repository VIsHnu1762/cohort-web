# Cohort Web Application - Complete Project Documentation

**Version:** 1.0.0  
**Last Updated:** December 20, 2025  
**Status:** Active Development

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [User Roles & Permissions](#user-roles--permissions)
5. [Five Development Pillars](#five-development-pillars)
6. [Project Structure](#project-structure)
7. [Key Features](#key-features)
8. [Installation & Setup](#installation--setup)
9. [API Documentation](#api-documentation)
10. [Testing Guide](#testing-guide)
11. [Feature Documentation](#feature-documentation)

---

## 🎯 Project Overview

Cohort Web Application is a comprehensive platform that connects students, mentors, floor/wing representatives, and administrators in a structured journey of academic and personal excellence. The platform tracks student development across five pillars of holistic growth with sophisticated submission workflows, review systems, and analytics.

### Purpose
- **Track & Manage** student development across multiple dimensions
- **Connect** students with mentors for personalized guidance
- **Monitor** institutional performance with real-time dashboards
- **Facilitate** communication between all stakeholders
- **Analyze** progress with comprehensive analytics

### Key Highlights
- Multi-role authentication system (Student, Mentor, Floor Wing, Admin)
- Five-pillar development tracking (CLT, SRI, CFC, IIPC, SCD)
- Campus and floor-based hierarchical organization
- Real-time notifications and messaging
- Comprehensive analytics and reporting
- Hackathon registration and tracking
- LeetCode profile integration
- Professional development logging

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER (React)                     │
├─────────────────────────────────────────────────────────────┤
│  Student UI  │  Mentor UI  │  Floor Wing UI  │  Admin UI   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   API GATEWAY (Django REST)                  │
├─────────────────────────────────────────────────────────────┤
│  JWT Auth  │  CORS  │  Rate Limiting  │  API Documentation │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND SERVICES                          │
├──────────────┬──────────────┬─────────────┬────────────────┤
│  Main Backend│ Admin Backend│ Mentor      │ Communication  │
│              │              │ Backend     │ Services       │
└──────────────┴──────────────┴─────────────┴────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   DATABASE (PostgreSQL)                      │
├─────────────────────────────────────────────────────────────┤
│  Users  │  Profiles  │  Submissions  │  Analytics  │  Logs │
└─────────────────────────────────────────────────────────────┘
```

### Component Architecture

- **Frontend (React 19.2.0 + Vite 7.2.4)**: Single-page application with role-based routing
- **Backend (Django 4.2.7 + DRF 3.14.0)**: RESTful API with JWT authentication
- **Database (PostgreSQL)**: Relational database with optimized indexes
- **File Storage**: Media files for submissions, certificates, and documents
- **Authentication**: JWT token-based with refresh mechanism

### Data Flow

1. **User Authentication** → JWT token generation → Role-based route access
2. **Student Submission** → Validation → File upload → Status tracking → Mentor review
3. **Mentor Review** → Submission evaluation → Status update → Student notification
4. **Analytics** → Data aggregation → Cache layer → Real-time dashboard updates

---

## 🛠️ Technology Stack

### Frontend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 19.2.0 | UI Framework |
| Vite | 7.2.4 | Build tool & dev server |
| React Router DOM | 6.20.0 | Client-side routing |
| Framer Motion | 11.15.0 | Animations |
| GSAP | 3.14.2 | Advanced animations |
| Three.js | 0.181.0 | 3D graphics |
| Lucide React | 0.559.0 | Icon library |
| Recharts | 3.5.1 | Data visualization |
| Zustand | 5.0.9 | State management |
| Axios | 1.13.2 | HTTP client |

### Backend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Django | 4.2.7 | Web framework |
| Django REST Framework | 3.14.0 | API framework |
| djangorestframework-simplejwt | 5.3.0 | JWT authentication |
| PostgreSQL | (psycopg2-binary 2.9.9) | Database |
| Pillow | 10.1.0 | Image processing |
| django-cors-headers | 4.3.1 | CORS handling |
| python-dotenv | 1.0.0 | Environment variables |
| cryptography | 41.0.7 | Security utilities |
| argon2-cffi | 23.1.0 | Password hashing |
| django-ratelimit | 4.1.0 | API rate limiting |
| gunicorn | 21.2.0 | Production server |
| whitenoise | 6.6.0 | Static file serving |
| drf-yasg | 1.21.7 | API documentation |

---

## 👥 User Roles & Permissions

### 1. Student 👨‍🎓

**Access Level:** Basic  
**Primary Dashboard:** Student Home

**Permissions:**
- View personal dashboard with progress tracking
- Submit activities across all five pillars
- Upload certificates and evidence files
- View submission status and mentor feedback
- Register for hackathons and competitions
- Manage LinkedIn profile verification
- Receive notifications from mentors and floor wing
- View floor announcements
- Track personal analytics and progress

**Restricted From:**
- Viewing other students' submissions
- Accessing mentor/admin dashboards
- Modifying system settings

### 2. Mentor 👨‍🏫

**Access Level:** Intermediate  
**Primary Dashboard:** Mentor Dashboard

**Permissions:**
- View assigned students list
- Review and approve/reject submissions
- Provide feedback on student work
- Track student progress across pillars
- Send messages to students
- Access student analytics
- View month-wise submission history
- Generate mentor reports

**Restricted From:**
- Accessing admin functions
- Viewing unassigned students (outside scope)
- Modifying system configurations

### 3. Floor Wing Representative 🏢

**Access Level:** Floor-Level Management  
**Primary Dashboard:** Floor Wing Dashboard

**Permissions:**
- View all students on assigned floor
- Monitor floor-level statistics
- Create and manage floor announcements
- Assign students to mentors
- Bulk assign operations
- View mentor workload analytics
- Track floor-wide pillar progress
- Manage student assignments
- View floor-specific reports

**Data Scope:** Strictly limited to assigned campus + floor

**Restricted From:**
- Accessing other floors/campuses
- Admin system configurations
- Direct submission review

### 4. Administrator 👨‍💼

**Access Level:** Full System Access  
**Primary Dashboard:** Admin Campus Selection → Floor Management

**Permissions:**
- Full access to all campuses and floors
- Student profile management
- Mentor assignment and management
- Floor and wing representative management
- System-wide analytics and reporting
- Communication center access
- Leaderboard management
- System configuration
- User role management
- Database administration

---

## 📚 Five Development Pillars

### 1. CLT (Continuous Learning Track) 📖

**Purpose:** Track continuous learning and skill development through online courses

**Features:**
- Course completion tracking
- Platform integration (Udemy, Coursera, etc.)
- Certificate upload and validation
- Progress monitoring
- Statistics dashboard

**Submission Workflow:**
1. Enter course details (title, platform, description)
2. Upload completion certificate
3. Submit for mentor review
4. Receive approval/feedback
5. Reflection on learning outcomes

### 2. SRI (Social Responsibility Initiative) 🤝

**Purpose:** Document social service and community engagement activities

**Features:**
- Event participation tracking
- Impact measurement
- Photo documentation
- Hour logging
- Organization partnerships

**Key Metrics:**
- Hours contributed
- Events participated
- Community impact
- Leadership roles

### 3. CFC (Career, Future & Competency) 🚀

**Purpose:** Professional development and career preparation

**Features:**
- Hackathon registration and tracking
- Competition participation
- Countdown timers for upcoming events
- LinkedIn profile verification
- Professional post tracking
- Award documentation

**Sub-modules:**
- **Hackathon Management**
  - Registration system
  - Participation tracking
  - Motivational reminders
  - Submission linking
- **LinkedIn Integration**
  - Profile verification
  - Post tracking
  - Professional networking

### 4. IIPC (Industry Interaction & Professional Connect) 💼

**Purpose:** Industry exposure and professional networking

**Features:**
- Industry visit documentation
- Guest lecture attendance
- Company interaction tracking
- Networking events
- Mentorship programs

**Outcomes Tracked:**
- Industry connections made
- Professional skills gained
- Career insights acquired
- Interview opportunities

### 5. SCD (Self-Code Development) 💻

**Purpose:** Technical skill development and coding practice

**Features:**
- LeetCode profile integration
- Problem-solving tracking
- Coding challenge participation
- Project development
- Technical skill assessment

**Integration:**
- LeetCode profile linking
- Problem count tracking
- Difficulty level analysis
- Consistency monitoring

---

## 📁 Project Structure

```
cohort_webapp/
│
├── backend/                          # Main Django Backend
│   ├── apps/                         # Django Applications
│   │   ├── __init__.py
│   │   ├── authentication.py         # Auth logic
│   │   ├── jwt_serializers.py        # JWT handling
│   │   ├── admin_views.py            # Admin endpoints
│   │   ├── admin_urls.py             # Admin routing
│   │   ├── mentor_views.py           # Mentor endpoints
│   │   ├── mentor_urls.py            # Mentor routing
│   │   ├── users_views.py            # User endpoints
│   │   ├── users_serializers.py      # User serialization
│   │   │
│   │   ├── profiles/                 # User Profiles
│   │   │   ├── models.py             # User, Profile models
│   │   │   ├── views.py              # Profile endpoints
│   │   │   ├── serializers.py        # Profile serialization
│   │   │   ├── announcement_views.py # Floor announcements
│   │   │   └── floor_wing_views.py   # Floor wing dashboard
│   │   │
│   │   ├── clt/                      # Continuous Learning Track
│   │   │   ├── models.py             # Course submissions
│   │   │   ├── views.py              # CLT endpoints
│   │   │   ├── serializers.py        # CLT serialization
│   │   │   └── urls.py               # CLT routing
│   │   │
│   │   ├── sri/                      # Social Responsibility
│   │   │   ├── models.py             # SRI submissions
│   │   │   ├── views.py              # SRI endpoints
│   │   │   └── serializers.py        # SRI serialization
│   │   │
│   │   ├── cfc/                      # Career & Competency
│   │   │   ├── models.py             # CFC, Hackathons
│   │   │   ├── views.py              # CFC endpoints
│   │   │   ├── serializers.py        # CFC serialization
│   │   │   └── urls.py               # CFC routing
│   │   │
│   │   ├── iipc/                     # Industry Interaction
│   │   │   ├── models.py             # IIPC submissions
│   │   │   ├── views.py              # IIPC endpoints
│   │   │   └── serializers.py        # IIPC serialization
│   │   │
│   │   ├── scd/                      # Self-Code Development
│   │   │   ├── models.py             # SCD, LeetCode
│   │   │   ├── views.py              # SCD endpoints
│   │   │   └── serializers.py        # SCD serialization
│   │   │
│   │   ├── hackathons/               # Hackathon System
│   │   │   ├── models.py             # Registrations
│   │   │   ├── views.py              # Hackathon API
│   │   │   └── serializers.py        # Serialization
│   │   │
│   │   └── dashboard/                # Dashboard Analytics
│   │       ├── views.py              # Analytics endpoints
│   │       └── serializers.py        # Data serialization
│   │
│   ├── config/                       # Django Configuration
│   │   ├── settings.py               # Main settings
│   │   ├── urls.py                   # URL routing
│   │   ├── wsgi.py                   # WSGI config
│   │   └── asgi.py                   # ASGI config
│   │
│   ├── media/                        # Uploaded Files
│   │   ├── certificates/             # Course certificates
│   │   ├── submissions/              # Submission files
│   │   └── profiles/                 # Profile pictures
│   │
│   ├── static/                       # Static Files
│   ├── manage.py                     # Django CLI
│   ├── requirements.txt              # Python dependencies
│   └── README.md                     # Backend docs
│
├── src/                              # React Frontend
│   ├── assets/                       # Static Assets
│   │   ├── images/
│   │   ├── fonts/
│   │   └── icons/
│   │
│   ├── components/                   # Reusable Components
│   │   ├── Button.jsx
│   │   ├── GlassCard.jsx
│   │   ├── Input.jsx
│   │   ├── ProgressBar.jsx
│   │   ├── ProtectedRoute.jsx
│   │   ├── ThemeToggle.jsx
│   │   ├── Navigation.jsx
│   │   ├── HackathonRegistrationModal.jsx
│   │   ├── UpcomingHackathonsWidget.jsx
│   │   └── admin/                    # Admin components
│   │
│   ├── context/                      # React Context
│   │   └── AuthContext.jsx           # Auth state management
│   │
│   ├── pages/                        # Page Components
│   │   ├── Login.jsx                 # Login page
│   │   ├── ParallaxIntro.jsx         # Landing page
│   │   │
│   │   ├── student/                  # Student Pages
│   │   │   ├── Home.jsx              # Student dashboard
│   │   │   ├── CLT.jsx               # Learning track
│   │   │   ├── SRI.jsx               # Social responsibility
│   │   │   ├── CFC.jsx               # Career & competency
│   │   │   ├── IIPC.jsx              # Industry interaction
│   │   │   └── SCD.jsx               # Code development
│   │   │
│   │   ├── mentor/                   # Mentor Pages
│   │   │   ├── MentorDashboard.jsx   # Mentor dashboard
│   │   │   └── MentorDashboard.css
│   │   │
│   │   ├── floorwing/                # Floor Wing Pages
│   │   │   ├── FloorWingDashboard.jsx
│   │   │   └── FloorWingDashboard.css
│   │   │
│   │   └── admin/                    # Admin Pages
│   │       ├── CampusSelect.jsx      # Campus selection
│   │       ├── CampusDetail.jsx      # Campus overview
│   │       └── FloorDetail.jsx       # Floor management
│   │
│   ├── services/                     # API Services
│   │   ├── api.js                    # Axios config
│   │   ├── auth.js                   # Auth API
│   │   ├── clt.js                    # CLT API
│   │   ├── sri.js                    # SRI API
│   │   ├── cfc.js                    # CFC API
│   │   ├── iipc.js                   # IIPC API
│   │   ├── scd.js                    # SCD API
│   │   ├── messageService.js         # Messaging API
│   │   └── adminService.js           # Admin API
│   │
│   ├── store/                        # State Management
│   │   └── useStore.js               # Zustand store
│   │
│   ├── theme/                        # Theme Configuration
│   │   └── colors.js
│   │
│   ├── App.jsx                       # Main app component
│   ├── App.css                       # Global styles
│   ├── main.jsx                      # Entry point
│   └── index.css                     # Root styles
│
├── public/                           # Public Assets
│   └── index.html
│
├── Documentation Files
├── README.md                         # Main readme
├── ARCHITECTURE_DIAGRAM.md           # System architecture
├── AUTH_SYSTEM.md                    # Authentication docs
├── CHAT_SYSTEM.md                    # Messaging docs
├── CLT_INTEGRATION_GUIDE.md          # CLT integration
├── FLOOR_WING_ENHANCEMENT.md         # Floor wing features
├── HACKATHON_REGISTRATION_FEATURE.md # Hackathon system
├── TESTING_GUIDE.md                  # Testing guide
├── CFC_TESTING_REPORT.md             # CFC tests
└── FLOOR_WING_BACKEND_REPORT.md      # Backend reports

├── Configuration Files
├── package.json                      # NPM dependencies
├── vite.config.js                    # Vite configuration
├── eslint.config.js                  # ESLint rules
└── index.html                        # HTML template

└── Utility Scripts                   # Backend utilities
    ├── create_superuser.py
    ├── create_test_users.py
    ├── assign_students_to_mentors.py
    ├── import_students_from_excel.py
    ├── test_*.py                     # Test scripts
    └── check_*.py                    # Validation scripts
```

---

## ✨ Key Features

### 1. Authentication & Authorization System

**Multi-Role Login:**
- Visual role selector with 4 role cards
- Email/password authentication
- JWT token-based sessions
- Role-based route protection
- Persistent authentication state

**Security Features:**
- Password hashing (Argon2)
- JWT token refresh mechanism
- CORS protection
- Rate limiting
- CSRF protection

### 2. Student Dashboard

**Personal Analytics:**
- Overall progress across all pillars
- Submission status tracking
- Upcoming deadlines
- Recent notifications
- Mentor messages

**Submission Management:**
- Multi-step submission forms
- File upload with validation
- Draft saving capability
- Status tracking (draft → submitted → under_review → approved/rejected)

**Notifications:**
- Mentor messages
- Submission status updates
- Floor announcements
- Hackathon reminders
- Auto-refresh every 30 seconds

### 3. Mentor Dashboard

**Student Management:**
- View assigned students list
- Student search and filtering
- Individual student progress cards
- Pillar-wise completion tracking

**Review System:**
- Submission review interface
- Approve/reject functionality
- Feedback provision
- Month-wise submission history
- Bulk review operations

**Communication:**
- Direct messaging to students
- Message type selection (general, completion, pending review)
- Chat modal interface
- Message history

**Analytics:**
- Student performance metrics
- Submission statistics
- Approval rates
- Time-based analytics

### 4. Floor Wing Dashboard

**Enhanced Dashboard (4 Tabs):**

**Tab 1: Dashboard Overview**
- 6 live stats cards (total students, active mentors, assigned/unassigned, avg completion, pending reviews)
- Pillar progress overview (CLT, CFC, SRI, IIPC, SCD)
- Mentor workload visualization
- Animated hover effects

**Tab 2: Student Management**
- Filter system (All, Unassigned, At Risk, Low Progress)
- Real-time search functionality
- Bulk selection with checkboxes
- Bulk mentor assignment
- Status badges (On Track, At Risk, Moderate)
- Individual progress bars
- Student detail drawer

**Tab 3: Mentor Overview**
- Mentor list with workload status
- Student count per mentor
- Pending review statistics
- Approval rates
- Last active tracking

**Tab 4: Announcements**
- Create floor-scoped announcements
- Priority levels (Normal, Important, Urgent)
- Status management (Draft, Published, Expired)
- Expiry date setting
- Read tracking per student
- Read statistics display
- CRUD operations
- Strict campus + floor data isolation

**Student Detail Drawer:**
- Slide-in panel from right
- Comprehensive student info
- Pillar-wise progress breakdown
- Mentor reassignment capability
- Overall progress percentage

### 5. Admin System

**Campus Management:**
- Campus selection interface
- Two campuses (Technology, Arts & Science)
- Campus-level overview

**Floor Management:**
- 4 floors per campus visualization
- Floor cards with statistics:
  - Student count
  - Mentor count
  - Floor wing assignment
  - Submission progress (approved/pending/rejected)
- Floor detail view
- Cross-floor analytics

**User Management:**
- Student profile management
- Mentor assignment
- Floor wing assignment
- Role management
- Bulk operations

**System Analytics:**
- Institution-wide reports
- Performance metrics
- Leaderboard system
- Custom report generation

### 6. Hackathon Registration System

**Two-Step Process:**
1. **Registration Phase:**
   - Student registers intent to participate
   - Provides hackathon details (name, mode, date, URL)
   - Adds personal preparation notes
   - System calculates countdown

2. **Submission Phase:**
   - After participation, creates linked submission
   - Uploads participation proof
   - Marks registration as completed

**Upcoming Hackathons Widget:**
- Displays top 3 upcoming hackathons
- Dynamic countdown timers
- Color-coded urgency levels:
  - 🔴 Red (Today/Tomorrow)
  - 🟠 Orange (2-3 days)
  - 🔵 Blue (4-7 days)
  - 🟢 Green (7+ days)
- Motivational messages
- Personal notes display
- Direct links to hackathon websites

### 7. Messaging System

**Mentor-to-Student Communication:**
- Chat interface with message types
- Message types:
  - General: Regular communication
  - Completion: Task completion notification
  - Pending Review: Review reminders
- Real-time delivery
- Notification display on student home
- Auto-refresh mechanism

**Student Notifications:**
- Messages appear in home page notifications
- Different icons per message type
- Read/unread status
- Timestamp display
- Mark as read functionality

### 8. LeetCode Integration

**Profile Linking:**
- LeetCode username integration
- Profile verification
- Problem count tracking
- Difficulty level breakdown

**Statistics Tracking:**
- Total problems solved
- Easy/Medium/Hard distribution
- Consistency monitoring
- Progress visualization

### 9. File Management

**Upload Features:**
- Multiple file upload (max 10 files)
- File size validation (10MB per file)
- Supported formats: PDF, PNG, JPG, JPEG
- Drag-and-drop interface
- Upload progress tracking

**Storage:**
- Organized media folder structure
- Secure file access
- URL generation for downloads
- File deletion capability

### 10. Floor Announcements

**Creation & Management:**
- Rich text announcement creation
- Priority levels (Normal, Important, Urgent)
- Expiry date configuration
- Status management (Draft, Published, Expired)
- Edit and delete operations

**Distribution:**
- Floor-scoped delivery (strict campus + floor filtering)
- Student read tracking
- Read statistics per announcement
- Unread count display
- Auto-expire functionality

**Student View:**
- View relevant floor announcements
- Mark announcements as read
- Unread badge display
- Priority-based styling

---

## 🚀 Installation & Setup

### Prerequisites

**Software Requirements:**
- Python 3.10 or higher
- Node.js 18 or higher
- PostgreSQL 15 or higher
- Git
- pip (Python package manager)
- npm (Node package manager)

### Backend Setup

#### 1. Clone Repository
```bash
git clone <repository-url>
cd cohort_webapp/cohort
```

#### 2. Create Virtual Environment
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Database

**Create PostgreSQL Database:**
```sql
CREATE DATABASE cohort_db;
CREATE USER cohort_user WITH PASSWORD 'your_secure_password';
ALTER ROLE cohort_user SET client_encoding TO 'utf8';
ALTER ROLE cohort_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE cohort_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE cohort_db TO cohort_user;
```

#### 5. Environment Configuration

Create `.env` file in `backend/` directory:
```env
# Database
DB_NAME=cohort_db
DB_USER=cohort_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Django
SECRET_KEY=your-secret-key-here-generate-secure-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5174

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440
```

#### 6. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 7. Create Superuser
```bash
python manage.py createsuperuser
```

#### 8. Create Test Data (Optional)
```bash
python create_test_users.py
python create_test_data.py
```

#### 9. Start Backend Server
```bash
python manage.py runserver 8000
```

Backend will be available at: `http://localhost:8000/`

### Frontend Setup

#### 1. Navigate to Project Root
```bash
cd cohort_webapp/cohort
```

#### 2. Install Dependencies
```bash
npm install
```

#### 3. Configure Environment (Optional)

Create `.env` file in root directory:
```env
VITE_API_BASE_URL=http://localhost:8000
```

#### 4. Start Development Server
```bash
npm run dev
```

Frontend will be available at: `http://localhost:5173/`

### Verification

1. **Backend API:**
   - Visit: `http://localhost:8000/admin/`
   - Login with superuser credentials
   - Verify admin panel loads

2. **Frontend:**
   - Visit: `http://localhost:5173/`
   - Should see landing page
   - Navigate to `/login`
   - Test login functionality

3. **API Documentation:**
   - Visit: `http://localhost:8000/api/docs/`
   - Swagger UI should load
   - Explore available endpoints

---

## 📡 API Documentation

### Base URLs

- **Backend API:** `http://localhost:8000/api/`
- **Admin Panel:** `http://localhost:8000/admin/`
- **API Docs:** `http://localhost:8000/api/docs/`

### Authentication Endpoints

#### Get JWT Token
```http
POST /api/auth/token/
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "password123"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Refresh Token
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### CLT (Continuous Learning Track) Endpoints

#### List Submissions
```http
GET /api/clt/submissions/
Authorization: Bearer {access_token}

Query Parameters:
- page: int (pagination)
- status: string (draft, submitted, under_review, approved, rejected)

Response:
{
  "count": 25,
  "next": "...",
  "previous": null,
  "results": [...]
}
```

#### Create Submission
```http
POST /api/clt/submissions/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Advanced React Course",
  "description": "Completed comprehensive React course",
  "platform": "Udemy",
  "completion_date": "2025-12-15",
  "status": "draft"
}
```

#### Upload Files
```http
POST /api/clt/submissions/{id}/upload_files/
Authorization: Bearer {access_token}
Content-Type: multipart/form-data

files: [file1, file2, ...]
```

#### Submit for Review
```http
POST /api/clt/submissions/{id}/submit/
Authorization: Bearer {access_token}
```

#### Get Statistics
```http
GET /api/clt/submissions/stats/
Authorization: Bearer {access_token}

Response:
{
  "total": 15,
  "draft": 2,
  "submitted": 3,
  "under_review": 4,
  "approved": 5,
  "rejected": 1
}
```

### CFC (Career, Future & Competency) Endpoints

#### Hackathon Registrations
```http
GET /api/cfc/hackathon-registrations/
POST /api/cfc/hackathon-registrations/
GET /api/cfc/hackathon-registrations/upcoming/
POST /api/cfc/hackathon-registrations/{id}/mark_completed/
POST /api/cfc/hackathon-registrations/{id}/create_submission/
```

### Floor Wing Endpoints

#### Dashboard Statistics
```http
GET /api/floorwing/dashboard/
Authorization: Bearer {access_token}

Response:
{
  "total_students": 120,
  "active_mentors": 12,
  "assigned_students": 110,
  "unassigned_students": 10,
  "avg_floor_completion": 78.5,
  "pending_reviews": 24,
  "pillar_stats": {...},
  "mentor_workload": [...]
}
```

#### Student List
```http
GET /api/floorwing/students/
Authorization: Bearer {access_token}

Query Parameters:
- filter: all|unassigned|at_risk|low_progress
- search: string

Response:
{
  "students": [...],
  "count": 120
}
```

#### Floor Announcements
```http
GET /api/announcements/floor/
POST /api/announcements/floor/
PUT /api/announcements/floor/{id}/
DELETE /api/announcements/floor/{id}/
GET /api/announcements/floor/stats/

# Student view
GET /api/announcements/student/
POST /api/announcements/student/{id}/mark_read/
GET /api/announcements/student/unread_count/
```

### Mentor Endpoints

#### Student List
```http
GET /api/mentor/students/
Authorization: Bearer {access_token}
```

#### Messages
```http
GET /api/communication/messages/
POST /api/communication/messages/
GET /api/communication/messages/unread/
POST /api/communication/messages/{id}/mark_read/
POST /api/communication/messages/mark_all_read/
```

### Admin Endpoints

#### Campus Data
```http
GET /api/admin/campuses/
GET /api/admin/campus/{campus_code}/floors/
GET /api/admin/campus/{campus_code}/floor/{floor_num}/
```

### SRI, IIPC, SCD Endpoints

Similar CRUD patterns:
- `GET /api/{module}/submissions/`
- `POST /api/{module}/submissions/`
- `GET /api/{module}/submissions/{id}/`
- `PUT /api/{module}/submissions/{id}/`
- `DELETE /api/{module}/submissions/{id}/`

---

## 🧪 Testing Guide

### Test User Credentials

#### Admin User
```
Email: admin@college.edu
Password: Test123!
Campus: (Any)
Floor: (Any)
```

#### Floor Wing User (Tech Campus, Floor 1)
```
Email: fw.tech.floor1@college.edu
Password: Test123!
Campus: TECH
Floor: 1
```

#### Mentor User (Tech Campus, Floor 1)
```
Email: mentor.tech.floor1@college.edu
Password: Test123!
Campus: TECH
Floor: 1
```

#### Student User (Tech Campus, Floor 1)
```
Email: student.tech.floor1@college.edu
Password: Test123!
Campus: TECH
Floor: 1
Mentor: mentor.tech.floor1
```

### Test Scenarios

#### 1. Student Flow Test
1. Login as student
2. Navigate to CLT page
3. Create new course submission
4. Upload certificate
5. Submit for review
6. Check notifications
7. View progress on home page

#### 2. Mentor Flow Test
1. Login as mentor
2. View assigned students
3. Select a student
4. Review pending submission
5. Provide feedback
6. Approve/reject submission
7. Send message to student

#### 3. Floor Wing Flow Test
1. Login as floor wing
2. View dashboard statistics
3. Navigate to Students tab
4. Filter by "Unassigned"
5. Bulk select students
6. Assign to mentor
7. Create floor announcement
8. Monitor mentor workload

#### 4. Admin Flow Test
1. Login as admin
2. Select campus (TECH)
3. View floor cards
4. Navigate to Floor 1 detail
5. View student list
6. Assign floor wing representative
7. Monitor system-wide analytics

### Running Backend Tests

```bash
cd backend

# Test specific module
python test_clt_endpoints.py
python test_floorwing_endpoints.py
python test_hackathon_api.py

# Test authentication
python test_login_api.py
python test_student_login.py

# Test integrations
python test_full_integration.py
```

### Manual API Testing

Use tools like:
- **Postman**: Import API collection
- **Swagger UI**: `http://localhost:8000/api/docs/`
- **curl**: Command-line testing

Example curl command:
```bash
# Get token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"student@test.com","password":"Test123!"}'

# Use token
curl http://localhost:8000/api/clt/submissions/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 📖 Feature Documentation

### Detailed Feature Guides

The following documentation files provide in-depth information about specific features:

1. **[ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md)**  
   Visual architecture diagrams for Floor Wing Dashboard with tab navigation

2. **[AUTH_SYSTEM.md](AUTH_SYSTEM.md)**  
   Complete authentication system documentation with role-based access control

3. **[CHAT_SYSTEM.md](CHAT_SYSTEM.md)**  
   Mentor-student messaging system with notification integration

4. **[CLT_INTEGRATION_GUIDE.md](CLT_INTEGRATION_GUIDE.md)**  
   Backend-frontend integration for Continuous Learning Track module

5. **[FLOOR_WING_ENHANCEMENT.md](FLOOR_WING_ENHANCEMENT.md)**  
   Floor Wing Dashboard transformation with announcements system

6. **[HACKATHON_REGISTRATION_FEATURE.md](HACKATHON_REGISTRATION_FEATURE.md)**  
   Two-step hackathon registration and reminder system

7. **[TESTING_GUIDE.md](TESTING_GUIDE.md)**  
   Comprehensive testing guide for role-based campus/floor system

8. **[CFC_TESTING_REPORT.md](CFC_TESTING_REPORT.md)**  
   CFC module testing results and validation

### Additional Resources

- **Backend README:** `backend/README.md`
- **API Documentation:** Swagger UI at `http://localhost:8000/api/docs/`
- **Frontend Components:** See `src/components/` for reusable components
- **API Services:** See `src/services/` for API integration examples

---

## 🔧 Configuration

### Vite Configuration

File: `vite.config.js`
```javascript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
```

### Django Settings Highlights

File: `backend/config/settings.py`
- **Database:** PostgreSQL with connection pooling
- **CORS:** Configured for frontend origins
- **JWT:** 60-minute access, 24-hour refresh tokens
- **File Upload:** 10MB max size, 10 files max per request
- **Static Files:** Whitenoise for production
- **Security:** HTTPS redirect in production, secure cookies

### Environment Variables

Required environment variables:
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
- `SECRET_KEY`
- `DEBUG` (True/False)
- `ALLOWED_HOSTS`
- `CORS_ALLOWED_ORIGINS`

---

## 🎨 Design System

### Color Palette

**Primary Colors:**
- Golden: `#FFD700` (Primary brand color)
- Deep Purple: `#1a0033` (Backgrounds)
- White: `#FFFFFF` (Text and cards)

**Status Colors:**
- Success: `#4CAF50` (Green)
- Warning: `#FF9800` (Orange)
- Error: `#F44336` (Red)
- Info: `#2196F3` (Blue)

**Role Colors:**
- Student: Blue gradient
- Mentor: Green gradient
- Floor Wing: Purple gradient
- Admin: Golden gradient

### Typography

- **Headings:** Poppins, Bold
- **Body:** Inter, Regular
- **Monospace:** Fira Code (for code blocks)

### Component Library

Reusable components:
- `GlassCard`: Glassmorphism card design
- `Button`: Multi-variant button component
- `Input`: Form input with validation
- `ProgressBar`: Animated progress indicator
- `Modal`: Centered modal dialog
- `Drawer`: Slide-in side panel

---

## 🚀 Deployment

### Production Checklist

- [ ] Set `DEBUG = False` in Django settings
- [ ] Configure production database
- [ ] Set secure `SECRET_KEY`
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up static file serving (Whitenoise)
- [ ] Configure HTTPS/SSL
- [ ] Set up environment variables securely
- [ ] Enable database backups
- [ ] Configure logging
- [ ] Set up monitoring (e.g., Sentry)
- [ ] Build frontend: `npm run build`
- [ ] Test production build
- [ ] Set up domain and DNS
- [ ] Configure CDN (optional)

### Recommended Hosting

- **Backend:** Heroku, AWS EC2, DigitalOcean
- **Database:** AWS RDS PostgreSQL, Heroku Postgres
- **Frontend:** Vercel, Netlify, AWS S3 + CloudFront
- **File Storage:** AWS S3, Cloudinary

---

## 🤝 Contributing

### Development Workflow

1. Create feature branch
2. Implement changes
3. Write tests
4. Update documentation
5. Submit pull request
6. Code review
7. Merge to main

### Code Style

**Python (Backend):**
- Follow PEP 8
- Use Black for formatting
- Type hints encouraged
- Docstrings for functions/classes

**JavaScript (Frontend):**
- Follow ESLint configuration
- Use Prettier for formatting
- Functional components preferred
- PropTypes or TypeScript

### Commit Messages

Format: `type(scope): description`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

Example: `feat(clt): add file upload validation`

---

## 📝 License

[Specify your license here]

---

## 👨‍💻 Team & Support

### Development Team

- **Backend Team:** Django REST Framework, PostgreSQL, API development
- **Frontend Team:** React, Vite, UI/UX implementation
- **DevOps Team:** Deployment, CI/CD, infrastructure

### Support

For issues and questions:
- **GitHub Issues:** [Project issues page]
- **Email:** [support email]
- **Documentation:** This file and related docs

---

## 📊 Statistics

- **Total Lines of Code:** ~50,000+
- **Backend Endpoints:** 100+
- **React Components:** 80+
- **Database Tables:** 25+
- **Active Features:** 15+
- **User Roles:** 4
- **Development Pillars:** 5

---

## 🔮 Future Enhancements

### Planned Features

1. **Mobile Application**
   - React Native implementation
   - Push notifications
   - Offline capability

2. **Advanced Analytics**
   - Machine learning predictions
   - Trend analysis
   - Personalized recommendations

3. **Integration Expansions**
   - GitHub profile integration
   - More online learning platforms
   - Industry partner APIs

4. **Communication Enhancements**
   - Real-time chat (WebSocket)
   - Video calling integration
   - Group messaging

5. **Gamification**
   - Achievement badges
   - Point system
   - Student rankings
   - Rewards program

6. **AI Features**
   - Automated submission review assistance
   - Chatbot support
   - Intelligent mentor matching

---

## ⚙️ System Requirements

### Development Environment

**Minimum:**
- 8GB RAM
- 256GB Storage
- Dual-core processor
- Windows 10/macOS/Linux

**Recommended:**
- 16GB RAM
- 512GB SSD
- Quad-core processor
- Modern browser (Chrome, Firefox, Edge)

### Production Environment

**Backend:**
- 4GB RAM minimum
- 50GB storage
- PostgreSQL 15+
- Python 3.10+

**Frontend:**
- CDN for static assets
- HTTPS enabled
- Modern browser support

---

## 📞 Quick Links

- **Live Demo:** [URL if available]
- **Documentation:** This file
- **API Docs:** `http://localhost:8000/api/docs/`
- **GitHub Repository:** [Repository URL]
- **Issue Tracker:** [Issues URL]

---

**Last Updated:** December 20, 2025  
**Version:** 1.0.0  
**Status:** Active Development

---

*For detailed information about specific features, please refer to the individual documentation files listed in the [Feature Documentation](#feature-documentation) section.*
