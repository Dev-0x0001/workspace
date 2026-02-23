// Configuration for metrics collection
module.exports = {
  collection: {
    interval: 5000,
    maxRetention: '30d',
    sampleRate: 1.0
  },
  
  // Alerting thresholds
  alerts: {
    cpu: { warning: 80, critical: 90 },
    memory: { warning: 85, critical: 95 }
  }
};