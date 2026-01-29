import React, { useEffect, useMemo, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    ChevronDown,
    BookOpen,
    Users,
    Trophy,
    Linkedin,
    Code,
    Heart,
    ArrowRight,
    Eye,
    TrendingUp,
    Target,
    Compass,
    Mail,
    Send,
    LogIn,
    Sparkles,
    CheckCircle,
    Loader2
} from 'lucide-react';
import './ParallaxIntro.css';

// ============================================
// CONFIGURATION & DATA
// ============================================

// Five Pillars Configuration
const PILLARS_CONFIG = [
    {
        icon: BookOpen,
        initial: 'CLT',
        title: 'Continuous Learning Track',
        description: 'Structured learning paths with measurable progress'
    },
    {
        icon: Heart,
        initial: 'SRI',
        title: 'Social Responsibility Initiative',
        description: 'Community engagement and social impact projects'
    },
    {
        icon: Trophy,
        initial: 'CFC',
        title: 'Co-curricular & Fitness Challenge',
        description: 'Holistic development through activities and wellness'
    },
    {
        icon: Linkedin,
        initial: 'IIPC',
        title: 'Industry & Interview Preparation',
        description: 'Professional readiness and career preparation'
    },
    {
        icon: Code,
        initial: 'SCD',
        title: 'Self-Code Development',
        description: 'Personal coding projects and technical growth'
    }
];

// Mentorship Features Configuration
const MENTORSHIP_FEATURES = [
    'Weekly Progress Reviews',
    'Submission Feedback',
    'Career Guidance',
    'Personal Development Tracking'
];

// Trust Indicators Configuration
const TRUST_INDICATORS = [
    'Secure & Private',
    'Instant Access',
    '24/7 Support'
];

// ============================================
// UTILITY FUNCTIONS
// ============================================

const generateAmbientParticles = (count = 20) => {
    return Array.from({ length: count }, (_, i) => ({
        id: i,
        left: `${Math.random() * 100}%`,
        delay: `${Math.random() * 5}s`,
        duration: `${3 + Math.random() * 4}s`
    }));
};

const isValidEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};

// ============================================
// BACKGROUND COMPONENTS
// ============================================

const AmbientBackground = ({ particles }) => (
    <div className="intro-ambient">
        <div className="intro-glow intro-glow-1" />
        <div className="intro-glow intro-glow-2" />
        <div className="intro-particles">
            {particles.map((p) => (
                <div
                    key={p.id}
                    className="intro-particle"
                    style={{
                        left: p.left,
                        animationDelay: p.delay,
                        animationDuration: p.duration
                    }}
                />
            ))}
        </div>
    </div>
);

// ============================================
// CONTENT BLOCK COMPONENTS
// ============================================

const HeroBlock = ({ scrollY }) => (
    <div className="content-block hero-block">
        <div className="hero-background">
            <div
                className="hero-layer hero-layer-back"
                style={{ transform: `translateY(${scrollY * 0.3}px)` }}
            />
            <div
                className="hero-layer hero-layer-mid"
                style={{ transform: `translateY(${scrollY * 0.15}px)` }}
            />
            <div className="hero-gradient-overlay" />
            <div className="hero-lines">
                <div className="hero-line hero-line-1" />
                <div className="hero-line hero-line-2" />
                <div className="hero-line hero-line-3" />
            </div>
        </div>

        <div className="hero-content">
            <div className="hero-badge">Cohort Community</div>
            <h1 className="hero-headline">
                Where Growth<br />
                <span className="hero-highlight">Meets Structure</span>
            </h1>
            <p className="hero-subheading">
                A unified platform connecting students, mentors, and institutions
                in a structured journey of academic and personal excellence.
            </p>
        </div>

        <div className="scroll-hint">
            <ChevronDown className="scroll-icon" />
        </div>
    </div>
);

const SolutionBlock = ({ scrollY }) => (
    <div className="content-block solution-block">
        <div className="solution-background">
            <div
                className="solution-layer solution-layer-1"
                style={{ transform: `translateY(${(scrollY - 1000) * 0.1}px)` }}
            />
            <div
                className="solution-layer solution-layer-2"
                style={{ transform: `translateY(${(scrollY - 1000) * 0.05}px)` }}
            />
        </div>

        <div className="solution-content">
            <div className="section-label section-label-light">The Solution</div>
            <h2 className="solution-headline">
                One Cohort.<br />
                One Ecosystem.<br />
                <span className="solution-highlight">Complete Visibility.</span>
            </h2>
            <p className="solution-description">
                Cohort brings together every aspect of student development into a single,
                unified platform. Every achievement tracked. Every milestone celebrated.
                Every student supported.
            </p>

            <div className="ecosystem-visual">
                <div className="ecosystem-ring ecosystem-ring-outer">
                    <span className="ecosystem-label">Institution</span>
                </div>
                <div className="ecosystem-ring ecosystem-ring-middle">
                    <span className="ecosystem-label">Mentors</span>
                </div>
                <div className="ecosystem-ring ecosystem-ring-inner">
                    <span className="ecosystem-label">Students</span>
                </div>
            </div>
        </div>
    </div>
);

