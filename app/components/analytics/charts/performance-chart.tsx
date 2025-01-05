import React, { useEffect, useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

interface PerformanceMetric {
  timestamp: string;
  total_views: number;
  total_clicks: number;
  conversion_rate: number;
  total_revenue: number;
}

interface PerformanceChartProps {
  timeRange?: 'day' | 'week' | 'month' | 'year';
}

export const PerformanceChart: React.FC<PerformanceChartProps> = ({ 
  timeRange = 'week' 
}) => {
  const [data, setData] = useState<PerformanceMetric[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPerformanceData = async () => {
      try {
        setLoading(true);
        const response = await fetch(`/api/analytics/performance?timeRange=${timeRange}`);
        if (!response.ok) {
          throw new Error('Failed to fetch performance data');
        }
        const performanceData = await response.json();
        setData(performanceData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchPerformanceData();
  }, [timeRange]);

  if (loading) {
    return <div>Loading performance metrics...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="w-full h-[400px] p-4">
      <h2 className="text-xl font-semibold mb-4">Performance Metrics</h2>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="timestamp" 
            tickFormatter={(value) => new Date(value).toLocaleDateString()}
          />
          <YAxis yAxisId="left" />
          <YAxis yAxisId="right" orientation="right" />
          <Tooltip
            labelFormatter={(value) => new Date(value).toLocaleString()}
            formatter={(value, name) => [
              value,
              name === 'conversion_rate' ? 'Conversion Rate' :
              name === 'total_views' ? 'Total Views' :
              name === 'total_clicks' ? 'Total Clicks' :
              'Revenue'
            ]}
          />
          <Legend />
          <Line
            yAxisId="left"
            type="monotone"
            dataKey="total_views"
            stroke="#8884d8"
            name="Total Views"
          />
          <Line
            yAxisId="left"
            type="monotone"
            dataKey="total_clicks"
            stroke="#82ca9d"
            name="Total Clicks"
          />
          <Line
            yAxisId="right"
            type="monotone"
            dataKey="conversion_rate"
            stroke="#ffc658"
            name="Conversion Rate (%)"
          />
          <Line
            yAxisId="right"
            type="monotone"
            dataKey="total_revenue"
            stroke="#ff7300"
            name="Revenue ($)"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PerformanceChart;
