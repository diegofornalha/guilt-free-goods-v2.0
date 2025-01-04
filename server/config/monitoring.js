const monitoring = {
  imageRecognition: {
    metrics: [
      'accuracy',
      'inference_time',
      'confidence_scores',
      'error_rates'
    ],
    thresholds: {
      accuracy: 0.85,
      inference_time: 2000, // ms
      minimum_confidence: 0.7
    }
  },
  marketAnalysis: {
    metrics: [
      'price_accuracy',
      'data_freshness',
      'coverage_rate'
    ],
    thresholds: {
      price_deviation: 0.15,
      max_data_age: 24 // hours
    }
  },
  descriptionGeneration: {
    metrics: [
      'relevance_score',
      'seo_score',
      'generation_time'
    ],
    thresholds: {
      minimum_relevance: 0.8,
      minimum_seo_score: 75
    }
  }
};

module.exports = monitoring;