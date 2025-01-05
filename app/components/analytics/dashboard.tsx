import React, { useState } from 'react';
import PerformanceChart from './charts/performance-chart';
import PlatformComparison from './charts/platform-comparison';
import CustomerBehavior from './charts/customer-behavior';
import PricingAnalysis from './charts/pricing-analysis';

type TimeRange = 'day' | 'week' | 'month' | 'year';

export const AnalyticsDashboard: React.FC = () => {
  const [timeRange, setTimeRange] = useState<TimeRange>('week');

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Analytics Dashboard</h1>
        <select
          value={timeRange}
          onChange={(e) => setTimeRange(e.target.value as TimeRange)}
          className="p-2 border rounded-md"
        >
          <option value="day">Last 24 Hours</option>
          <option value="week">Last Week</option>
          <option value="month">Last Month</option>
          <option value="year">Last Year</option>
        </select>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white rounded-lg shadow-lg">
          <PerformanceChart timeRange={timeRange} />
        </div>
        <div className="bg-white rounded-lg shadow-lg">
          <PlatformComparison />
        </div>
        <div className="bg-white rounded-lg shadow-lg">
          <CustomerBehavior />
        </div>
        <div className="bg-white rounded-lg shadow-lg">
          <PricingAnalysis />
        </div>
      </div>

      <div className="mt-8">
        <h2 className="text-2xl font-semibold mb-4">Key Insights</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white p-4 rounded-lg shadow">
            <h3 className="text-lg font-medium text-gray-600">Total Revenue</h3>
            <div className="text-2xl font-bold mt-2" id="total-revenue">
              Loading...
            </div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <h3 className="text-lg font-medium text-gray-600">Active Listings</h3>
            <div className="text-2xl font-bold mt-2" id="active-listings">
              Loading...
            </div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <h3 className="text-lg font-medium text-gray-600">Conversion Rate</h3>
            <div className="text-2xl font-bold mt-2" id="conversion-rate">
              Loading...
            </div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <h3 className="text-lg font-medium text-gray-600">Avg. Price</h3>
            <div className="text-2xl font-bold mt-2" id="average-price">
              Loading...
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;
