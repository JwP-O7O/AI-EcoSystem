import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
    const currentYear = new Date().getFullYear();
    return (
        <footer className="bg-brand-secondary mt-16">
            <div className="container mx-auto px-6 py-8">
                <div className="flex flex-col md:flex-row justify-between items-center">
                    <p className="text-slate-400 text-center md:text-left">&copy; {currentYear} AgentForge. All Rights Reserved.</p>
                    <div className="flex space-x-4 mt-4 md:mt-0">
                        <Link to="/" className="text-slate-400 hover:text-white transition-colors">Terms of Service</Link>
                        <Link to="/" className="text-slate-400 hover:text-white transition-colors">Privacy Policy</Link>
                    </div>
                </div>
            </div>
        </footer>
    );
};

export default Footer;