import React from 'react';
import MetricsCards from '../components/dashboard/MetricsCards';
import ModelManagementSection from '../components/dashboard/ModelManagementSection';
import DatasetSection from '../components/dashboard/DatasetSection';
import UserAnalyticsSection from '../components/dashboard/UserAnalyticsSection';
import PredictionsSection from '../components/dashboard/PredictionsSection';
import SystemMonitoringSection from '../components/dashboard/SystemMonitoringSection';
import useAdminData from '../hooks/useAdminData';
import useRealTimeUpdates from '../hooks/useRealTimeUpdates';
import { Bell, LogOut, User, Wifi, WifiOff } from 'lucide-react';

const AdminDashboard = () => {
  const { data, loading, error, refreshData } = useAdminData();
  const { isConnected, lastUpdate } = useRealTimeUpdates();

  return (
    <div className="min-h-screen bg-[#F3F3E0] p-6">
      {/* Header */}
      <header className="bg-white rounded-lg shadow-sm p-6 mb-8">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-[#183B4E]">Admin Dashboard - Diabetes Prediction</h1>
            <p className="text-[#374151] mt-1">Comprehensive ML model and user management</p>
            <div className="flex items-center mt-2 text-sm">
              {isConnected ? (
                <Wifi size={14} className="text-green-500 mr-1" />
              ) : (
                <WifiOff size={14} className="text-red-500 mr-1" />
              )}
              <span className={isConnected ? 'text-green-600' : 'text-red-600'}>
                {isConnected ? 'Real-time connected' : 'Disconnected'}
              </span>
              <span className="text-gray-500 ml-2">
                Last update: {lastUpdate.toLocaleTimeString()}
              </span>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
              <span className="text-sm text-[#183B4E]">
                {isConnected ? 'System Healthy' : 'Connection Issues'}
              </span>
            </div>
            <button
              onClick={refreshData}
              disabled={loading}
              className="p-2 text-[#27548A] hover:bg-[#F3F3E0] rounded-lg disabled:opacity-50"
            >
              <Bell size={20} />
            </button>
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-[#27548A] rounded-full flex items-center justify-center">
                <User size={16} className="text-white" />
              </div>
              <span className="text-[#183B4E] font-medium">Admin User</span>
            </div>
            <button className="px-4 py-2 bg-[#27548A] text-white rounded-lg hover:bg-[#183B4E] transition-colors">
              <LogOut size={16} className="inline mr-2" />
              Logout
            </button>
          </div>
        </div>
      </header>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-8">
          <p className="text-red-800">Error loading dashboard data: {error}</p>
        </div>
      )}

      {/* Metrics Cards */}
      <MetricsCards data={data.metrics} loading={loading} />

      {/* Two-column layout for main sections */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 mb-8">
        <ModelManagementSection data={data} loading={loading} />
        <DatasetSection data={data.datasets} loading={loading} />
      </div>

      {/* Full-width analytics */}
      <div className="mb-8">
        <UserAnalyticsSection data={data.recentUsers} loading={loading} />
      </div>

      {/* Predictions analytics */}
      <div className="mb-8">
        <PredictionsSection loading={loading} />
      </div>

      {/* System monitoring */}
      <SystemMonitoringSection loading={loading} />
    </div>
  );
};

export default AdminDashboard;
