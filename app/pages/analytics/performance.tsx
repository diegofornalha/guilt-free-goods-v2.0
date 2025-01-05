import React from 'react';
import { PerformanceChart } from '../../components/analytics/charts/performance-chart';

export default function PerformancePage() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold mb-8">Performance Analytics</h1>
      <div className="bg-white rounded-lg shadow-lg">
        <PerformanceChart timeRange="month" />
      </div>
    </div>
  );
}
