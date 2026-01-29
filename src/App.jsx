import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation, Navigate, useNavigate } from 'react-router-dom';
// eslint-disable-next-line no-unused-vars
import { motion, AnimatePresence } from 'framer-motion';
import { Home, Lightbulb, Heart, Trophy, Linkedin, Code, Menu, X, LogOut, Zap, Users, ClipboardCheck, Megaphone, Gamepad2 } from 'lucide-react';
import { ThemeProvider } from './theme/ThemeContext';
import { AuthProvider, useAuth } from './context/AuthContext';
import ThemeToggle from './components/ThemeToggle';
import ProtectedRoute from './components/ProtectedRoute';
import HomePage from './pages/student/Home';
import CLT from './pages/student/CLT';
import SRI from './pages/student/SRI';
import CFC from './pages/student/CFC';
import IIPC from './pages/student/IIPC';
import SCD from './pages/student/SCD';
import Games from './pages/student/Games';
import ProfileSettings from './pages/student/ProfileSettings';
import MonthlyReport from './pages/student/MonthlyReport';
import AdminDashboard from './pages/admin/AdminDashboard';
import AdminLayout from './pages/admin/AdminLayout';
import StudentProfiles from './pages/admin/profiles/StudentProfiles';
import MentorProfiles from './pages/admin/profiles/MentorProfiles';
import MentorManagement from './pages/admin/mentor/MentorManagement';
import FloorManagement from './pages/admin/floors/FloorManagement';
import SubmissionsManagement from './pages/admin/submissions/SubmissionsManagement';
import PillarRulesConfig from './pages/admin/rules/PillarRulesConfig';
import CommunicationCenter from './pages/admin/communication/CommunicationCenter';
import Leaderboard from './pages/admin/leaderboard/Leaderboard';
import Notifications from './pages/admin/notifications/Notifications';
import Roles from './pages/admin/roles/Roles';
import Settings from './pages/admin/settings/Settings';
import StudentMentorAssignment from './pages/admin/assignments/StudentMentorAssignment';
import CampusSelection from './pages/admin/campus/CampusSelection';
import CampusOverview from './pages/admin/campus/CampusOverview';
import FloorDetail from './pages/admin/campus/FloorDetail';
import MentorLayout from './pages/mentor/MentorLayout';
import FloorWingDashboard from './pages/floorwing/FloorWingDashboard';
import Login from './pages/Login';
import ParallaxIntro from './pages/ParallaxIntro';
import './App.css';

const NAV_ITEMS = [
  { path: '/', label: 'Home', icon: Home },
  { path: '/clt', label: 'CLT', icon: Lightbulb },
  { path: '/scd', label: 'SCD', icon: Code },
  { path: '/cfc', label: 'CFC', icon: Trophy },
  { path: '/iipc', label: 'IIPC', icon: Linkedin },
  { path: '/sri', label: 'SRI', icon: Heart },
];

