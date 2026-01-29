import React from 'react';
import { motion } from 'framer-motion';
import { Trophy, Medal, TrendingUp, Award } from 'lucide-react';
import GlassCard from '../../../components/GlassCard';
import './Leaderboard.css';

const Leaderboard = () => {
    const topStudents = [
        { rank: 1, name: 'Amal Krishna', xp: 4850, pillarsCompleted: 5, avatar: 'AK' },
        { rank: 2, name: 'Sreeram', xp: 4520, pillarsCompleted: 5, avatar: 'SR' },
        { rank: 3, name: 'Vishnu', xp: 4200, pillarsCompleted: 4, avatar: 'VI' },
        { rank: 4, name: 'Athira', xp: 3890, pillarsCompleted: 4, avatar: 'AT' },
        { rank: 5, name: 'Rahul', xp: 3650, pillarsCompleted: 4, avatar: 'RA' },
        { rank: 6, name: 'Priya', xp: 3420, pillarsCompleted: 3, avatar: 'PR' },
        { rank: 7, name: 'Karthik', xp: 3180, pillarsCompleted: 3, avatar: 'KA' },
        { rank: 8, name: 'Anjali', xp: 2950, pillarsCompleted: 3, avatar: 'AN' },
        { rank: 9, name: 'Arjun', xp: 2720, pillarsCompleted: 2, avatar: 'AR' },
        { rank: 10, name: 'Meera', xp: 2500, pillarsCompleted: 2, avatar: 'ME' },
    ];

    return (
        <div className="leaderboard-page">
            <motion.div
                className="page-header"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <div>
                    <h1 className="page-title">
                        <Trophy size={32} />
                        Leaderboard
                    </h1>
                    <p className="page-subtitle">Top performing students in the cohort</p>
                </div>
            </motion.div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
            >
                <GlassCard>
                    <div className="leaderboard-container">
                        {topStudents.map((student, index) => (
                            <motion.div
                                key={student.rank}
                                className={`leaderboard-item ${student.rank <= 3 ? 'top-three' : ''}`}
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: 0.15 + index * 0.05 }}
                            >
                                <div className="rank-badge" data-rank={student.rank}>
                                    {student.rank <= 3 ? (
                                        <Medal size={24} className={`medal-${student.rank}`} />
                                    ) : (
                                        <span className="rank-number">#{student.rank}</span>
                                    )}
                                </div>
                                <div className="student-avatar">{student.avatar}</div>
                                <div className="student-details">
                                    <h3 className="student-name">{student.name}</h3>
                                    <div className="student-stats">
                                        <span><Award size={14} /> {student.pillarsCompleted} pillars</span>
                                    </div>
                                </div>
                                <div className="xp-display">
                                    <TrendingUp size={16} />
                                    <span className="xp-value">{student.xp.toLocaleString()} XP</span>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </GlassCard>
            </motion.div>
        </div>
    );
};

export default Leaderboard;
