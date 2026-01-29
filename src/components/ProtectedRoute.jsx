import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ProtectedRoute = ({ children, requiredRole }) => {
    const { user, hasAccess, loading } = useAuth();
    const location = useLocation();

    if (loading) {
        return (
            <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                minHeight: '100vh',
                fontSize: '1.5rem',
                color: 'var(--text-secondary)'
            }}>
                Loading...
            </div>
        );
    }

    if (!user) {
        return <Navigate to="/login" state={{ from: location }} replace />;
    }

    // Check for required role if specified
    if (requiredRole) {
        const userRole = user.role || user.profile?.role;
        if (userRole !== requiredRole) {
            return (
                <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    minHeight: '100vh',
                    padding: '2rem',
                    textAlign: 'center'
                }}>
                    <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>🚫</h1>
                    <h2 style={{ marginBottom: '0.5rem' }}>Access Denied</h2>
                    <p style={{ color: 'var(--text-secondary)' }}>
                        You don't have permission to access this page.
                    </p>
                </div>
            );
        }
    }

    if (!hasAccess(location.pathname)) {
        return (
            <div style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                minHeight: '100vh',
                padding: '2rem',
                textAlign: 'center'
            }}>
                <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>🚫</h1>
                <h2 style={{ marginBottom: '0.5rem' }}>Access Denied</h2>
                <p style={{ color: 'var(--text-secondary)' }}>
                    You don't have permission to access this page.
                </p>
            </div>
        );
    }

    return children;
};

export default ProtectedRoute;
