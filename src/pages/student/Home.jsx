import React, { useState, useEffect } from 'react';
// eslint-disable-next-line no-unused-vars
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import {
  Lightbulb, Heart, Trophy, Linkedin, Code, Gamepad2,
  User, Mail, Phone, Users, Bell, Clock,
  CheckCircle, XCircle, AlertCircle, FileText, Settings, Loader2, Calendar, Megaphone, ShoppingBag
} from 'lucide-react';
import GlassCard from '../../components/GlassCard';
import Button from '../../components/Button';
import GamificationCard from '../../components/GamificationCard';
import ProgressAlert from '../../components/ProgressAlert';
import BatchStatsCard from '../../components/BatchStatsCard';
import { useAuth } from '../../context/AuthContext';
import dashboardService from '../../services/dashboard';
import { getUpcomingHackathons } from '../../services/cfc';
import { getStudentAnnouncements, markAnnouncementAsRead } from '../../services/announcements';
import gamificationAPI from '../../services/gamification';
import './Home.css';

const PILLARS = [
  {
    id: 'clt',
    title: 'Center for Learning and Teaching',
    description: 'Document your creative projects and showcase your learning journey',
    icon: Lightbulb,
    color: '#ffcc00',
    path: '/clt',
  },
  {
    id: 'scd',
    title: 'Skill and Career Development',
    description: 'Track your coding skills and competitive programming journey',
    icon: Code,
    color: '#FF5722',
    path: '/scd',
  },
  {
    id: 'cfc',
    title: 'Center for Creativity',
    description: 'Build your professional portfolio and track career development',
    icon: Trophy,
    color: '#FFC107',
    path: '/cfc',
  },
  {
    id: 'iipc',
    title: 'Industry Institute Partnership Cell',
    description: 'Verify your LinkedIn activity and professional network',
    icon: Linkedin,
    color: '#0A66C2',
    path: '/iipc',
  },
  {
    id: 'sri',
    title: 'Social Responsibility Initiatives',
    description: 'Track your community service and social impact activities',
    icon: Heart,
    color: '#ffcc00',
    path: '/sri',
  },
  {
    id: 'games',
    title: 'Brain Games',
    description: 'Challenge yourself with daily puzzles and track your progress',
    icon: Gamepad2,
    color: '#9C27B0',
    path: '/games',
  },
];

