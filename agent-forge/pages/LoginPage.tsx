import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const navigate = useNavigate();
    const location = useLocation();
    const { login } = useAuth();

    const from = location.state?.from || '/dashboard';

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (username.trim()) {
            login(username);
            navigate(from, { replace: true });
        }
    };

    return (
        <div className="container mx-auto px-6 py-20 flex justify-center items-center">
            <div className="w-full max-w-md">
                <div className="bg-brand-secondary border border-slate-700 rounded-xl p-8 shadow-2xl shadow-brand-accent-end/10">
                    <h1 className="text-3xl font-extrabold text-center text-white mb-6">Command Center Access</h1>
                    <p className="text-center text-slate-400 mb-8">Log in to manage your forged agents.</p>
                    <form onSubmit={handleSubmit}>
                        <div className="space-y-6">
                            <div>
                                <label htmlFor="username" className="block text-sm font-medium text-slate-300 mb-2">Username</label>
                                <input
                                    type="text"
                                    id="username"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    className="w-full bg-slate-800 border border-slate-600 rounded-lg p-3 text-white focus:ring-brand-accent-start focus:border-brand-accent-start"
                                    placeholder="YourName"
                                    required
                                />
                            </div>
                        </div>
                        <div className="mt-8">
                            <button
                                type="submit"
                                className="w-full bg-gradient-to-r from-brand-accent-start to-brand-accent-end text-black font-bold py-3 rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50"
                            >
                                Login
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;