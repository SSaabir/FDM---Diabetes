import React from 'react';
import { Users, Activity, Target, Zap, TrendingUp, TrendingDown } from 'lucide-react';

const StatCard = ({ title, value, change, icon, color, status }) => {
  const iconMap = {
    Users,
    Activity,
    Target,
    Zap
  };

  const IconComponent = iconMap[icon];

  const colorClasses = {
    blue: 'bg-[#27548A] text-white',
    green: 'bg-green-500 text-white',
    gold: 'bg-[#DDA853] text-white',
    purple: 'bg-purple-500 text-white'
  };

  const getChangeColor = (change) => {
    if (!change) return '';
    if (change.startsWith('+')) return 'text-green-600';
    if (change.startsWith('-')) return 'text-red-600';
    return 'text-gray-600';
  };

  const getChangeIcon = (change) => {
    if (!change) return null;
    if (change.startsWith('+')) return <TrendingUp size={14} className="inline ml-1" />;
    if (change.startsWith('-')) return <TrendingDown size={14} className="inline ml-1" />;
    return null;
  };

  return (
    <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-100">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600 mb-1">{title}</p>
          <p className="text-2xl font-bold text-[#183B4E]">{value}</p>
          {change && (
            <p className={`text-sm font-medium ${getChangeColor(change)} mt-1`}>
              {change}
              {getChangeIcon(change)}
            </p>
          )}
        </div>
        <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
          <IconComponent size={24} />
        </div>
      </div>
      {status && (
        <div className="mt-4">
          <div className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
            status === 'good' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
          }`}>
            {status === 'good' ? 'Excellent' : 'Needs Attention'}
          </div>
        </div>
      )}
    </div>
  );
};

export default StatCard;
