import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { User, Code, Github, Linkedin, Save, Loader2 } from 'lucide-react';
import GlassCard from '../../components/GlassCard';
import Button from '../../components/Button';
import Input from '../../components/Input';
import { getUserProfile, updateUserProfile } from '../../services/profile';
import { useAuth } from '../../context/AuthContext';
import authService from '../../services/auth';
import './ProfileSettings.css';

export const ProfileSettings = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  const [profileData, setProfileData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    leetcode_id: '',
    github_id: '',
    linkedin_id: '',
  });

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      setLoading(true);
      const data = await getUserProfile();
      setProfileData({
        username: data.username || '',
        email: data.email || '',
        first_name: data.first_name || '',
        last_name: data.last_name || '',
        leetcode_id: data.leetcode_id || '',
        github_id: data.github_id || '',
        linkedin_id: data.linkedin_id || '',
      });
      setError('');
    } catch (err) {
      console.error('Error loading profile:', err);
      console.error('Error details:', err.response);
      const errorMsg = err.response?.status === 401 
        ? 'Please login again to access profile settings.'
        : err.response?.status === 403
        ? 'Access denied. You do not have permission to view this profile.'
        : err.response?.data?.detail || err.response?.data?.message || 'Failed to load profile. Please try again.';
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError('');
    setSuccess('');

    try {
      const updateData = {
        first_name: profileData.first_name || '',
        last_name: profileData.last_name || '',
        leetcode_id: profileData.leetcode_id || null,
        github_id: profileData.github_id || null,
        linkedin_id: profileData.linkedin_id || null,
      };

      await updateUserProfile(updateData);
      
      // Update user data in localStorage to reflect changes
      const updatedUser = {
        ...user,
        first_name: profileData.first_name,
        last_name: profileData.last_name,
      };
      localStorage.setItem('user', JSON.stringify(updatedUser));
      
      // Force a page reload to update the auth context
      window.location.reload();
      
      setSuccess('Profile updated successfully!');
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      console.error('Error updating profile:', err);
      setError(err.response?.data?.message || 'Failed to update profile. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="profile-settings">
        <div className="profile-settings-loading">
          <Loader2 className="profile-settings-spinner" />
          <p>Loading profile...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="profile-settings">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="profile-settings-title">Profile Settings</h1>
        <p className="profile-settings-subtitle">
          Manage your account information and platform IDs
        </p>

        <GlassCard className="profile-settings-card">
          <form onSubmit={handleSubmit}>
            {/* User Information */}
            <div className="profile-settings-section">
              <div className="profile-settings-section-header">
                <User size={20} />
                <h2>Account Information</h2>
              </div>
              
              <div className="profile-settings-info-grid">
                <div className="profile-settings-info-item">
                  <label>Username</label>
                  <p>{profileData.username}</p>
                </div>
                <div className="profile-settings-info-item">
                  <label>Email</label>
                  <p>{profileData.email}</p>
                </div>
              </div>

              <Input
                label="First Name"
                placeholder="Enter your first name"
                value={profileData.first_name}
                onChange={(e) => setProfileData({ ...profileData, first_name: e.target.value })}
                icon={<User size={20} />}
                floatingLabel
              />

              <Input
                label="Last Name"
                placeholder="Enter your last name"
                value={profileData.last_name}
                onChange={(e) => setProfileData({ ...profileData, last_name: e.target.value })}
                icon={<User size={20} />}
                floatingLabel
              />
            </div>

            {/* Platform IDs (Editable) */}
            <div className="profile-settings-section">
              <div className="profile-settings-section-header">
                <Code size={20} />
                <h2>Platform IDs</h2>
              </div>
              <p className="profile-settings-section-description">
                Link your coding platform accounts for automatic data syncing
              </p>

              <Input
                label="LeetCode Username"
                placeholder="Enter your LeetCode username"
                value={profileData.leetcode_id}
                onChange={(e) => setProfileData({ ...profileData, leetcode_id: e.target.value })}
                icon={<Code size={20} />}
                floatingLabel
              />

              <Input
                label="GitHub Username"
                placeholder="Enter your GitHub username"
                value={profileData.github_id}
                onChange={(e) => setProfileData({ ...profileData, github_id: e.target.value })}
                icon={<Github size={20} />}
                floatingLabel
              />

              <Input
                label="LinkedIn Profile URL or ID"
                placeholder="Enter your LinkedIn profile URL"
                value={profileData.linkedin_id}
                onChange={(e) => setProfileData({ ...profileData, linkedin_id: e.target.value })}
                icon={<Linkedin size={20} />}
                floatingLabel
              />
            </div>

            {/* Messages */}
            {error && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="profile-settings-error"
              >
                {error}
              </motion.div>
            )}

            {success && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="profile-settings-success"
              >
                {success}
              </motion.div>
            )}

            {/* Submit Button */}
            <div className="profile-settings-actions">
              <Button
                type="submit"
                variant="primary"
                disabled={saving}
                icon={saving ? <Loader2 className="profile-settings-button-spinner" /> : <Save size={20} />}
              >
                {saving ? 'Saving...' : 'Save Changes'}
              </Button>
            </div>
          </form>
        </GlassCard>
      </motion.div>
    </div>
  );
};

export default ProfileSettings;
