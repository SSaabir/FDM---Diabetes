import React, { useEffect, useState } from "react";
import axios from "axios";
import StatCard from "../ui/StatCard";

const MetricsCards = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchMetrics = async () => {
    try {
      const res = await axios.get("http://localhost:8000/api/metrics/metrics"); 
      setData(res.data);
    } catch (error) {
      console.error("Error fetching metrics:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 30000); // refresh every 30s
    return () => clearInterval(interval);
  }, []);

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
      value: data?.totalUsers?.toLocaleString(),
      change: "+12%", // optional, calculate in backend later
      icon: "Users",
      color: "blue"
    },
    {
      title: "Active Today",
      value: data?.activeToday?.toLocaleString(),
      change: null,
      icon: "Activity",
      color: "green"
    },
    {
      title: "Model Accuracy",
      value: `${(data?.modelAccuracy * 100).toFixed(1)}%`,
      change: null,
      icon: "Target",
      color: "gold",
      status: "good"
    },
    {
      title: "Training Jobs",
      value: `${data?.trainingJobs?.active} Active`,
      change: `${data?.trainingJobs?.completed} completed today`,
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
