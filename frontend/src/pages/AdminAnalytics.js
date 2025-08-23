import React, { useState, useEffect } from 'react';
import { 
  ChartBarIcon,
  CalendarIcon,
  TrendingUpIcon,
  TrendingDownIcon,
  EyeIcon,
  UserIcon,
  DocumentTextIcon,
  ClockIcon
} from '@heroicons/react/24/outline';
import apiService from '../services/apiService';
import { useAuth } from '../context/AuthContext';
import toast from 'react-hot-toast';
import SEO from '../components/SEO';

const AdminAnalytics = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('7d');
  
  // Analytics data
  const [systemStats, setSystemStats] = useState(null);
  const [userAnalytics, setUserAnalytics] = useState(null);
  const [contentAnalytics, setContentAnalytics] = useState(null);
  const [performanceMetrics, setPerformanceMetrics] = useState(null);

  useEffect(() => {
    if (user && user.is_admin) {
      loadAnalytics();
    }
  }, [user, timeRange]);

  const loadAnalytics = async () => {
    try {
      setLoading(true);
      
      // Load system stats
      const stats = await apiService.getSystemStats();
      setSystemStats(stats);
      
      // Load user analytics (mock data for now)
      setUserAnalytics({
        new_users: { today: 12, week: 89, month: 342 },
        active_users: { today: 156, week: 892, month: 3245 },
        user_retention: { day_1: 85, day_7: 62, day_30: 45 },
        top_referrers: [
          { source: 'Google', users: 1245, percentage: 45 },
          { source: 'Direct', users: 892, percentage: 32 },
          { source: 'Social Media', users: 456, percentage: 16 },
          { source: 'Other', users: 234, percentage: 7 }
        ]
      });
      
      // Load content analytics (mock data for now)
      setContentAnalytics({
        total_content: 156,
        published_content: 142,
        draft_content: 14,
        content_views: { today: 2345, week: 15678, month: 45678 },
        top_content: [
          { title: 'AFL Round 15 Predictions', views: 1234, engagement: 89 },
          { title: 'Brownlow Medal Analysis', views: 987, engagement: 76 },
          { title: 'Team Performance Review', views: 756, engagement: 65 },
          { title: 'Betting Tips Guide', views: 654, engagement: 54 }
        ]
      });
      
      // Load performance metrics (mock data for now)
      setPerformanceMetrics({
        response_time: { avg: 245, p95: 890, p99: 1200 },
        error_rate: { total: 0.12, api: 0.08, frontend: 0.04 },
        uptime: { current: 99.8, month: 99.5, year: 99.2 },
        server_load: { cpu: 45, memory: 62, disk: 23 }
      });
      
    } catch (error) {
      console.error('Error loading analytics:', error);
      toast.error('Failed to load analytics data');
    } finally {
      setLoading(false);
    }
  };

  const formatNumber = (num) => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
  };

  const formatPercentage = (num) => {
    return num.toFixed(1) + '%';
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
    { id: 'overview', name: 'Overview', icon: ChartBarIcon },
    { id: 'users', name: 'User Analytics', icon: UserIcon },
    { id: 'content', name: 'Content Analytics', icon: EyeIcon },
    { id: 'performance', name: 'Performance', icon: TrendingUpIcon },
  ];

  return (
    <>
      <SEO 
        title="Admin Analytics - FootyBets.ai"
        description="Detailed analytics and system metrics"
        noindex={true}
        nofollow={true}
      />
      
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <div className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-6">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Admin Analytics</h1>
                <p className="text-gray-600">Detailed system metrics and performance data</p>
              </div>
              <div className="flex space-x-3">
                <select
                  value={timeRange}
                  onChange={(e) => setTimeRange(e.target.value)}
                  className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="1d">Last 24 hours</option>
                  <option value="7d">Last 7 days</option>
                  <option value="30d">Last 30 days</option>
                  <option value="90d">Last 90 days</option>
                </select>
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
              {/* Overview Tab */}
              {activeTab === 'overview' && systemStats && (
                <div className="space-y-6">
                  {/* Key Metrics */}
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <div className="bg-white rounded-lg shadow p-6">
                      <div className="flex items-center">
                        <div className="p-2 bg-blue-100 rounded-lg">
                          <UserIcon className="w-6 h-6 text-blue-600" />
                        </div>
                        <div className="ml-4">
                          <p className="text-sm font-medium text-gray-600">Total Users</p>
                          <p className="text-2xl font-bold text-gray-900">{formatNumber(systemStats.total_users)}</p>
                          <p className="text-xs text-green-600">+12% from last month</p>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow p-6">
                      <div className="flex items-center">
                        <div className="p-2 bg-green-100 rounded-lg">
                          <TrendingUpIcon className="w-6 h-6 text-green-600" />
                        </div>
                        <div className="ml-4">
                          <p className="text-sm font-medium text-gray-600">Active Users</p>
                          <p className="text-2xl font-bold text-gray-900">{formatNumber(systemStats.active_users)}</p>
                          <p className="text-xs text-green-600">+8% from last month</p>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow p-6">
                      <div className="flex items-center">
                        <div className="p-2 bg-purple-100 rounded-lg">
                          <DocumentTextIcon className="w-6 h-6 text-purple-600" />
                        </div>
                        <div className="ml-4">
                          <p className="text-sm font-medium text-gray-600">Subscribers</p>
                          <p className="text-2xl font-bold text-gray-900">{formatNumber(systemStats.subscriber_users)}</p>
                          <p className="text-xs text-green-600">+15% from last month</p>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow p-6">
                      <div className="flex items-center">
                        <div className="p-2 bg-yellow-100 rounded-lg">
                          <ClockIcon className="w-6 h-6 text-yellow-600" />
                        </div>
                        <div className="ml-4">
                          <p className="text-sm font-medium text-gray-600">Recent Logins</p>
                          <p className="text-2xl font-bold text-gray-900">{formatNumber(systemStats.recent_logins)}</p>
                          <p className="text-xs text-green-600">+5% from last week</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Detailed Charts */}
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div className="bg-white rounded-lg shadow p-6">
                      <h3 className="text-lg font-medium text-gray-900 mb-4">User Growth</h3>
                      <div className="space-y-3">
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-600">New Registrations</span>
                          <span className="text-sm font-bold text-gray-900">{formatNumber(systemStats.recent_registrations)}</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-600">Verified Users</span>
                          <span className="text-sm font-bold text-gray-900">{formatNumber(systemStats.verified_users)}</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-600">Admin Users</span>
                          <span className="text-sm font-bold text-gray-900">{formatNumber(systemStats.admin_users)}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow p-6">
                      <h3 className="text-lg font-medium text-gray-900 mb-4">Subscription Distribution</h3>
                      <div className="space-y-3">
                        {Object.entries(systemStats.users_by_subscription).map(([tier, count]) => (
                          <div key={tier} className="flex justify-between items-center">
                            <span className="text-sm text-gray-600 capitalize">{tier}</span>
                            <span className="text-sm font-bold text-gray-900">{formatNumber(count)}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* User Analytics Tab */}
              {activeTab === 'users' && userAnalytics && (
                <div className="space-y-6">
                  {/* User Metrics */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="bg-white rounded-lg shadow p-6">
                      <h3 className="text-lg font-medium text-gray-900 mb-4">New Users</h3>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">Today</span>
                          <span className="text-sm font-bold text-gray-900">{userAnalytics.new_users.today}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">This Week</span>
                          <span className="text-sm font-bold text-gray-900">{userAnalytics.new_users.week}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">This Month</span>
                          <span className="text-sm font-bold text-gray-900">{userAnalytics.new_users.month}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow p-6">
                      <h3 className="text-lg font-medium text-gray-900 mb-4">Active Users</h3>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">Today</span>
                          <span className="text-sm font-bold text-gray-900">{userAnalytics.active_users.today}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">This Week</span>
                          <span className="text-sm font-bold text-gray-900">{userAnalytics.active_users.week}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">This Month</span>
                          <span className="text-sm font-bold text-gray-900">{userAnalytics.active_users.month}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow p-6">
                      <h3 className="text-lg font-medium text-gray-900 mb-4">User Retention</h3>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">Day 1</span>
                          <span className="text-sm font-bold text-gray-900">{formatPercentage(userAnalytics.user_retention.day_1)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">Day 7</span>
                          <span className="text-sm font-bold text-gray-900">{formatPercentage(userAnalytics.user_retention.day_7)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">Day 30</span>
                          <span className="text-sm font-bold text-gray-900">{formatPercentage(userAnalytics.user_retention.day_30)}</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Top Referrers */}
                  <div className="bg-white rounded-lg shadow p-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">Top Traffic Sources</h3>
                    <div className="space-y-3">
                      {userAnalytics.top_referrers.map((referrer, index) => (
                        <div key={referrer.source} className="flex items-center justify-between">
                          <div className="flex items-center">
                            <span className="text-sm font-medium text-gray-900 w-8">{index + 1}.</span>
                            <span className="text-sm text-gray-600">{referrer.source}</span>
                          </div>
                          <div className="flex items-center space-x-4">
                            <span className="text-sm font-bold text-gray-900">{formatNumber(referrer.users)} users</span>
                            <span className="text-sm text-gray-500">{formatPercentage(referrer.percentage)}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Content Analytics Tab */}
              {activeTab === 'content' && contentAnalytics && (
                <div className="space-y-6">
                  {/* Content Metrics */}
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                    <div className="bg-white rounded-lg shadow p-6">
                      <div className="flex items-center">
                        <div className="p-2 bg-blue-100 rounded-lg">
                          <EyeIcon className="w-6 h-6 text-blue-600" />
                        </div>
                        <div className="ml-4">
                          <p className="text-sm font-medium text-gray-600">Total Content</p>
                          <p className="text-2xl font-bold text-gray-900">{contentAnalytics.total_content}</p>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow p-6">
                      <div className="flex items-center">
                        <div className="p-2 bg-green-100 rounded-lg">
                          <DocumentTextIcon className="w-6 h-6 text-green-600" />
                        </div>
                        <div className="ml-4">
                          <p className="text-sm font-medium text-gray-600">Published</p>
                          <p className="text-2xl font-bold text-gray-900">{contentAnalytics.published_content}</p>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow p-6">
                      <div className="flex items-center">
                        <div className="p-2 bg-yellow-100 rounded-lg">
                          <ClockIcon className="w-6 h-6 text-yellow-600" />
                        </div>
                        <div className="ml-4">
                          <p className="text-sm font-medium text-gray-600">Drafts</p>
                          <p className="text-2xl font-bold text-gray-900">{contentAnalytics.draft_content}</p>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow p-6">
                      <div className="flex items-center">
                        <div className="p-2 bg-purple-100 rounded-lg">
                          <CalendarIcon className="w-6 h-6 text-purple-600" />
                        </div>
                        <div className="ml-4">
                          <p className="text-sm font-medium text-gray-600">Total Views</p>
                          <p className="text-2xl font-bold text-gray-900">{formatNumber(contentAnalytics.content_views.month)}</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Top Content */}
                  <div className="bg-white rounded-lg shadow p-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">Top Performing Content</h3>
                    <div className="space-y-4">
                      {contentAnalytics.top_content.map((item, index) => (
                        <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                          <div className="flex items-center">
                            <span className="text-sm font-medium text-gray-900 w-8">{index + 1}.</span>
                            <div>
                              <h4 className="text-sm font-medium text-gray-900">{item.title}</h4>
                              <p className="text-xs text-gray-500">{formatNumber(item.views)} views</p>
                            </div>
                          </div>
                          <div className="text-right">
                            <span className="text-sm font-bold text-gray-900">{formatPercentage(item.engagement)}</span>
                            <p className="text-xs text-gray-500">engagement</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Performance Tab */}
              {activeTab === 'performance' && performanceMetrics && (
                <div className="space-y-6">
                  {/* Performance Metrics */}
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <div className="bg-white rounded-lg shadow p-6">
                      <h3 className="text-lg font-medium text-gray-900 mb-4">Response Time</h3>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">Average</span>
                          <span className="text-sm font-bold text-gray-900">{performanceMetrics.response_time.avg}ms</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">P95</span>
                          <span className="text-sm font-bold text-gray-900">{performanceMetrics.response_time.p95}ms</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">P99</span>
                          <span className="text-sm font-bold text-gray-900">{performanceMetrics.response_time.p99}ms</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow p-6">
                      <h3 className="text-lg font-medium text-gray-900 mb-4">Error Rate</h3>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">Total</span>
                          <span className="text-sm font-bold text-gray-900">{formatPercentage(performanceMetrics.error_rate.total)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">API</span>
                          <span className="text-sm font-bold text-gray-900">{formatPercentage(performanceMetrics.error_rate.api)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">Frontend</span>
                          <span className="text-sm font-bold text-gray-900">{formatPercentage(performanceMetrics.error_rate.frontend)}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow p-6">
                      <h3 className="text-lg font-medium text-gray-900 mb-4">Uptime</h3>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">Current</span>
                          <span className="text-sm font-bold text-green-600">{formatPercentage(performanceMetrics.uptime.current)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">This Month</span>
                          <span className="text-sm font-bold text-green-600">{formatPercentage(performanceMetrics.uptime.month)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">This Year</span>
                          <span className="text-sm font-bold text-green-600">{formatPercentage(performanceMetrics.uptime.year)}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow p-6">
                      <h3 className="text-lg font-medium text-gray-900 mb-4">Server Load</h3>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">CPU</span>
                          <span className="text-sm font-bold text-gray-900">{formatPercentage(performanceMetrics.server_load.cpu)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">Memory</span>
                          <span className="text-sm font-bold text-gray-900">{formatPercentage(performanceMetrics.server_load.memory)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">Disk</span>
                          <span className="text-sm font-bold text-gray-900">{formatPercentage(performanceMetrics.server_load.disk)}</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* System Health */}
                  <div className="bg-white rounded-lg shadow p-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">System Health</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="flex items-center justify-between p-4 border rounded-lg">
                        <div>
                          <h4 className="text-sm font-medium text-gray-900">Database</h4>
                          <p className="text-xs text-gray-500">Connection status</p>
                        </div>
                        <div className="flex items-center">
                          <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                          <span className="text-sm text-green-600">Healthy</span>
                        </div>
                      </div>
                      
                      <div className="flex items-center justify-between p-4 border rounded-lg">
                        <div>
                          <h4 className="text-sm font-medium text-gray-900">API Services</h4>
                          <p className="text-xs text-gray-500">Response time</p>
                        </div>
                        <div className="flex items-center">
                          <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                          <span className="text-sm text-green-600">Optimal</span>
                        </div>
                      </div>
                      
                      <div className="flex items-center justify-between p-4 border rounded-lg">
                        <div>
                          <h4 className="text-sm font-medium text-gray-900">External APIs</h4>
                          <p className="text-xs text-gray-500">Third-party services</p>
                        </div>
                        <div className="flex items-center">
                          <div className="w-3 h-3 bg-yellow-500 rounded-full mr-2"></div>
                          <span className="text-sm text-yellow-600">Warning</span>
                        </div>
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

export default AdminAnalytics; 