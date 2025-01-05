import React from 'react';
import { PlatformComparison } from '../../components/analytics/charts/platform-comparison';

export default function PlatformsPage() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold mb-8">Platform Analytics</h1>
      <div className="bg-white rounded-lg shadow-lg">
        <PlatformComparison />
      </div>
    </div>
  );
}
