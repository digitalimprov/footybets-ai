import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { HelmetProvider } from 'react-helmet-async';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Predictions from './pages/Predictions';
import Analytics from './pages/Analytics';
import Games from './pages/Games';
import GameDetail from './pages/GameDetail';
import Tips from './pages/Tips';
import Scraping from './pages/Scraping';
import Login from './pages/Login';
import Register from './pages/Register';
import AdminDashboard from './pages/AdminDashboard';
import AdminGenerateContent from './pages/AdminGenerateContent';
import AdminSettings from './pages/AdminSettings';
import AdminAnalytics from './pages/AdminAnalytics';
import ProtectedRoute from './components/ProtectedRoute';
import './App.css';

// Maintenance mode configuration
const MAINTENANCE_MODE = false;

// Maintenance mode component
const MaintenanceMode = () => {
  useEffect(() => {
    // Redirect to maintenance page
    window.location.href = '/maintenance.html';
  }, []);

  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      height: '100vh',
      backgroundColor: '#667eea',
      color: 'white',
      fontFamily: 'Arial, sans-serif'
    }}>
      <div style={{ textAlign: 'center' }}>
        <h1>FootyBets.ai</h1>
        <p>🔧 Under Maintenance</p>
        <p>Redirecting to maintenance page...</p>
        <p>If you're not redirected, <a href="/maintenance.html" style={{ color: '#ffeb3b' }}>click here</a></p>
      </div>
    </div>
  );
};

