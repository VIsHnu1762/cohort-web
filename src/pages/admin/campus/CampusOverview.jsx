import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useParams, useNavigate } from 'react-router-dom';
import { Users, UserCheck, Clock, ChevronRight, ArrowLeft } from 'lucide-react';
import GlassCard from '../../../components/GlassCard';
import Button from '../../../components/Button';
import { getCampusOverview } from '../../../services/admin';
import './CampusOverview.css';

function CampusOverview() {
    const { campus } = useParams();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [campusData, setCampusData] = useState(null);

    useEffect(() => {
        loadCampusData();
    }, [campus]);

    const loadCampusData = async () => {
        try {
            const data = await getCampusOverview(campus);
            setCampusData(data);
        } catch (error) {
            console.error('Failed to load campus data:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="campus-overview-container">
                <div style={{ textAlign: 'center', padding: '3rem' }}>Loading...</div>
            </div>
        );
    }

    if (!campusData) {
        return (
            <div className="campus-overview-container">
                <div style={{ textAlign: 'center', padding: '3rem' }}>Failed to load campus data</div>
            </div>
        );
    }

    // Helper for subtitle label
    const floorLabel = campus === 'TECH' ? 'Floors' : 'Years';
    return (
        <div className="campus-overview-container">
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="campus-overview-header"
            >
                <div>
                    <Button
                        variant="secondary"
                        size="small"
                        onClick={() => navigate('/admin/campus-select')}
                        style={{ marginBottom: '1rem' }}
                    >
                        <ArrowLeft size={16} />
                        Back to Campus Selection
                    </Button>
                    <h1 className="campus-overview-title">{campusData.campus_name}</h1>
                    <p className="campus-overview-subtitle">
                        {campusData.floors?.length || 0} {floorLabel} - Manage {floorLabel.toLowerCase()} wings, mentors, and students
                    </p>
                </div>
            </motion.div>

            <div className="floors-grid">
                {campusData.floors?.map((floor, index) => (
                    <motion.div
                        key={floor.floor}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: index * 0.1 }}
                    >
                        <GlassCard
                            hoverable
                            onClick={() => navigate(`/admin/campus/${campus}/floor/${floor.floor}`)}
                            style={{ cursor: 'pointer', height: '100%' }}
                        >
                            <div className="floor-card">
                                <div className="floor-header">
                                    <div>
                                        <h2 className="floor-title">{floor.floor_name}</h2>
                                        <p className="floor-subtitle">{campus === 'TECH' ? 'Engineering Floor' : ''}</p>
                                    </div>
                                    <ChevronRight size={24} color="var(--primary-color)" />
                                </div>

                                <div className="floor-stats">
                                    <div className="floor-stat">
                                        <Users size={20} color="#2196F3" />
                                        <span className="stat-number">{floor.total_students}</span>
                                        <span className="stat-label">Students</span>
                                    </div>
                                    <div className="floor-stat">
                                        <UserCheck size={20} color="#4CAF50" />
                                        <span className="stat-number">{floor.total_mentors}</span>
                                        <span className="stat-label">Mentors</span>
                                    </div>
                                </div>

                                <div className="floor-wing-info">
                                    {floor.floor_wing ? (
                                        <div className="floor-wing-assigned">
                                            <span className="fw-label">Floor Wing:</span>
                                            <span className="fw-name">{floor.floor_wing}</span>
                                        </div>
                                    ) : (
                                        <div className="floor-wing-unassigned">
                                            <Clock size={16} />
                                            <span>No Floor Wing assigned</span>
                                        </div>
                                    )}
                                </div>

                                {floor.submissions && (
                                    <div className="submission-stats">
                                        <div className="progress-bar">
                                            <div 
                                                className="progress-fill"
                                                style={{ 
                                                    width: `${floor.submissions.progress_percentage}%`,
                                                    background: 'linear-gradient(90deg, #4CAF50, #8BC34A)'
                                                }}
                                            />
                                        </div>
                                        <div className="submission-details">
                                            <span className="detail-item approved">
                                                ✓ {floor.submissions.approved} Approved
                                            </span>
                                            <span className="detail-item pending">
                                                ⏳ {floor.submissions.pending} Pending
                                            </span>
                                            <span className="detail-item rejected">
                                                ✗ {floor.submissions.rejected} Rejected
                                            </span>
                                        </div>
                                    </div>
                                )}
                            </div>
                        </GlassCard>
                    </motion.div>
                ))}
            </div>
        </div>
    );
}

export default CampusOverview;
