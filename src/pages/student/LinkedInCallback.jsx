import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { handleLinkedInCallback } from '../../services/iipc';
import { motion } from 'framer-motion';
import { Linkedin, CheckCircle, XCircle } from 'lucide-react';
import './LinkedInCallback.css';

export const LinkedInCallback = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState('processing'); // 'processing', 'success', 'error'
  const [error, setError] = useState('');
  const [profileData, setProfileData] = useState(null);

  useEffect(() => {
    const processCallback = async () => {
      const code = searchParams.get('code');
      const state = searchParams.get('state');
      const error = searchParams.get('error');

      // Check for OAuth errors
      if (error) {
        setStatus('error');
        setError(`LinkedIn authentication failed: ${error}`);
        return;
      }

      if (!code) {
        setStatus('error');
        setError('No authorization code received from LinkedIn');
        return;
      }

      try {
        // Exchange code for profile data
        const response = await handleLinkedInCallback(code, state);
        
        if (response.success) {
          setStatus('success');
          setProfileData(response.profile);
          
          // Store profile data in sessionStorage for IIPC page to use
          sessionStorage.setItem('linkedin_profile', JSON.stringify(response.profile));
          
          // Redirect to IIPC page after 2 seconds
          setTimeout(() => {
            navigate('/student/iipc', { 
              state: { linkedInProfile: response.profile }
            });
          }, 2000);
        } else {
          setStatus('error');
          setError('Failed to verify LinkedIn profile');
        }
      } catch (err) {
        setStatus('error');
        setError(err.response?.data?.error || 'An error occurred while connecting to LinkedIn');
      }
    };

    processCallback();
  }, [searchParams, navigate]);

  return (
    <div className="linkedin-callback-container">
      <motion.div
        className="linkedin-callback-card"
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        {status === 'processing' && (
          <>
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
            >
              <Linkedin size={64} className="linkedin-icon-processing" />
            </motion.div>
            <h2>Connecting to LinkedIn...</h2>
            <p>Please wait while we verify your profile</p>
          </>
        )}

        {status === 'success' && (
          <>
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', delay: 0.2 }}
            >
              <CheckCircle size={64} className="linkedin-icon-success" />
            </motion.div>
            <h2>Successfully Connected!</h2>
            <p>Your LinkedIn profile has been verified</p>
            {profileData && (
              <div className="profile-preview">
                {profileData.profile_picture && (
                  <img 
                    src={profileData.profile_picture} 
                    alt={profileData.full_name}
                    className="profile-picture"
                  />
                )}
                <p className="profile-name">{profileData.full_name}</p>
                <p className="profile-email">{profileData.email}</p>
              </div>
            )}
            <p className="redirect-message">Redirecting to IIPC page...</p>
          </>
        )}

        {status === 'error' && (
          <>
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', delay: 0.2 }}
            >
              <XCircle size={64} className="linkedin-icon-error" />
            </motion.div>
            <h2>Connection Failed</h2>
            <p className="error-message">{error}</p>
            <button 
              className="retry-button"
              onClick={() => navigate('/student/iipc')}
            >
              Return to IIPC
            </button>
          </>
        )}
      </motion.div>
    </div>
  );
};

export default LinkedInCallback;
