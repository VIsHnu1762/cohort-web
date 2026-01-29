import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import MentorHome from './MentorHome';
import MentorDashboard from './MentorDashboard';
import PillarReview from './PillarReview';
import Announcements from './Announcements';
import './MentorLayout.css';

function MentorLayout() {
    return (
        <div className="mentor-layout">
            <Routes>
                <Route index element={<MentorHome />} />
                <Route path="students" element={<MentorDashboard />} />
                <Route path="pillar-review" element={<PillarReview />} />
                <Route path="announcements" element={<Announcements />} />
                <Route path="*" element={<Navigate to="/mentor-dashboard" replace />} />
            </Routes>
        </div>
    );
}

export default MentorLayout;
