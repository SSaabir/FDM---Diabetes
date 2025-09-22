import React, { useState } from 'react';
import { Upload, FileText, Download, Eye, CheckCircle, AlertCircle } from 'lucide-react';
import FileUpload from '../ui/FileUpload';
import DataTable from '../ui/DataTable';

const DatasetSection = ({ data, loading }) => {
  const [uploadedFiles, setUploadedFiles] = useState([]);

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <div className="h-6 bg-gray-200 rounded mb-6 animate-pulse"></div>
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 mb-6">
          <div className="h-8 bg-gray-200 rounded mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-3/4 mx-auto"></div>
        </div>
        <div className="h-48 bg-gray-200 rounded"></div>
      </div>
    );
  }

  const datasets = data || [
    {
      id: 1,
      name: "diabetes_march_2024.csv",
      size: "2.3 MB",
      rows: 10500,
      uploadDate: "2024-03-20",
      status: "Ready"
    },
    {
      id: 2,
      name: "diabetes_feb_2024.csv",
      size: "1.8 MB",
      rows: 8900,
      uploadDate: "2024-03-15",
      status: "Processing"
    },
    {
      id: 3,
      name: "diabetes_jan_2024.csv",
      size: "2.1 MB",
      rows: 9750,
      uploadDate: "2024-03-10",
      status: "Ready"
    }
  ];

  const handleFileUpload = (files) => {
    // Simulate file upload
    const newFiles = files.map((file, index) => ({
      id: Date.now() + index,
      name: file.name,
      size: `${(file.size / 1024 / 1024).toFixed(1)} MB`,
      rows: 'Processing...',
      uploadDate: new Date().toISOString().split('T')[0],
      status: 'Uploading'
    }));
    setUploadedFiles([...uploadedFiles, ...newFiles]);
  };

  const columns = [
    { key: 'name', header: 'Dataset Name', render: (row) => (
      <div className="flex items-center">
        <FileText size={16} className="text-[#27548A] mr-2" />
        <span className="font-medium">{row.name}</span>
      </div>
    )},
    { key: 'size', header: 'Size' },
    { key: 'rows', header: 'Rows' },
    { key: 'uploadDate', header: 'Upload Date' },
    { key: 'status', header: 'Status', render: (row) => (
      <div className="flex items-center">
        {row.status === 'Ready' ? (
          <CheckCircle size={14} className="text-green-500 mr-1" />
        ) : row.status === 'Processing' ? (
          <AlertCircle size={14} className="text-yellow-500 mr-1" />
        ) : (
          <Upload size={14} className="text-blue-500 mr-1" />
        )}
        <span className={`text-sm ${
          row.status === 'Ready' ? 'text-green-700' :
          row.status === 'Processing' ? 'text-yellow-700' : 'text-blue-700'
        }`}>
          {row.status}
        </span>
      </div>
    )},
    { key: 'actions', header: 'Actions', render: (row) => (
      <div className="flex space-x-2">
        <button key={`view-${row.id}`} className="p-1 text-[#27548A] hover:bg-blue-50 rounded">
          <Eye size={14} />
        </button>
        <button key={`download-${row.id}`} className="p-1 text-[#27548A] hover:bg-blue-50 rounded">
          <Download size={14} />
        </button>
      </div>
    )}
  ];

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <h2 className="text-xl font-bold text-[#183B4E] mb-6">Dataset Management</h2>

      <div className="space-y-6">
        {/* File Upload Area */}
        <div>
          <h3 className="text-lg font-semibold text-[#183B4E] mb-4">Upload New Dataset</h3>
          <FileUpload onUpload={handleFileUpload} />
        </div>

        {/* Dataset List */}
        <div>
          <h3 className="text-lg font-semibold text-[#183B4E] mb-4">Recent Datasets</h3>
          <DataTable
            data={[...datasets, ...uploadedFiles]}
            columns={columns}
            className="border border-gray-200 rounded-lg"
          />
        </div>
      </div>
    </div>
  );
};

export default DatasetSection;
