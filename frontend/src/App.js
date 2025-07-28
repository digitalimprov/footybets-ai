import React from 'react';
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

function App() {
  return (
    <HelmetProvider>
      <AuthProvider>
        <Router>
          <div className="min-h-screen bg-gray-50">
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