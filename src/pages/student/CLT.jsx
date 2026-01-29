import React, { useState, useEffect } from 'react';
// eslint-disable-next-line no-unused-vars
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, FileText, CheckCircle, Image as ImageIcon } from 'lucide-react';
import GlassCard from '../../components/GlassCard';
import Button from '../../components/Button';
import Input from '../../components/Input';
import ProgressBar from '../../components/ProgressBar';
import cltService from '../../services/clt';
import './CLT.css';

export const CLT = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    platform: '',
    completionDate: '',
    duration: '',
    driveLink: '',
  });
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submissions, setSubmissions] = useState([]);
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);

  const steps = [
    { id: 1, label: 'Course Details', icon: FileText },
    { id: 2, label: 'Learning Evidence', icon: ImageIcon },
    { id: 3, label: 'Review & Submit', icon: CheckCircle },
  ];

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const files = Array.from(e.dataTransfer.files);
    setFormData({ ...formData, files: [...formData.files, ...files] });
  };

  const handleFileInput = (e) => {
    const files = Array.from(e.target.files);
    // Validate file size (10MB max per file)
    const validFiles = files.filter(file => {
      if (file.size > 10 * 1024 * 1024) {
        alert(`File ${file.name} exceeds 10MB limit`);
        return false;
      }
      return true;
    });
    setFormData({ ...formData, files: [...formData.files, ...validFiles] });
  };

  // Load submissions and stats on component mount
  useEffect(() => {
    loadSubmissions();
    loadStats();
  }, []);

  const loadSubmissions = async () => {
    try {
      const data = await cltService.getSubmissions();
      setSubmissions(data.results || data);
    } catch (err) {
      console.error('Failed to load submissions:', err);
      setError('Failed to load submissions. Please ensure you are logged in.');
    }
  };

  const loadStats = async () => {
    try {
      const data = await cltService.getStats();
      setStats(data);
    } catch (err) {
      console.error('Failed to load stats:', err);
      console.error('Stats error details:', {
        status: err.response?.status,
        statusText: err.response?.statusText,
        data: err.response?.data,
        url: err.config?.url
      });
      // Stats are not critical, don't show error to user
      setStats(null);
    }
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    setError(null);

    try {
      console.log('Starting submission...', {
        title: formData.title,
        description: formData.description,
        platform: formData.platform,
        completionDate: formData.completionDate,
        driveLink: formData.driveLink
      });

      // Validate drive link is present
      if (!formData.driveLink || formData.driveLink.trim() === '') {
        throw new Error('Please provide a Google Drive link to your certificate/evidence.');
      }

      // Check if user has auth token
      const token = localStorage.getItem('accessToken');
      if (!token) {
        throw new Error('Not authenticated. Please log in again.');
      }

      // Simulate upload progress for better UX
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => Math.min(prev + 10, 90));
      }, 200);

      // Create submission with drive link
      const submissionData = {
        title: formData.title,
        description: formData.description,
        platform: formData.platform,
        completion_date: formData.completionDate,
        drive_link: formData.driveLink,
      };

      console.log('Calling createSubmission API...');
      const createdSubmission = await cltService.createSubmission(submissionData);
      console.log('Submission created:', createdSubmission);

      clearInterval(progressInterval);
      setUploadProgress(100);

      // Wait a moment to show 100% progress
      setTimeout(async () => {
        try {
          // Submit the submission for review
          console.log('Submitting for review...', { submissionId: createdSubmission.id });

          await cltService.submitForReview(createdSubmission.id);
          console.log('Submitted successfully!');

          alert('Submission successful! Your submission is now under review.');

          // Reset form
          setFormData({
            title: '',
            description: '',
            platform: '',
            completionDate: '',
            driveLink: ''
          });
          setCurrentStep(1);
          setUploadProgress(0);
          setIsSubmitting(false);

          // Reload data
          loadSubmissions();
          loadStats();
        } catch (submitErr) {
          console.error('Submit for review failed:', submitErr);
          console.error('Error response:', submitErr.response?.data);

          // Even if submit fails, the draft was created
          const errorMsg = submitErr.response?.data?.error || submitErr.message || 'Could not submit for review';
          alert(`Draft saved but could not submit: ${errorMsg}\nYou can submit it later from your submissions list.`);
          setIsSubmitting(false);
          loadSubmissions();
          loadStats();
        }
      }, 500);

    } catch (err) {
      console.error('Submission failed:', err);
      console.error('Error details:', err.response?.data);

      let errorMessage = 'Submission failed. ';
      if (err.response?.data) {
        // Handle different error formats
        if (typeof err.response.data === 'string') {
          errorMessage += err.response.data;
        } else if (err.response.data.error) {
          errorMessage += err.response.data.error;
        } else if (err.response.data.message) {
          errorMessage += err.response.data.message;
        } else if (err.response.data.detail) {
          errorMessage += err.response.data.detail;
        } else {
          errorMessage += JSON.stringify(err.response.data);
        }
      } else {
        errorMessage += err.message;
      }

      setError(errorMessage);
      setIsSubmitting(false);
      setUploadProgress(0);
      alert(errorMessage);
    }
  };

  return (
    <div className="clt-container">

      {/* Header */}
      <motion.div
        className="clt-header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <h1 className="clt-title">Center for Learning and Teaching</h1>
        <p className="clt-subtitle">
          Document your creative projects and learning journey
        </p>
      </motion.div>

      {/* Step Indicators */}
      <div className="clt-steps">
        {steps.map((step, index) => {
          const StepIcon = step.icon;
          const isActive = currentStep === step.id;
          const isCompleted = currentStep > step.id;

          return (
            <React.Fragment key={step.id}>
              <motion.div
                className={`clt-step ${isActive ? 'clt-step--active' : ''} ${isCompleted ? 'clt-step--completed' : ''}`}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
              >
                <div className="clt-step-icon">
                  <StepIcon size={20} />
                  {isCompleted && (
                    <motion.div
                      className="clt-step-check"
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ type: 'spring' }}
                    >
                      <CheckCircle size={16} />
                    </motion.div>
                  )}
                </div>
                <span className="clt-step-label">{step.label}</span>
              </motion.div>

              {index < steps.length - 1 && (
                <div className="clt-step-connector">
                  <motion.div
                    className="clt-step-connector-fill"
                    initial={{ width: 0 }}
                    animate={{ width: isCompleted ? '100%' : '0%' }}
                    transition={{ duration: 0.5 }}
                  />
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>

      {/* Form Content */}
      <GlassCard variant="medium" className="clt-form-card">
        <AnimatePresence mode="wait">
          {currentStep === 1 && (
            <motion.div
              key="step1"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="clt-step-content"
            >
              <h2 className="clt-form-title">Course Details</h2>

              <Input
                label="Course Title"
                placeholder="Enter course title"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                floatingLabel
              />

              <div className="clt-textarea-wrapper">
                <label className="clt-textarea-label">Course Description</label>
                <textarea
                  className="clt-textarea"
                  rows="5"
                  placeholder="Describe the course you had completed..."
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                />
              </div>

              <Input
                label="Platform"
                placeholder="e.g., Coursera, Udemy, edX"
                value={formData.platform}
                onChange={(e) => setFormData({ ...formData, platform: e.target.value })}
                floatingLabel
              />

              <Input
                label="Completion Date"
                type="date"
                value={formData.completionDate}
                onChange={(e) => setFormData({ ...formData, completionDate: e.target.value })}
                floatingLabel
              />

              <Input
                label="Total Duration (hours)"
                type="number"
                placeholder="e.g., 40"
                min="10"
                value={formData.duration}
                onChange={(e) => setFormData({ ...formData, duration: e.target.value })}
                floatingLabel
              />

              <div className="clt-form-actions">
                <Button
                  variant="primary"
                  onClick={() => {
                    if (formData.title && formData.description) {
                      if (formData.duration && parseInt(formData.duration) < 10) {
                        alert('Total duration must be at least 10 hours');
                        return;
                      }
                      setCurrentStep(2);
                    } else {
                      alert('Please fill in all required fields');
                    }
                  }}
                >
                  Next Step
                </Button>
              </div>
            </motion.div>
          )}

          {currentStep === 2 && (
            <motion.div
              key="step2"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="clt-step-content"
            >
              <h2 className="clt-form-title">Certificate/Evidence Link</h2>

              <p className="clt-form-description" style={{ marginBottom: '1.5rem', color: 'var(--text-secondary)' }}>
                Please upload your certificate or evidence to Google Drive and share the link below.
                Make sure the link is accessible to anyone with the link.
              </p>

              <Input
                label="Google Drive Link"
                placeholder="https://drive.google.com/file/d/..."
                value={formData.driveLink}
                onChange={(e) => setFormData({ ...formData, driveLink: e.target.value })}
                floatingLabel
              />

              <p className="clt-upload-hint" style={{ marginTop: '0.5rem', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                💡 Tip: Right-click your file in Google Drive → Get link → Copy link
              </p>

              <div className="clt-form-actions">
                <Button
                  variant="outline"
                  onClick={() => setCurrentStep(1)}
                >
                  Back
                </Button>
                <Button
                  variant="primary"
                  onClick={() => {
                    if (formData.driveLink && formData.driveLink.trim() !== '') {
                      setCurrentStep(3);
                    } else {
                      alert('Please provide a Google Drive link');
                    }
                  }}
                >
                  Next Step
                </Button>
              </div>
            </motion.div>
          )}

          {currentStep === 3 && (
            <motion.div
              key="step3"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="clt-step-content"
            >
              <h2 className="clt-form-title">Review & Submit</h2>

              <div className="clt-review-section">
                <h3 className="clt-review-label">Course Title</h3>
                <p className="clt-review-value">{formData.title}</p>
              </div>

              <div className="clt-review-section">
                <h3 className="clt-review-label">Description</h3>
                <p className="clt-review-value">{formData.description}</p>
              </div>

              <div className="clt-review-section">
                <h3 className="clt-review-label">Platform</h3>
                <p className="clt-review-value">{formData.platform}</p>
              </div>

              <div className="clt-review-section">
                <h3 className="clt-review-label">Completion Date</h3>
                <p className="clt-review-value">{formData.completionDate}</p>
              </div>

              <div className="clt-review-section">
                <h3 className="clt-review-label">Total Duration</h3>
                <p className="clt-review-value">{formData.duration} hours</p>
              </div>

              <div className="clt-review-section">
                <h3 className="clt-review-label">Google Drive Link</h3>
                <p className="clt-review-value" style={{ wordBreak: 'break-all' }}>{formData.driveLink}</p>
              </div>

              {error && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="clt-error-section"
                  style={{
                    padding: '1rem',
                    marginBottom: '1rem',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    border: '1px solid rgba(239, 68, 68, 0.3)',
                    borderRadius: '0.5rem',
                    color: '#ef4444'
                  }}
                >
                  <p>{error}</p>
                </motion.div>
              )}

              {isSubmitting && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="clt-progress-section"
                >
                  <p className="clt-progress-label">Uploading your submission...</p>
                  <ProgressBar progress={uploadProgress} animated />
                </motion.div>
              )}

              <div className="clt-form-actions">
                <Button
                  variant="outline"
                  onClick={() => setCurrentStep(2)}
                  disabled={isSubmitting}
                >
                  Back
                </Button>
                <Button
                  variant="primary"
                  withGlow
                  onClick={handleSubmit}
                  disabled={isSubmitting}
                >
                  {isSubmitting ? 'Submitting...' : 'Finalize Submission'}
                </Button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </GlassCard>
    </div>
  );
};

export default CLT;
