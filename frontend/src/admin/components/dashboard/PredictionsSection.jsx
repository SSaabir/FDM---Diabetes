import React from 'react';
import AreaChart from '../charts/AreaChart';
import LineChart from '../charts/LineChart';
import BarChart from '../charts/BarChart';

const PredictionsSection = ({ loading }) => {
  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <div className="h-6 bg-gray-200 rounded mb-6 animate-pulse"></div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="lg:col-span-2 h-64 bg-gray-200 rounded animate-pulse"></div>
          <div className="h-64 bg-gray-200 rounded animate-pulse"></div>
        </div>
        <div className="h-64 bg-gray-200 rounded animate-pulse"></div>
      </div>
    );
  }
  // Mock data for predictions over time
  const predictionsOverTime = [
    { date: '2024-03-14', predictions: 1247 },
    { date: '2024-03-15', predictions: 1356 },
    { date: '2024-03-16', predictions: 1189 },
    { date: '2024-03-17', predictions: 1423 },
    { date: '2024-03-18', predictions: 1387 },
    { date: '2024-03-19', predictions: 1298 },
    { date: '2024-03-20', predictions: 1456 }
  ];

  // Mock data for accuracy trend
  const accuracyTrend = [
    { date: '2024-03-14', accuracy: 83.2 },
    { date: '2024-03-15', accuracy: 84.1 },
    { date: '2024-03-16', accuracy: 82.9 },
    { date: '2024-03-17', accuracy: 85.3 },
    { date: '2024-03-18', accuracy: 84.7 },
    { date: '2024-03-19', accuracy: 83.8 },
    { date: '2024-03-20', accuracy: 84.7 }
  ];

  // Mock data for risk factor distribution
  const riskFactors = [
    { factor: 'Age', count: 2456 },
    { factor: 'BMI', count: 1890 },
    { factor: 'Blood Pressure', count: 1654 },
    { factor: 'Glucose', count: 2134 },
    { factor: 'Family History', count: 987 },
    { factor: 'Lifestyle', count: 1456 }
  ];

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <h2 className="text-xl font-bold text-[#183B4E] mb-6">Predictions Analytics</h2>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Predictions Over Time */}
        <div className="lg:col-span-2">
          <h3 className="text-lg font-semibold text-[#183B4E] mb-4">Predictions Made Over Time</h3>
          <AreaChart
            data={predictionsOverTime}
            xKey="date"
            yKey="predictions"
            height={250}
          />
        </div>

        {/* Prediction Accuracy Trend */}
        <div>
          <h3 className="text-lg font-semibold text-[#183B4E] mb-4">Prediction Accuracy Trend</h3>
          <LineChart
            data={accuracyTrend}
            xKey="date"
            yKey="accuracy"
            height={250}
          />
        </div>
      </div>

      {/* Risk Factor Distribution */}
      <div className="mt-8">
        <h3 className="text-lg font-semibold text-[#183B4E] mb-4">Risk Factor Distribution</h3>
        <BarChart
          data={riskFactors}
          xKey="factor"
          yKey="count"
          height={300}
        />
      </div>
    </div>
  );
};

export default PredictionsSection;
