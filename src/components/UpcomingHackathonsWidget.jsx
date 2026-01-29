import React, { useEffect, useState } from 'react';
import { Trophy, Calendar, Clock, ExternalLink, CheckCircle, AlertCircle, Zap } from 'lucide-react';
import { Link } from 'react-router-dom';
import { getUpcomingHackathons } from '../services/cfc';
import './UpcomingHackathonsWidget.css';

const UpcomingHackathonsWidget = () => {
  const [hackathons, setHackathons] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUpcomingHackathons();
  }, []);

  const fetchUpcomingHackathons = async () => {
    try {
      const data = await getUpcomingHackathons();
      setHackathons(data);
    } catch (error) {
      console.error('Failed to fetch upcoming hackathons:', error);
    } finally {
      setLoading(false);
    }
  };

  const getMotivationalMessage = (daysLeft) => {
    if (daysLeft === 0) {
      return { text: "It's TODAY! Give it your best shot! 🚀", icon: Zap, className: 'urgent' };
    } else if (daysLeft === 1) {
      return { text: "Tomorrow's the day! Get ready! 🔥", icon: AlertCircle, className: 'urgent' };
    } else if (daysLeft <= 3) {
      return { text: "Just a few days left! Time to shine! ✨", icon: Clock, className: 'soon' };
    } else if (daysLeft <= 7) {
      return { text: "One week to go! Keep preparing! 💪", icon: Calendar, className: 'upcoming' };
    } else {
      return { text: "Start preparing now! You got this! 🎯", icon: Trophy, className: 'planned' };
    }
  };

  if (loading) {
    return null; // Don't show while loading
  }

  if (hackathons.length === 0) {
    return null; // Don't show if no upcoming hackathons
  }

  return (
    <div className="upcoming-hackathons-widget">
      <div className="widget-header">
        <Trophy className="widget-icon" />
        <h3>Upcoming Hackathons</h3>
      </div>

      <div className="hackathons-list">
        {hackathons.slice(0, 3).map((hackathon) => {
          const motivation = getMotivationalMessage(hackathon.days_until_event);
          const MotivationIcon = motivation.icon;

          return (
            <div key={hackathon.id} className={`hackathon-card ${motivation.className}`}>
              <div className="hackathon-card-header">
                <h4 className="hackathon-name">{hackathon.hackathon_name}</h4>
                <span className="hackathon-mode">{hackathon.mode}</span>
              </div>

              <div className="hackathon-date">
                <Calendar size={16} />
                <span>{new Date(hackathon.participation_date).toLocaleDateString('en-US', { 
                  weekday: 'short', 
                  year: 'numeric', 
                  month: 'short', 
                  day: 'numeric' 
                })}</span>
              </div>

              <div className={`hackathon-countdown ${motivation.className}`}>
                <MotivationIcon size={18} />
                <span className="countdown-text">
                  {hackathon.days_until_event === 0 ? 'Today!' : 
                   hackathon.days_until_event === 1 ? 'Tomorrow' : 
                   `${hackathon.days_until_event} days left`}
                </span>
              </div>

              <div className="hackathon-motivation">
                <p>{motivation.text}</p>
              </div>

              {hackathon.notes && (
                <div className="hackathon-notes">
                  <p>{hackathon.notes}</p>
                </div>
              )}

              {hackathon.hackathon_url && (
                <a 
                  href={hackathon.hackathon_url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="hackathon-link"
                >
                  Visit Website <ExternalLink size={14} />
                </a>
              )}
            </div>
          );
        })}
      </div>

      {hackathons.length > 3 && (
        <Link to="/cfc" className="view-all-link">
          View all {hackathons.length} registered hackathons →
        </Link>
      )}
    </div>
  );
};

export default UpcomingHackathonsWidget;
