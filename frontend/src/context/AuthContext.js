import React, { createContext, useContext, useState, useEffect } from 'react';
import apiService from '../services/apiService';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Temporary admin user for testing
const TEMP_ADMIN_USER = {
  id: 1,
  email: "admin@footybets.ai",
  username: "admin",
  full_name: "System Administrator",
  is_active: true,
  is_verified: true,
  is_admin: true,
  subscription_tier: "admin",
  subscription_status: "active",
  is_subscriber: true,
  roles: ["admin"],
  permissions: ["read_users", "write_users", "read_system", "write_system", "view_security_logs"],
  created_at: new Date().toISOString(),
  last_login: new Date().toISOString()
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check if user is logged in on app start and verify with backend
  useEffect(() => {
    const initializeAuth = async () => {
      const token = localStorage.getItem('accessToken');
      const userData = localStorage.getItem('userData');
      
      if (token && userData) {
        try {
          const parsedUserData = JSON.parse(userData);
          setUser(parsedUserData);
          
          // Verify token with backend and get updated user data
          try {
            const currentUser = await apiService.getCurrentUser();
            if (currentUser) {
              // Update user data if backend has newer info
              setUser(currentUser);
              localStorage.setItem('userData', JSON.stringify(currentUser));
            }
          } catch (error) {
            console.error('Error verifying user with backend:', error);
            // If token is invalid, clear stored data
            if (error.response?.status === 401) {
              localStorage.removeItem('accessToken');
              localStorage.removeItem('userData');
              setUser(null);
            }
          }
        } catch (error) {
          console.error('Error parsing user data:', error);
          localStorage.removeItem('accessToken');
          localStorage.removeItem('userData');
          setUser(null);
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, []);

  const login = (userData, token) => {
    console.log('Logging in user:', userData);
    setUser(userData);
    localStorage.setItem('accessToken', token);
    localStorage.setItem('userData', JSON.stringify(userData));
  };

  const loginAsTestAdmin = () => {
    console.log('Logging in as test admin for development');
    setUser(TEMP_ADMIN_USER);
    localStorage.setItem('accessToken', 'test_admin_token');
    localStorage.setItem('userData', JSON.stringify(TEMP_ADMIN_USER));
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('accessToken');
    localStorage.removeItem('userData');
  };

  const isAdmin = () => {
    const adminStatus = user && (user.is_admin === true || user.roles?.includes('admin'));
    console.log('Admin check:', { user, is_admin: user?.is_admin, roles: user?.roles, adminStatus });
    return adminStatus;
  };

  const isSubscriber = () => {
    return user && (user.is_subscriber || user.roles?.includes('subscriber'));
  };

  const hasPermission = (permission) => {
    if (!user) return false;
    return user.permissions?.includes(permission) || isAdmin();
  };

  const value = {
    user,
    loading,
    login,
    loginAsTestAdmin,
    logout,
    isAdmin,
    isSubscriber,
    hasPermission,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 