# Cohort Web Application

A comprehensive platform connecting students, mentors, and institutions in a structured journey of academic and personal excellence through five pillars of holistic development.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![React](https://img.shields.io/badge/React-19.2.0-61DAFB?logo=react)
![Django](https://img.shields.io/badge/Django-4.2.7-092E20?logo=django)
![Vite](https://img.shields.io/badge/Vite-7.2.4-646CFF?logo=vite)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Five Pillars](#five-pillars)
- [User Roles](#user-roles)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)

## 🎯 Overview

Cohort Web is a unified platform designed to track and manage student development across multiple dimensions. It provides:

- **For Students**: Track progress across five development pillars with structured submission workflows
- **For Mentors**: Review and evaluate student submissions with comprehensive analytics
- **For Administrators**: Monitor institutional performance with real-time dashboards and reports
- **For Floor/Wing Representatives**: Manage floor-specific activities and communications

## ✨ Features

### Student Features
- 📊 Personal dashboard with progress tracking
- 📝 Submit activities across five pillars (CLT, SRI, CFC, IIPC, SCD)
- 📈 Visual progress indicators and analytics
- 🏆 Hackathon and competition tracking
- 💼 Professional development logging
- 🔗 LinkedIn profile and post verification
- 📱 Responsive design for mobile access

### Mentor Features
- 👥 Student list management
- ✅ Submission review and approval system
- 📊 Pillar-wise progress tracking
- 💬 Direct messaging with students
- 📈 Performance analytics
- 🗓️ Month-wise submission reviews

### Admin Features
- 🏢 Institutional dashboard
- 👨‍🎓 Student profile management
- 👨‍🏫 Mentor assignment and management
- 🏢 Floor and wing management
- 📊 Comprehensive analytics and reporting
- 📢 Communication center
- 🏅 Leaderboard system

### Floor/Wing Features
- 🏠 Floor-specific dashboards
- 📢 Announcements and communications
- 📊 Floor-level analytics

## 🛠️ Tech Stack

### Frontend
- **Framework**: React 19.2.0
- **Build Tool**: Vite 7.2.4
- **Routing**: React Router DOM 6.20.0
- **Animations**: Framer Motion 11.15.0, GSAP 3.14.2
- **3D Graphics**: Three.js 0.181.0
- **Icons**: Lucide React 0.559.0
- **Charts**: Recharts 3.5.1
- **State Management**: Zustand 5.0.9
- **HTTP Client**: Axios 1.13.2
- **Styling**: CSS Modules with custom design system

### Backend
- **Framework**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Authentication**: JWT (djangorestframework-simplejwt 5.3.0)
- **Database**: PostgreSQL (psycopg2-binary 2.9.9)
- **Image Processing**: Pillow 10.1.0
- **CORS**: django-cors-headers 4.3.1
- **Security**: Cryptography 41.0.7, Argon2 23.1.0

## 📁 Project Structure

```
Cohort_Web_App/
├── backend/                      # Main Django backend
│   ├── apps/                     # Django applications
│   │   ├── cfc/                 # Center for Creativity
│   │   ├── clt/                 # Continuous Learning Track
│   │   ├── iipc/                # Industry & Interview Prep
│   │   ├── profiles/            # User profiles
│   │   ├── scd/                 # Self-Code Development
│   │   └── sri/                 # Social Responsibility Initiative
│   ├── config/                  # Django settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── media/                   # User uploaded files
│   ├── static/                  # Static files
│   ├── manage.py
│   └── requirements.txt
│
├── backend_admin/               # Admin-specific backend
│   ├── apps/
│   │   ├── analytics/          # Analytics dashboard
│   │   ├── cohort_management/  # Cohort operations
│   │   ├── mentor_management/  # Mentor assignment
│   │   └── user_management/    # User administration
│   ├── config/
│   └── manage.py
│
├── backend_mentor/              # Mentor-specific backend
│   ├── apps/
│   │   ├── communication/      # Messaging system
│   │   ├── mentor_reports/     # Report generation
│   │   ├── student_tracking/   # Progress tracking
│   │   └── submission_review/  # Review workflows
│   ├── config/
│   └── manage.py
│
├── src/                         # React frontend
│   ├── assets/                  # Images, fonts, etc.
│   ├── components/              # Reusable components
│   │   ├── Button.jsx
│   │   ├── GlassCard.jsx
│   │   ├── Input.jsx
│   │   ├── ProgressBar.jsx
│   │   ├── ProtectedRoute.jsx
│   │   ├── ThemeToggle.jsx
│   │   └── admin/              # Admin-specific components
│   │
│   ├── context/                 # React Context
│   │   └── AuthContext.jsx     # Authentication state
│   │
│   ├── pages/                   # Page components
│   │   ├── Login.jsx           # Login page
│   │   ├── ParallaxIntro.jsx   # Landing page
│   │   │
│   │   ├── student/            # Student pages
│   │   │   ├── Home.jsx
│   │   │   ├── CLT.jsx
│   │   │   ├── SRI.jsx
│   │   │   ├── CFC.jsx
│   │   │   ├── IIPC.jsx
│   │   │   ├── SCD.jsx
│   │   │   ├── Hackathons.jsx
│   │   │   ├── MonthlyReport.jsx
│   │   │   └── ProfileSettings.jsx
│   │   │
│   │   ├── mentor/             # Mentor pages
│   │   │   ├── MentorLayout.jsx
│   │   │   ├── MentorHome.jsx
│   │   │   ├── MentorDashboard.jsx
│   │   │   ├── SubmissionReview.jsx
│   │   │   └── PillarReview.jsx
│   │   │
│   │   ├── admin/              # Admin pages
│   │   │   ├── AdminLayout.jsx
│   │   │   ├── AdminDashboard.jsx
│   │   │   ├── profiles/
│   │   │   ├── mentor/
│   │   │   ├── floors/
│   │   │   ├── submissions/
│   │   │   ├── communication/
│   │   │   ├── leaderboard/
│   │   │   └── settings/
│   │   │
│   │   └── floorwing/          # Floor/Wing pages
│   │       └── FloorWingDashboard.jsx
│   │
│   ├── services/                # API services
│   │   ├── api.js              # Base API configuration
│   │   ├── auth.js             # Authentication
│   │   ├── cfc.js              # CFC pillar
│   │   ├── clt.js              # CLT pillar
│   │   ├── iipc.js             # IIPC pillar
│   │   ├── scd.js              # SCD pillar
│   │   ├── admin.js            # Admin operations
│   │   └── profile.js          # User profiles
│   │
│   ├── store/                   # State management
│   │   └── adminStore.js       # Admin state (Zustand)
│   │
│   ├── theme/                   # Theming
│   │   ├── theme.js
│   │   └── ThemeContext.jsx
│   │
│   ├── App.jsx                  # Main app component
│   ├── main.jsx                 # Entry point
│   └── index.css                # Global styles
│
├── public/                      # Public assets
├── .env                         # Environment variables
├── package.json                 # Node dependencies
├── vite.config.js              # Vite configuration
├── eslint.config.js            # ESLint configuration
└── README.md                    # This file
```

## 🚀 Installation

### Prerequisites

- **Node.js** 18.x or higher
- **Python** 3.10 or higher
- **PostgreSQL** 14.x or higher
- **Git**

### Clone Repository

```bash
git clone https://github.com/Amal0318/Cohort_Web_App.git
cd Cohort_Web_App
```

### Frontend Setup

```bash
# Install dependencies
npm install

# Create .env file for frontend
cat > .env << EOF
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_LINKEDIN_CLIENT_ID=your_linkedin_client_id
VITE_LINKEDIN_REDIRECT_URI=http://localhost:5173/iipc/callback
EOF
```

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file for backend
cat > .env << EOF
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_NAME=cohort_db
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5174
JWT_SECRET_KEY=your-jwt-secret-key
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
LINKEDIN_REDIRECT_URI=http://localhost:5173/iipc/callback
EOF

# Run migrations
python3 manage.py migrate

# Create superuser
python3 manage.py createsuperuser

# Create test users (optional)
python3 create_test_users.py
```

### Database Setup

```bash
# Create PostgreSQL database
psql -U postgres
CREATE DATABASE cohort_db;
CREATE USER your_db_user WITH PASSWORD 'your_db_password';
GRANT ALL PRIVILEGES ON DATABASE cohort_db TO your_db_user;
\q
```

## 🏃 Running the Application

### Development Mode

**Terminal 1 - Frontend:**
```bash
npm run dev
# Frontend runs on http://localhost:5173 (or 5174 if 5173 is busy)
```

**Terminal 2 - Backend:**
```bash
cd backend
source .venv/bin/activate  # Activate virtual environment
python3 manage.py runserver
# Backend runs on http://127.0.0.1:8000
```

### Production Build

```bash
# Build frontend
npm run build

# Preview production build
npm run preview

# Serve with backend
cd backend
python3 manage.py collectstatic
python3 manage.py runserver --insecure  # For testing static files
```

### Access Points

- **Frontend**: http://localhost:5173
- **Backend API**: http://127.0.0.1:8000
- **Admin Panel**: http://127.0.0.1:8000/admin
- **API Docs**: http://127.0.0.1:8000/api/docs

## 🎓 Five Pillars

### 1. CLT - Continuous Learning Track 📚
Track structured learning paths including:
- Online courses (Coursera, Udemy, edX)
- Certifications and achievements
- Workshop participation
- Skill development progress

### 2. SRI - Social Responsibility Initiative ❤️
Document community engagement:
- Social service activities
- Community projects
- Volunteer work
- Impact assessments

### 3. CFC - Center for Creativity 🏆
Build professional portfolio:
- Hackathon participation
- BMC video presentations
- Internship experiences
- GenAI projects

### 4. IIPC - Industry & Interview Preparation 💼
Professional networking and preparation:
- LinkedIn profile verification
- Post engagement tracking
- Connection management
- Industry insights

### 5. SCD - Self-Code Development 💻
Personal coding growth:
- LeetCode challenges
- GitHub projects
- Technical blog posts
- Open source contributions

## 👥 User Roles

### Student
- **Login**: Regular user credentials
- **Access**: Personal dashboard, pillar submissions, progress tracking
- **Capabilities**: Submit activities, view mentor feedback, track progress

### Mentor
- **Login**: Mentor credentials
- **Access**: Student list, submission reviews, analytics
- **Capabilities**: Review submissions, provide feedback, track mentee progress

### Admin
- **Login**: Superuser credentials
- **Access**: Full system access
- **Capabilities**: User management, system configuration, institutional analytics

### Floor/Wing Representative
- **Login**: Floor wing credentials
- **Access**: Floor-specific dashboard
- **Capabilities**: Floor management, announcements, local analytics

## 🔌 API Documentation

### Authentication Endpoints
```
POST /api/auth/token/          # Login (get JWT tokens)
POST /api/auth/token/refresh/  # Refresh access token
GET  /api/auth/user/           # Get current user info
```

### Student Endpoints
```
POST /api/clt/submissions/     # Submit CLT activity
POST /api/sri/submissions/     # Submit SRI activity
POST /api/cfc/hackathon/       # Submit hackathon
POST /api/iipc/posts/          # Submit LinkedIn post
POST /api/scd/submissions/     # Submit SCD activity
GET  /api/dashboard/stats/     # Get dashboard statistics
```

### Mentor Endpoints
```
GET  /api/mentor/students/             # Get assigned students
GET  /api/mentor/submissions/          # Get submissions to review
POST /api/mentor/review/               # Submit review
GET  /api/mentor/analytics/            # Get analytics
```

### Admin Endpoints
```
GET    /api/admin/users/              # List all users
POST   /api/admin/users/              # Create user
PUT    /api/admin/users/{id}/         # Update user
DELETE /api/admin/users/{id}/         # Delete user
GET    /api/admin/analytics/          # System analytics
```

## 🎨 Design System

### Color Palette
- **Primary Gradient**: `#F7C948` → `#E53935`
- **Background (Light)**: `#FFFFFF`
- **Background (Dark)**: `#121212`
- **Text Primary (Light)**: `#000000`
- **Text Primary (Dark)**: `#FFFFFF`
- **Text Secondary (Light)**: `#616161`
- **Text Secondary (Dark)**: `#BDBDBD`

### Typography
- **Headings**: Sora (700-800 weight)
- **Body**: Inter (400-600 weight)
- **UI Elements**: Manrope (500-700 weight)

### Components
- **GlassCard**: Glassmorphism design with backdrop blur
- **Button**: Primary (gradient), Secondary, Outline variants
- **Input**: Consistent styling with focus states
- **ProgressBar**: Animated progress indicators

## 📝 Environment Variables

### Frontend (.env)
```env
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_LINKEDIN_CLIENT_ID=your_linkedin_client_id
VITE_LINKEDIN_REDIRECT_URI=http://localhost:5173/iipc/callback
```

### Backend (.env)
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_NAME=cohort_db
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173
JWT_SECRET_KEY=your-jwt-secret
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
```

## 🧪 Testing

### Frontend Tests
```bash
npm run lint      # Run ESLint
npm run preview   # Test production build
```

### Backend Tests
```bash
cd backend
python3 manage.py test                    # Run all tests
python3 test_clt_endpoints.py            # Test CLT endpoints
python3 test_full_integration.py         # Integration tests
python3 test_iipc_endpoints.py           # Test IIPC endpoints
```

## 📖 Additional Documentation

- **Authentication System**: See [AUTH_SYSTEM.md](AUTH_SYSTEM.md)
- **CLT Integration**: See [CLT_INTEGRATION_GUIDE.md](CLT_INTEGRATION_GUIDE.md)
- **CFC Testing**: See [CFC_TESTING_REPORT.md](CFC_TESTING_REPORT.md)
- **Chat System**: See [CHAT_SYSTEM.md](CHAT_SYSTEM.md)

## 🤝 Contributing

### Branch Strategy
- `main`: Production-ready code
- `develop`: Development branch
- `feature/*`: Feature branches
- `bugfix/*`: Bug fix branches

### Commit Convention
```
type(scope): description

Types: feat, fix, docs, style, refactor, test, chore
Example: feat(cfc): add hackathon submission validation
```

### Pull Request Process
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is proprietary software. All rights reserved.

## 👨‍💻 Development Team

- **Frontend Lead**: React, Vite, UI/UX
- **Backend Lead**: Django, PostgreSQL, API Design
- **DevOps**: Deployment, CI/CD
- **QA**: Testing, Documentation

## 🐛 Known Issues

- Migration warnings for `clt` app (non-blocking)
- Port 5173 may be occupied (app automatically uses 5174)

## 🚀 Future Enhancements

- [ ] Mobile app (React Native)
- [ ] Real-time notifications (WebSockets)
- [ ] Advanced analytics dashboard
- [ ] AI-powered insights
- [ ] Integration with more learning platforms
- [ ] Gamification features
- [ ] Export reports (PDF/Excel)

## 📞 Support

For support, please contact:
- **Email**: support@cohortweb.com
- **Issues**: GitHub Issues
- **Documentation**: Project Wiki

---

**Built with ❤️ by the Cohort Team**

*Last Updated: January 2025*
#   F o r c e   r e b u i l d   1 2 / 2 3 / 2 0 2 5   0 0 : 5 6 : 1 6  
 