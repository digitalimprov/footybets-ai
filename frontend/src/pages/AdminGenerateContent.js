import React, { useState } from 'react';
import { 
  PlusIcon,
  SparklesIcon,
  DocumentTextIcon,
  ChartBarIcon,
  TrophyIcon,
  NewspaperIcon,
  UserGroupIcon,
  PlayIcon
} from '@heroicons/react/24/outline';
import apiService from '../services/apiService';
import { useAuth } from '../context/AuthContext';
import toast from 'react-hot-toast';
import SEO from '../components/SEO';

const AdminGenerateContent = () => {
  const { user } = useAuth();
  const [contentType, setContentType] = useState('article');
  const [gameId, setGameId] = useState('');
  const [teamId, setTeamId] = useState('');
  const [season, setSeason] = useState('2024');
  const [customPrompt, setCustomPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  const contentTypes = [
    { id: 'article', name: 'General Article', icon: DocumentTextIcon, description: 'Create a general AFL article' },
    { id: 'game_analysis', name: 'Game Analysis', icon: ChartBarIcon, description: 'Analyze a specific game' },
    { id: 'team_preview', name: 'Team Preview', icon: UserGroupIcon, description: 'Preview a team for the season' },
    { id: 'brownlow', name: 'Brownlow Analysis', icon: TrophyIcon, description: 'Brownlow Medal analysis' },
    { id: 'news', name: 'News Article', icon: NewspaperIcon, description: 'Current AFL news' },
    { id: 'prediction', name: 'Prediction Article', icon: SparklesIcon, description: 'Game predictions' }
  ];

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleContextChange = (key, value) => {
    setFormData(prev => ({
      ...prev,
      context: {
        ...prev.context,
        [key]: value
      }
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.template_name) {
      toast.error('Please select a template');
      return;
    }

    setGenerating(true);
    try {
      const response = await apiService.generateContent(formData);
      toast.success('Content generated successfully!');
      
      // Redirect to the admin dashboard
      window.location.href = '/admin/dashboard';
    } catch (error) {
      console.error('Error generating content:', error);
      toast.error('Failed to generate content');
    } finally {
      setGenerating(false);
    }
  };

  const generateGameAnalysis = async (gameId) => {
    setGenerating(true);
    try {
      const response = await apiService.generateGameAnalysis(gameId);
      toast.success('Game analysis generated successfully!');
      window.location.href = '/admin/dashboard';
    } catch (error) {
      console.error('Error generating game analysis:', error);
      toast.error('Failed to generate game analysis');
    } finally {
      setGenerating(false);
    }
  };

  const generateTeamPreview = async (teamId) => {
    setGenerating(true);
    try {
      const response = await apiService.generateTeamPreview(teamId);
      toast.success('Team preview generated successfully!');
      window.location.href = '/admin/dashboard';
    } catch (error) {
      console.error('Error generating team preview:', error);
      toast.error('Failed to generate team preview');
    } finally {
      setGenerating(false);
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

  return (
    <>
      <SEO 
        title="Generate Content - Admin"
        description="Generate AI-powered content"
        noindex={true}
        nofollow={true}
      />
      
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <div className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-6">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Generate Content</h1>
                <p className="text-gray-600">Create AI-powered content for your site</p>
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

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Quick Generate Section */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Quick Generate</h2>
              
              {/* Game Analysis */}
              <div className="mb-6">
                <h3 className="text-lg font-medium text-gray-900 mb-3">Game Analysis</h3>
                <div className="flex space-x-2">
                  <select
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    onChange={(e) => {
                      if (e.target.value) {
                        generateGameAnalysis(e.target.value);
                      }
                    }}
                  >
                    <option value="">Select a game...</option>
                    {games.map(game => (
                      <option key={game.id} value={game.id}>
                        {game.home_team_name} vs {game.away_team_name} - Round {game.round_number}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Team Preview */}
              <div className="mb-6">
                <h3 className="text-lg font-medium text-gray-900 mb-3">Team Preview</h3>
                <div className="flex space-x-2">
                  <select
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    onChange={(e) => {
                      if (e.target.value) {
                        generateTeamPreview(e.target.value);
                      }
                    }}
                  >
                    <option value="">Select a team...</option>
                    {teams.map(team => (
                      <option key={team.id} value={team.id}>
                        {team.name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            {/* Custom Content Form */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Custom Content</h2>
              
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Title
                  </label>
                  <input
                    type="text"
                    name="title"
                    value={formData.title}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Enter content title..."
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Content Type
                  </label>
                  <select
                    name="content_type"
                    value={formData.content_type}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="article">Article</option>
                    <option value="analysis">Analysis</option>
                    <option value="prediction">Prediction</option>
                    <option value="brownlow">Brownlow Analysis</option>
                    <option value="news">News</option>
                    <option value="game_analysis">Game Analysis</option>
                    <option value="team_preview">Team Preview</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Template
                  </label>
                  <select
                    name="template_name"
                    value={formData.template_name}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Select a template...</option>
                    {templates.map(template => (
                      <option key={template.name} value={template.name}>
                        {template.name} - {template.description}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Context (JSON)
                  </label>
                  <textarea
                    value={JSON.stringify(formData.context, null, 2)}
                    onChange={(e) => {
                      try {
                        const parsed = JSON.parse(e.target.value);
                        setFormData(prev => ({ ...prev, context: parsed }));
                      } catch (error) {
                        // Invalid JSON, ignore
                      }
                    }}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows="4"
                    placeholder='{"key": "value"}'
                  />
                </div>

                <div className="flex space-x-4">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      name="is_premium"
                      checked={formData.is_premium}
                      onChange={handleInputChange}
                      className="mr-2"
                    />
                    <span className="text-sm text-gray-700">Premium Content</span>
                  </label>
                  
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      name="is_featured"
                      checked={formData.is_featured}
                      onChange={handleInputChange}
                      className="mr-2"
                    />
                    <span className="text-sm text-gray-700">Featured</span>
                  </label>
                </div>

                <button
                  type="submit"
                  disabled={generating}
                  className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium py-2 px-4 rounded-md transition-colors"
                >
                  {generating ? 'Generating...' : 'Generate Content'}
                </button>
              </form>
            </div>
          </div>

          {/* Available Templates */}
          <div className="mt-8 bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Available Templates</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {templates.map(template => (
                <div key={template.name} className="border rounded-lg p-4">
                  <h3 className="font-medium text-gray-900 mb-2">{template.name}</h3>
                  <p className="text-sm text-gray-600 mb-2">{template.description}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-500">
                      Type: {template.content_type}
                    </span>
                    <span className="text-xs text-gray-500">
                      Used: {template.usage_count} times
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default AdminGenerateContent; 