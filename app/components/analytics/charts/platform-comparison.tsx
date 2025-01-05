import React, { useEffect, useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

interface PlatformMetric {
  platform: string;
  total_listings: number;
  active_listings: number;
  total_sales: number;
  average_price: number;
}

export const PlatformComparison: React.FC = () => {
  const [data, setData] = useState<PlatformMetric[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPlatformData = async () => {
      try {
        setLoading(true);
        const response = await fetch('/api/analytics/platforms');
        if (!response.ok) {
          throw new Error('Failed to fetch platform data');
        }
        const platformData = await response.json();
        setData(platformData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchPlatformData();
  }, []);

  if (loading) {
    return <div>Loading platform metrics...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="w-full h-[400px] p-4">
      <h2 className="text-xl font-semibold mb-4">Platform Comparison</h2>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="platform" />
          <YAxis yAxisId="left" />
          <YAxis yAxisId="right" orientation="right" />
          <Tooltip />
          <Legend />
          <Bar yAxisId="left" dataKey="total_listings" fill="#8884d8" name="Total Listings" />
          <Bar yAxisId="left" dataKey="active_listings" fill="#82ca9d" name="Active Listings" />
          <Bar yAxisId="right" dataKey="total_sales" fill="#ffc658" name="Total Sales" />
          <Bar yAxisId="right" dataKey="average_price" fill="#ff7300" name="Average Price ($)" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PlatformComparison;
