import React, { useState } from 'react';
// eslint-disable-next-line no-unused-vars
import { motion } from 'framer-motion';
import { useNavigate, Link } from 'react-router-dom';
import { Eye, EyeOff, Mail, Lock, LogIn, UserPlus, Lightbulb, ArrowRight, GraduationCap, Users, Crown } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import GlassCard from '../components/GlassCard';
import { Input } from '../components/Input';
import { Button } from '../components/Button';
import WingsIcon from '../components/WingsIcon';
import './Login.css';

const ROLES = [
    { id: 'STUDENT', label: 'Student', icon: GraduationCap, color: '#ffcc00', description: 'Access student dashboard' },
    { id: 'MENTOR', label: 'Mentor', icon: Users, color: '#42A5F5', description: 'Guide and support students' },
    { id: 'FLOOR_WING', label: 'Floor Wing', icon: WingsIcon, color: '#66BB6A', description: 'Manage floor operations' },
    { id: 'ADMIN', label: 'Admin', icon: Crown, color: '#ffcc00', description: 'Full system access' },
];
//vishnu
const Login = () => {
    const navigate = useNavigate();
    const { login, getHomePath } = useAuth();
    const [showPassword, setShowPassword] = useState(false);
    const [isLogin, setIsLogin] = useState(true);
    const [selectedRole, setSelectedRole] = useState('STUDENT');
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        confirmPassword: '',
        name: '',
    });
    const [errors, setErrors] = useState({});

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
        // Clear error when user starts typing
        if (errors[name]) {
            setErrors(prev => ({ ...prev, [name]: '' }));
        }
    };

    const validateForm = () => {
        const newErrors = {};
        
        console.log('Validating form with data:', formData);

        if (!formData.email) {
            newErrors.email = 'Email is required';
        } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
            newErrors.email = 'Email is invalid';
        }

        if (!formData.password) {
            newErrors.password = 'Password is required';
        } else if (formData.password.length < 6) {
            newErrors.password = 'Password must be at least 6 characters';
        }

        if (!isLogin) {
            if (!formData.name) {
                newErrors.name = 'Name is required';
            }
            if (!formData.confirmPassword) {
                newErrors.confirmPassword = 'Please confirm your password';
            } else if (formData.password !== formData.confirmPassword) {
                newErrors.confirmPassword = 'Passwords do not match';
            }
        }
        
        console.log('Validation errors:', newErrors);
        console.log('Validation result:', Object.keys(newErrors).length === 0);

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (validateForm()) {
            try {
                console.log('Login form - attempting login with:', formData.email);
                
                // Use email as username for login
                await login(formData.email, formData.password, selectedRole);

                // Navigate to role-based home path
                const homePath = getHomePath();
                navigate(homePath);
            } catch (error) {
                console.error('Login error:', error);
                console.error('Error response:', error.response?.data);
                
                const errorMessage = error.response?.data?.detail || 
                                   error.response?.data?.message || 
                                   'Invalid email or password';
                
                setErrors({
                    email: errorMessage,
                    password: 'Please check your credentials',
                });
            }
        }
    };

    const toggleMode = () => {
        setIsLogin(!isLogin);
        setErrors({});
        setFormData({
            email: '',
            password: '',
            confirmPassword: '',
            name: '',
        });
    };

    return (
        <div className="login-page">
            {/* Animated Background */}
            <div className="login-background">
                <motion.div
                    className="login-gradient-orb login-gradient-orb--1"
                    animate={{
                        x: [0, 100, 0],
                        y: [0, -50, 0],
                        scale: [1, 1.2, 1],
                    }}
                    transition={{
                        duration: 8,
                        repeat: Infinity,
                        ease: 'easeInOut',
                    }}
                />
                <motion.div
                    className="login-gradient-orb login-gradient-orb--2"
                    animate={{
                        x: [0, -80, 0],
                        y: [0, 100, 0],
                        scale: [1, 1.1, 1],
                    }}
                    transition={{
                        duration: 10,
                        repeat: Infinity,
                        ease: 'easeInOut',
                    }}
                />
                <motion.div
                    className="login-gradient-orb login-gradient-orb--3"
                    animate={{
                        x: [0, 60, 0],
                        y: [0, -80, 0],
                        scale: [1, 1.3, 1],
                    }}
                    transition={{
                        duration: 12,
                        repeat: Infinity,
                        ease: 'easeInOut',
                    }}
                />
            </div>

            {/* Login Container */}
            <div className="login-container">
                {/* Branding Section */}
                <motion.div
                    className="login-branding"
                    initial={{ opacity: 0, x: -50 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.6 }}
                >
                    <motion.div
                        className="login-logo"
                        whileHover={{ rotate: 360 }}
                        transition={{ duration: 0.6 }}
                    >
                        <Lightbulb size={64} />
                    </motion.div>
                    <h1 className="login-title">Cohort Web</h1>
                    <p className="login-subtitle">
                        Track your academic journey, showcase your skills, and build your professional portfolio
                    </p>

                    <div className="login-features">
                        <motion.div
                            className="login-feature"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.2 }}
                        >
                            <div className="login-feature-icon">✨</div>
                            <span>Creative Learning</span>
                        </motion.div>
                        <motion.div
                            className="login-feature"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.3 }}
                        >
                            <div className="login-feature-icon">🚀</div>
                            <span>Career Development</span>
                        </motion.div>
                        <motion.div
                            className="login-feature"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.4 }}
                        >
                            <div className="login-feature-icon">💼</div>
                            <span>Portfolio Building</span>
                        </motion.div>
                    </div>
                </motion.div>

                {/* Login Form Card */}
                <motion.div
                    className="login-card-wrapper"
                    initial={{ opacity: 0, x: 50 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.6 }}
                >
                    <GlassCard className="login-card" hoverable={false}>
                        <div className="login-card-header">
                            <h2 className="login-card-title">
                                {isLogin ? 'Welcome Back' : 'Create Account'}
                            </h2>
                            <p className="login-card-description">
                                {isLogin
                                    ? 'Sign in to continue your learning journey'
                                    : 'Join us to start tracking your achievements'}
                            </p>
                        </div>

                        <form onSubmit={handleSubmit} className="login-form">
                            {isLogin && (
                                <>
                                    {/* Role Selection */}
                                    <div className="role-selection">
                                        <label className="role-selection-label">Select Your Role</label>
                                        <div className="role-grid">
                                            {ROLES.map((role) => {
                                                const Icon = role.icon;
                                                return (
                                                    <motion.button
                                                        key={role.id}
                                                        type="button"
                                                        className={`role-card ${selectedRole === role.id ? 'role-card--active' : ''}`}
                                                        onClick={() => setSelectedRole(role.id)}
                                                        whileHover={{ scale: 1.05 }}
                                                        whileTap={{ scale: 0.95 }}
                                                        style={{
                                                            '--role-color': role.color,
                                                        }}
                                                    >
                                                        <Icon size={24} />
                                                        <span className="role-card-label">{role.label}</span>
                                                        {selectedRole === role.id && (
                                                            <motion.div
                                                                className="role-card-checkmark"
                                                                initial={{ scale: 0 }}
                                                                animate={{ scale: 1 }}
                                                                transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                                                            >
                                                                ✓
                                                            </motion.div>
                                                        )}
                                                    </motion.button>
                                                );
                                            })}
                                        </div>
                                    </div>

                                    <Input
                                        label="Email Address"
                                        name="email"
                                        type="email"
                                        value={formData.email}
                                        onChange={handleInputChange}
                                        error={errors.email}
                                        icon={<Mail size={20} />}
                                        placeholder="Enter your email"
                                    />

                                    <div className="login-password-field">
                                        <Input
                                            label="Password"
                                            name="password"
                                            type={showPassword ? 'text' : 'password'}
                                            value={formData.password}
                                            onChange={handleInputChange}
                                            error={errors.password}
                                            icon={<Lock size={20} />}
                                            placeholder="Enter your password"
                                        />
                                        <button
                                            type="button"
                                            className="login-password-toggle"
                                            onClick={() => setShowPassword(!showPassword)}
                                            aria-label={showPassword ? 'Hide password' : 'Show password'}
                                        >
                                            {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                                        </button>
                                    </div>

                                    {Object.keys(errors).length > 0 && (
                                        <motion.div
                                            className="login-error-summary"
                                            initial={{ opacity: 0, y: -10 }}
                                            animate={{ opacity: 1, y: 0 }}
                                        >
                                            {Object.values(errors).map((error, index) => (
                                                <div key={index} className="login-error-item">
                                                    {error}
                                                </div>
                                            ))}
                                        </motion.div>
                                    )}

                                    <div className="login-options">
                                        <label className="login-remember">
                                            <input type="checkbox" />
                                            <span>Remember me</span>
                                        </label>
                                        <Link to="/forgot-password" className="login-forgot">
                                            Forgot Password?
                                        </Link>
                                    </div>
                                </>
                            )}

                            {isLogin && (
                                <Button
                                    type="submit"
                                    variant="primary"
                                    size="large"
                                    withGlow={true}
                                    className="login-submit-button"
                                >
                                    <LogIn size={20} />
                                    Sign In
                                </Button>
                            )}

                            {!isLogin && (
                                <div className="contact-admin-message">
                                    <div className="contact-admin-icon">
                                        <UserPlus size={48} />
                                    </div>
                                    <h3>Account Registration</h3>
                                    <p>New user accounts must be created by administrators.</p>
                                    <p className="contact-admin-cta">
                                        Please contact your administrator to get access to the platform.
                                    </p>
                                </div>
                            )}
                        </form>

                        <div className="login-card-footer">
                            <p>
                                {isLogin ? "Don't have an account?" : 'Already have an account?'}
                                <button
                                    type="button"
                                    className="login-toggle-mode"
                                    onClick={toggleMode}
                                >
                                    {isLogin ? 'Sign Up' : 'Sign In'}
                                    <ArrowRight size={16} />
                                </button>
                            </p>
                        </div>
                    </GlassCard>
                </motion.div>
            </div>
        </div>
    );
};

export default Login;
