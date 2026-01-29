import React, { createContext, useContext, useState } from 'react';
import authService from '../services/auth';

const AuthContext = createContext();

// Role-based access control configuration
const ROLE_ACCESS = {
    STUDENT: ['/', '/clt', '/sri', '/cfc', '/iipc', '/scd', '/games', '/hackathons', '/monthly-report', '/profile-settings'],
    MENTOR: ['/mentor-dashboard', '/mentor-dashboard/students', '/mentor-dashboard/pillar-review', '/mentor-dashboard/announcements'],
    FLOOR_WING: ['/floorwing-dashboard'],
    ADMIN: [
        '/admin/campus-select',
        '/admin/campus',
        '/admin-dashboard',
        '/admin/students',
        '/admin/mentors',
        '/admin/assignments',
        '/admin/floors',
        '/admin/submissions',
        '/admin/rules',
        '/admin/communication',
        '/admin/leaderboard',
        '/admin/notifications',
        '/admin/roles',
        '/admin/settings'
    ],
};

// Role home paths
const ROLE_HOME_PATHS = {
    STUDENT: '/',
    MENTOR: '/mentor-dashboard',
    FLOOR_WING: '/floorwing-dashboard',
    ADMIN: '/admin/campus-select'
};

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(() => {
        // Initialize state from localStorage
        return authService.getCurrentUser();
    });
    const [loading, setLoading] = useState(false);

    const login = async (username, password, role) => {
        try {
            setLoading(true);
            const response = await authService.login(username, password);

            // Extract role from backend response (profile.role)
            const userRole = response.user?.profile?.role || role || 'STUDENT';
            const campus = response.user?.profile?.campus;
            const floor = response.user?.profile?.floor;

            const userWithRole = {
                ...response.user,
                role: userRole,
                campus: campus,
                floor: floor,
                timestamp: new Date().toISOString(),
            };

            setUser(userWithRole);
            localStorage.setItem('user', JSON.stringify(userWithRole));
            return userWithRole;
        } catch (error) {
            console.error('Login failed:', error);
            throw error;
        } finally {
            setLoading(false);
        }
    };

    const logout = () => {
        authService.logout();
        setUser(null);
    };

    const hasAccess = (path) => {
        if (!user) return false;
        const allowedPaths = ROLE_ACCESS[user.role] || [];
        // Check for exact match or if path starts with an allowed path
        return allowedPaths.some(allowedPath =>
            path === allowedPath || path.startsWith(allowedPath + '/')
        ) || path === '/login';
    };

    const getToken = () => {
        return authService.getAccessToken();
    };

    const getHomePath = () => {
        if (!user || !user.role) return '/login';
        return ROLE_HOME_PATHS[user.role] || '/login';
    };

    const value = {
        user,
        login,
        logout,
        hasAccess,
        loading,
        isAuthenticated: authService.isAuthenticated(),
        getToken,
        getHomePath,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export function useAuth() {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider');
    }
    return context;
}
