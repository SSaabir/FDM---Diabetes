import React from 'react';
import { Play, Eye, RotateCcw, Upload, Clock, CheckCircle } from 'lucide-react';
import ProgressBar from '../ui/ProgressBar';
import Badge from '../ui/Badge';

const ModelManagementSection = ({ data, loading }) => {
  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <div className="h-6 bg-gray-200 rounded mb-6 animate-pulse"></div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="border border-gray-200 rounded-lg p-4 animate-pulse">
            <div className="h-4 bg-gray-200 rounded mb-4"></div>
            <div className="space-y-3">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="h-4 bg-gray-200 rounded"></div>
              ))}
            </div>
          </div>
          <div className="border border-gray-200 rounded-lg p-4 animate-pulse">
            <div className="h-4 bg-gray-200 rounded mb-4"></div>
            <div className="h-8 bg-gray-200 rounded mb-4"></div>
            <div className="space-y-3">
              {[...Array(2)].map((_, i) => (
                <div key={i} className="h-12 bg-gray-200 rounded"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  const currentModel = data?.currentModel || {
    name: "Diabetes Risk Model v2.1",
    version: "2.1.0",
    accuracy: 0.847,
    status: "Production",
    deployedDate: "2024-03-15"
  };

  const trainingJobs = data?.trainingJobs || [
    {
      id: 1,
      modelName: "Diabetes Risk Model v2.2",
      status: "Training",
      progress: 67,
      accuracy: 0.821,
      startTime: "2024-03-20 10:30"
    },
    {
      id: 2,
      modelName: "Diabetes Risk Model v2.0",
      status: "Completed",
      progress: 100,
      accuracy: 0.834,
      startTime: "2024-03-19 14:15"
    }
  ];

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <h2 className="text-xl font-bold text-[#183B4E] mb-6">ML Model Management</h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Current Production Model */}
        <div className="border border-gray-200 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-[#183B4E] mb-4">Current Production Model</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Model Name:</span>
              <span className="font-medium text-[#27548A]">{currentModel.name}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Version:</span>
              <Badge variant="secondary">{currentModel.version}</Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Accuracy:</span>
              <span className="font-bold text-[#DDA853]">{(currentModel.accuracy * 100).toFixed(1)}%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Status:</span>
              <Badge variant="success">{currentModel.status}</Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Deployed:</span>
              <span className="text-sm text-gray-800">{currentModel.deployedDate}</span>
            </div>
          </div>
          <div className="flex space-x-2 mt-4">
            <button className="flex-1 px-3 py-2 bg-[#27548A] text-white text-sm rounded hover:bg-[#183B4E] transition-colors">
              <Eye size={14} className="inline mr-1" />
              View Details
            </button>
            <button className="flex-1 px-3 py-2 bg-gray-200 text-gray-700 text-sm rounded hover:bg-gray-300 transition-colors">
              <RotateCcw size={14} className="inline mr-1" />
              Roll Back
            </button>
          </div>
        </div>

        {/* Model Training */}
        <div className="border border-gray-200 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-[#183B4E] mb-4">Model Training</h3>

          {/* Quick Start Training */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">Quick Start Training</label>
            <div className="flex space-x-2">
              <select className="flex-1 px-3 py-2 border border-gray-300 rounded text-sm">
                <option>Select Dataset</option>
                <option>diabetes_march_2024.csv</option>
                <option>diabetes_feb_2024.csv</option>
              </select>
              <button className="px-4 py-2 bg-[#DDA853] text-white rounded hover:bg-[#B89446] transition-colors">
                <Play size={16} />
              </button>
            </div>
          </div>

          {/* Active Training Jobs */}
          <div className="space-y-3">
            <h4 className="text-sm font-medium text-gray-700">Recent Training Jobs</h4>
            {trainingJobs.map((job) => (
              <div key={job.id} className="border border-gray-100 rounded p-3">
                <div className="flex justify-between items-start mb-2">
                  <span className="text-sm font-medium text-[#183B4E]">{job.modelName}</span>
                  <Badge variant={job.status === 'Training' ? 'warning' : 'success'}>
                    {job.status === 'Training' ? <Clock size={12} className="inline mr-1" /> : <CheckCircle size={12} className="inline mr-1" />}
                    {job.status}
                  </Badge>
                </div>
                <ProgressBar progress={job.progress} className="mb-2" />
                <div className="flex justify-between text-xs text-gray-600">
                  <span>Accuracy: {(job.accuracy * 100).toFixed(1)}%</span>
                  <span>Started: {job.startTime}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModelManagementSection;
