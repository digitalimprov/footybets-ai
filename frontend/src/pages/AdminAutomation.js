import React, { useState, useEffect } from 'react';
import { apiService } from '../services/apiService';
import {
  CogIcon,
  PlayIcon,
  PauseIcon,
  ArrowPathIcon,
  ClockIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  ChartBarIcon,
  CalendarIcon,
  SparklesIcon,
  DocumentTextIcon
} from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';
import SEO from '../components/SEO';

const AdminAutomation = () => {
  const [schedulerStatus, setSchedulerStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [operationInProgress, setOperationInProgress] = useState(null);

  useEffect(() => {
    loadSchedulerStatus();
  }, []);

  const loadSchedulerStatus = async () => {
    try {
      setLoading(true);
      const response = await apiService.get('/automation/scheduler/status');
      setSchedulerStatus(response.data);
    } catch (error) {
      console.error('Error loading scheduler status:', error);
      toast.error('Failed to load scheduler status');
    } finally {
      setLoading(false);
    }
  };

  const handleSchedulerAction = async (action) => {
    try {
      setOperationInProgress(action);
      const response = await apiService.post(`/automation/scheduler/${action}`);
      
      if (response.data.success) {
        toast.success(response.data.message);
        await loadSchedulerStatus();
      } else {
        toast.error(response.data.message || `Failed to ${action} scheduler`);
      }
    } catch (error) {
      console.error(`Error ${action} scheduler:`, error);
      toast.error(`Failed to ${action} scheduler`);
    } finally {
      setOperationInProgress(null);
    }
  };

  const runJobManually = async (jobId, jobName) => {
    try {
      setOperationInProgress(jobId);
      const response = await apiService.post(`/automation/scheduler/run-job/${jobId}`);
      
      if (response.data.success) {
        toast.success(`${jobName} completed successfully`);
      } else {
        toast.error(response.data.error || `Failed to run ${jobName}`);
      }
    } catch (error) {
      console.error(`Error running job ${jobId}:`, error);
      toast.error(`Failed to run ${jobName}`);
    } finally {
      setOperationInProgress(null);
    }
  };

  const runFullWeeklyUpdate = async () => {
    try {
      setOperationInProgress('full_update');
      toast.loading('Running full weekly update...', { id: 'full_update' });
      
      const response = await apiService.post('/automation/automation/full-weekly-update');
      
      if (response.data.success) {
        toast.success('Full weekly update completed successfully', { id: 'full_update' });
        
        // Show details in a more detailed toast
        const steps = response.data.steps_completed;
        if (steps && steps.length > 0) {
          toast.success(`Completed: ${steps.join(', ')}`, { duration: 5000 });
        }
        
        if (response.data.errors && response.data.errors.length > 0) {
          toast.error(`Some errors occurred: ${response.data.errors.slice(0, 2).join(', ')}`, { duration: 5000 });
        }
      } else {
        toast.error('Full weekly update failed', { id: 'full_update' });
        
        if (response.data.errors) {
          toast.error(`Errors: ${response.data.errors.slice(0, 2).join(', ')}`, { duration: 5000 });
        }
      }
    } catch (error) {
      console.error('Error running full weekly update:', error);
      toast.error('Failed to run full weekly update', { id: 'full_update' });
    } finally {
      setOperationInProgress(null);
    }
  };

  const runScrapingTask = async (type, taskName) => {
    try {
      setOperationInProgress(type);
      toast.loading(`Running ${taskName}...`, { id: type });
      
      const endpoint = type === 'upcoming' ? '/automation/scraping/upcoming' : '/automation/scraping/results';
      const response = await apiService.get(endpoint);
      
      if (response.data.success) {
        toast.success(`${taskName} completed: ${response.data.message}`, { id: type });
      } else {
        toast.error(`${taskName} failed`, { id: type });
      }
    } catch (error) {
      console.error(`Error running ${type} scraping:`, error);
      toast.error(`Failed to run ${taskName}`, { id: type });
    } finally {
      setOperationInProgress(null);
    }
  };

  const formatNextRun = (nextRunString) => {
    if (!nextRunString) return 'Not scheduled';
    
    const nextRun = new Date(nextRunString);
    const now = new Date();
    const diffMs = nextRun - now;
    
    if (diffMs < 0) return 'Overdue';
    
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffDays > 0) {
      return `In ${diffDays} day${diffDays > 1 ? 's' : ''}`;
    } else if (diffHours > 0) {
      return `In ${diffHours} hour${diffHours > 1 ? 's' : ''}`;
    } else {
      const diffMinutes = Math.floor(diffMs / (1000 * 60));
      return `In ${diffMinutes} minute${diffMinutes > 1 ? 's' : ''}`;
    }
  };

  const JobCard = ({ job, onRunManually }) => {
    const getJobIcon = (jobId) => {
      switch (jobId) {
        case 'scrape_upcoming_games':
          return <CalendarIcon className="h-6 w-6 text-blue-600" />;
        case 'scrape_recent_results':
          return <ChartBarIcon className="h-6 w-6 text-green-600" />;
        case 'generate_weekly_tips':
          return <SparklesIcon className="h-6 w-6 text-purple-600" />;
        case 'update_prediction_accuracy':
          return <CheckCircleIcon className="h-6 w-6 text-indigo-600" />;
        case 'daily_health_check':
          return <DocumentTextIcon className="h-6 w-6 text-orange-600" />;
        default:
          return <CogIcon className="h-6 w-6 text-gray-600" />;
      }
    };

    const getJobColor = (jobId) => {
      switch (jobId) {
        case 'scrape_upcoming_games':
          return 'blue';
        case 'scrape_recent_results':
          return 'green';
        case 'generate_weekly_tips':
          return 'purple';
        case 'update_prediction_accuracy':
          return 'indigo';
        case 'daily_health_check':
          return 'orange';
        default:
          return 'gray';
      }
    };

    const color = getJobColor(job.id);
    const isRunning = operationInProgress === job.id;

    return (
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center space-x-3">
            {getJobIcon(job.id)}
            <div>
              <h3 className="text-lg font-semibold text-gray-900">{job.name}</h3>
              <p className="text-sm text-gray-600">{job.trigger}</p>
            </div>
          </div>
          <button
            onClick={() => onRunManually(job.id, job.name)}
            disabled={isRunning}
            className={`bg-${color}-100 text-${color}-700 px-3 py-2 rounded-lg text-sm font-medium hover:bg-${color}-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2`}
          >
            {isRunning ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-current"></div>
                <span>Running...</span>
              </>
            ) : (
              <>
                <PlayIcon className="h-4 w-4" />
                <span>Run Now</span>
              </>
            )}
          </button>
        </div>
        
        <div className="bg-gray-50 rounded-lg p-3">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">Next run:</span>
            <span className="font-medium text-gray-900">{formatNextRun(job.next_run)}</span>
          </div>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading automation dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <SEO 
        title="Admin Automation Dashboard - FootyBets.ai"
        description="Manage automated AFL data scraping, tip generation, and system monitoring."
      />
      
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 via-indigo-600 to-blue-600 text-white">
        <div className="container mx-auto px-4 py-8">
          <div className="flex items-center space-x-4">
            <CogIcon className="h-12 w-12" />
            <div>
              <h1 className="text-4xl font-bold mb-2">Automation Dashboard</h1>
              <p className="text-xl text-purple-100">Manage AFL data automation and AI processes</p>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {/* Scheduler Status */}
        <div className="mb-8">
          <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-3">
                <ClockIcon className="h-8 w-8 text-indigo-600" />
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">Scheduler Status</h2>
                  <p className="text-gray-600">Automated task scheduling system</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-4">
                <div className={`px-4 py-2 rounded-full text-sm font-semibold flex items-center space-x-2 ${
                  schedulerStatus?.scheduler_running 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-red-100 text-red-800'
                }`}>
                  {schedulerStatus?.scheduler_running ? (
                    <>
                      <CheckCircleIcon className="h-4 w-4" />
                      <span>Running</span>
                    </>
                  ) : (
                    <>
                      <ExclamationTriangleIcon className="h-4 w-4" />
                      <span>Stopped</span>
                    </>
                  )}
                </div>

                <div className="flex space-x-2">
                  {schedulerStatus?.scheduler_running ? (
                    <button
                      onClick={() => handleSchedulerAction('stop')}
                      disabled={operationInProgress === 'stop'}
                      className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 flex items-center space-x-2"
                    >
                      <PauseIcon className="h-4 w-4" />
                      <span>Stop</span>
                    </button>
                  ) : (
                    <button
                      onClick={() => handleSchedulerAction('start')}
                      disabled={operationInProgress === 'start'}
                      className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50 flex items-center space-x-2"
                    >
                      <PlayIcon className="h-4 w-4" />
                      <span>Start</span>
                    </button>
                  )}
                  
                  <button
                    onClick={loadSchedulerStatus}
                    disabled={loading}
                    className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors disabled:opacity-50 flex items-center space-x-2"
                  >
                    <ArrowPathIcon className="h-4 w-4" />
                    <span>Refresh</span>
                  </button>
                </div>
              </div>
            </div>

            {schedulerStatus && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-gray-50 rounded-lg p-4 text-center">
                  <p className="text-2xl font-bold text-gray-900">{schedulerStatus.total_jobs}</p>
                  <p className="text-gray-600">Active Jobs</p>
                </div>
                <div className="bg-blue-50 rounded-lg p-4 text-center">
                  <p className="text-2xl font-bold text-blue-600">
                    {schedulerStatus.scheduler_running ? 'Active' : 'Inactive'}
                  </p>
                  <p className="text-gray-600">Scheduler State</p>
                </div>
                <div className="bg-green-50 rounded-lg p-4 text-center">
                  <p className="text-2xl font-bold text-green-600">Automated</p>
                  <p className="text-gray-600">Operation Mode</p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Quick Actions</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <button
              onClick={runFullWeeklyUpdate}
              disabled={operationInProgress === 'full_update'}
              className="bg-gradient-to-r from-purple-500 to-indigo-600 text-white p-6 rounded-xl hover:from-purple-600 hover:to-indigo-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <SparklesIcon className="h-8 w-8 mb-3 mx-auto" />
              <h3 className="font-semibold mb-2">Full Weekly Update</h3>
              <p className="text-sm text-purple-100">Run complete automation cycle</p>
              {operationInProgress === 'full_update' && (
                <div className="mt-2">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mx-auto"></div>
                </div>
              )}
            </button>

            <button
              onClick={() => runScrapingTask('upcoming', 'Upcoming Games Scraping')}
              disabled={operationInProgress === 'upcoming'}
              className="bg-gradient-to-r from-blue-500 to-blue-600 text-white p-6 rounded-xl hover:from-blue-600 hover:to-blue-700 transition-all disabled:opacity-50"
            >
              <CalendarIcon className="h-8 w-8 mb-3 mx-auto" />
              <h3 className="font-semibold mb-2">Scrape Upcoming</h3>
              <p className="text-sm text-blue-100">Get future AFL fixtures</p>
              {operationInProgress === 'upcoming' && (
                <div className="mt-2">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mx-auto"></div>
                </div>
              )}
            </button>

            <button
              onClick={() => runScrapingTask('results', 'Recent Results Scraping')}
              disabled={operationInProgress === 'results'}
              className="bg-gradient-to-r from-green-500 to-green-600 text-white p-6 rounded-xl hover:from-green-600 hover:to-green-700 transition-all disabled:opacity-50"
            >
              <ChartBarIcon className="h-8 w-8 mb-3 mx-auto" />
              <h3 className="font-semibold mb-2">Scrape Results</h3>
              <p className="text-sm text-green-100">Get completed game results</p>
              {operationInProgress === 'results' && (
                <div className="mt-2">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mx-auto"></div>
                </div>
              )}
            </button>

            <button
              onClick={() => runJobManually('generate_weekly_tips', 'Generate Weekly Tips')}
              disabled={operationInProgress === 'generate_weekly_tips'}
              className="bg-gradient-to-r from-orange-500 to-red-600 text-white p-6 rounded-xl hover:from-orange-600 hover:to-red-700 transition-all disabled:opacity-50"
            >
              <SparklesIcon className="h-8 w-8 mb-3 mx-auto" />
              <h3 className="font-semibold mb-2">Generate Tips</h3>
              <p className="text-sm text-orange-100">Create AI predictions</p>
              {operationInProgress === 'generate_weekly_tips' && (
                <div className="mt-2">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mx-auto"></div>
                </div>
              )}
            </button>
          </div>
        </div>

        {/* Scheduled Jobs */}
        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Scheduled Jobs</h2>
          
          {schedulerStatus?.jobs && schedulerStatus.jobs.length > 0 ? (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {schedulerStatus.jobs.map((job) => (
                <JobCard
                  key={job.id}
                  job={job}
                  onRunManually={runJobManually}
                />
              ))}
            </div>
          ) : (
            <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-12 text-center">
              <ClockIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">No Scheduled Jobs</h3>
              <p className="text-gray-600">Start the scheduler to see available jobs</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdminAutomation; 