function Navigation() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [isMenuOpen, setIsMenuOpen] = React.useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // Determine home path based on user role
  const getHomePath = () => {
    if (!user) return '/login';
    const role = user.role || user.profile?.role;
    switch (role) {
      case 'STUDENT':
      case 'student':
        return '/';
      case 'MENTOR':
      case 'mentor':
        return '/mentor-dashboard';
      case 'FLOOR_WING':
      case 'floorwing':
        return '/floorwing-dashboard';
      case 'ADMIN':
      case 'admin':
        return '/admin/campus-select';
      default:
        return '/login';
    }
  };

  // Show navigation items based on role
  const userRole = user?.role || user?.profile?.role;
  const showNavItems = user && (userRole === 'STUDENT' || userRole === 'student');
  const showMentorNavItems = user && (userRole === 'MENTOR' || userRole === 'mentor');
  const showFloorWingNavItems = user && (userRole === 'FLOOR_WING' || userRole === 'floorwing');

  const MENTOR_NAV_ITEMS = [
    { path: '/mentor-dashboard', label: 'Home', icon: Home },
    { path: '/mentor-dashboard/students', label: 'Student List', icon: Users },
    { path: '/mentor-dashboard/pillar-review', label: 'Pillar Review', icon: ClipboardCheck },
    { path: '/mentor-dashboard/announcements', label: 'Announcements', icon: Megaphone },
  ];

  const FLOOR_WING_NAV_ITEMS = [
    { path: '/floorwing-dashboard', label: 'Dashboard', icon: Home },
  ];

  return (
    <nav className="nav">
      <div className="nav-container">
        {/* Logo */}
        <Link to={getHomePath()} className="nav-logo">
          <motion.div
            className="nav-logo-icon"
            whileHover={{ rotate: 360 }}
            transition={{ duration: 0.6 }}
          >
            <Lightbulb size={32} />
          </motion.div>
          <span className="nav-logo-text">Cohort Web</span>
        </Link>

        {/* Desktop Navigation */}
        {showNavItems && (
          <div className="nav-links">
            {NAV_ITEMS.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;

              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`nav-link ${isActive ? 'nav-link--active' : ''}`}
                >
                  <Icon size={20} />
                  <span>{item.label}</span>
                  {isActive && (
                    <motion.div
                      className="nav-link-indicator"
                      layoutId="activeLink"
                      transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                    />
                  )}
                </Link>
              );
            })}
          </div>
        )}

        {/* Desktop Navigation - Mentor */}
        {showMentorNavItems && (
          <div className="nav-links">
            {MENTOR_NAV_ITEMS.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;

              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`nav-link ${isActive ? 'nav-link--active' : ''}`}
                >
                  <Icon size={20} />
                  <span>{item.label}</span>
                  {isActive && (
                    <motion.div
                      className="nav-link-indicator"
                      layoutId="activeLink"
                      transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                    />
                  )}
                </Link>
              );
            })}
          </div>
        )}

        {/* Desktop Navigation - Floor Wing */}
        {showFloorWingNavItems && (
          <div className="nav-links">
            {FLOOR_WING_NAV_ITEMS.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;

              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`nav-link ${isActive ? 'nav-link--active' : ''}`}
                >
                  <Icon size={20} />
                  <span>{item.label}</span>
                  {isActive && (
                    <motion.div
                      className="nav-link-indicator"
                      layoutId="activeLink"
                      transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                    />
                  )}
                </Link>
              );
            })}
          </div>
        )}

        {/* Theme Toggle & Mobile Menu */}
        <div className="nav-actions">
          {user && (
            <div className="nav-user-info">
              <span className="nav-user-role">{user.first_name || user.username || user.role}</span>
            </div>
          )}
          <ThemeToggle />
          {user && (
            <button
              className="nav-logout-button"
              onClick={handleLogout}
              aria-label="Logout"
              title="Logout"
            >
              <LogOut size={20} />
            </button>
          )}
          <button
            className="nav-menu-button"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            aria-label="Toggle menu"
          >
            {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>      {/* Mobile Menu - Student */}
      <AnimatePresence>
        {isMenuOpen && showNavItems && (
          <motion.div
            className="nav-mobile"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
          >
            {NAV_ITEMS.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;

              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`nav-mobile-link ${isActive ? 'nav-mobile-link--active' : ''}`}
                  onClick={() => setIsMenuOpen(false)}
                >
                  <Icon size={20} />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </motion.div>
        )}

        {/* Mobile Menu - Mentor */}
        {isMenuOpen && showMentorNavItems && (
          <motion.div
            className="nav-mobile"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
          >
            {MENTOR_NAV_ITEMS.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;

              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`nav-mobile-link ${isActive ? 'nav-mobile-link--active' : ''}`}
                  onClick={() => setIsMenuOpen(false)}
                >
                  <Icon size={20} />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </motion.div>
        )}

        {/* Mobile Menu - Floor Wing */}
        {isMenuOpen && showFloorWingNavItems && (
          <motion.div
            className="nav-mobile"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
          >
            {FLOOR_WING_NAV_ITEMS.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;

              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`nav-mobile-link ${isActive ? 'nav-mobile-link--active' : ''}`}
                  onClick={() => setIsMenuOpen(false)}
                >
                  <Icon size={20} />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
}

function AppContent() {
  const location = useLocation();
  const { user } = useAuth();
  const isLoginPage = location.pathname === '/login';
  const isIntroPage = location.pathname === '/intro';

  // If not logged in and not on login or intro page, redirect to login
  if (!user && location.pathname !== '/login' && location.pathname !== '/intro') {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="app">
      {user && !isLoginPage && !isIntroPage && <Navigation />}

      <main className="app-main">
        <Routes>
          {/* Public Routes */}
          <Route path="/intro" element={<ParallaxIntro />} />
          <Route path="/login" element={<Login />} />

          {/* Student Routes */}
          <Route path="/" element={<ProtectedRoute><HomePage /></ProtectedRoute>} />
          <Route path="/clt" element={<ProtectedRoute><CLT /></ProtectedRoute>} />
          <Route path="/sri" element={<ProtectedRoute><SRI /></ProtectedRoute>} />
          <Route path="/cfc" element={<ProtectedRoute><CFC /></ProtectedRoute>} />
          <Route path="/iipc" element={<ProtectedRoute><IIPC /></ProtectedRoute>} />
          <Route path="/scd" element={<ProtectedRoute><SCD /></ProtectedRoute>} />
          <Route path="/games" element={<ProtectedRoute><Games /></ProtectedRoute>} />
          {/* Redirect old hackathons route to CFC */}
          <Route path="/hackathons" element={<Navigate to="/cfc" replace />} />
          <Route path="/monthly-report" element={<ProtectedRoute><MonthlyReport /></ProtectedRoute>} />
          <Route path="/profile-settings" element={<ProtectedRoute><ProfileSettings /></ProtectedRoute>} />

          {/* Admin Campus Routes - Before AdminLayout */}
          <Route 
            path="/admin/campus-select" 
            element={
              <ProtectedRoute requiredRole="ADMIN">
                <CampusSelection />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/admin/campus/:campus" 
            element={
              <ProtectedRoute requiredRole="ADMIN">
                <CampusOverview />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/admin/campus/:campus/floor/:floor" 
            element={
              <ProtectedRoute requiredRole="ADMIN">
                <FloorDetail />
              </ProtectedRoute>
            } 
          />

          {/* Admin Routes with Sidebar Layout */}
          <Route path="/admin-dashboard" element={<ProtectedRoute><AdminLayout /></ProtectedRoute>}>
            <Route index element={<AdminDashboard />} />
          </Route>

          {/* Admin routes with /admin prefix */}
          <Route path="/admin" element={<ProtectedRoute><AdminLayout /></ProtectedRoute>}>
            <Route path="students" element={<StudentProfiles />} />
            <Route path="mentors" element={<MentorManagement />} />
            <Route path="assignments" element={<StudentMentorAssignment />} />
            <Route path="floors" element={<FloorManagement />} />
            <Route path="submissions" element={<SubmissionsManagement />} />
            <Route path="rules" element={<PillarRulesConfig />} />
            <Route path="communication" element={<CommunicationCenter />} />
            <Route path="leaderboard" element={<Leaderboard />} />
            <Route path="notifications" element={<Notifications />} />
            <Route path="roles" element={<Roles />} />
            <Route path="settings" element={<Settings />} />
          </Route>

          {/* Other Role Dashboards */}
          <Route 
            path="/mentor-dashboard/*" 
            element={
              <ProtectedRoute requiredRole="MENTOR">
                <MentorLayout />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/floorwing-dashboard" 
            element={
              <ProtectedRoute requiredRole="FLOOR_WING">
                <FloorWingDashboard />
              </ProtectedRoute>
            } 
          />
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <Router>
          <AppContent />
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
