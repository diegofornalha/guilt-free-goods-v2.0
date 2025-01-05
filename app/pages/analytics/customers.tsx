import React from 'react';
import { CustomerBehavior } from '../../components/analytics/charts/customer-behavior';

export default function CustomersPage() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold mb-8">Customer Analytics</h1>
      <div className="bg-white rounded-lg shadow-lg">
        <CustomerBehavior />
      </div>
    </div>
  );
}
