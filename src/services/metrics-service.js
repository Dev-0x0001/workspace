const metrics = require('../metrics');
const { MetricsCollector } = require('../../metrics/collector');

class MetricsService {
  constructor() {
    this.collector = new MetricsCollector();
    this.enabled = true;
  }

  startCollection() {
    if (this.enabled) {
      this.collector.start();
    }
  }

  stopCollection() {
    this.collector.stop();
  }

  // Example: Record a custom metric
  recordCustomMetric(key, value) {
    metrics.track(key, value);
  }
}

module.exports = MetricsService;