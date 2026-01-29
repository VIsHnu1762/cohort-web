import React, { useState } from 'react';
import { X, Calendar, Link as LinkIcon, Save } from 'lucide-react';
import Input from './Input';
import Button from './Button';
import './HackathonRegistrationModal.css';

const HackathonRegistrationModal = ({ isOpen, onClose, onRegister }) => {
  const [formData, setFormData] = useState({
    hackathon_name: '',
    mode: 'online',
    registration_date: '',
    participation_date: '',
    hackathon_url: '',
    notes: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onRegister(formData);
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  if (!isOpen) return null;

  return (
    <div className="hackathon-modal-overlay" onClick={onClose}>
      <div className="hackathon-modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="hackathon-modal-header">
          <h2>Register for Hackathon</h2>
          <button className="hackathon-modal-close" onClick={onClose}>
            <X size={24} />
          </button>
        </div>

        <div className="hackathon-modal-body">
          <p className="hackathon-modal-description">
            Save the hackathon you're planning to participate in. We'll remind you and track your progress!
          </p>

          <form onSubmit={handleSubmit}>
            <Input
              label="Hackathon Name"
              placeholder="e.g., Smart India Hackathon 2025"
              value={formData.hackathon_name}
              onChange={(e) => handleChange('hackathon_name', e.target.value)}
              required
              floatingLabel
            />

            <div className="hackathon-input-group">
              <label className="hackathon-label">Mode of Participation</label>
              <div className="hackathon-radio-group">
                <label className="hackathon-radio-label">
                  <input
                    type="radio"
                    name="mode"
                    value="online"
                    checked={formData.mode === 'online'}
                    onChange={(e) => handleChange('mode', e.target.value)}
                  />
                  <span>Online</span>
                </label>
                <label className="hackathon-radio-label">
                  <input
                    type="radio"
                    name="mode"
                    value="offline"
                    checked={formData.mode === 'offline'}
                    onChange={(e) => handleChange('mode', e.target.value)}
                  />
                  <span>Offline</span>
                </label>
                <label className="hackathon-radio-label">
                  <input
                    type="radio"
                    name="mode"
                    value="hybrid"
                    checked={formData.mode === 'hybrid'}
                    onChange={(e) => handleChange('mode', e.target.value)}
                  />
                  <span>Hybrid</span>
                </label>
              </div>
            </div>

            <Input
              label="Registration Date"
              type="date"
              value={formData.registration_date}
              onChange={(e) => handleChange('registration_date', e.target.value)}
              required
              floatingLabel
              icon={<Calendar size={20} />}
            />

            <Input
              label="Participation Date"
              type="date"
              value={formData.participation_date}
              onChange={(e) => handleChange('participation_date', e.target.value)}
              required
              floatingLabel
              icon={<Calendar size={20} />}
            />

            <Input
              label="Hackathon URL (Optional)"
              placeholder="https://hackathon-website.com"
              value={formData.hackathon_url}
              onChange={(e) => handleChange('hackathon_url', e.target.value)}
              floatingLabel
              icon={<LinkIcon size={20} />}
            />

            <div className="hackathon-textarea-group">
              <label className="hackathon-label">Notes (Optional)</label>
              <textarea
                placeholder="Add any notes or preparation goals..."
                value={formData.notes}
                onChange={(e) => handleChange('notes', e.target.value)}
                rows={3}
                className="hackathon-textarea"
              />
            </div>

            <div className="hackathon-modal-actions">
              <Button variant="secondary" onClick={onClose} type="button">
                Cancel
              </Button>
              <Button variant="primary" type="submit">
                <Save size={20} />
                Register Hackathon
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default HackathonRegistrationModal;
