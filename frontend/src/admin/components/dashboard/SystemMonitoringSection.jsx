import React from 'react';
import { Activity, AlertTriangle, Settings, RefreshCw, Clock } from 'lucide-react';
import Badge from '../ui/Badge';

const SystemMonitoringSection = ({ loading }) => {
  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <div className="h-6 bg-gray-200 rounded mb-6 animate-pulse"></div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="h-20 bg-gray-200 rounded animate-pulse"></div>
            ))}
          </div>
          <div className="space-y-3">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-12 bg-gray-200 rounded animate-pulse"></div>
            ))}
          </div>
          <div className="space-y-3">
            {[...Array(2)].map((_, i) => (
              <div key={i} className="h-16 bg-gray-200 rounded animate-pulse"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }
  const systemHealth = {
    status: 'healthy',
    uptime: '99.9%',
    lastIncident: '2024-03-18 14:30'
  };

  const recentActivities = [
    {
      id: 1,
      action: 'Model deployment completed',
      timestamp: '2024-03-20 11:45',
      type: 'success'
    },
    {
      id: 2,
      action: 'Dataset preprocessing finished',
      timestamp: '2024-03-20 10:30',
      type: 'info'
    },
    {
      id: 3,
      action: 'High CPU usage detected',
      timestamp: '2024-03-20 09:15',
      type: 'warning'
    },
    {
      id: 4,
      action: 'Backup completed successfully',
      timestamp: '2024-03-20 08:00',
      type: 'success'
    },
    {
      id: 5,
      action: 'User authentication failed (3 attempts)',
      timestamp: '2024-03-20 07:22',
      type: 'error'
    }
  ];

  const alerts = [
    {
      id: 1,
      message: 'Disk space running low (85% used)',
      severity: 'warning',
      time: '2 hours ago'
    },
    {
      id: 2,
      message: 'Scheduled maintenance in 24 hours',
      severity: 'info',
      time: '1 day ago'
    }
  ];

  const getActivityIcon = (type) => {
    switch (type) {
      case 'success':
        return <Activity size={16} className="text-green-500" />;
      case 'warning':
        return <AlertTriangle size={16} className="text-yellow-500" />;
      case 'error':
        return <AlertTriangle size={16} className="text-red-500" />;
      default:
        return <Clock size={16} className="text-blue-500" />;
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <h2 className="text-xl font-bold text-[#183B4E] mb-6">System Monitoring</h2>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* System Health Status */}
        <div className="lg:col-span-1">
          <h3 className="text-lg font-semibold text-[#183B4E] mb-4">System Health</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg">
              <div>
                <p className="font-medium text-green-800">Status</p>
                <p className="text-sm text-green-600">All systems operational</p>
              </div>
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            </div>

            <div className="p-4 bg-blue-50 rounded-lg">
              <p className="font-medium text-blue-800">Uptime</p>
              <p className="text-2xl font-bold text-blue-900">{systemHealth.uptime}</p>
            </div>

            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="font-medium text-gray-800">Last Incident</p>
              <p className="text-sm text-gray-600">{systemHealth.lastIncident}</p>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="mt-6">
            <h4 className="text-md font-semibold text-[#183B4E] mb-3">Quick Actions</h4>
            <div className="space-y-2">
              <button className="w-full px-4 py-2 bg-[#27548A] text-white rounded hover:bg-[#183B4E] transition-colors flex items-center justify-center">
                <RefreshCw size={16} className="mr-2" />
                Refresh Status
              </button>
              <button className="w-full px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition-colors flex items-center justify-center">
                <Settings size={16} className="mr-2" />
                System Settings
              </button>
            </div>
          </div>
        </div>

        {/* Recent Activity Log */}
        <div className="lg:col-span-1">
          <h3 className="text-lg font-semibold text-[#183B4E] mb-4">Recent Activity</h3>
          <div className="space-y-3 max-h-80 overflow-y-auto">
            {recentActivities.map((activity) => (
              <div key={activity.id} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                {getActivityIcon(activity.type)}
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">{activity.action}</p>
                  <p className="text-xs text-gray-500">{activity.timestamp}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Alerts and Notifications */}
        <div className="lg:col-span-1">
          <h3 className="text-lg font-semibold text-[#183B4E] mb-4">Alerts & Notifications</h3>
          <div className="space-y-3">
            {alerts.map((alert) => (
              <div key={alert.id} className={`p-3 rounded-lg border-l-4 ${
                alert.severity === 'warning' ? 'bg-yellow-50 border-yellow-400' :
                alert.severity === 'error' ? 'bg-red-50 border-red-400' :
                'bg-blue-50 border-blue-400'
              }`}>
                <div className="flex items-start">
                  <AlertTriangle size={16} className={`mt-0.5 mr-2 ${
                    alert.severity === 'warning' ? 'text-yellow-600' :
                    alert.severity === 'error' ? 'text-red-600' :
                    'text-blue-600'
                  }`} />
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900">{alert.message}</p>
                    <p className="text-xs text-gray-500">{alert.time}</p>
                  </div>
                </div>
              </div>
            ))}

            {alerts.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                <Activity size={32} className="mx-auto mb-2 opacity-50" />
                <p>No active alerts</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SystemMonitoringSection;
