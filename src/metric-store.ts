export default class MetricStore {
  static instance = null;

  static getInstance() {
    if (!this.instance) {
      this.instance = new MetricStore();
    }
    return this.instance;
  }

  metrics = {};

  addMetrics(newMetrics) {
    Object.keys(newMetrics).forEach(category => {
      if (!this.metrics[category]) {
        this.metrics[category] = {};
      }
      Object.keys(newMetrics[category]).forEach(metric => {
        if (!this.metrics[category][metric]) {
          this.metrics[category][metric] = [];
        }
        this.metrics[category][metric].push(...newMetrics[category][metric]);
      });
    });
    return this;
  }

  getMetrics(category = null, metric = null) {
    if (category && metric) {
      return this.metrics[category]?.[metric] || [];
    } else if (category) {
      return this.metrics[category] || {};
    }
    return this.metrics;
  }

  clearMetrics() {
    this.metrics = {};
    return this;
  }
}
