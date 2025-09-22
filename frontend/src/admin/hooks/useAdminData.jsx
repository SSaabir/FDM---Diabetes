import { useState, useEffect } from 'react';

const useAdminData = () => {
  const [data, setData] = useState({
    metrics: {
      totalUsers: 12547,
      activeToday: 1823,
      modelAccuracy: 0.847,
      trainingJobs: { active: 1, completed: 2 }
    },
    currentModel: {
      name: "Diabetes Risk Model v2.1",
      version: "2.1.0",
      accuracy: 0.847,
      status: "Production",
      deployedDate: "2024-03-15"
    },
    trainingJobs: [
      {
        id: 1,
        modelName: "Diabetes Risk Model v2.2",
        status: "Training",
        progress: 67,
        accuracy: 0.821,
        startTime: "2024-03-20 10:30"
      }
    ],
    datasets: [
      {
        id: 1,
        name: "diabetes_march_2024.csv",
        size: "2.3 MB",
        rows: 10500,
        uploadDate: "2024-03-20",
        status: "Ready"
      }
    ],
    recentUsers: [
      {
        id: 1,
        name: "John Doe",
        email: "john@example.com",
        registrationDate: "2024-03-20",
        riskLevel: "Medium"
      }
    ]
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const refreshData = async () => {
    setLoading(true);
    try {
      // In a real app, this would fetch from API
      // For now, we'll simulate with a timeout
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Simulate updated data
      setData(prevData => ({
        ...prevData,
        metrics: {
          ...prevData.metrics,
          activeToday: prevData.metrics.activeToday + Math.floor(Math.random() * 50) - 25
        }
      }));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshData();
  }, []);

  return { data, loading, error, refreshData };
};

export default useAdminData;