const PillarsBlock = () => (
    <div className="content-block pillars-block">
        <div className="pillars-content">
            <div className="section-label">The Framework</div>
            <h2 className="pillars-headline">
                Five Pillars of<br />
                <span className="pillars-highlight">Holistic Development</span>
            </h2>

            <div className="pillars-grid">
                {PILLARS_CONFIG.map((pillar) => (
                    <div key={pillar.initial} className="pillar-card">
                        <div className="pillar-icon-wrapper">
                            <pillar.icon size={28} />
                        </div>
                        <div className="pillar-initial">{pillar.initial}</div>
                        <h3 className="pillar-title">{pillar.title}</h3>
                        <p className="pillar-description">{pillar.description}</p>
                    </div>
                ))}
            </div>
        </div>
    </div>
);

const MentorshipBlock = () => (
    <div className="content-block mentorship-block">
        <div className="mentorship-content">
            <div className="mentorship-text">
                <div className="section-label section-label-light">Guidance</div>
                <h2 className="mentorship-headline">
                    Mentors Who<br />
                    <span className="mentorship-highlight">Shape Futures</span>
                </h2>
                <p className="mentorship-description">
                    Every student is assigned a dedicated mentor who tracks progress,
                    reviews submissions, and provides personalized guidance throughout
                    their academic journey.
                </p>

                <div className="mentorship-features">
                    {MENTORSHIP_FEATURES.map((feature, index) => (
                        <div key={index} className="mentorship-feature">
                            <div className="feature-check">✓</div>
                            <span>{feature}</span>
                        </div>
                    ))}
                </div>
            </div>

            <div className="mentorship-visual">
                <div className="mentor-card-preview">
                    <div className="preview-header">
                        <div className="preview-avatar" />
                        <div className="preview-info">
                            <div className="preview-name" />
                            <div className="preview-role" />
                        </div>
                    </div>
                    <div className="preview-stats">
                        <div className="preview-stat" />
                        <div className="preview-stat" />
                        <div className="preview-stat" />
                    </div>
                    <div className="preview-progress">
                        <div className="preview-progress-bar" />
                    </div>
                </div>
            </div>
        </div>
    </div>
);

const InstitutionBlock = () => (
    <div className="content-block institution-block">
        <div className="institution-content">
            <div className="institution-text">
                <div className="section-label">Visibility</div>
                <h2 className="institution-headline">
                    Complete Institutional<br />
                    <span className="institution-highlight">Oversight</span>
                </h2>
                <p className="institution-description">
                    Administrators gain real-time visibility into cohort performance,
                    student progress, and mentor effectiveness through comprehensive
                    analytics and reporting.
                </p>
            </div>

            <div className="dashboard-preview">
                <div className="dashboard-grid">
                    <div className="dashboard-card dashboard-card-large">
                        <div className="dashboard-card-header">
                            <TrendingUp size={20} />
                            <span>Overall Progress</span>
                        </div>
                        <div className="dashboard-chart">
                            {[1, 2, 3, 4, 5].map((i) => (
                                <div key={i} className={`chart-bar chart-bar-${i}`} />
                            ))}
                        </div>
                    </div>
                    <div className="dashboard-card">
                        <div className="dashboard-metric">
                            <span className="metric-value">847</span>
                            <span className="metric-label">Active Students</span>
                        </div>
                    </div>
                    <div className="dashboard-card">
                        <div className="dashboard-metric">
                            <span className="metric-value">42</span>
                            <span className="metric-label">Mentors</span>
                        </div>
                    </div>
                    <div className="dashboard-card">
                        <div className="dashboard-metric">
                            <span className="metric-value">94%</span>
                            <span className="metric-label">Engagement</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
);

