import React, { useEffect } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import { useAuth } from '../hooks/useAuth';

const DashboardLayout = () => {
    const { user } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        if (!user) {
            navigate('/login', { state: { from: '/dashboard' } });
        }
    }, [user, navigate]);

    if (!user) {
        // Render a loader or nothing while redirecting
        return (
            <div className="w-full h-screen flex items-center justify-center">
                <p className="text-white">Loading Command Center...</p>
            </div>
        );
    }

    return (
        <div className="container mx-auto px-6 py-8">
            <div className="flex flex-col md:flex-row gap-8">
                <aside className="w-full md:w-64 flex-shrink-0">
                    <Sidebar />
                </aside>
                <section className="flex-grow">
                    <Outlet />
                </section>
            </div>
        </div>
    );
};

export default DashboardLayout;