import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet-async';
import { apiService } from '../services/apiService';
import { useAuth } from '../context/AuthContext';
import toast from 'react-hot-toast';
import SEO from '../components/SEO';

const AdminDashboard = () => {
  const { user } = useAuth();
  const [content, setContent] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // all, published, draft, archived
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedContent, setSelectedContent] = useState(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [stats, setStats] = useState({
    total: 0,
    published: 0,
    draft: 0,
    archived: 0
  });

  useEffect(() => {
    fetchContent();
  }, []);

  const fetchContent = async () => {
    try {
      setLoading(true);
      const response = await apiService.getContent({ limit: 100 });
      const contentData = response.data || [];
      setContent(contentData);
      
      // Calculate stats
      const stats = {
        total: contentData.length,
        published: contentData.filter(item => item.status === 'published').length,
        draft: contentData.filter(item => item.status === 'draft').length,
        archived: contentData.filter(item => item.status === 'archived').length
      };
      setStats(stats);
    } catch (error) {
      console.error('Error fetching content:', error);
      toast.error('Failed to load content');
    } finally {
      setLoading(false);
    }
  };

  const handleStatusChange = async (contentId, newStatus) => {
    try {
      if (newStatus === 'published') {
        await apiService.publishContent(contentId);
        toast.success('Content published successfully!');
      } else if (newStatus === 'archived') {
        await apiService.archiveContent(contentId);
        toast.success('Content archived successfully!');
      }
      fetchContent(); // Refresh the list
    } catch (error) {
      console.error('Error updating content status:', error);
      toast.error('Failed to update content status');
    }
  };

  const handleDelete = async () => {
    if (!selectedContent) return;
    
    try {
      await apiService.deleteContent(selectedContent.id);
      toast.success('Content deleted successfully!');
      setShowDeleteModal(false);
      setSelectedContent(null);
      fetchContent(); // Refresh the list
    } catch (error) {
      console.error('Error deleting content:', error);
      toast.error('Failed to delete content');
    }
  };

  const filteredContent = content.filter(item => {
    const matchesFilter = filter === 'all' || item.status === filter;
    const matchesSearch = item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.content_type.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesFilter && matchesSearch;
  });

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

  return (
    <>
      <SEO 
        title="Admin Dashboard - Content Management"
        description="Manage all published content and posts"
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
                <p className="text-gray-600">Manage your content and posts</p>
              </div>
              <div className="flex space-x-3">
                <button
                  onClick={() => window.location.href = '/admin/generate-content'}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium"
                >
                  + Generate New Content
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <span className="text-2xl">📊</span>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Total Content</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="p-2 bg-green-100 rounded-lg">
                  <span className="text-2xl">✅</span>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Published</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.published}</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="p-2 bg-yellow-100 rounded-lg">
                  <span className="text-2xl">📝</span>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Drafts</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.draft}</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="p-2 bg-gray-100 rounded-lg">
                  <span className="text-2xl">📁</span>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Archived</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.archived}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Filters and Search */}
          <div className="bg-white rounded-lg shadow mb-6">
            <div className="p-6">
              <div className="flex flex-col sm:flex-row gap-4">
                <div className="flex-1">
                  <input
                    type="text"
                    placeholder="Search content by title or type..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div className="flex space-x-2">
                  <select
                    value={filter}
                    onChange={(e) => setFilter(e.target.value)}
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
          </div>

          {/* Content List */}
          <div className="bg-white rounded-lg shadow">
            {loading ? (
              <div className="p-8 text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p className="mt-4 text-gray-600">Loading content...</p>
              </div>
            ) : filteredContent.length === 0 ? (
              <div className="p-8 text-center">
                <p className="text-gray-600">No content found matching your criteria.</p>
              </div>
            ) : (
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
                                onClick={() => handleStatusChange(item.id, 'published')}
                                className="text-purple-600 hover:text-purple-900"
                              >
                                Publish
                              </button>
                            )}
                            {item.status === 'published' && (
                              <button
                                onClick={() => handleStatusChange(item.id, 'archived')}
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
            )}
          </div>
        </div>
      </div>

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
                  onClick={handleDelete}
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