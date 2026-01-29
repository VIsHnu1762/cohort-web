import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import AdminSidebar from './components/AdminSidebar';
import './AdminLayout.css';

const AdminLayout = () => {
    const [isCollapsed, setIsCollapsed] = useState(false);

    return (
        <div className="admin-layout">
            <AdminSidebar isCollapsed={isCollapsed} setIsCollapsed={setIsCollapsed} />
            <div className={`admin-content ${isCollapsed ? 'admin-content--sidebar-collapsed' : ''}`}>
                <Outlet />
            </div>
        </div>
    );
};

export default AdminLayout;
