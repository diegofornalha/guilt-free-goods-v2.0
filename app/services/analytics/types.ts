export interface AnalyticsData {
  views: number;
  clicks: number;
  conversions: number;
  revenue: number;
  timeRange: string;
  trends: {
    date: string;
    value: number;
  }[];
}

export interface PlatformMetrics {
  platform: string;
  totalListings: number;
  activeListings: number;
  totalSales: number;
  averagePrice: number;
}

export interface CustomerBehavior {
  engagementRate: number;
  averageTimeOnListing: number;
  returnRate: number;
  demographics: {
    age: string;
    percentage: number;
  }[];
  interests: {
    category: string;
    score: number;
  }[];
}

export interface PricingData {
  category: string;
  averagePrice: number;
  priceRange: {
    min: number;
    max: number;
  };
  competitorPrices: {
    platform: string;
    price: number;
  }[];
  seasonalTrends: {
    season: string;
    priceChange: number;
  }[];
}
