
import React from 'react';
import StatCard from '../ui/StatCard';

const MetricsCards = ({ data, loading }) => {
  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {[...Array(4)].map((_, index) => (
          <div key={index} className="bg-white rounded-lg shadow-sm p-6 animate-pulse">
            <div className="h-4 bg-gray-200 rounded mb-2"></div>
            <div className="h-8 bg-gray-200 rounded mb-2"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          </div>
        ))}
      </div>
    );
  }

  const metrics = [
    {
      title: "Total Users",
      value: data?.totalUsers?.toLocaleString() || "12,547",
      change: "+12%",
      icon: "Users",
      color: "blue"
    },
    {
      title: "Active Today",
      value: data?.activeToday?.toLocaleString() || "1,823",
      change: null,
      icon: "Activity",
      color: "green"
    },
    {
      title: "Model Accuracy",
      value: data?.modelAccuracy ? `${(data.modelAccuracy * 100).toFixed(1)}%` : "84.7%",
      change: null,
      icon: "Target",
      color: "gold",
      status: "good"
    },
    {
      title: "Training Jobs",
      value: data?.trainingJobs ? `${data.trainingJobs.active} Active` : "1 Active",
      change: data?.trainingJobs ? `${data.trainingJobs.completed} completed today` : "2 completed today",
      icon: "Zap",
      color: "purple"
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {metrics.map((metric, index) => (
        <StatCard key={index} {...metric} />
      ))}
    </div>
  );
};

export default MetricsCards;