export const HomePage = () => {
  const { user } = useAuth();
  const [showProfile, setShowProfile] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [dashboardData, setDashboardData] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [upcomingHackathons, setUpcomingHackathons] = useState([]);
  const [showHackathonModal, setShowHackathonModal] = useState(false);
  const [announcements, setAnnouncements] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [showAnnouncementsModal, setShowAnnouncementsModal] = useState(false);
  const [showStoreModal, setShowStoreModal] = useState(false);
  const [storeItems, setStoreItems] = useState([]);
  const [userCredits, setUserCredits] = useState(0);
  const [loadingStore, setLoadingStore] = useState(false);
  const [leaderboard, setLeaderboard] = useState([]);
  const [seasonActive, setSeasonActive] = useState(false);

  useEffect(() => {
    document.title = 'Dashboard | Cohort Web';
    
    // Check if user is authenticated
    const token = localStorage.getItem('accessToken');
    if (!token) {
      setError('Please log in to view dashboard');
      setLoading(false);
      return;
    }
    
    fetchDashboardData();
    fetchHackathons();
    fetchAnnouncements();
    fetchLeaderboard();

    // Set up auto-refresh every 30 seconds
    const refreshInterval = setInterval(() => {
      fetchDashboardData(true); // Silent refresh
      fetchAnnouncements(true);
    }, 30000);

    // Cleanup interval on unmount
    return () => {
      clearInterval(refreshInterval);
    };
  }, []);

  const fetchHackathons = async () => {
    try {
      const data = await getUpcomingHackathons();
      setUpcomingHackathons(data);
    } catch (err) {
      console.error('Failed to fetch hackathons:', err);
    }
  };

  const fetchAnnouncements = async (silent = false) => {
    try {
      const data = await getStudentAnnouncements();
      setAnnouncements(data.announcements || []);
      setUnreadCount(data.unread_count || 0);
    } catch (err) {
      console.error('Failed to fetch announcements:', err);
      if (!silent) {
        setAnnouncements([]);
        setUnreadCount(0);
      }
    }
  };

  const handleMarkAsRead = async (announcementId) => {
    try {
      await markAnnouncementAsRead(announcementId);
      // Refresh announcements to update read status
      await fetchAnnouncements(true);
    } catch (err) {
      console.error('Failed to mark announcement as read:', err);
    }
  };

  const fetchDashboardData = async (silent = false) => {
    if (!silent) {
      setLoading(true);
    }
    setError(null);
    
    try {
      const data = await dashboardService.getStats();
      setDashboardData(data);
      setLastUpdated(new Date());
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
      console.error('Error response:', err.response?.data);
      console.error('Error status:', err.response?.status);
      if (!silent) {
        const errorMessage = err.response?.data?.detail || err.message || 'Failed to load dashboard data';
        setError(errorMessage);
      }
    } finally {
      if (!silent) {
        setLoading(false);
      }
    }
  };

  // Get pillar progress from API data
  const pillarProgress = dashboardData ? {
    clt: {
      completed: dashboardData.pillars.clt.completed,
      total: dashboardData.pillars.clt.monthly_target,
      percentage: dashboardData.pillars.clt.percentage
    },
    sri: {
      completed: dashboardData.pillars.sri.completed,
      total: dashboardData.pillars.sri.monthly_target,
      percentage: dashboardData.pillars.sri.percentage
    },
    cfc: {
      completed: dashboardData.pillars.cfc.completed,
      total: dashboardData.pillars.cfc.monthly_target,
      percentage: dashboardData.pillars.cfc.percentage
    },
    iipc: {
      completed: dashboardData.pillars.iipc.completed,
      total: dashboardData.pillars.iipc.monthly_target,
      percentage: dashboardData.pillars.iipc.percentage
    },
    scd: {
      completed: dashboardData.pillars.scd.completed,
      total: dashboardData.pillars.scd.monthly_target,
      percentage: dashboardData.pillars.scd.percentage
    },
    games: {
      completed: 0,
      total: 30,
      percentage: 0
    },
  } : {
    clt: { completed: 0, total: 1, percentage: 0 },
    sri: { completed: 0, total: 0, percentage: 0 },
    cfc: { completed: 0, total: 3, percentage: 0 },
    iipc: { completed: 0, total: 2, percentage: 0 },
    scd: { completed: 0, total: 1, percentage: 0 },
    games: { completed: 0, total: 30, percentage: 0 },
  };

  const notifications = dashboardData?.notifications || [];
  const recentActivities = dashboardData?.recent_activities || [];
  const overallProgress = dashboardData?.overall?.percentage || 0;

  const getStatusIcon = (status) => {
    if (status === 'completed' || status === 'approved') return <CheckCircle size={16} color="#4CAF50" />;
    if (status === 'pending' || status === 'submitted' || status === 'under_review') return <AlertCircle size={16} color="#FF9800" />;
    return <XCircle size={16} color="#f44336" />;
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return '1 day ago';
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
    return `${Math.floor(diffDays / 30)} months ago`;
  };

  const fetchStoreItems = async () => {
    try {
      setLoadingStore(true);
      const [titlesResponse, walletResponse] = await Promise.all([
        gamificationAPI.getTitles(),
        gamificationAPI.getMyWallet()
      ]);
      setStoreItems(titlesResponse.data);
      setUserCredits(walletResponse.data.available_credits);
    } catch (err) {
      console.error('Error fetching store items:', err);
    } finally {
      setLoadingStore(false);
    }
  };

  const handleRedeemTitle = async (titleId, cost) => {
    if (userCredits < cost) {
      alert('Insufficient credits!');
      return;
    }

    try {
      await gamificationAPI.redeemTitle(titleId);
      alert('Title redeemed successfully!');
      fetchStoreItems(); // Refresh store data
    } catch (err) {
      console.error('Error redeeming title:', err);
      alert(err.response?.data?.error || 'Failed to redeem title');
    }
  };

  const handleEquipTitle = async (titleId) => {
    try {
      await gamificationAPI.equipTitle(titleId);
      alert('Title equipped successfully!');
      fetchStoreItems(); // Refresh store data
    } catch (err) {
      console.error('Error equipping title:', err);
      alert(err.response?.data?.error || 'Failed to equip title');
    }
  };

  const fetchLeaderboard = async () => {
    try {
      const response = await gamificationAPI.getCurrentSeasonLeaderboard();
      // Get top 3 performers only
      const top3 = response.data.slice(0, 3);
      setLeaderboard(top3);
      setSeasonActive(true);
    } catch (err) {
      console.error('Error fetching leaderboard:', err);
      // If 404, season might not be active
      if (err.response?.status === 404) {
        setSeasonActive(false);
      }
    }
  };

  if (loading) {
    return (
      <div className="home-container">
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
          <Loader2 size={48} className="spinner" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="home-container">
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <XCircle size={48} color="#ffcc00" style={{ marginBottom: '1rem' }} />
          <h2>{error}</h2>
          {error.includes('log in') ? (
            <Button onClick={() => window.location.href = '/login'} style={{ marginTop: '1rem' }}>
              Go to Login
            </Button>
          ) : (
            <Button onClick={fetchDashboardData} style={{ marginTop: '1rem' }}>
              Retry
            </Button>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="home-container">
      {/* Progress Alert - Random Motivational Notifications */}
      <ProgressAlert />

      {/* Profile Modal */}
      {showProfile && (
        <motion.div
          className="profile-modal-overlay"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          onClick={() => setShowProfile(false)}
        >
          <motion.div
            className="profile-modal"
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            onClick={(e) => e.stopPropagation()}
          >
            <GlassCard>
              <div className="profile-modal-content">
                <div className="profile-avatar">
                  <User size={48} />
                </div>
                <h2>{dashboardData?.student_info?.name || user?.username || 'Student'}</h2>
                <div className="profile-details">
                  <div className="profile-detail-item">
                    <Mail size={18} />
                    <span>{dashboardData?.student_info?.email || user?.email || 'student@test.com'}</span>
                  </div>
                  <div className="profile-detail-item">
                    <FileText size={18} />
                    <span>Roll No: {dashboardData?.student_info?.roll_number || user?.roll_number || 'N/A'}</span>
                  </div>
                  <div className="profile-detail-item">
                    <Phone size={18} />
                    <span>{dashboardData?.student_info?.phone || user?.phone || 'N/A'}</span>
                  </div>
                  <div className="profile-detail-item">
                    <Users size={18} />
                    <span>Mentor: {dashboardData?.student_info?.mentor_name || user?.mentor_name || 'Not Assigned'}</span>
                  </div>
                </div>
                <Link to="/profile-settings" className="profile-settings-button">
                  <Button variant="primary" icon={<Settings size={18} />}>
                    Profile Settings
                  </Button>
                </Link>
              </div>
            </GlassCard>
          </motion.div>
        </motion.div>
      )}

      {/* Hackathon Notifications Modal */}
      {showHackathonModal && (
        <motion.div
          className="profile-modal-overlay"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          onClick={() => setShowHackathonModal(false)}
        >
          <motion.div
            className="profile-modal"
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            onClick={(e) => e.stopPropagation()}
            style={{ maxWidth: '650px', maxHeight: '85vh', display: 'flex', flexDirection: 'column' }}
          >
            <GlassCard>
              <div className="profile-modal-content" style={{ display: 'flex', flexDirection: 'column', maxHeight: '80vh' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', paddingBottom: '1rem', borderBottom: '2px solid rgba(255, 193, 7, 0.2)' }}>
                  <Trophy size={32} style={{ color: '#FFC107' }} />
                  <h2 style={{ margin: 0, fontSize: '1.75rem', fontWeight: '700' }}>Upcoming Hackathons</h2>
                  {upcomingHackathons.length > 0 && (
                    <span style={{
                      marginLeft: 'auto',
                      padding: '0.35rem 0.85rem',
                      background: 'rgba(255, 193, 7, 0.2)',
                      color: '#FFC107',
                      borderRadius: '20px',
                      fontSize: '0.9rem',
                      fontWeight: '700'
                    }}>
                      {upcomingHackathons.length} Event{upcomingHackathons.length !== 1 ? 's' : ''}
                    </span>
                  )}
                </div>
                
                {upcomingHackathons.length > 0 ? (
                  <div style={{ 
                    display: 'flex', 
                    flexDirection: 'column', 
                    gap: '1rem',
                    overflowY: 'auto',
                    maxHeight: '500px',
                    padding: '1rem 0.25rem',
                    marginTop: '1rem'
                  }}>
                    {upcomingHackathons.map((hackathon) => {
                      const daysLeft = hackathon.days_until_event;
                      const isUrgent = daysLeft <= 3;
                      const motivationMsg = daysLeft === 0 ? "It's TODAY! Give it your best shot! 🚀" :
                                           daysLeft === 1 ? "Tomorrow's the day! Get ready! 🔥" :
                                           daysLeft <= 3 ? "Just a few days left! Time to shine! ✨" :
                                           "Start preparing now! You got this! 🎯";
                      
                      return (
                        <div key={hackathon.id} style={{
                          padding: '1.25rem',
                          background: isUrgent ? 'rgba(255, 71, 87, 0.08)' : 'rgba(255, 255, 255, 0.03)',
                          borderRadius: '14px',
                          border: `2px solid ${isUrgent ? 'rgba(255, 71, 87, 0.4)' : 'rgba(255, 193, 7, 0.3)'}`,
                          transition: 'all 0.3s ease',
                          boxShadow: isUrgent ? '0 4px 12px rgba(255, 71, 87, 0.15)' : '0 2px 8px rgba(0, 0, 0, 0.1)'
                        }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '0.85rem' }}>
                            <strong style={{ fontSize: '1.15rem', color: 'var(--text-primary)', lineHeight: '1.3', flex: 1 }}>
                              {hackathon.hackathon_name}
                            </strong>
                            <span style={{
                              padding: '0.4rem 0.85rem',
                              background: isUrgent ? 'rgba(255, 71, 87, 0.2)' : 'rgba(255, 193, 7, 0.2)',
                              color: isUrgent ? '#ff4757' : '#FFC107',
                              borderRadius: '8px',
                              fontSize: '0.85rem',
                              fontWeight: '700',
                              whiteSpace: 'nowrap',
                              marginLeft: '1rem',
                              border: `1px solid ${isUrgent ? 'rgba(255, 71, 87, 0.3)' : 'rgba(255, 193, 7, 0.3)'}`
                            }}>
                              {daysLeft === 0 ? '🔴 Today!' : daysLeft === 1 ? '🟠 Tomorrow' : `⏰ ${daysLeft} days`}
                            </span>
                          </div>
                          <p style={{ margin: '0.65rem 0', fontSize: '0.95rem', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            <Calendar size={16} style={{ color: '#FFC107', flexShrink: 0 }} />
                            <span>
                              {new Date(hackathon.participation_date).toLocaleDateString('en-US', { 
                                weekday: 'long', month: 'long', day: 'numeric', year: 'numeric'
                              })} • {hackathon.mode}
                            </span>
                          </p>
                          <p style={{ 
                            margin: '0.85rem 0 0 0', 
                            fontSize: '0.9rem', 
                            color: 'var(--text-primary)',
                            fontWeight: '600',
                            padding: '0.65rem 0.85rem',
                            background: isUrgent ? 'rgba(255, 71, 87, 0.1)' : 'rgba(255, 193, 7, 0.1)',
                            borderRadius: '8px',
                            borderLeft: `3px solid ${isUrgent ? '#ff4757' : '#FFC107'}`
                          }}>
                            {motivationMsg}
                          </p>
                          {hackathon.hackathon_url && (
                            <a 
                              href={hackathon.hackathon_url} 
                              target="_blank" 
                              rel="noopener noreferrer"
                              style={{
                                display: 'inline-flex',
                                alignItems: 'center',
                                gap: '0.5rem',
                                marginTop: '0.85rem',
                                padding: '0.5rem 1rem',
                                background: 'rgba(255, 193, 7, 0.15)',
                                border: '1px solid rgba(255, 193, 7, 0.3)',
                                borderRadius: '8px',
                                color: '#FFC107',
                                textDecoration: 'none',
                                fontSize: '0.9rem',
                                fontWeight: '600',
                                transition: 'all 0.2s ease'
                              }}
                              onMouseEnter={(e) => {
                                e.target.style.background = 'rgba(255, 193, 7, 0.25)';
                                e.target.style.transform = 'translateX(4px)';
                              }}
                              onMouseLeave={(e) => {
                                e.target.style.background = 'rgba(255, 193, 7, 0.15)';
                                e.target.style.transform = 'translateX(0)';
                              }}
                            >
                              View Details →
                            </a>
                          )}
                        </div>
                      );
                    })}
                  </div>
                ) : (
                  <div style={{ 
                    textAlign: 'center', 
                    padding: '3rem 2rem',
                    color: 'var(--text-secondary)'
                  }}>
                    <Trophy size={64} style={{ color: 'rgba(255, 193, 7, 0.3)', marginBottom: '1.5rem' }} />
                    <h3 style={{ fontSize: '1.25rem', fontWeight: '600', marginBottom: '0.5rem', color: 'var(--text-primary)' }}>No upcoming hackathons registered yet</h3>
                    <p style={{ fontSize: '0.95rem', marginTop: '0.75rem' }}>Go to CFC page to register for exciting hackathons!</p>
                  </div>
                )}
                
                <div style={{ marginTop: '1.5rem', paddingTop: '1rem', borderTop: '2px solid rgba(255, 255, 255, 0.05)', textAlign: 'center' }}>
                  <Button onClick={() => setShowHackathonModal(false)} style={{ minWidth: '150px' }}>
                    Close
                  </Button>
                </div>
              </div>
            </GlassCard>
          </motion.div>
        </motion.div>
      )}

      {/* Announcements Modal */}
      {showAnnouncementsModal && (
        <motion.div
          className="profile-modal-overlay"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          onClick={() => setShowAnnouncementsModal(false)}
        >
          <motion.div
            className="profile-modal"
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            onClick={(e) => e.stopPropagation()}
            style={{ maxWidth: '700px' }}
          >
            <GlassCard>
              <div className="profile-modal-content">
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.5rem' }}>
                  <Megaphone size={32} style={{ color: '#ffcc00' }} />
                  <h2 style={{ margin: 0 }}>Announcements from Mentor</h2>
                </div>
                
                {announcements.length > 0 ? (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', maxHeight: '500px', overflowY: 'auto' }}>
                    {announcements.map((announcement) => {
                      const getCategoryColor = (category) => {
                        const colors = {
                          general: '#6b7280',
                          event: '#8b5cf6',
                          deadline: '#ef4444',
                          important: '#f59e0b',
                          reminder: '#10b981'
                        };
                        return colors[category] || colors.general;
                      };

                      const getPriorityLabel = (priority) => {
                        return priority === 'high' ? '🔴 High' : priority === 'medium' ? '🟠 Medium' : '🟢 Low';
                      };
                      
                      return (
                        <div key={announcement.id} style={{
                          padding: '1.25rem',
                          background: announcement.is_read ? 'rgba(255, 255, 255, 0.02)' : 'rgba(247, 201, 72, 0.05)',
                          borderRadius: '12px',
                          border: `2px solid ${announcement.is_read ? getCategoryColor(announcement.category) + '20' : getCategoryColor(announcement.category) + '40'}`,
                          transition: 'all 0.3s ease',
                          opacity: announcement.is_read ? 0.7 : 1
                        }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '0.75rem' }}>
                            <div style={{ flex: 1 }}>
                              <strong style={{ fontSize: '1.15rem', color: 'var(--text-primary)' }}>
                                {!announcement.is_read && <span style={{ color: '#ffcc00', marginRight: '0.5rem' }}>●</span>}
                                {announcement.title}
                              </strong>
                            </div>
                            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginLeft: '1rem' }}>
                              <span style={{
                                padding: '0.25rem 0.65rem',
                                background: `${getCategoryColor(announcement.category)}20`,
                                color: getCategoryColor(announcement.category),
                                borderRadius: '6px',
                                fontSize: '0.75rem',
                                fontWeight: '700',
                                textTransform: 'uppercase',
                                whiteSpace: 'nowrap'
                              }}>
                                {announcement.category}
                              </span>
                              <span style={{
                                padding: '0.25rem 0.65rem',
                                background: 'rgba(255, 255, 255, 0.1)',
                                color: 'var(--text-secondary)',
                                borderRadius: '6px',
                                fontSize: '0.75rem',
                                fontWeight: '600',
                                whiteSpace: 'nowrap'
                              }}>
                                {getPriorityLabel(announcement.priority)}
                              </span>
                            </div>
                          </div>
                          <p style={{ margin: '0.75rem 0', fontSize: '0.95rem', color: 'var(--text-secondary)', lineHeight: '1.6' }}>
                            {announcement.description}
                          </p>
                          {announcement.event_date && (
                            <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.9rem', color: 'var(--text-primary)' }}>
                              <Calendar size={16} style={{ verticalAlign: 'middle', marginRight: '0.5rem', color: '#ffcc00' }} />
                              {new Date(announcement.event_date).toLocaleDateString('en-US', { 
                                weekday: 'long', month: 'long', day: 'numeric', year: 'numeric'
                              })}
                            </p>
                          )}
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '0.75rem' }}>
                            <p style={{ 
                              margin: 0, 
                              fontSize: '0.8rem', 
                              color: 'var(--text-secondary)',
                              fontStyle: 'italic'
                            }}>
                              Posted {announcement.time_ago}
                            </p>
                            {!announcement.is_read && (
                              <button
                                onClick={() => handleMarkAsRead(announcement.id)}
                                style={{
                                  padding: '0.4rem 0.9rem',
                                  background: 'rgba(247, 201, 72, 0.2)',
                                  border: '1px solid rgba(247, 201, 72, 0.4)',
                                  borderRadius: '8px',
                                  color: '#ffcc00',
                                  fontSize: '0.8rem',
                                  fontWeight: '600',
                                  cursor: 'pointer',
                                  transition: 'all 0.2s ease'
                                }}
                                onMouseEnter={(e) => {
                                  e.target.style.background = 'rgba(247, 201, 72, 0.3)';
                                  e.target.style.transform = 'translateY(-2px)';
                                }}
                                onMouseLeave={(e) => {
                                  e.target.style.background = 'rgba(247, 201, 72, 0.2)';
                                  e.target.style.transform = 'translateY(0)';
                                }}
                              >
                                <CheckCircle size={14} style={{ verticalAlign: 'middle', marginRight: '0.3rem' }} />
                                Mark as Read
                              </button>
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                ) : (
                  <div style={{ 
                    textAlign: 'center', 
                    padding: '2rem',
                    color: 'var(--text-secondary)'
                  }}>
                    <Megaphone size={48} style={{ color: 'var(--border-color)', marginBottom: '1rem' }} />
                    <p>No announcements yet.</p>
                    <p style={{ fontSize: '0.9rem', marginTop: '0.5rem' }}>Your mentor hasn't posted any announcements.</p>
                  </div>
                )}
                
                <div style={{ marginTop: '1.5rem', textAlign: 'center' }}>
                  <Button onClick={() => setShowAnnouncementsModal(false)}>
                    Close
                  </Button>
                </div>
              </div>
            </GlassCard>
          </motion.div>
        </motion.div>
      )}

      {/* Header with Profile */}
      <div className="home-header">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="home-welcome"
        >
          <h1>Welcome back, <span className="home-title-gradient">{user?.first_name || user?.username || 'Student'}!</span></h1>
          <p>Track your progress and stay updated with your learning journey</p>
          {lastUpdated && (
            <p className="last-updated-home">
              <Clock size={14} /> Last updated: {lastUpdated.toLocaleTimeString()}
            </p>
          )}
        </motion.div>

        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          {/* Hackathon Notifications Button */}
          <motion.button
            className="hackathon-notif-btn"
            onClick={() => setShowHackathonModal(true)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              padding: '0.75rem',
              background: 'rgba(255, 193, 7, 0.1)',
              border: '1px solid rgba(255, 193, 7, 0.3)',
              borderRadius: '12px',
              cursor: 'pointer',
              position: 'relative',
              width: '48px',
              height: '48px'
            }}
          >
            <Trophy size={22} style={{ color: '#FFC107' }} />
            {upcomingHackathons.length > 0 && (
              <span style={{
                position: 'absolute',
                top: '-6px',
                right: '-6px',
                background: '#ff4757',
                color: 'white',
                borderRadius: '50%',
                width: '20px',
                height: '20px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '0.7rem',
                fontWeight: 'bold'
              }}>
                {upcomingHackathons.length}
              </span>
            )}
          </motion.button>

          {/* Games Button */}
          <Link to="/games">
            <motion.button
              className="hackathon-notif-btn"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                padding: '0.75rem',
                background: 'rgba(233, 30, 99, 0.1)',
                border: '1px solid rgba(233, 30, 99, 0.3)',
                borderRadius: '12px',
                cursor: 'pointer',
                position: 'relative',
                width: '48px',
                height: '48px'
              }}
            >
              <Gamepad2 size={22} style={{ color: '#E91E63' }} />
            </motion.button>
          </Link>

          {/* Announcements Button */}
          <motion.button
            className="hackathon-notif-btn"
            onClick={() => setShowAnnouncementsModal(true)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              padding: '0.75rem',
              background: 'rgba(247, 201, 72, 0.1)',
              border: '1px solid rgba(247, 201, 72, 0.3)',
              borderRadius: '12px',
              cursor: 'pointer',
              position: 'relative',
              width: '48px',
              height: '48px'
            }}
          >
            <Megaphone size={22} style={{ color: '#ffcc00' }} />
            {unreadCount > 0 && (
              <span style={{
                position: 'absolute',
                top: '-6px',
                right: '-6px',
                background: '#ffcc00',
                color: '#000',
                borderRadius: '50%',
                width: '20px',
                height: '20px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '0.7rem',
                fontWeight: 'bold'
              }}>
                {unreadCount}
              </span>
            )}
          </motion.button>

          {/* Store Button */}
          <motion.button
            className="hackathon-notif-btn"
            onClick={() => {
              setShowStoreModal(true);
              fetchStoreItems();
            }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              padding: '0.75rem',
              background: 'rgba(255, 193, 7, 0.1)',
              border: '1px solid rgba(255, 193, 7, 0.3)',
              borderRadius: '12px',
              cursor: 'pointer',
              position: 'relative',
              width: '48px',
              height: '48px'
            }}
          >
            <ShoppingBag size={22} style={{ color: '#FFC107' }} />
          </motion.button>

          <motion.button
            className="profile-icon-btn"
            onClick={() => setShowProfile(true)}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
          >
            <User size={24} />
          </motion.button>
        </div>
      </div>

      {/* Main Dashboard Content */}
      <div className="home-dashboard">
        {/* Left Column */}
        <div className="home-left-column">
          {/* Overall Progress */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            <GlassCard>
              <div className="overall-progress-card">
                <h2>Overall Progress</h2>
                <div className="progress-circle">
                  <svg viewBox="0 0 100 100">
                    <defs>
                      <linearGradient id="progressGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#ffcc00" />
                        <stop offset="100%" stopColor="#ffcc00" />
                      </linearGradient>
                    </defs>
                    <circle cx="50" cy="50" r="45" className="progress-bg" />
                    <circle
                      cx="50"
                      cy="50"
                      r="45"
                      className="progress-fill"
                      style={{ strokeDashoffset: 283 - (283 * overallProgress) / 100 }}
                    />
                  </svg>
                  <div className="progress-text">{overallProgress}%</div>
                </div>
                <p className="progress-label">Completed</p>
                <Link to="/monthly-report" className="monthly-report-link">
                  <Button variant="secondary" icon={<Calendar size={18} />}>
                    View Monthly Reports
                  </Button>
                </Link>
              </div>
            </GlassCard>
          </motion.div>

          {/* Batch Statistics Card */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <BatchStatsCard />
          </motion.div>

          <GamificationCard />
        </div>

        {/* Right Column */}
        <div className="home-right-column">
          {/* Top 3 Performers Podium */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.8 }}
          >
            <GlassCard>
              <div className="podium-card">
                <h2 style={{ marginBottom: '2.5rem', textAlign: 'center', fontSize: '1.8rem', fontWeight: '700' }}>
                  🏆 Season Champions
                </h2>
                
                {!seasonActive || leaderboard.length === 0 ? (
                  <div className="podium-locked">
                    <Trophy size={80} style={{ opacity: 0.2, marginBottom: '1rem' }} />
                    <p style={{ opacity: 0.5, textAlign: 'center', fontSize: '1.1rem' }}>Complete the season to unlock the podium</p>
                  </div>
                ) : (
                  <div className="podium-container">
                    {/* Rank 2 - Left */}
                    {leaderboard[1] && (
                      <motion.div
                        className="podium-position rank-2"
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.5, duration: 0.6 }}
                        whileHover={{ scale: 1.05, y: -5 }}
                      >
                        <div className="podium-rank">2</div>
                        <div className="podium-content">
                          <div className="podium-avatar">
                            <User size={42} />
                          </div>
                          <h3>{leaderboard[1].student_name}</h3>
                          <p className="podium-title">Elite Performer</p>
                          <div className="podium-score">
                            <span className="score-value">{leaderboard[1].total_score}</span>
                            <span className="score-label">pts</span>
                          </div>
                        </div>
                        <div className="podium-base rank-2-base"></div>
                      </motion.div>
                    )}

                    {/* Rank 1 - Center (Champion) */}
                    {leaderboard[0] && (
                      <motion.div
                        className="podium-position rank-1"
                        initial={{ opacity: 0, y: 40 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.7, duration: 0.7 }}
                        whileHover={{ scale: 1.08, y: -8 }}
                      >
                        <div className="podium-crown">👑</div>
                        <div className="podium-rank champion">1</div>
                        <div className="podium-content">
                          <div className="podium-avatar champion-avatar">
                            <User size={52} />
                          </div>
                          <h3>{leaderboard[0].student_name}</h3>
                          <p className="podium-title champion-title">Champion</p>
                          <div className="podium-score champion-score">
                            <span className="score-value">{leaderboard[0].total_score}</span>
                            <span className="score-label">pts</span>
                          </div>
                        </div>
                        <div className="podium-base rank-1-base"></div>
                      </motion.div>
                    )}

                    {/* Rank 3 - Right */}
                    {leaderboard[2] && (
                      <motion.div
                        className="podium-position rank-3"
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.6, duration: 0.6 }}
                        whileHover={{ scale: 1.05, y: -5 }}
                      >
                        <div className="podium-rank">3</div>
                        <div className="podium-content">
                          <div className="podium-avatar">
                            <User size={42} />
                          </div>
                          <h3>{leaderboard[2].student_name}</h3>
                          <p className="podium-title">Elite Performer</p>
                          <div className="podium-score">
                            <span className="score-value">{leaderboard[2].total_score}</span>
                            <span className="score-label">pts</span>
                          </div>
                        </div>
                        <div className="podium-base rank-3-base"></div>
                      </motion.div>
                    )}
                  </div>
                )}
              </div>
            </GlassCard>
          </motion.div>

          {/* Mentor Notifications */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
          >
            <GlassCard>
              <div className="notifications-card">
                <h2><Bell size={20} /> Notifications</h2>
                <div className="notifications-list">
                  {/* Regular Notifications */}
                  {notifications.length > 0 ? (
                    notifications.map((notif) => (
                      <div key={notif.id} className={`notification-item ${notif.read ? 'read' : 'unread'}`}>
                        <div className="notification-dot" />
                        <div className="notification-content">
                          <p>{notif.message}</p>
                          <span><Clock size={14} /> {notif.time}</span>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
                      <Bell size={32} style={{ marginBottom: '0.5rem', opacity: 0.5 }} />
                      <p>No new notifications</p>
                    </div>
                  )}
                </div>
              </div>
            </GlassCard>
          </motion.div>

          {/* Recent Activities */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
          >
            <GlassCard>
              <div className="activities-card">
                <h2>Recent Activities</h2>
                <div className="activities-list">
                  {recentActivities.length > 0 ? (
                    recentActivities.map((activity) => (
                      <div key={activity.id} className="activity-item">
                        <div className="activity-status">
                          {getStatusIcon(activity.status)}
                        </div>
                        <div className="activity-content">
                          <h4>{activity.title}</h4>
                          <div className="activity-meta">
                            <span className={`status-badge ${activity.status}`}>
                              {activity.status}
                            </span>
                            <span className="activity-date">
                              <Clock size={14} /> {formatDate(activity.date)}
                            </span>
                          </div>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
                      <AlertCircle size={32} style={{ marginBottom: '0.5rem', opacity: 0.5 }} />
                      <p>No recent activities</p>
                    </div>
                  )}
                </div>
              </div>
            </GlassCard>
          </motion.div>
        </div>
      </div>

      {/* Store Modal */}
      {showStoreModal && (
        <motion.div
          className="profile-modal-overlay"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          onClick={() => setShowStoreModal(false)}
        >
          <motion.div
            className="profile-modal"
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            onClick={(e) => e.stopPropagation()}
            style={{ maxWidth: '800px', width: '90%' }}
          >
            <GlassCard>
              <div style={{ padding: '2rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '2rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <ShoppingBag size={32} style={{ color: '#FFC107' }} />
                    <h2 style={{ margin: 0, fontSize: '1.75rem', fontWeight: '700' }}>Vault Store</h2>
                  </div>
                  <div style={{
                    padding: '0.75rem 1.25rem',
                    background: 'rgba(255, 193, 7, 0.2)',
                    border: '1px solid rgba(255, 193, 7, 0.3)',
                    borderRadius: '12px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem'
                  }}>
                    <span style={{ fontSize: '1.1rem', fontWeight: '700', color: '#FFC107' }}>
                      {userCredits} Credits
                    </span>
                  </div>
                </div>

                {loadingStore ? (
                  <div style={{ display: 'flex', justifyContent: 'center', padding: '3rem' }}>
                    <Loader2 size={48} className="spinner" />
                  </div>
                ) : (
                  <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))',
                    gap: '1.5rem',
                    maxHeight: '500px',
                    overflowY: 'auto',
                    padding: '0.5rem'
                  }}>
                    {storeItems.length > 0 ? (
                      storeItems.map((item) => (
                        <div key={item.id} style={{
                          padding: '1.5rem',
                          background: 'rgba(255, 255, 255, 0.03)',
                          border: `2px solid ${
                            item.rarity === 'legendary' ? 'rgba(255, 215, 0, 0.5)' :
                            item.rarity === 'epic' ? 'rgba(147, 51, 234, 0.5)' :
                            item.rarity === 'rare' ? 'rgba(59, 130, 246, 0.5)' :
                            'rgba(255, 255, 255, 0.1)'
                          }`,
                          borderRadius: '12px',
                          transition: 'all 0.3s ease',
                          position: 'relative',
                          overflow: 'hidden'
                        }}>
                          {item.rarity && (
                            <div style={{
                              position: 'absolute',
                              top: '0.75rem',
                              right: '0.75rem',
                              padding: '0.25rem 0.6rem',
                              background: 
                                item.rarity === 'legendary' ? 'rgba(255, 215, 0, 0.2)' :
                                item.rarity === 'epic' ? 'rgba(147, 51, 234, 0.2)' :
                                item.rarity === 'rare' ? 'rgba(59, 130, 246, 0.2)' :
                                'rgba(255, 255, 255, 0.1)',
                              borderRadius: '8px',
                              fontSize: '0.7rem',
                              fontWeight: '700',
                              textTransform: 'uppercase',
                              color: 
                                item.rarity === 'legendary' ? '#FFD700' :
                                item.rarity === 'epic' ? '#9333ea' :
                                item.rarity === 'rare' ? '#3b82f6' :
                                '#fff'
                            }}>
                              {item.rarity}
                            </div>
                          )}
                          
                          <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1.1rem', color: 'var(--text-primary)', paddingRight: '60px' }}>
                            {item.name}
                          </h3>
                          <p style={{ margin: '0 0 1rem 0', fontSize: '0.85rem', opacity: 0.7, lineHeight: '1.4' }}>
                            {item.description}
                          </p>
                          
                          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: '1rem' }}>
                            <span style={{
                              padding: '0.4rem 0.8rem',
                              background: 'rgba(255, 193, 7, 0.2)',
                              border: '1px solid rgba(255, 193, 7, 0.3)',
                              borderRadius: '8px',
                              fontSize: '0.9rem',
                              fontWeight: '700',
                              color: '#FFC107'
                            }}>
                              {item.cost} Credits
                            </span>
                            
                            {item.is_owned ? (
                              item.is_equipped ? (
                                <span style={{
                                  padding: '0.5rem 1rem',
                                  background: 'rgba(76, 175, 80, 0.2)',
                                  border: '1px solid rgba(76, 175, 80, 0.3)',
                                  borderRadius: '8px',
                                  fontSize: '0.85rem',
                                  fontWeight: '600',
                                  color: '#4caf50'
                                }}>
                                  ✓ Equipped
                                </span>
                              ) : (
                                <button
                                  onClick={() => handleEquipTitle(item.id)}
                                  style={{
                                    padding: '0.5rem 1rem',
                                    background: 'rgba(59, 130, 246, 0.2)',
                                    border: '1px solid rgba(59, 130, 246, 0.3)',
                                    borderRadius: '8px',
                                    fontSize: '0.85rem',
                                    fontWeight: '600',
                                    color: '#3b82f6',
                                    cursor: 'pointer',
                                    transition: 'all 0.3s ease'
                                  }}
                                  onMouseOver={(e) => {
                                    e.currentTarget.style.background = 'rgba(59, 130, 246, 0.3)';
                                    e.currentTarget.style.transform = 'scale(1.05)';
                                  }}
                                  onMouseOut={(e) => {
                                    e.currentTarget.style.background = 'rgba(59, 130, 246, 0.2)';
                                    e.currentTarget.style.transform = 'scale(1)';
                                  }}
                                >
                                  Equip
                                </button>
                              )
                            ) : (
                              <button
                                onClick={() => handleRedeemTitle(item.id, item.cost)}
                                disabled={userCredits < item.cost}
                                style={{
                                  padding: '0.5rem 1rem',
                                  background: userCredits >= item.cost ? 'rgba(255, 193, 7, 0.2)' : 'rgba(255, 255, 255, 0.05)',
                                  border: `1px solid ${userCredits >= item.cost ? 'rgba(255, 193, 7, 0.3)' : 'rgba(255, 255, 255, 0.1)'}`,
                                  borderRadius: '8px',
                                  fontSize: '0.85rem',
                                  fontWeight: '600',
                                  color: userCredits >= item.cost ? '#FFC107' : 'rgba(255, 255, 255, 0.3)',
                                  cursor: userCredits >= item.cost ? 'pointer' : 'not-allowed',
                                  transition: 'all 0.3s ease',
                                  opacity: userCredits >= item.cost ? 1 : 0.5
                                }}
                                onMouseOver={(e) => {
                                  if (userCredits >= item.cost) {
                                    e.currentTarget.style.background = 'rgba(255, 193, 7, 0.3)';
                                    e.currentTarget.style.transform = 'scale(1.05)';
                                  }
                                }}
                                onMouseOut={(e) => {
                                  if (userCredits >= item.cost) {
                                    e.currentTarget.style.background = 'rgba(255, 193, 7, 0.2)';
                                    e.currentTarget.style.transform = 'scale(1)';
                                  }
                                }}
                              >
                                Redeem
                              </button>
                            )}
                          </div>
                        </div>
                      ))
                    ) : (
                      <div style={{ textAlign: 'center', padding: '3rem', gridColumn: '1 / -1' }}>
                        <ShoppingBag size={48} style={{ opacity: 0.3, marginBottom: '1rem' }} />
                        <p style={{ opacity: 0.6 }}>No items available in store</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </GlassCard>
          </motion.div>
        </motion.div>
      )}

      {/* Footer */}
      <footer className="home-footer">
        <div className="footer-content">
          <div className="footer-section">
            <h3>Cohort Web</h3>
            <p>© 2025 All rights reserved</p>
          </div>
          <div className="footer-section">
            <h3>Contact</h3>
            <p>Email: support@cohortweb.edu</p>
            <p>Phone: +91 1234567890</p>
          </div>
          <div className="footer-section">
            <h3>Quick Links</h3>
            <div className="footer-links">
              <Link to="/clt">CLT</Link>
              <Link to="/sri">SRI</Link>
              <Link to="/cfc">CFC</Link>
              <Link to="/iipc">IIPC</Link>
              <Link to="/scd">SCD</Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
