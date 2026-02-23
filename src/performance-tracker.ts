export default class PerformanceTracker {
  static instance = null;

  static getInstance() {
    if (!this.instance) {
      this.instance = new PerformanceTracker();
    }
    return this.instance;
  }

  performanceData = {
    metrics: {},
    timestamps: {};
  };

  startMeasurement(name) {
    this.performanceData.timestamps[name] = {
      start: new Date().getTime(),
      end: null,
      duration: null
    };
    return this;
  }

  endMeasurement(name) {
    const measurement = this.performanceData.timestamps[name];
    if (measurement) {
      measurement.end = new Date().getTime();
      measurement.duration = measurement.end - measurement.start;
      measurement.timestamp = new Date().toISOString();

      // Record this metric
      if (!this.performanceData.metrics[name]) {
        this.performanceData.metrics[name] = [];
      }
      this.performanceData.metrics[name].push(measurement);
    }
    return this;
  }

  getMeasurement(name) {
    return this.performanceData.metrics[name] || [];
  }

  clearMeasurements() {
    this.performanceData = {
      metrics: {},
      timestamps: {}
    };
    return this;
  }
}
