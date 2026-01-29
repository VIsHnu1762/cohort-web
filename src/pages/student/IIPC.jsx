import React, { useState, useEffect } from 'react';
// eslint-disable-next-line no-unused-vars
import { motion, AnimatePresence } from 'framer-motion';
import { Linkedin, Upload, Search, CheckCircle, TrendingUp, Hash, Calendar, Users, XCircle } from 'lucide-react';
import { useLocation } from 'react-router-dom';
import GlassCard from '../../components/GlassCard';
import Button from '../../components/Button';
import Input from '../../components/Input';
import { 
  connectLinkedInProfile, 
  getLinkedInAuthUrl,
  createLinkedInPost,
  createLinkedInConnection,
  submitPostForReview,
  submitConnectionForReview
} from '../../services/iipc';
import './IIPC.css';

export const IIPC = () => {
  const location = useLocation();
  const [activeSection, setActiveSection] = useState('post');

  // Post Verification State
  const [postUrl, setPostUrl] = useState('');
  const [postDate, setPostDate] = useState('');
  const [characterCount, setCharacterCount] = useState('');
  const [hashtagCount, setHashtagCount] = useState('');
  const [isVerifying, setIsVerifying] = useState(false);
  const [postData, setPostData] = useState(null);
  const [postError, setPostError] = useState('');
  const [postSuccess, setPostSuccess] = useState('');

  // Connections Verification State
  const [verificationMethod, setVerificationMethod] = useState('screenshot'); // 'screenshot' or 'profile'
  const [screenshotLinks, setScreenshotLinks] = useState(['']);
  const [profileUrl, setProfileUrl] = useState('');
  const [totalConnections, setTotalConnections] = useState('');
  const [connectionsData, setConnectionsData] = useState(null);
  const [isConnectingProfile, setIsConnectingProfile] = useState(false);
  const [profileError, setProfileError] = useState('');
  const [profileSuccess, setProfileSuccess] = useState('');

  // Check for LinkedIn profile data from OAuth callback
  useEffect(() => {
    // Check location state first (from redirect)
    if (location.state?.linkedInProfile) {
      const profile = location.state.linkedInProfile;
      setProfileUrl(profile.profile_url || '');
      setProfileSuccess(`Welcome ${profile.full_name}! Your LinkedIn profile has been verified.`);
      setVerificationMethod('profile');
      setActiveSection('connections');
    } 
    // Check sessionStorage (in case of page reload)
    else {
      const storedProfile = sessionStorage.getItem('linkedin_profile');
      if (storedProfile) {
        const profile = JSON.parse(storedProfile);
        setProfileUrl(profile.profile_url || '');
        setProfileSuccess(`Welcome ${profile.full_name}! Your LinkedIn profile has been verified.`);
        setVerificationMethod('profile');
        setActiveSection('connections');
        // Clear from session storage after use
        sessionStorage.removeItem('linkedin_profile');
      }
    }
  }, [location]);

  const handleVerifyPost = async () => {
    setPostError('');
    setPostSuccess('');
    
    // Check authentication
    const token = localStorage.getItem('accessToken');
    if (!token) {
      setPostError('Please login to continue');
      return;
    }
    
    // Validate required fields
    if (!postUrl.trim()) {
      setPostError('Please enter LinkedIn post URL');
      return;
    }
    if (!postDate) {
      setPostError('Please select post date');
      return;
    }
    if (!characterCount || characterCount <= 0) {
      setPostError('Character count must be greater than 0');
      return;
    }
    
    setIsVerifying(true);
    
    try {
      const postPayload = {
        post_url: postUrl,
        post_date: postDate,
        character_count: parseInt(characterCount),
        hashtag_count: parseInt(hashtagCount) || 0
      };
      
      const response = await createLinkedInPost(postPayload);
      console.log('Post created successfully, response:', response);
      
      if (!response.id) {
        console.error('Warning: Response missing ID field', response);
      }
      
      setPostData(response);
      setPostSuccess('Post details saved successfully! Click Submit to send for mentor review.');
    } catch (error) {
      console.error('Post verification error:', error);
      console.error('Error details:', error.response?.data);
      
      // Handle authentication errors
      if (error.response?.status === 401) {
        setPostError('Session expired. Please login again.');
        setTimeout(() => {
          window.location.href = '/login';
        }, 2000);
        return;
      }
      
      // Extract detailed error message
      let errorMessage = 'Failed to create post verification';
      
      if (error.response?.data) {
        const errorData = error.response.data;
        
        // Handle different error formats
        if (errorData.error) {
          errorMessage = errorData.error;
        } else if (errorData.detail) {
          errorMessage = errorData.detail;
        } else if (typeof errorData === 'object') {
          // Handle field-specific errors
          const fieldErrors = [];
          for (const [field, messages] of Object.entries(errorData)) {
            if (Array.isArray(messages)) {
              fieldErrors.push(`${field}: ${messages.join(', ')}`);
            } else {
              fieldErrors.push(`${field}: ${messages}`);
            }
          }
          if (fieldErrors.length > 0) {
            errorMessage = fieldErrors.join('; ');
          }
        }
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      setPostError(errorMessage);
    } finally {
      setIsVerifying(false);
    }
  };
  
  const handleSubmitPost = async () => {
    console.log('Submit button clicked, postData:', postData);
    
    if (!postData) {
      setPostError('Please save post details first');
      return;
    }
    
    if (!postData.id) {
      setPostError('Post ID missing. Please save your post details again.');
      return;
    }
    
    setIsVerifying(true);
    setPostError('');
    setPostSuccess('');
    
    try {
      console.log('Submitting post with ID:', postData.id);
      const response = await submitPostForReview(postData.id);
      console.log('Submit response:', response);
      setPostSuccess('Post submitted successfully! Your mentor will review it shortly.');
      setPostData({ ...postData, status: 'pending' });
    } catch (error) {
      console.error('Submit post error:', error);
      console.error('Error response:', error.response);
      
      // Handle authentication errors
      if (error.response?.status === 401) {
        setPostError('Session expired. Please logout and login again.');
        return;
      }
      
      const errorMessage = error.response?.data?.error || error.response?.data?.detail || 'Failed to submit post for review';
      setPostError(errorMessage);
    } finally {
      setIsVerifying(false);
    }
  };

  const addScreenshotLink = () => {
    setScreenshotLinks([...screenshotLinks, '']);
  };

  const removeScreenshotLink = (index) => {
    const newLinks = screenshotLinks.filter((_, i) => i !== index);
    setScreenshotLinks(newLinks.length > 0 ? newLinks : ['']);
  };

  const updateScreenshotLink = (index, value) => {
    const newLinks = [...screenshotLinks];
    newLinks[index] = value;
    setScreenshotLinks(newLinks);
  };

  const handleLinkedInOAuth = async () => {
    try {
      const response = await getLinkedInAuthUrl();
      // Redirect to LinkedIn authorization
      window.location.href = response.authorization_url;
    } catch (error) {
      console.error('LinkedIn OAuth error:', error);
      setProfileError('Failed to initiate LinkedIn connection');
    }
  };

  const handleConnectProfile = async () => {
    // Reset messages
    setProfileError('');
    setProfileSuccess('');
    
    // Validate inputs
    if (!profileUrl.trim()) {
      setProfileError('Please enter your LinkedIn profile URL');
      return;
    }
    
    setIsConnectingProfile(true);
    
    try {
      const response = await connectLinkedInProfile(profileUrl, 0); // Total connections not required
      console.log('Profile connected successfully, response:', response);
      setProfileSuccess('Profile details saved successfully! Click Submit to send for mentor review.');
      
      // Set connections data for display - use consistent field names
      setConnectionsData({
        ...response.verification,
        verificationId: response.verification.id,
      });
    } catch (error) {
      console.error('Profile connection error:', error);
      const errorMessage = error.response?.data?.error || 'Failed to connect profile. Please try again.';
      setProfileError(errorMessage);
    } finally {
      setIsConnectingProfile(false);
    }
  };

  const handleVerifyConnections = async () => {
    setProfileError('');
    setProfileSuccess('');
    
    // Validate screenshot links
    const validLinks = screenshotLinks.filter(link => link.trim() !== '');
    if (validLinks.length === 0) {
      setProfileError('Please provide at least one Google Drive screenshot link');
      return;
    }
    
    setIsConnectingProfile(true);
    
    try {
      const connectionPayload = {
        verification_method: 'screenshot',
        total_connections: 0, // Not required anymore
        screenshot_urls: validLinks,
        verified_connections: [] // Can add verified connections later
      };
      
      const response = await createLinkedInConnection(connectionPayload);
      console.log('Connection created successfully, response:', response);
      
      if (!response.id) {
        console.error('Warning: Response missing ID field', response);
      }
      
      setConnectionsData({
        ...response,
        verificationId: response.id
      });
      setProfileSuccess('Connection details saved successfully! Click Submit to send for mentor review.');
    } catch (error) {
      console.error('Connection verification error:', error);
      const errorMessage = error.response?.data?.error || 'Failed to create connection verification';
      setProfileError(errorMessage);
    } finally {
      setIsConnectingProfile(false);
    }
  };
  
  const handleSubmitConnection = async () => {
    console.log('Submit connection button clicked, connectionsData:', connectionsData);
    
    if (!connectionsData) {
      setProfileError('Please save connection details first');
      return;
    }
    
    const verificationId = connectionsData.verificationId || connectionsData.id;
    
    if (!verificationId) {
      setProfileError('Connection ID missing. Please save your connection details again.');
      return;
    }
    
    setIsConnectingProfile(true);
    setProfileError('');
    setProfileSuccess('');
    
    try {
      console.log('Submitting connection with ID:', verificationId);
      const response = await submitConnectionForReview(verificationId);
      console.log('Submit connection response:', response);
      setProfileSuccess('Connections submitted successfully! Your mentor will review it shortly.');
      setConnectionsData({ ...connectionsData, status: 'pending' });
    } catch (error) {
      console.error('Submit connection error:', error);
      console.error('Error response:', error.response);
      
      // Handle authentication errors
      if (error.response?.status === 401) {
        setProfileError('Session expired. Please logout and login again.');
        return;
      }
      
      const errorMessage = error.response?.data?.error || error.response?.data?.detail || 'Failed to submit connection for review';
      setProfileError(errorMessage);
    } finally {
      setIsConnectingProfile(false);
    }
  };

  return (
    <div className="iipc-container">
      {/* Header */}
      <motion.div
        className="iipc-header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <h1 className="iipc-title">Industry Institute Partneship Cell</h1>
        <p className="iipc-subtitle">
          Verify your LinkedIn activity and professional network
        </p>
      </motion.div>

      {/* Section Selector */}
      <div className="iipc-section-selector">
        <Button
          variant={activeSection === 'post' ? 'primary' : 'outline'}
          onClick={() => setActiveSection('post')}
        >
          Post Verification
        </Button>
        <Button
          variant={activeSection === 'connections' ? 'primary' : 'outline'}
          onClick={() => setActiveSection('connections')}
        >
          Connections Verification
        </Button>
      </div>

      {/* Post Verification Section */}
      <AnimatePresence mode="wait">
        {activeSection === 'post' && (
          <motion.div
            key="post"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <GlassCard variant="medium" className="iipc-card">
              <div className="iipc-card-header">
                <TrendingUp size={32} className="iipc-card-icon" />
                <div>
                  <h2 className="iipc-card-title">LinkedIn Post Verification</h2>
                  <p className="iipc-card-subtitle">
                    Verify your LinkedIn post for engagement and quality
                  </p>
                </div>
              </div>

              <div className="iipc-post-form">
                <Input
                  label="LinkedIn Post URL"
                  placeholder="https://www.linkedin.com/posts/..."
                  value={postUrl}
                  onChange={(e) => {
                    setPostUrl(e.target.value);
                    setPostError('');
                  }}
                  icon={<Linkedin size={20} />}
                  floatingLabel
                />
                
                <Input
                  label="Post Date"
                  type="date"
                  value={postDate}
                  onChange={(e) => {
                    setPostDate(e.target.value);
                    setPostError('');
                  }}
                  icon={<Calendar size={20} />}
                  floatingLabel
                />
                
                <div className="iipc-form-row">
                  <Input
                    label="Character Count"
                    type="number"
                    placeholder="Number of characters in post"
                    value={characterCount}
                    onChange={(e) => {
                      setCharacterCount(e.target.value);
                      setPostError('');
                    }}
                    icon={<Hash size={20} />}
                    floatingLabel
                  />
                  
                  <Input
                    label="Hashtag Count"
                    type="number"
                    placeholder="Number of hashtags used"
                    value={hashtagCount}
                    onChange={(e) => {
                      setHashtagCount(e.target.value);
                      setPostError('');
                    }}
                    icon={<Hash size={20} />}
                    floatingLabel
                  />
                </div>
                
                {postError && (
                  <motion.div
                    className="iipc-error-message"
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                  >
                    {postError}
                  </motion.div>
                )}
                
                {postSuccess && (
                  <motion.div
                    className="iipc-success-message"
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                  >
                    {postSuccess}
                  </motion.div>
                )}

                <div className="iipc-button-group">
                  {(!postData || postData?.status === 'draft') && (
                    <Button
                      variant="primary"
                      onClick={handleVerifyPost}
                      disabled={isVerifying}
                      withGlow={postUrl && !isVerifying}
                    >
                      {isVerifying ? (
                        <motion.span
                          animate={{ rotate: 360 }}
                          transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                          style={{ display: 'inline-block' }}
                        >
                          <Search size={20} />
                        </motion.span>
                      ) : (
                        postData ? 'Update Details' : 'Save Post Details'
                      )}
                    </Button>
                  )}
                  
                  {postData && (postData.status === 'draft' || !postData.status) && (
                    <Button
                      variant="primary"
                      onClick={handleSubmitPost}
                      disabled={isVerifying}
                      style={{ background: 'linear-gradient(135deg, #66BB6A 0%, #43A047 100%)' }}
                    >
                      {isVerifying ? 'Submitting...' : 'Submit for Review'}
                    </Button>
                  )}
                  
                  {postData?.status === 'pending' && (
                    <div className="iipc-status-badge iipc-status-pending">
                      <Search size={18} />
                      <span>Submitted - Awaiting Mentor Review</span>
                    </div>
                  )}
                  
                  {postData?.status === 'approved' && (
                    <div className="iipc-status-badge iipc-status-approved">
                      <CheckCircle size={18} />
                      <span>Verified by Mentor ✓</span>
                    </div>
                  )}
                  
                  {postData?.status === 'rejected' && (
                    <div className="iipc-status-badge iipc-status-rejected">
                      <XCircle size={18} />
                      <span>Revision Requested</span>
                    </div>
                  )}
                </div>
              </div>

              {isVerifying && (
                <motion.div
                  className="iipc-scanning"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                >
                  <motion.div
                    className="iipc-scanning-bar"
                    animate={{
                      x: ['-100%', '100%'],
                    }}
                    transition={{
                      duration: 1.5,
                      repeat: Infinity,
                      ease: 'easeInOut',
                    }}
                  />
                  <p className="iipc-scanning-text">Scanning LinkedIn post...</p>
                </motion.div>
              )}

              {postData && postData.status === 'draft' && !isVerifying && (
                <motion.div
                  className="iipc-summary-card"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <div className="iipc-summary-content">
                    <CheckCircle size={20} className="iipc-summary-icon" />
                    <div className="iipc-summary-text">
                      <span className="iipc-summary-label">Post Saved:</span>
                      <span className="iipc-summary-details">{postData.post_url || postUrl}</span>
                    </div>
                  </div>
                </motion.div>
              )}
            </GlassCard>
          </motion.div>
        )}

        {activeSection === 'connections' && (
          <motion.div
            key="connections"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <GlassCard variant="medium" className="iipc-card">
              <div className="iipc-card-header">
                <Users size={32} className="iipc-card-icon" />
                <div>
                  <h2 className="iipc-card-title">LinkedIn Connections Verification</h2>
                  <p className="iipc-card-subtitle">
                    Verify your LinkedIn connections from industry professionals
                  </p>
                </div>
              </div>

              {/* Verification Method Selection */}
              <div className="iipc-method-selector">
                <motion.button
                  className={`iipc-method-button ${verificationMethod === 'screenshot' ? 'iipc-method-button--active' : ''}`}
                  onClick={() => setVerificationMethod('screenshot')}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <Upload size={24} />
                  <div>
                    <div className="iipc-method-title">Screenshot Links</div>
                    <div className="iipc-method-subtitle">Provide Google Drive links to screenshots</div>
                  </div>
                </motion.button>

                <motion.button
                  className={`iipc-method-button ${verificationMethod === 'profile' ? 'iipc-method-button--active' : ''}`}
                  onClick={() => setVerificationMethod('profile')}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <Linkedin size={24} />
                  <div>
                    <div className="iipc-method-title">Link Profile</div>
                    <div className="iipc-method-subtitle">Connect your LinkedIn profile directly</div>
                  </div>
                </motion.button>
              </div>

              <AnimatePresence mode="wait">
                {verificationMethod === 'screenshot' && (
                  <motion.div
                    key="screenshot"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    transition={{ duration: 0.3 }}
                  >
                    <div className="iipc-screenshot-links-section">
                      <p className="iipc-instruction-text">
                        Provide Google Drive links to your connection screenshots
                      </p>
                      
                      {screenshotLinks.map((link, index) => (
                        <motion.div
                          key={index}
                          className="iipc-link-input-group"
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: index * 0.05 }}
                        >
                          <Input
                            label={`Screenshot Link ${index + 1}`}
                            placeholder="https://drive.google.com/file/d/..."
                            value={link}
                            onChange={(e) => updateScreenshotLink(index, e.target.value)}
                            icon={<Upload size={20} />}
                            floatingLabel
                          />
                          {screenshotLinks.length > 1 && (
                            <Button
                              variant="outline"
                              onClick={() => removeScreenshotLink(index)}
                              style={{ marginTop: '8px' }}
                            >
                              Remove
                            </Button>
                          )}
                        </motion.div>
                      ))}
                      
                      <Button
                        variant="outline"
                        onClick={addScreenshotLink}
                        style={{ marginTop: '12px' }}
                      >
                        + Add Another Link
                      </Button>
                    </div>

                    {profileError && (
                      <motion.div
                        className="iipc-error-message"
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        style={{ marginTop: '1rem' }}
                      >
                        {profileError}
                      </motion.div>
                    )}
                    
                    {profileSuccess && (
                      <motion.div
                        className="iipc-success-message"
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        style={{ marginTop: '1rem' }}
                      >
                        {profileSuccess}
                      </motion.div>
                    )}

                    {screenshotLinks.some(link => link.trim() !== '') && (
                      <div className="iipc-button-group" style={{ marginTop: '20px' }}>
                        {(!connectionsData || connectionsData?.status === 'draft') && (
                          <Button
                            variant="primary"
                            onClick={handleVerifyConnections}
                            disabled={isConnectingProfile}
                            withGlow={!isConnectingProfile}
                          >
                            {isConnectingProfile ? (
                              <motion.span
                                animate={{ rotate: 360 }}
                                transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                                style={{ display: 'inline-block' }}
                              >
                                <Search size={20} />
                              </motion.span>
                            ) : (
                              connectionsData ? 'Update Details' : 'Save Connection Details'
                            )}
                          </Button>
                        )}
                        
                        {connectionsData && (connectionsData.status === 'draft' || !connectionsData.status) && (
                          <Button
                            variant="primary"
                            onClick={handleSubmitConnection}
                            disabled={isConnectingProfile}
                            style={{ background: 'linear-gradient(135deg, #66BB6A 0%, #43A047 100%)' }}
                          >
                            {isConnectingProfile ? 'Submitting...' : 'Submit for Review'}
                          </Button>
                        )}
                        
                        {connectionsData?.status === 'pending' && (
                          <div className="iipc-status-badge iipc-status-pending">
                            <Search size={18} />
                            <span>Submitted - Awaiting Mentor Review</span>
                          </div>
                        )}
                        
                        {connectionsData?.status === 'approved' && (
                          <div className="iipc-status-badge iipc-status-approved">
                            <CheckCircle size={18} />
                            <span>Verified by Mentor ✓</span>
                          </div>
                        )}
                        
                        {connectionsData?.status === 'rejected' && (
                          <div className="iipc-status-badge iipc-status-rejected">
                            <XCircle size={18} />
                            <span>Revision Requested</span>
                          </div>
                        )}
                      </div>
                    )}
                  </motion.div>
                )}

                {verificationMethod === 'profile' && (
                  <motion.div
                    key="profile"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    transition={{ duration: 0.3 }}
                  >
                    <div className="iipc-profile-section">
                      <p className="iipc-instruction-text">
                        Connect your LinkedIn profile to verify your professional network
                      </p>
                      
                      {/* LinkedIn OAuth Button */}
                      <div className="linkedin-oauth-container">
                        <Button
                          variant="primary"
                          onClick={handleLinkedInOAuth}
                          style={{
                            background: 'linear-gradient(135deg, #0A66C2 0%, #004182 100%)',
                            width: '100%',
                            marginBottom: '1.5rem'
                          }}
                        >
                          <Linkedin size={20} style={{ marginRight: '8px' }} />
                          Sign in with LinkedIn
                        </Button>
                        
                        <div className="oauth-divider">
                          <span>OR</span>
                        </div>
                      </div>
                      
                      <Input
                        label="LinkedIn Profile URL"
                        placeholder="https://www.linkedin.com/in/your-profile"
                        value={profileUrl}
                        onChange={(e) => {
                          setProfileUrl(e.target.value);
                          setProfileError('');
                        }}
                        icon={<Linkedin size={20} />}
                        floatingLabel
                      />
                      
                      {profileError && (
                        <motion.div
                          className="iipc-error-message"
                          initial={{ opacity: 0, y: -10 }}
                          animate={{ opacity: 1, y: 0 }}
                        >
                          {profileError}
                        </motion.div>
                      )}
                      
                      {profileSuccess && (
                        <motion.div
                          className="iipc-success-message"
                          initial={{ opacity: 0, y: -10 }}
                          animate={{ opacity: 1, y: 0 }}
                        >
                          {profileSuccess}
                        </motion.div>
                      )}
                    </div>

                    <div className="iipc-button-group" style={{ marginTop: '20px' }}>
                      {(!connectionsData || connectionsData?.status === 'draft') && (
                        <Button
                          variant="primary"
                          onClick={handleConnectProfile}
                          disabled={isConnectingProfile}
                          withGlow={profileUrl && !isConnectingProfile}
                        >
                          {isConnectingProfile ? (
                            <motion.span
                              animate={{ rotate: 360 }}
                              transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                              style={{ display: 'inline-block' }}
                            >
                              <Search size={20} />
                            </motion.span>
                          ) : (
                            connectionsData ? 'Update Details' : 'Save Profile Details'
                          )}
                        </Button>
                      )}
                      
                      {connectionsData && (connectionsData.status === 'draft' || !connectionsData.status) && (
                        <Button
                          variant="primary"
                          onClick={handleSubmitConnection}
                          disabled={isConnectingProfile}
                          style={{ background: 'linear-gradient(135deg, #66BB6A 0%, #43A047 100%)' }}
                        >
                          {isConnectingProfile ? 'Submitting...' : 'Submit for Review'}
                        </Button>
                      )}
                      
                      {connectionsData?.status === 'pending' && (
                        <div className="iipc-status-badge iipc-status-pending">
                          <Search size={18} />
                          <span>Submitted - Awaiting Mentor Review</span>
                        </div>
                      )}
                      
                      {connectionsData?.status === 'approved' && (
                        <div className="iipc-status-badge iipc-status-approved">
                          <CheckCircle size={18} />
                          <span>Verified by Mentor ✓</span>
                        </div>
                      )}
                      
                      {connectionsData?.status === 'rejected' && (
                        <div className="iipc-status-badge iipc-status-rejected">
                          <XCircle size={18} />
                          <span>Revision Requested</span>
                        </div>
                      )}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </GlassCard>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default IIPC;
