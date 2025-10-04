import React from 'react';
import MetricsCards from '../components/dashboard/MetricsCards';
import ModelManagementSection from '../components/dashboard/ModelManagementSection';
import DatasetSection from '../components/dashboard/DatasetSection';
import UserAnalyticsSection from '../components/dashboard/UserAnalyticsSection';
import PredictionsSection from '../components/dashboard/PredictionsSection';
import SystemMonitoringSection from '../components/dashboard/SystemMonitoringSection';
import useAdminData from '../hooks/useAdminData';
import useRealTimeUpdates from '../hooks/useRealTimeUpdates';
import { Bell, LogOut, User, Wifi, WifiOff, UserPlus, Shield, AlertCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

const AdminDashboard = () => {
  const { 
    data, 
    loading, 
    error, 
    refreshData 
  } = useAdminData();
  
  const { isConnected, lastUpdate } = useRealTimeUpdates();
  const navigate = useNavigate();
  
  const { 
    userInfo, 
    userType, 
    logout, 
    displayName, 
    roleDisplayText, 
    isSuperAdmin
  } = useAuth();

  // Get role-specific capabilities
  const canAddAdmin = isSuperAdmin;
  const userRole = userInfo?.role || 'admin';

  return (
    <div className="min-h-screen bg-[#F3F3E0] p-6">
      {/* Header */}
      <header className="bg-white rounded-lg shadow-sm p-6 mb-8">
        <div className="flex justify-between items-center">
          <div>
            <div className="flex items-center space-x-3 mb-2">
              <h1 className="text-3xl font-bold text-[#183B4E]">Admin Dashboard</h1>
              <Badge variant={userRole === 'superadmin' ? 'default' : 'secondary'}>
                {roleDisplayText}
              </Badge>
            </div>
            <p className="text-[#374151] mt-1">Diabetes Prediction System Management</p>
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
              title="Refresh Data"
            >
              <Bell size={20} />
            </button>
            
            {/* User Info */}
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-[#27548A] rounded-full flex items-center justify-center">
                {userRole === 'superadmin' ? (
                  <Shield size={16} className="text-white" />
                ) : (
                  <User size={16} className="text-white" />
                )}
              </div>
              <div className="text-right">
                <div className="text-[#183B4E] font-medium">{displayName}</div>
                <div className="text-xs text-gray-500">{userInfo?.email}</div>
              </div>
            </div>
            
            {/* Action Buttons */}
            <div className="flex flex-col space-y-2">
              <Button
                onClick={logout}
                variant="outline"
                size="sm"
                className="border-[#27548A] text-[#27548A] hover:bg-[#27548A] hover:text-white"
              >
                <LogOut size={16} className="mr-2" />
                Logout
              </Button>
              
              {canAddAdmin && (
                <Button
                  onClick={() => navigate('/admin/add-admin')}
                  size="sm"
                  className="bg-[#27548A] hover:bg-[#183B4E] text-white"
                >
                  <UserPlus size={16} className="mr-2" />
                  Add Admin
                </Button>
              )}
            </div>
          </div>
        </div>
        
        {/* Role-specific info */}
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center space-x-4">
              <span className="text-gray-600">
                Role: <span className="font-medium text-[#ffffff]">{roleDisplayText}</span>
              </span>
              {userInfo?.position && (
                <span className="text-gray-600">
                  Position: <span className="font-medium text-[#ffffff]">{userInfo.position}</span>
                </span>
              )}
            </div>
            <div className="flex items-center space-x-2 text-gray-600">
              <span>Access Level:</span>
              <Badge variant={userRole === 'superadmin' ? 'default' : 'secondary'}>
                {userRole === 'superadmin' ? 'Full Access' : 'Limited Access'}
              </Badge>
            </div>
          </div>
        </div>
      </header>

      {error && (
        <Card className="mb-8 border-red-200 bg-red-50">
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <AlertCircle className="h-5 w-5 text-red-600" />
              <p className="text-red-800">Error loading dashboard data: {error}</p>
            </div>
          </CardContent>
        </Card>
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
