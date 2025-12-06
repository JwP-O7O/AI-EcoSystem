import React from 'react';
import { useAuth } from '../../hooks/useAuth';


const AccountPage = () => {
    const { user } = useAuth();
    return (
        <div>
            <h1 className="text-3xl font-bold text-white mb-6">Account Settings</h1>
            <div className="bg-brand-secondary p-8 rounded-xl border border-slate-700">
                 <div className="space-y-4">
                    <div>
                        <label className="text-sm font-medium text-slate-400">Username</label>
                        <p className="text-lg text-white font-semibold mt-1">{user?.name}</p>
                    </div>
                     <div>
                        <label className="text-sm font-medium text-slate-400">Email (from checkout)</label>
                        <p className="text-lg text-white font-semibold mt-1">user@example.com (placeholder)</p>
                    </div>
                     <div className="border-t border-slate-700 pt-4">
                         <p className="text-slate-400">More account and preference management options will be available here soon.</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AccountPage;