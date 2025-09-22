import React, { useRef } from 'react';
import { Upload, FileText } from 'lucide-react';

const FileUpload = ({ onUpload }) => {
  const fileInputRef = useRef(null);

  const handleDrop = (e) => {
    e.preventDefault();
    const files = Array.from(e.dataTransfer.files);
    onUpload(files);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files);
    onUpload(files);
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div
      className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-[#27548A] transition-colors cursor-pointer"
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onClick={handleClick}
    >
      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept=".csv,.json,.xlsx,.xls"
        onChange={handleFileSelect}
        className="hidden"
      />
      <Upload size={48} className="text-gray-400 mx-auto mb-4" />
      <p className="text-lg font-medium text-[#183B4E] mb-2">
        Drop files here or click to browse
      </p>
      <p className="text-sm text-gray-600">
        Supported formats: CSV, JSON, Excel
      </p>
      <p className="text-xs text-gray-500 mt-2">
        Maximum file size: 50MB
      </p>
    </div>
  );
};

export default FileUpload;
