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

interface PricingMetric {
  timestamp: string;
  average_price: number;
  price_range_low: number;
  price_range_high: number;
  optimal_price: number;
}

export const PricingAnalysis: React.FC = () => {
  const [data, setData] = useState<PricingMetric[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPricingData = async () => {
      try {
        setLoading(true);
        const response = await fetch('/api/analytics/pricing');
        if (!response.ok) {
          throw new Error('Failed to fetch pricing data');
        }
        const pricingData = await response.json();
        setData(pricingData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchPricingData();
  }, []);

  if (loading) {
    return <div>Loading pricing metrics...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="w-full h-[400px] p-4">
      <h2 className="text-xl font-semibold mb-4">Pricing Analysis</h2>
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
          <YAxis />
          <Tooltip
            labelFormatter={(value) => new Date(value).toLocaleString()}
            formatter={(value) => [`$${value}`, 'Price']}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="average_price"
            stroke="#8884d8"
            name="Average Price"
          />
          <Line
            type="monotone"
            dataKey="price_range_low"
            stroke="#82ca9d"
            name="Price Range (Low)"
          />
          <Line
            type="monotone"
            dataKey="price_range_high"
            stroke="#ffc658"
            name="Price Range (High)"
          />
          <Line
            type="monotone"
            dataKey="optimal_price"
            stroke="#ff7300"
            name="Optimal Price"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PricingAnalysis;