function App() {
  const [isMaintenanceMode, setIsMaintenanceMode] = useState(MAINTENANCE_MODE);
  const [adminBypass, setAdminBypass] = useState(false);

  useEffect(() => {
    // Check for admin bypass
    const checkAdminBypass = () => {
      const bypass = localStorage.getItem('maintenance_bypass');
      const bypassTime = localStorage.getItem('maintenance_bypass_time');
      const now = Date.now();
      const oneHour = 60 * 60 * 1000;
      
      if (bypass === 'true' && bypassTime && (now - bypassTime < oneHour)) {
        setAdminBypass(true);
        return true;
      }
      
      // Clear expired bypass
      localStorage.removeItem('maintenance_bypass');
      localStorage.removeItem('maintenance_bypass_time');
      setAdminBypass(false);
      return false;
    };

    // Check URL parameters for admin bypass
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('admin_bypass') === 'true') {
      localStorage.setItem('maintenance_bypass', 'true');
      localStorage.setItem('maintenance_bypass_time', Date.now());
      setAdminBypass(true);
      
      // Clean URL
      window.history.replaceState({}, document.title, window.location.pathname);
    } else {
      checkAdminBypass();
    }
  }, []);

  // Show maintenance mode if enabled and no admin bypass
  if (isMaintenanceMode && !adminBypass) {
    return <MaintenanceMode />;
  }

  return (
    <HelmetProvider>
      <AuthProvider>
        <Router>
          <div className="min-h-screen bg-gray-50">
            {/* Maintenance notice for admins */}
            {isMaintenanceMode && adminBypass && (
              <div style={{
                background: 'linear-gradient(90deg, #ff6b6b, #ee5a24)',
                color: 'white',
                padding: '0.5rem',
                textAlign: 'center',
                fontSize: '0.9rem',
                fontWeight: '600',
                position: 'sticky',
                top: 0,
                zIndex: 1000,
                boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
              }}>
                ⚠️ MAINTENANCE MODE ACTIVE - Admin Access Only
                <button 
                  onClick={() => {
                    localStorage.removeItem('maintenance_bypass');
                    localStorage.removeItem('maintenance_bypass_time');
                    window.location.reload();
                  }}
                  style={{
                    marginLeft: '1rem',
                    background: 'rgba(255,255,255,0.2)',
                    border: '1px solid rgba(255,255,255,0.3)',
                    color: 'white',
                    padding: '0.25rem 0.5rem',
                    borderRadius: '4px',
                    fontSize: '0.8rem',
                    cursor: 'pointer'
                  }}
                >
                  Exit Admin Mode
                </button>
              </div>
            )}
            
            <Navbar />
            <main className="container mx-auto px-4 py-8">
              <Routes>
                {/* Main pages */}
                <Route path="/" element={<Home />} />
                <Route path="/dashboard" element={<Dashboard />} />
                
                {/* SEO-optimized tips and predictions */}
                <Route path="/afl-betting-tips" element={<Tips />} />
                <Route path="/afl-betting-tips/round-:roundNumber" element={<Tips />} />
                <Route path="/afl-betting-tips/:season" element={<Tips />} />
                <Route path="/afl-betting-tips/team/:teamSlug" element={<Tips />} />
                <Route path="/afl-betting-tips/upcoming" element={<Tips />} />
                <Route path="/afl-betting-tips/today" element={<Tips />} />
                <Route path="/afl-betting-tips/weekend" element={<Tips />} />
                
                {/* Individual game predictions (SEO gold) */}
                <Route path="/afl-prediction/:homeTeam-vs-:awayTeam-round-:round-:season" element={<GameDetail />} />
                <Route path="/afl-betting-tips/:homeTeam-vs-:awayTeam-round-:round-:season" element={<GameDetail />} />
                <Route path="/afl-analysis/:homeTeam-vs-:awayTeam-round-:round-:season" element={<GameDetail />} />
                
                {/* Team pages */}
                <Route path="/afl-team/:teamSlug/predictions" element={<Predictions />} />
                <Route path="/afl-team/:teamSlug/betting-tips" element={<Tips />} />
                <Route path="/afl-team/:teamSlug/statistics" element={<Analytics />} />
                <Route path="/afl-team/:teamSlug/history" element={<Analytics />} />
                
                {/* Analytics and stats */}
                <Route path="/afl-analytics" element={<Analytics />} />
                <Route path="/afl-analytics/performance" element={<Analytics />} />
                <Route path="/afl-analytics/accuracy" element={<Analytics />} />
                <Route path="/afl-analytics/trends" element={<Analytics />} />
                <Route path="/afl-analytics/comparison" element={<Analytics />} />
                
                {/* Games and fixtures */}
                <Route path="/afl-fixtures" element={<Games />} />
                <Route path="/afl-fixtures/upcoming" element={<Games />} />
                <Route path="/afl-fixtures/results" element={<Games />} />
                <Route path="/afl-fixtures/:season" element={<Games />} />
                <Route path="/afl-fixtures/:season/round-:round" element={<Games />} />
                
                {/* AI Predictions */}
                <Route path="/ai-predictions" element={<Predictions />} />
                <Route path="/ai-predictions/upcoming" element={<Predictions />} />
                <Route path="/ai-predictions/accuracy" element={<Predictions />} />
                <Route path="/ai-predictions/generate" element={<Predictions />} />
                
                {/* Legacy routes (redirects) */}
                <Route path="/tips" element={<Tips />} />
                <Route path="/predictions" element={<Predictions />} />
                <Route path="/analytics" element={<Analytics />} />
                <Route path="/games" element={<Games />} />
                <Route path="/games/:gameId" element={<GameDetail />} />
                
                {/* Admin routes (hidden from SEO) */}
                <Route path="/admin/login" element={<Login />} />
                <Route 
                  path="/admin/scraping" 
                  element={
                    <ProtectedRoute requireAdmin={true}>
                      <Scraping />
                    </ProtectedRoute>
                  } 
                />
                <Route 
                  path="/admin/dashboard" 
                  element={
                    <ProtectedRoute requireAdmin={true}>
                      <AdminDashboard />
                    </ProtectedRoute>
                  } 
                />
                <Route 
                  path="/admin/generate-content" 
                  element={
                    <ProtectedRoute requireAdmin={true}>
                      <AdminGenerateContent />
                    </ProtectedRoute>
                  } 
                />
                <Route 
                  path="/admin/settings" 
                  element={
                    <ProtectedRoute requireAdmin={true}>
                      <AdminSettings />
                    </ProtectedRoute>
                  } 
                />
                <Route 
                  path="/admin/analytics" 
                  element={
                    <ProtectedRoute requireAdmin={true}>
                      <AdminAnalytics />
                    </ProtectedRoute>
                  } 
                />
                
                {/* Authentication routes */}
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route 
                  path="/scraping" 
                  element={
                    <ProtectedRoute requireAdmin={true}>
                      <Scraping />
                    </ProtectedRoute>
                  } 
                />
              </Routes>
            </main>
            <Toaster position="top-right" />
          </div>
        </Router>
      </AuthProvider>
    </HelmetProvider>
  );
}

export default App; 