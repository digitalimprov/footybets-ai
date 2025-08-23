import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet-async';
import { 
  UsersIcon, 
  ChartBarIcon, 
  ShieldCheckIcon, 
  DocumentTextIcon,
  CogIcon,
  EyeIcon,
  PencilIcon,
  TrashIcon,
  CheckCircleIcon,
  XCircleIcon,
  LockClosedIcon,
  LockOpenIcon,
  UserPlusIcon,
  UserMinusIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';
import apiService from '../services/apiService';
import { useAuth } from '../context/AuthContext';
import toast from 'react-hot-toast';
import SEO from '../components/SEO';

const AdminDashboard = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Overview/Stats state
  const [systemStats, setSystemStats] = useState(null);
  
  // User management state
  const [users, setUsers] = useState([]);
  const [userFilters, setUserFilters] = useState({
    role: '',
    subscription_tier: '',
    is_active: '',
    search: ''
  });
  const [selectedUser, setSelectedUser] = useState(null);
  const [showUserModal, setShowUserModal] = useState(false);
  const [userUpdateData, setUserUpdateData] = useState({});
  
  // Security logs state
  const [securityLogs, setSecurityLogs] = useState([]);
  const [logFilters, setLogFilters] = useState({
    user_id: '',
    event_type: '',
    success: ''
  });
  
  // Content management state
  const [content, setContent] = useState([]);
  const [contentFilters, setContentFilters] = useState({
    status: 'all',
    search: ''
  });
  const [selectedContent, setSelectedContent] = useState(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);

  useEffect(() => {
    if (user && user.is_admin) {
      loadDashboardData();
    } else if (user && !user.is_admin) {
      setError('Access denied. Admin privileges required.');
      setLoading(false);
    }
  }, [user, activeTab]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      switch (activeTab) {
        case 'overview':
          await loadSystemStats();
          break;
        case 'users':
          await loadUsers();
          break;
        case 'security':
          await loadSecurityLogs();
          break;
        case 'content':
          await loadContent();
          break;
        default:
          await loadSystemStats();
      }
    } catch (error) {
      console.error('Error loading dashboard data:', error);
      setError(`Failed to load ${activeTab} data. ${error.message || 'Please try again.'}`);
      toast.error(`Failed to load ${activeTab} data`);
    } finally {
      setLoading(false);
    }
  };

  const loadSystemStats = async () => {
    try {
      const stats = await apiService.getSystemStats();
      setSystemStats(stats);
    } catch (error) {
      console.error('Error loading system stats:', error);
      if (error.response?.status === 401) {
        toast.error('Authentication required. Please log in again.');
        window.location.href = '/login';
      } else {
        // Set mock data for development/testing
        const mockStats = {
          total_users: 1245,
          active_users: 892,
          admin_users: 3,
          recent_registrations: 24,
          users_by_role: {
            "user": 1100,
            "subscriber": 142,
            "admin": 3
          },
          users_by_subscription: {
            "free": 1100,
            "basic": 89,
            "premium": 53,
            "pro": 3
          }
        };
        setSystemStats(mockStats);
        toast.warning('Using mock data - backend unavailable');
      }
    }
  };

  const loadUsers = async () => {
    try {
      const params = {};
      if (userFilters.role) params.role = userFilters.role;
      if (userFilters.subscription_tier) params.subscription_tier = userFilters.subscription_tier;
      if (userFilters.is_active !== '') params.is_active = userFilters.is_active === 'true';
      if (userFilters.search) params.search = userFilters.search;
      
      const usersData = await apiService.getUsers(params);
      setUsers(Array.isArray(usersData) ? usersData : []);
    } catch (error) {
      console.error('Error loading users:', error);
      if (error.response?.status === 401) {
        toast.error('Authentication required. Please log in again.');
        window.location.href = '/login';
      } else {
        // Set mock users for development/testing
        const mockUsers = [
          {
            id: 1,
            email: "admin@footybets.ai",
            username: "admin",
            is_active: true,
            is_verified: true,
            subscription_tier: "admin",
            roles: ["admin"],
            is_admin: true
          },
          {
            id: 2,
            email: "user@example.com",
            username: "testuser",
            is_active: true,
            is_verified: true,
            subscription_tier: "premium",
            roles: ["subscriber"],
            is_admin: false
          }
        ];
        setUsers(mockUsers);
        toast.warning('Using mock data - backend unavailable');
      }
    }
  };

  const loadSecurityLogs = async () => {
    try {
      const params = {};
      if (logFilters.user_id) params.user_id = logFilters.user_id;
      if (logFilters.event_type) params.event_type = logFilters.event_type;
      if (logFilters.success !== '') params.success = logFilters.success === 'true';
      
      const logsData = await apiService.getSecurityLogs(params);
      setSecurityLogs(logsData.logs || []);
    } catch (error) {
      console.error('Error loading security logs:', error);
      // Set mock security logs for development/testing
      const mockLogs = [
        {
          id: 1,
          user_id: 1,
          event_type: "login",
          success: true,
          created_at: new Date().toISOString(),
          details: { ip_address: "127.0.0.1" }
        },
        {
          id: 2,
          user_id: 1,
          event_type: "admin_users_viewed",
          success: true,
          created_at: new Date(Date.now() - 3600000).toISOString(),
          details: { action: "viewed_user_list" }
        }
      ];
      setSecurityLogs(mockLogs);
      toast.warning('Using mock data - backend unavailable');
    }
  };

  const loadContent = async () => {
    try {
      const response = await apiService.getContent({ limit: 100 });
      const contentData = response.data || response || [];
      setContent(Array.isArray(contentData) ? contentData : []);
    } catch (error) {
      console.error('Error loading content:', error);
      // Set mock content for development/testing
      const mockContent = [
        {
          id: 1,
          title: "AFL Season 2024 Preview",
          slug: "afl-season-2024-preview",
          content_type: "article",
          status: "published",
          view_count: 1250,
          created_at: new Date().toISOString()
        },
        {
          id: 2,
          title: "Round 15 Predictions",
          slug: "round-15-predictions",
          content_type: "prediction",
          status: "draft",
          view_count: 0,
          created_at: new Date(Date.now() - 86400000).toISOString()
        }
      ];
      setContent(mockContent);
      toast.warning('Using mock data - backend unavailable');
    }
  };

  const handleUserUpdate = async () => {
    if (!selectedUser) return;
    
    try {
      await apiService.updateUser(selectedUser.id, userUpdateData);
      toast.success('User updated successfully!');
      setShowUserModal(false);
      setSelectedUser(null);
      setUserUpdateData({});
      loadUsers();
    } catch (error) {
      console.error('Error updating user:', error);
      toast.error('Failed to update user');
    }
  };

  const handlePromoteToAdmin = async (userId) => {
    try {
      await apiService.promoteUserToAdmin(userId);
      toast.success('User promoted to admin successfully!');
      loadUsers();
    } catch (error) {
      console.error('Error promoting user:', error);
      toast.error('Failed to promote user');
    }
  };

  const handleDemoteFromAdmin = async (userId) => {
    try {
      await apiService.demoteUserFromAdmin(userId);
      toast.success('User demoted from admin successfully!');
      loadUsers();
    } catch (error) {
      console.error('Error demoting user:', error);
      toast.error('Failed to demote user');
    }
  };

  const handleUpgradeSubscription = async (userId, tier, duration = 30) => {
    try {
      await apiService.upgradeUserSubscription(userId, tier, duration);
      toast.success(`User upgraded to ${tier} subscription!`);
      loadUsers();
    } catch (error) {
      console.error('Error upgrading subscription:', error);
      toast.error('Failed to upgrade subscription');
    }
  };

  const handleDowngradeSubscription = async (userId) => {
    try {
      await apiService.downgradeUserSubscription(userId);
      toast.success('User downgraded to free subscription!');
      loadUsers();
    } catch (error) {
      console.error('Error downgrading subscription:', error);
      toast.error('Failed to downgrade subscription');
    }
  };

  const handleUnlockAccount = async (userId) => {
    try {
      await apiService.unlockUserAccount(userId);
      toast.success('User account unlocked successfully!');
      loadUsers();
    } catch (error) {
      console.error('Error unlocking account:', error);
      toast.error('Failed to unlock account');
    }
  };

  const handleContentStatusChange = async (contentId, newStatus) => {
    try {
      if (newStatus === 'published') {
        await apiService.publishContent(contentId);
        toast.success('Content published successfully!');
      } else if (newStatus === 'archived') {
        await apiService.archiveContent(contentId);
        toast.success('Content archived successfully!');
      }
      loadContent();
    } catch (error) {
      console.error('Error updating content status:', error);
      toast.error('Failed to update content status');
    }
  };

  const handleDeleteContent = async () => {
    if (!selectedContent) return;
    
    try {
      await apiService.deleteContent(selectedContent.id);
      toast.success('Content deleted successfully!');
      setShowDeleteModal(false);
      setSelectedContent(null);
      loadContent();
    } catch (error) {
      console.error('Error deleting content:', error);
      toast.error('Failed to delete content');
    }
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      published: { color: 'bg-green-100 text-green-800', label: 'Published' },
      draft: { color: 'bg-yellow-100 text-yellow-800', label: 'Draft' },
      archived: { color: 'bg-gray-100 text-gray-800', label: 'Archived' },
      scheduled: { color: 'bg-blue-100 text-blue-800', label: 'Scheduled' }
    };
    
    const config = statusConfig[status] || statusConfig.draft;
    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.color}`}>
        {config.label}
      </span>
    );
  };

  const getContentTypeIcon = (contentType) => {
    const icons = {
      article: '📄',
      analysis: '📊',
      prediction: '🎯',
      brownlow: '🏆',
      news: '📰',
      game_analysis: '⚽',
      team_preview: '👥'
    };
    return icons[contentType] || '📝';
  };

  const filteredContent = content.filter(item => {
    const matchesFilter = contentFilters.status === 'all' || item.status === contentFilters.status;
    const matchesSearch = item.title.toLowerCase().includes(contentFilters.search.toLowerCase()) ||
                         item.content_type.toLowerCase().includes(contentFilters.search.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!user.is_admin) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Access Denied</h1>
          <p className="text-gray-600">You need admin privileges to access this page.</p>
          <button 
            onClick={() => window.location.href = '/dashboard'}
            className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
          >
            Go to Dashboard
          </button>
        </div>
      </div>
    );
  }

  const tabs = [
    { id: 'overview', name: 'Overview', icon: ChartBarIcon },
    { id: 'users', name: 'User Management', icon: UsersIcon },
    { id: 'security', name: 'Security Logs', icon: ShieldCheckIcon },
    { id: 'content', name: 'Content Management', icon: DocumentTextIcon },
  ];

  return (
    <>
      <SEO 
        title="Admin Dashboard - FootyBets.ai"
        description="Admin dashboard for managing users, content, and system settings"
        noindex={true}
        nofollow={true}
      />
      
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <div className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-6">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
                <p className="text-gray-600">Manage users, content, and system settings</p>
              </div>
              <div className="flex space-x-3">
                <button
                  onClick={() => window.location.href = '/admin/generate-content'}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium"
                >
                  + Generate Content
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
          ) : error ? (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
              <strong className="font-bold">Error!</strong>
              <span className="block sm:inline"> {error}</span>
            </div>
          ) : (
            <>
              {/* Overview Tab */}
              {activeTab === 'overview' && systemStats && (
                <div className="space-y-6">
                  {/* System Stats Cards */}
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <div className="bg-white rounded-lg shadow p-6">
                      <div className="flex items-center">
                        <div className="p-2 bg-blue-100 rounded-lg">
                          <UsersIcon className="w-6 h-6 text-blue-600" />
                        </div>
                        <div className="ml-4">
                          <p className="text-sm font-medium text-gray-600">Total Users</p>
                          <p className="text-2xl font-bold text-gray-900">{systemStats.total_users}</p>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow p-6">
                      <div className="flex items-center">
                        <div className="p-2 bg-green-100 rounded-lg">
                          <CheckCircleIcon className="w-6 h-6 text-green-600" />
                        </div>
                        <div className="ml-4">
                          <p className="text-sm font-medium text-gray-600">Active Users</p>
                          <p className="text-2xl font-bold text-gray-900">{systemStats.active_users}</p>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow p-6">
                      <div className="flex items-center">
                        <div className="p-2 bg-purple-100 rounded-lg">
                          <CogIcon className="w-6 h-6 text-purple-600" />
                        </div>
                        <div className="ml-4">
                          <p className="text-sm font-medium text-gray-600">Admin Users</p>
                          <p className="text-2xl font-bold text-gray-900">{systemStats.admin_users}</p>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow p-6">
                      <div className="flex items-center">
                        <div className="p-2 bg-yellow-100 rounded-lg">
                          <UserPlusIcon className="w-6 h-6 text-yellow-600" />
                        </div>
                        <div className="ml-4">
                          <p className="text-sm font-medium text-gray-600">Recent Registrations</p>
                          <p className="text-2xl font-bold text-gray-900">{systemStats.recent_registrations}</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Detailed Stats */}
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div className="bg-white rounded-lg shadow p-6">
                      <h3 className="text-lg font-medium text-gray-900 mb-4">Users by Role</h3>
                      <div className="space-y-3">
                        {Object.entries(systemStats.users_by_role).map(([role, count]) => (
                          <div key={role} className="flex justify-between items-center">
                            <span className="text-sm font-medium text-gray-600 capitalize">{role}</span>
                            <span className="text-sm font-bold text-gray-900">{count}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow p-6">
                      <h3 className="text-lg font-medium text-gray-900 mb-4">Users by Subscription</h3>
                      <div className="space-y-3">
                        {Object.entries(systemStats.users_by_subscription).map(([tier, count]) => (
                          <div key={tier} className="flex justify-between items-center">
                            <span className="text-sm font-medium text-gray-600 capitalize">{tier}</span>
                            <span className="text-sm font-bold text-gray-900">{count}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Users Tab */}
              {activeTab === 'users' && (
                <div className="space-y-6">
                  {/* User Filters */}
                  <div className="bg-white rounded-lg shadow p-6">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                      <input
                        type="text"
                        placeholder="Search users..."
                        value={userFilters.search}
                        onChange={(e) => setUserFilters({...userFilters, search: e.target.value})}
                        className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                      <select
                        value={userFilters.role}
                        onChange={(e) => setUserFilters({...userFilters, role: e.target.value})}
                        className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="">All Roles</option>
                        <option value="user">User</option>
                        <option value="subscriber">Subscriber</option>
                        <option value="admin">Admin</option>
                        <option value="moderator">Moderator</option>
                      </select>
                      <select
                        value={userFilters.subscription_tier}
                        onChange={(e) => setUserFilters({...userFilters, subscription_tier: e.target.value})}
                        className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="">All Subscriptions</option>
                        <option value="free">Free</option>
                        <option value="basic">Basic</option>
                        <option value="premium">Premium</option>
                        <option value="pro">Pro</option>
                      </select>
                      <select
                        value={userFilters.is_active}
                        onChange={(e) => setUserFilters({...userFilters, is_active: e.target.value})}
                        className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="">All Status</option>
                        <option value="true">Active</option>
                        <option value="false">Inactive</option>
                      </select>
                    </div>
                    <div className="mt-4">
                      <button
                        onClick={loadUsers}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md"
                      >
                        Apply Filters
                      </button>
                    </div>
                  </div>

                  {/* Users Table */}
                  <div className="bg-white rounded-lg shadow overflow-hidden">
                    <div className="overflow-x-auto">
                      <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                          <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              User
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              Status
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              Subscription
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              Roles
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              Actions
                            </th>
                          </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                          {users.map((user) => (
                            <tr key={user.id} className="hover:bg-gray-50">
                              <td className="px-6 py-4 whitespace-nowrap">
                                <div>
                                  <div className="text-sm font-medium text-gray-900">{user.username}</div>
                                  <div className="text-sm text-gray-500">{user.email}</div>
                                </div>
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap">
                                <div className="flex items-center space-x-2">
                                  {user.is_active ? (
                                    <CheckCircleIcon className="w-5 h-5 text-green-500" />
                                  ) : (
                                    <XCircleIcon className="w-5 h-5 text-red-500" />
                                  )}
                                  <span className={`text-sm ${user.is_active ? 'text-green-800' : 'text-red-800'}`}>
                                    {user.is_active ? 'Active' : 'Inactive'}
                                  </span>
                                </div>
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap">
                                <span className="text-sm text-gray-900 capitalize">{user.subscription_tier}</span>
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap">
                                <div className="flex flex-wrap gap-1">
                                  {user.roles.map((role) => (
                                    <span key={role} className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                      {role}
                                    </span>
                                  ))}
                                </div>
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                <div className="flex space-x-2">
                                  <button
                                    onClick={() => {
                                      setSelectedUser(user);
                                      setUserUpdateData({});
                                      setShowUserModal(true);
                                    }}
                                    className="text-blue-600 hover:text-blue-900"
                                  >
                                    Edit
                                  </button>
                                  {!user.is_admin ? (
                                    <button
                                      onClick={() => handlePromoteToAdmin(user.id)}
                                      className="text-green-600 hover:text-green-900"
                                    >
                                      Promote
                                    </button>
                                  ) : (
                                    <button
                                      onClick={() => handleDemoteFromAdmin(user.id)}
                                      className="text-orange-600 hover:text-orange-900"
                                    >
                                      Demote
                                    </button>
                                  )}
                                  {user.subscription_tier === 'free' ? (
                                    <button
                                      onClick={() => handleUpgradeSubscription(user.id, 'basic')}
                                      className="text-purple-600 hover:text-purple-900"
                                    >
                                      Upgrade
                                    </button>
                                  ) : (
                                    <button
                                      onClick={() => handleDowngradeSubscription(user.id)}
                                      className="text-red-600 hover:text-red-900"
                                    >
                                      Downgrade
                                    </button>
                                  )}
                                </div>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              )}

              {/* Security Tab */}
              {activeTab === 'security' && (
                <div className="space-y-6">
                  {/* Security Log Filters */}
                  <div className="bg-white rounded-lg shadow p-6">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <input
                        type="text"
                        placeholder="User ID"
                        value={logFilters.user_id}
                        onChange={(e) => setLogFilters({...logFilters, user_id: e.target.value})}
                        className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                      <select
                        value={logFilters.event_type}
                        onChange={(e) => setLogFilters({...logFilters, event_type: e.target.value})}
                        className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="">All Events</option>
                        <option value="login">Login</option>
                        <option value="logout">Logout</option>
                        <option value="admin_users_viewed">Admin Users Viewed</option>
                        <option value="admin_user_updated">Admin User Updated</option>
                      </select>
                      <select
                        value={logFilters.success}
                        onChange={(e) => setLogFilters({...logFilters, success: e.target.value})}
                        className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="">All Results</option>
                        <option value="true">Success</option>
                        <option value="false">Failed</option>
                      </select>
                    </div>
                    <div className="mt-4">
                      <button
                        onClick={loadSecurityLogs}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md"
                      >
                        Apply Filters
                      </button>
                    </div>
                  </div>

                  {/* Security Logs Table */}
                  <div className="bg-white rounded-lg shadow overflow-hidden">
                    <div className="overflow-x-auto">
                      <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                          <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              Timestamp
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              User
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              Event
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              Success
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              Details
                            </th>
                          </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                          {securityLogs.map((log) => (
                            <tr key={log.id} className="hover:bg-gray-50">
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                {new Date(log.created_at).toLocaleString()}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                {log.user_id}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                {log.event_type}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap">
                                {log.success ? (
                                  <CheckCircleIcon className="w-5 h-5 text-green-500" />
                                ) : (
                                  <XCircleIcon className="w-5 h-5 text-red-500" />
                                )}
                              </td>
                              <td className="px-6 py-4 text-sm text-gray-900">
                                <details className="cursor-pointer">
                                  <summary className="hover:text-blue-600">View Details</summary>
                                  <pre className="mt-2 text-xs bg-gray-100 p-2 rounded overflow-auto">
                                    {JSON.stringify(log.details, null, 2)}
                                  </pre>
                                </details>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              )}

              {/* Content Tab */}
              {activeTab === 'content' && (
                <div className="space-y-6">
                  {/* Content Filters */}
                  <div className="bg-white rounded-lg shadow p-6">
                    <div className="flex flex-col sm:flex-row gap-4">
                      <div className="flex-1">
                        <input
                          type="text"
                          placeholder="Search content by title or type..."
                          value={contentFilters.search}
                          onChange={(e) => setContentFilters({...contentFilters, search: e.target.value})}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      </div>
                      <div className="flex space-x-2">
                        <select
                          value={contentFilters.status}
                          onChange={(e) => setContentFilters({...contentFilters, status: e.target.value})}
                          className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                          <option value="all">All Content</option>
                          <option value="published">Published</option>
                          <option value="draft">Drafts</option>
                          <option value="archived">Archived</option>
                        </select>
                      </div>
                    </div>
                  </div>

                  {/* Content Table */}
                  <div className="bg-white rounded-lg shadow">
                    <div className="overflow-x-auto">
                      <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                          <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              Content
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              Type
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              Status
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              Views
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              Created
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              Actions
                            </th>
                          </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                          {filteredContent.map((item) => (
                            <tr key={item.id} className="hover:bg-gray-50">
                              <td className="px-6 py-4 whitespace-nowrap">
                                <div className="flex items-center">
                                  <div className="text-2xl mr-3">
                                    {getContentTypeIcon(item.content_type)}
                                  </div>
                                  <div>
                                    <div className="text-sm font-medium text-gray-900">
                                      {item.title}
                                    </div>
                                    <div className="text-sm text-gray-500">
                                      {item.slug}
                                    </div>
                                  </div>
                                </div>
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap">
                                <span className="text-sm text-gray-900 capitalize">
                                  {item.content_type.replace('_', ' ')}
                                </span>
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap">
                                {getStatusBadge(item.status)}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                {item.view_count || 0}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                {new Date(item.created_at).toLocaleDateString()}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                <div className="flex space-x-2">
                                  <button
                                    onClick={() => window.open(`/content/${item.slug}`, '_blank')}
                                    className="text-blue-600 hover:text-blue-900"
                                  >
                                    View
                                  </button>
                                  <button
                                    onClick={() => window.location.href = `/admin/edit/${item.id}`}
                                    className="text-green-600 hover:text-green-900"
                                  >
                                    Edit
                                  </button>
                                  {item.status === 'draft' && (
                                    <button
                                      onClick={() => handleContentStatusChange(item.id, 'published')}
                                      className="text-purple-600 hover:text-purple-900"
                                    >
                                      Publish
                                    </button>
                                  )}
                                  {item.status === 'published' && (
                                    <button
                                      onClick={() => handleContentStatusChange(item.id, 'archived')}
                                      className="text-orange-600 hover:text-orange-900"
                                    >
                                      Archive
                                    </button>
                                  )}
                                  <button
                                    onClick={() => {
                                      setSelectedContent(item);
                                      setShowDeleteModal(true);
                                    }}
                                    className="text-red-600 hover:text-red-900"
                                  >
                                    Delete
                                  </button>
                                </div>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>

      {/* User Edit Modal */}
      {showUserModal && selectedUser && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Edit User: {selectedUser.username}</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Active Status</label>
                  <select
                    value={userUpdateData.is_active !== undefined ? userUpdateData.is_active : selectedUser.is_active}
                    onChange={(e) => setUserUpdateData({...userUpdateData, is_active: e.target.value === 'true'})}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value={true}>Active</option>
                    <option value={false}>Inactive</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Verified Status</label>
                  <select
                    value={userUpdateData.is_verified !== undefined ? userUpdateData.is_verified : selectedUser.is_verified}
                    onChange={(e) => setUserUpdateData({...userUpdateData, is_verified: e.target.value === 'true'})}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value={true}>Verified</option>
                    <option value={false}>Not Verified</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Subscription Tier</label>
                  <select
                    value={userUpdateData.subscription_tier || selectedUser.subscription_tier}
                    onChange={(e) => setUserUpdateData({...userUpdateData, subscription_tier: e.target.value})}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="free">Free</option>
                    <option value="basic">Basic</option>
                    <option value="premium">Premium</option>
                    <option value="pro">Pro</option>
                  </select>
                </div>
              </div>
              <div className="flex justify-center space-x-4 mt-6">
                <button
                  onClick={() => setShowUserModal(false)}
                  className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
                >
                  Cancel
                </button>
                <button
                  onClick={handleUserUpdate}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Update User
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3 text-center">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Delete Content</h3>
              <p className="text-sm text-gray-500 mb-6">
                Are you sure you want to delete "{selectedContent?.title}"? This action cannot be undone.
              </p>
              <div className="flex justify-center space-x-4">
                <button
                  onClick={() => setShowDeleteModal(false)}
                  className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
                >
                  Cancel
                </button>
                <button
                  onClick={handleDeleteContent}
                  className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default AdminDashboard; 