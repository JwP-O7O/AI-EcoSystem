import React from 'react';
import { Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage';
import BuilderPage from './pages/BuilderPage';
import CheckoutPage from './pages/CheckoutPage';
import ConfirmationPage from './pages/ConfirmationPage';
import LoginPage from './pages/LoginPage';
import DashboardLayout from './layouts/DashboardLayout';
import AgentsPage from './pages/dashboard/AgentsPage';
import AccountPage from './pages/dashboard/AccountPage';
import Header from './components/Header';
import Footer from './components/Footer';

function App() {
  return (
    <div className="bg-brand-dark text-slate-200 min-h-screen flex flex-col">
      <Header />
      <main className="flex-grow">
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />

          {/* Semi-Public (can be part of dashboard or public) */}
          <Route path="/builder" element={<BuilderPage />} />
          <Route path="/checkout" element={<CheckoutPage />} />
          <Route path="/confirmation" element={<ConfirmationPage />} />

          {/* Protected Dashboard Routes */}
          <Route path="/dashboard" element={<DashboardLayout />}>
            <Route index element={<AgentsPage />} />
            <Route path="agents" element={<AgentsPage />} />
            <Route path="account" element={<AccountPage />} />
          </Route>
        </Routes>
      </main>
      <Footer />
    </div>
  );
}

export default App;