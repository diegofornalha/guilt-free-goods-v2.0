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

interface CustomerMetric {
  timestamp: string;
  unique_visitors: number;
  repeat_customers: number;
  average_session_duration: number;
  cart_abandonment_rate: number;
}

export const CustomerBehavior: React.FC = () => {
  const [data, setData] = useState<CustomerMetric[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCustomerData = async () => {
      try {
        setLoading(true);
        const response = await fetch('/api/analytics/customers');
        if (!response.ok) {
          throw new Error('Failed to fetch customer data');
        }
        const customerData = await response.json();
        setData(customerData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchCustomerData();
  }, []);

  if (loading) {
    return <div>Loading customer metrics...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="w-full h-[400px] p-4">
      <h2 className="text-xl font-semibold mb-4">Customer Behavior Analysis</h2>
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
          />
          <Legend />
          <Line
            yAxisId="left"
            type="monotone"
            dataKey="unique_visitors"
            stroke="#8884d8"
            name="Unique Visitors"
          />
          <Line
            yAxisId="left"
            type="monotone"
            dataKey="repeat_customers"
            stroke="#82ca9d"
            name="Repeat Customers"
          />
          <Line
            yAxisId="right"
            type="monotone"
            dataKey="average_session_duration"
            stroke="#ffc658"
            name="Avg Session Duration (min)"
          />
          <Line
            yAxisId="right"
            type="monotone"
            dataKey="cart_abandonment_rate"
            stroke="#ff7300"
            name="Cart Abandonment Rate (%)"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default CustomerBehavior;
