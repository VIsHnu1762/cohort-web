import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Calendar, MapPin, ExternalLink, Loader2, Globe, Building2, Zap, Trophy, Sparkles } from 'lucide-react';
import GlassCard from '../../components/GlassCard';
import Button from '../../components/Button';
import hackathonService from '../../services/hackathons';
import './Hackathons.css';

export const Hackathons = () => {
  const [hackathons, setHackathons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState('all'); // all, online, in-person
  const [currentMessage, setCurrentMessage] = useState(0);

  const notificationMessages = [
    { text: "🚀 Apply now and showcase your skills!", icon: Zap },
    { text: "🏆 Don't miss out on amazing prizes!", icon: Trophy },
    { text: "✨ Build something awesome this weekend!", icon: Sparkles },
    { text: "💡 Network with top developers worldwide!", icon: Globe },
    { text: "⚡ Limited spots available - Register today!", icon: Zap },
  ];

  useEffect(() => {
    document.title = 'Hackathons & Competitions | Cohort Web';
    loadHackathons();
    
    // Rotate notification messages every 5 seconds
    const interval = setInterval(() => {
      setCurrentMessage((prev) => (prev + 1) % notificationMessages.length);
    }, 5000);
    
    return () => clearInterval(interval);
  }, []);

  const loadHackathons = async () => {
    try {
      setLoading(true);
      const data = await hackathonService.getHackathons();
      setHackathons(data.hackathons || []);
      setError('');
    } catch (err) {
      console.error('Error loading hackathons:', err);
      setError('Failed to load hackathons. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const filteredHackathons = hackathons.filter(hack => {
    if (filter === 'all') return true;
    if (filter === 'online') return hack.is_online;
    if (filter === 'in-person') return !hack.is_online;
    return true;
  });

  if (loading) {
    return (
      <div className="hackathons-container">
        <div className="hackathons-loading">
          <Loader2 className="hackathons-spinner" size={48} />
          <p>Loading hackathons...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="hackathons-container">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="hackathons-header"
      >
        <h1 className="hackathons-title">Hackathons & Competitions</h1>
        <p className="hackathons-subtitle">
          Discover and participate in amazing hackathons from around the world
        </p>
      </motion.div>

      {/* Fun Notification Banner */}
      {hackathons.length > 0 && (
        <motion.div
          key={currentMessage}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: 20 }}
          transition={{ duration: 0.5 }}
          className="hackathons-notification"
        >
          <div className="notification-content">
            <span className="notification-icon">
              {notificationMessages[currentMessage].text.split(' ')[0]}
            </span>
            <span className="notification-text">
              {notificationMessages[currentMessage].text.substring(notificationMessages[currentMessage].text.indexOf(' ') + 1)}
            </span>
          </div>
        </motion.div>
      )}

      {/* Filters */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="hackathons-filters"
      >
        <button
          className={`hackathons-filter-btn ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          All Hackathons
        </button>
        <button
          className={`hackathons-filter-btn ${filter === 'online' ? 'active' : ''}`}
          onClick={() => setFilter('online')}
        >
          <Globe size={18} />
          Online
        </button>
        <button
          className={`hackathons-filter-btn ${filter === 'in-person' ? 'active' : ''}`}
          onClick={() => setFilter('in-person')}
        >
          <Building2 size={18} />
          In-Person
        </button>
      </motion.div>

      {/* Error Message */}
      {error && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="hackathons-error"
        >
          {error}
        </motion.div>
      )}

      {/* Hackathons Grid */}
      <div className="hackathons-grid">
        {filteredHackathons.map((hackathon, index) => (
          <motion.div
            key={hackathon.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <GlassCard className="hackathon-card">
              {/* Logo/Image */}
              {hackathon.logo && (
                <div className="hackathon-logo-container">
                  <img 
                    src={hackathon.logo} 
                    alt={hackathon.name}
                    className="hackathon-logo"
                    onError={(e) => {
                      e.target.style.display = 'none';
                    }}
                  />
                </div>
              )}

              {/* Content */}
              <div className="hackathon-content">
                <h3 className="hackathon-name">{hackathon.name}</h3>
                
                {hackathon.description && (
                  <p className="hackathon-description">{hackathon.description}</p>
                )}

                <div className="hackathon-details">
                  <div className="hackathon-detail-item">
                    <Calendar size={16} />
                    <span>{hackathon.start_date}</span>
                  </div>
                  <div className="hackathon-detail-item">
                    <MapPin size={16} />
                    <span>{hackathon.location}</span>
                    {hackathon.is_online && (
                      <span className="hackathon-badge">Online</span>
                    )}
                  </div>
                </div>

                {/* Register Button */}
                <Button
                  variant="primary"
                  className="hackathon-register-btn"
                  onClick={() => window.open(hackathon.url, '_blank')}
                  icon={<ExternalLink size={18} />}
                >
                  Register Now
                </Button>
              </div>
            </GlassCard>
          </motion.div>
        ))}
      </div>

      {/* Empty State */}
      {filteredHackathons.length === 0 && !loading && !error && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="hackathons-empty"
        >
          <p>No hackathons found for the selected filter.</p>
        </motion.div>
      )}
    </div>
  );
};

export default Hackathons;
