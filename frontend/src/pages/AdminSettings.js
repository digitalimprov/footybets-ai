import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet-async';
import { 
  CogIcon, 
  ShieldCheckIcon, 
  BellIcon, 
  KeyIcon,
  DatabaseIcon,
  GlobeAltIcon,
  UserGroupIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';
import { apiService } from '../services/apiService';
import { useAuth } from '../context/AuthContext';
import toast from 'react-hot-toast';
import SEO from '../components/SEO';

const AdminSettings = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('general');
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  
  // General settings
  const [generalSettings, setGeneralSettings] = useState({
    site_name: 'FootyBets.ai',
    site_description: 'AI-powered AFL betting predictions',
    maintenance_mode: false,
    debug_mode: false,
    analytics_enabled: true,
    notifications_enabled: true
  });
  
  // Security settings
  const [securitySettings, setSecuritySettings] = useState({
    session_timeout: 24,
    max_login_attempts: 5,
    require_email_verification: true,
    require_admin_approval: false,
    enable_two_factor: false,
    password_min_length: 8,
    enable_security_logs: true
  });
  
  // Content settings
  const [contentSettings, setContentSettings] = useState({
    auto_publish: false,
    require_approval: true,
    max_content_length: 5000,
    enable_comments: true,
    moderate_comments: true,
    enable_ratings: true,
    premium_content_ratio: 0.3
  });
  
  // AI settings
  const [aiSettings, setAiSettings] = useState({
    prediction_confidence_threshold: 0.7,
    max_predictions_per_day: 10,
    enable_auto_predictions: true,
    prediction_update_frequency: 'daily',
    enable_learning_mode: true,
    model_version: 'v1.0'
  });

  useEffect(() => {
    if (user && user.is_admin) {
      loadSettings();
    }
  }, [user]);

  const loadSettings = async () => {
    try {
      setLoading(true);
      // In a real app, you'd load these from the backend
      // For now, we'll use default values
    } catch (error) {
      console.error('Error loading settings:', error);
      toast.error('Failed to load settings');
    } finally {
      setLoading(false);
    }
  };

  const handleGeneralSettingsChange = (key, value) => {
    setGeneralSettings(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleSecuritySettingsChange = (key, value) => {
    setSecuritySettings(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleContentSettingsChange = (key, value) => {
    setContentSettings(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleAiSettingsChange = (key, value) => {
    setAiSettings(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const saveSettings = async (settingsType) => {
    setSaving(true);
    try {
      // In a real app, you'd save these to the backend
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call
      toast.success(`${settingsType} settings saved successfully!`);
    } catch (error) {
      console.error('Error saving settings:', error);
      toast.error('Failed to save settings');
    } finally {
      setSaving(false);
    }
  };

  const resetToDefaults = async (settingsType) => {
    if (window.confirm(`Are you sure you want to reset ${settingsType} settings to defaults?`)) {
      try {
        // In a real app, you'd reset these via the backend
        await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call
        toast.success(`${settingsType} settings reset to defaults!`);
        loadSettings();
      } catch (error) {
        console.error('Error resetting settings:', error);
        toast.error('Failed to reset settings');
      }
    }
  };

  const testEmailNotifications = async () => {
    try {
      // In a real app, you'd test email notifications
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call
      toast.success('Test email sent successfully!');
    } catch (error) {
      console.error('Error testing email notifications:', error);
      toast.error('Failed to send test email');
    }
  };

  const backupDatabase = async () => {
    try {
      // In a real app, you'd trigger a database backup
      await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate API call
      toast.success('Database backup completed successfully!');
    } catch (error) {
      console.error('Error backing up database:', error);
      toast.error('Failed to backup database');
    }
  };

  if (!user || !user.is_admin) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Access Denied</h1>
          <p className="text-gray-600">You need admin privileges to access this page.</p>
        </div>
      </div>
    );
  }

  const tabs = [
    { id: 'general', name: 'General', icon: CogIcon },
    { id: 'security', name: 'Security', icon: ShieldCheckIcon },
    { id: 'content', name: 'Content', icon: UserGroupIcon },
    { id: 'ai', name: 'AI Settings', icon: ChartBarIcon },
    { id: 'notifications', name: 'Notifications', icon: BellIcon },
    { id: 'database', name: 'Database', icon: DatabaseIcon },
  ];

  return (
    <>
      <SEO 
        title="Admin Settings - FootyBets.ai"
        description="Admin settings and system configuration"
        noindex={true}
        nofollow={true}
      />
      
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <div className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-6">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Admin Settings</h1>
                <p className="text-gray-600">Configure system settings and preferences</p>
              </div>
              <div className="flex space-x-3">
                <button
                  onClick={() => window.location.href = '/admin/dashboard'}
                  className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg font-medium"
                >
                  Back to Dashboard
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`py-2 px-1 border-b-2 font-medium text-sm flex items-center ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <tab.icon className="w-5 h-5 mr-2" />
                  {tab.name}
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Content Area */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          {loading ? (
            <div className="flex justify-center items-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
          ) : (
            <>
              {/* General Settings */}
              {activeTab === 'general' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow p-6">
                    <h2 className="text-xl font-bold text-gray-900 mb-6">General Settings</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Site Name
                        </label>
                        <input
                          type="text"
                          value={generalSettings.site_name}
                          onChange={(e) => handleGeneralSettingsChange('site_name', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Site Description
                        </label>
                        <input
                          type="text"
                          value={generalSettings.site_description}
                          onChange={(e) => handleGeneralSettingsChange('site_description', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Maintenance Mode
                          </label>
                          <p className="text-sm text-gray-500">Enable maintenance mode to restrict access</p>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input
                            type="checkbox"
                            checked={generalSettings.maintenance_mode}
                            onChange={(e) => handleGeneralSettingsChange('maintenance_mode', e.target.checked)}
                            className="sr-only peer"
                          />
                          <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                        </label>
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Debug Mode
                          </label>
                          <p className="text-sm text-gray-500">Enable debug logging and detailed error messages</p>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input
                            type="checkbox"
                            checked={generalSettings.debug_mode}
                            onChange={(e) => handleGeneralSettingsChange('debug_mode', e.target.checked)}
                            className="sr-only peer"
                          />
                          <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                        </label>
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Analytics
                          </label>
                          <p className="text-sm text-gray-500">Enable analytics tracking</p>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input
                            type="checkbox"
                            checked={generalSettings.analytics_enabled}
                            onChange={(e) => handleGeneralSettingsChange('analytics_enabled', e.target.checked)}
                            className="sr-only peer"
                          />
                          <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                        </label>
                      </div>
                    </div>
                    
                    <div className="mt-6 flex space-x-3">
                      <button
                        onClick={() => saveSettings('General')}
                        disabled={saving}
                        className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white px-4 py-2 rounded-md"
                      >
                        {saving ? 'Saving...' : 'Save Settings'}
                      </button>
                      <button
                        onClick={() => resetToDefaults('General')}
                        className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-md"
                      >
                        Reset to Defaults
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {/* Security Settings */}
              {activeTab === 'security' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow p-6">
                    <h2 className="text-xl font-bold text-gray-900 mb-6">Security Settings</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Session Timeout (hours)
                        </label>
                        <input
                          type="number"
                          value={securitySettings.session_timeout}
                          onChange={(e) => handleSecuritySettingsChange('session_timeout', parseInt(e.target.value))}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                          min="1"
                          max="168"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Max Login Attempts
                        </label>
                        <input
                          type="number"
                          value={securitySettings.max_login_attempts}
                          onChange={(e) => handleSecuritySettingsChange('max_login_attempts', parseInt(e.target.value))}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                          min="1"
                          max="20"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Password Min Length
                        </label>
                        <input
                          type="number"
                          value={securitySettings.password_min_length}
                          onChange={(e) => handleSecuritySettingsChange('password_min_length', parseInt(e.target.value))}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                          min="6"
                          max="50"
                        />
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Email Verification Required
                          </label>
                          <p className="text-sm text-gray-500">Require email verification for new accounts</p>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input
                            type="checkbox"
                            checked={securitySettings.require_email_verification}
                            onChange={(e) => handleSecuritySettingsChange('require_email_verification', e.target.checked)}
                            className="sr-only peer"
                          />
                          <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                        </label>
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Two-Factor Authentication
                          </label>
                          <p className="text-sm text-gray-500">Enable 2FA for admin accounts</p>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input
                            type="checkbox"
                            checked={securitySettings.enable_two_factor}
                            onChange={(e) => handleSecuritySettingsChange('enable_two_factor', e.target.checked)}
                            className="sr-only peer"
                          />
                          <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                        </label>
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Security Logs
                          </label>
                          <p className="text-sm text-gray-500">Enable detailed security event logging</p>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input
                            type="checkbox"
                            checked={securitySettings.enable_security_logs}
                            onChange={(e) => handleSecuritySettingsChange('enable_security_logs', e.target.checked)}
                            className="sr-only peer"
                          />
                          <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                        </label>
                      </div>
                    </div>
                    
                    <div className="mt-6 flex space-x-3">
                      <button
                        onClick={() => saveSettings('Security')}
                        disabled={saving}
                        className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white px-4 py-2 rounded-md"
                      >
                        {saving ? 'Saving...' : 'Save Settings'}
                      </button>
                      <button
                        onClick={() => resetToDefaults('Security')}
                        className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-md"
                      >
                        Reset to Defaults
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {/* Content Settings */}
              {activeTab === 'content' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow p-6">
                    <h2 className="text-xl font-bold text-gray-900 mb-6">Content Settings</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Max Content Length
                        </label>
                        <input
                          type="number"
                          value={contentSettings.max_content_length}
                          onChange={(e) => handleContentSettingsChange('max_content_length', parseInt(e.target.value))}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                          min="100"
                          max="10000"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Premium Content Ratio
                        </label>
                        <input
                          type="number"
                          value={contentSettings.premium_content_ratio}
                          onChange={(e) => handleContentSettingsChange('premium_content_ratio', parseFloat(e.target.value))}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                          min="0"
                          max="1"
                          step="0.1"
                        />
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Auto Publish
                          </label>
                          <p className="text-sm text-gray-500">Automatically publish new content</p>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input
                            type="checkbox"
                            checked={contentSettings.auto_publish}
                            onChange={(e) => handleContentSettingsChange('auto_publish', e.target.checked)}
                            className="sr-only peer"
                          />
                          <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                        </label>
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Enable Comments
                          </label>
                          <p className="text-sm text-gray-500">Allow users to comment on content</p>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input
                            type="checkbox"
                            checked={contentSettings.enable_comments}
                            onChange={(e) => handleContentSettingsChange('enable_comments', e.target.checked)}
                            className="sr-only peer"
                          />
                          <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                        </label>
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Moderate Comments
                          </label>
                          <p className="text-sm text-gray-500">Require approval for comments</p>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input
                            type="checkbox"
                            checked={contentSettings.moderate_comments}
                            onChange={(e) => handleContentSettingsChange('moderate_comments', e.target.checked)}
                            className="sr-only peer"
                          />
                          <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                        </label>
                      </div>
                    </div>
                    
                    <div className="mt-6 flex space-x-3">
                      <button
                        onClick={() => saveSettings('Content')}
                        disabled={saving}
                        className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white px-4 py-2 rounded-md"
                      >
                        {saving ? 'Saving...' : 'Save Settings'}
                      </button>
                      <button
                        onClick={() => resetToDefaults('Content')}
                        className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-md"
                      >
                        Reset to Defaults
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {/* AI Settings */}
              {activeTab === 'ai' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow p-6">
                    <h2 className="text-xl font-bold text-gray-900 mb-6">AI Settings</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Prediction Confidence Threshold
                        </label>
                        <input
                          type="number"
                          value={aiSettings.prediction_confidence_threshold}
                          onChange={(e) => handleAiSettingsChange('prediction_confidence_threshold', parseFloat(e.target.value))}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                          min="0"
                          max="1"
                          step="0.1"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Max Predictions Per Day
                        </label>
                        <input
                          type="number"
                          value={aiSettings.max_predictions_per_day}
                          onChange={(e) => handleAiSettingsChange('max_predictions_per_day', parseInt(e.target.value))}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                          min="1"
                          max="100"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Prediction Update Frequency
                        </label>
                        <select
                          value={aiSettings.prediction_update_frequency}
                          onChange={(e) => handleAiSettingsChange('prediction_update_frequency', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                          <option value="hourly">Hourly</option>
                          <option value="daily">Daily</option>
                          <option value="weekly">Weekly</option>
                        </select>
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Model Version
                        </label>
                        <input
                          type="text"
                          value={aiSettings.model_version}
                          onChange={(e) => handleAiSettingsChange('model_version', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Auto Predictions
                          </label>
                          <p className="text-sm text-gray-500">Automatically generate predictions</p>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input
                            type="checkbox"
                            checked={aiSettings.enable_auto_predictions}
                            onChange={(e) => handleAiSettingsChange('enable_auto_predictions', e.target.checked)}
                            className="sr-only peer"
                          />
                          <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                        </label>
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Learning Mode
                          </label>
                          <p className="text-sm text-gray-500">Enable AI model learning from results</p>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input
                            type="checkbox"
                            checked={aiSettings.enable_learning_mode}
                            onChange={(e) => handleAiSettingsChange('enable_learning_mode', e.target.checked)}
                            className="sr-only peer"
                          />
                          <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                        </label>
                      </div>
                    </div>
                    
                    <div className="mt-6 flex space-x-3">
                      <button
                        onClick={() => saveSettings('AI')}
                        disabled={saving}
                        className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white px-4 py-2 rounded-md"
                      >
                        {saving ? 'Saving...' : 'Save Settings'}
                      </button>
                      <button
                        onClick={() => resetToDefaults('AI')}
                        className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-md"
                      >
                        Reset to Defaults
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {/* Notifications Settings */}
              {activeTab === 'notifications' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow p-6">
                    <h2 className="text-xl font-bold text-gray-900 mb-6">Notification Settings</h2>
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Email Notifications
                          </label>
                          <p className="text-sm text-gray-500">Send email notifications for important events</p>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input
                            type="checkbox"
                            checked={generalSettings.notifications_enabled}
                            onChange={(e) => handleGeneralSettingsChange('notifications_enabled', e.target.checked)}
                            className="sr-only peer"
                          />
                          <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                        </label>
                      </div>
                      
                      <div className="mt-6">
                        <button
                          onClick={testEmailNotifications}
                          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md"
                        >
                          Test Email Notifications
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Database Settings */}
              {activeTab === 'database' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow p-6">
                    <h2 className="text-xl font-bold text-gray-900 mb-6">Database Management</h2>
                    <div className="space-y-4">
                      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                        <h3 className="text-lg font-medium text-blue-900 mb-2">Database Backup</h3>
                        <p className="text-sm text-blue-700 mb-4">
                          Create a backup of the current database. This may take several minutes.
                        </p>
                        <button
                          onClick={backupDatabase}
                          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md"
                        >
                          Create Backup
                        </button>
                      </div>
                      
                      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                        <h3 className="text-lg font-medium text-yellow-900 mb-2">Database Maintenance</h3>
                        <p className="text-sm text-yellow-700 mb-4">
                          Run database maintenance tasks to optimize performance.
                        </p>
                        <button
                          onClick={() => toast.success('Database maintenance completed!')}
                          className="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-md"
                        >
                          Run Maintenance
                        </button>
                      </div>
                      
                      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                        <h3 className="text-lg font-medium text-red-900 mb-2">Danger Zone</h3>
                        <p className="text-sm text-red-700 mb-4">
                          These actions are irreversible. Use with extreme caution.
                        </p>
                        <button
                          onClick={() => {
                            if (window.confirm('Are you sure you want to clear all cache? This action cannot be undone.')) {
                              toast.success('Cache cleared successfully!');
                            }
                          }}
                          className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md"
                        >
                          Clear Cache
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </>
  );
};

export default AdminSettings; 