const CTABlock = ({
    email,
    setEmail,
    isEmailFocused,
    setIsEmailFocused,
    emailSubmitState,
    handleEmailSubmit,
    handleEmailKeyDown,
    showLoginOption,
    handleLoginTransition,
    emailInputRef
}) => (
    <div className="content-block cta-block">
        <div className="cta-content">
            <div className="cta-badge">
                <Sparkles size={16} />
                <span>Get Started Today</span>
            </div>

            <h2 className="cta-headline">
                Ready to Begin<br />
                <span className="cta-highlight">Your Journey?</span>
            </h2>

            <p className="cta-description">
                Enter your email to receive your login credentials, or sign in if you already have an account.
            </p>

            <div className={`email-capture-container ${isEmailFocused ? 'focused' : ''} ${emailSubmitState}`}>
                {emailSubmitState === 'success' ? (
                    <div className="email-success">
                        <div className="success-icon">
                            <CheckCircle size={32} />
                        </div>
                        <h3>Credentials Sent!</h3>
                        <p>Check your inbox for login details.</p>
                    </div>
                ) : (
                    <form onSubmit={handleEmailSubmit} className="email-form">
                        <div className="email-input-wrapper">
                            <Mail className="email-icon" size={20} />
                            <input
                                ref={emailInputRef}
                                type="email"
                                placeholder="Enter your email address"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                onFocus={() => setIsEmailFocused(true)}
                                onBlur={() => setIsEmailFocused(false)}
                                onKeyDown={handleEmailKeyDown}
                                className="email-input"
                                disabled={emailSubmitState === 'loading'}
                            />
                            <button
                                type="submit"
                                className={`email-submit-btn ${isValidEmail(email) ? 'valid' : ''}`}
                                disabled={!isValidEmail(email) || emailSubmitState === 'loading'}
                            >
                                {emailSubmitState === 'loading' ? (
                                    <Loader2 size={20} className="spin" />
                                ) : (
                                    <Send size={20} />
                                )}
                            </button>
                        </div>
                        <div className="email-hint">
                            {email && !isValidEmail(email) && (
                                <span className="email-error">Please enter a valid email</span>
                            )}
                        </div>
                    </form>
                )}
            </div>

            <div className="cta-divider">
                <span>or</span>
            </div>

            <div className={`login-option ${showLoginOption ? 'highlight' : ''}`}>
                <p className="login-text">Already have credentials?</p>
                <button className="login-button" onClick={handleLoginTransition}>
                    <LogIn size={20} />
                    <span>Sign In</span>
                    <ArrowRight size={18} className="login-arrow" />
                </button>
            </div>

            <div className="trust-indicators">
                {TRUST_INDICATORS.map((indicator, index) => (
                    <div key={index} className="trust-item">
                        <CheckCircle size={16} />
                        <span>{indicator}</span>
                    </div>
                ))}
            </div>
        </div>

        <div className="cta-footer">
            <p>Cohort Community Platform © 2025</p>
        </div>
    </div>
);

// ============================================
// MAIN COMPONENT
// ============================================

const ParallaxIntro = () => {
    const navigate = useNavigate();
    const [scrollY, setScrollY] = useState(0);
    const [isTransitioning, setIsTransitioning] = useState(false);

    // Email capture states
    const [email, setEmail] = useState('');
    const [isEmailFocused, setIsEmailFocused] = useState(false);
    const [emailSubmitState, setEmailSubmitState] = useState('idle');
    const [showLoginOption, setShowLoginOption] = useState(false);
    const emailInputRef = useRef(null);

    // Memoized ambient particles
    const ambientParticles = useMemo(() => generateAmbientParticles(20), []);

    // Scroll effect
    useEffect(() => {
        const handleScroll = () => {
            setScrollY(window.scrollY);
        };

        window.addEventListener('scroll', handleScroll, { passive: true });
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    // Event handlers
    const handleLoginTransition = () => {
        setIsTransitioning(true);
        setTimeout(() => {
            navigate('/login');
        }, 600);
    };

    const handleEmailSubmit = async (e) => {
        e.preventDefault();
        if (!isValidEmail(email)) return;

        setEmailSubmitState('loading');

        try {
            // TODO: Replace with actual API call
            await new Promise(resolve => setTimeout(resolve, 1500));
            setEmailSubmitState('success');

            setTimeout(() => {
                setShowLoginOption(true);
            }, 1000);
        } catch (error) {
            setEmailSubmitState('error');
        }
    };

    const handleEmailKeyDown = (e) => {
        if (e.key === 'Enter' && isValidEmail(email)) {
            handleEmailSubmit(e);
        }
    };

    return (
        <div className="parallax-intro-container">
            <div className={`transition-overlay ${isTransitioning ? 'active' : ''}`} />

            <section className="unified-intro-section">
                <AmbientBackground particles={ambientParticles} />

                <HeroBlock scrollY={scrollY} />
                <SolutionBlock scrollY={scrollY} />
                <PillarsBlock />
                <MentorshipBlock />
                <InstitutionBlock />
                <CTABlock
                    email={email}
                    setEmail={setEmail}
                    isEmailFocused={isEmailFocused}
                    setIsEmailFocused={setIsEmailFocused}
                    emailSubmitState={emailSubmitState}
                    handleEmailSubmit={handleEmailSubmit}
                    handleEmailKeyDown={handleEmailKeyDown}
                    showLoginOption={showLoginOption}
                    handleLoginTransition={handleLoginTransition}
                    emailInputRef={emailInputRef}
                />
            </section>
        </div>
    );
};

export default ParallaxIntro;
