import React from 'react';
import { Search, Users, AlertTriangle } from 'lucide-react';
import LineChart from '../charts/LineChart';
import DonutChart from '../charts/DonutChart';
import DataTable from '../ui/DataTable';

const UserAnalyticsSection = ({ data, loading }) => {
  // Mock data for charts
  const userRegistrationData = [
    { date: '2024-03-14', users: 45 },
    { date: '2024-03-15', users: 52 },
    { date: '2024-03-16', users: 38 },
    { date: '2024-03-17', users: 61 },
    { date: '2024-03-18', users: 49 },
    { date: '2024-03-19', users: 55 },
    { date: '2024-03-20', users: 42 }
  ];

  const riskDistributionData = [
    { name: 'Low Risk', value: 45, color: '#10B981' },
    { name: 'Medium Risk', value: 35, color: '#F59E0B' },
    { name: 'High Risk', value: 20, color: '#EF4444' }
  ];

  const recentUsers = data || [
    {
      id: 1,
      name: "John Doe",
      email: "john@example.com",
      registrationDate: "2024-03-20",
      riskLevel: "Medium"
    },
    {
      id: 2,
      name: "Jane Smith",
      email: "jane@example.com",
      registrationDate: "2024-03-19",
      riskLevel: "Low"
    },
    {
      id: 3,
      name: "Bob Johnson",
      email: "bob@example.com",
      registrationDate: "2024-03-18",
      riskLevel: "High"
    }
  ];

  const userColumns = [
    { key: 'name', header: 'Name' },
    { key: 'email', header: 'Email' },
    { key: 'registrationDate', header: 'Registration Date' },
    { key: 'riskLevel', header: 'Risk Level', render: (row) => (
      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
        row.riskLevel === 'Low' ? 'bg-green-100 text-green-800' :
        row.riskLevel === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
        'bg-red-100 text-red-800'
      }`}>
        {row.riskLevel}
      </span>
    )}
  ];

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <div className="h-6 bg-gray-200 rounded mb-6 animate-pulse"></div>
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
          <div className="space-y-6">
            <div className="h-48 bg-gray-200 rounded animate-pulse"></div>
            <div className="h-48 bg-gray-200 rounded animate-pulse"></div>
          </div>
          <div className="space-y-6">
            <div className="h-32 bg-gray-200 rounded animate-pulse"></div>
            <div className="h-48 bg-gray-200 rounded animate-pulse"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <h2 className="text-xl font-bold text-[#183B4E] mb-6">User Analytics</h2>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
        {/* Charts Section */}
        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold text-[#183B4E] mb-4">User Registration Trend</h3>
            <LineChart
              data={userRegistrationData}
              xKey="date"
              yKey="users"
              height={200}
            />
          </div>

          <div>
            <h3 className="text-lg font-semibold text-[#183B4E] mb-4">Risk Level Distribution</h3>
            <DonutChart
              data={riskDistributionData}
              height={200}
            />
          </div>
        </div>

        {/* User Management Section */}
        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold text-[#183B4E] mb-4">User Management</h3>

            {/* Search */}
            <div className="relative mb-4">
              <Search size={16} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Search users..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#27548A] focus:border-transparent"
              />
            </div>

            {/* User Status Summary */}
            <div className="grid grid-cols-3 gap-4 mb-4">
              <div className="text-center p-3 bg-green-50 rounded-lg">
                <Users size={20} className="text-green-600 mx-auto mb-1" />
                <p className="text-sm font-medium text-green-800">Active</p>
                <p className="text-lg font-bold text-green-900">8,542</p>
              </div>
              <div className="text-center p-3 bg-gray-50 rounded-lg">
                <Users size={20} className="text-gray-600 mx-auto mb-1" />
                <p className="text-sm font-medium text-gray-800">Inactive</p>
                <p className="text-lg font-bold text-gray-900">4,005</p>
              </div>
              <div className="text-center p-3 bg-red-50 rounded-lg">
                <AlertTriangle size={20} className="text-red-600 mx-auto mb-1" />
                <p className="text-sm font-medium text-red-800">High Risk</p>
                <p className="text-lg font-bold text-red-900">1,234</p>
              </div>
            </div>
          </div>

          {/* Recent Registrations */}
          <div>
            <h4 className="text-md font-semibold text-[#183B4E] mb-3">Recent Registrations</h4>
            <DataTable
              data={recentUsers}
              columns={userColumns}
              className="border border-gray-200 rounded-lg"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserAnalyticsSection;
