import { AnalyticsData, PlatformMetrics, CustomerBehavior, PricingData } from './types';

export const fetchAnalytics = async (listingId: string): Promise<AnalyticsData> => {
  try {
    const response = await fetch(`/api/analytics/performance/${listingId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch analytics data');
    }
    return response.json();
  } catch (error) {
    console.error('Error fetching analytics:', error);
    throw error;
  }
};

export const fetchPlatformMetrics = async (): Promise<PlatformMetrics[]> => {
  try {
    const response = await fetch('/api/analytics/platforms');
    if (!response.ok) {
      throw new Error('Failed to fetch platform metrics');
    }
    return response.json();
  } catch (error) {
    console.error('Error fetching platform metrics:', error);
    throw error;
  }
};

export const fetchCustomerBehavior = async (timeRange: string): Promise<CustomerBehavior> => {
  try {
    const response = await fetch(`/api/analytics/customers?timeRange=${timeRange}`);
    if (!response.ok) {
      throw new Error('Failed to fetch customer behavior data');
    }
    return response.json();
  } catch (error) {
    console.error('Error fetching customer behavior:', error);
    throw error;
  }
};

export const fetchPricingAnalytics = async (category: string): Promise<PricingData> => {
  try {
    const response = await fetch(`/api/analytics/pricing?category=${category}`);
    if (!response.ok) {
      throw new Error('Failed to fetch pricing analytics');
    }
    return response.json();
  } catch (error) {
    console.error('Error fetching pricing analytics:', error);
    throw error;
  }
};
