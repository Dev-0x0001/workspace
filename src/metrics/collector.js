const metrics = require('./metrics');

class MetricsCollector {
  constructor() {
    this.metrics = {};
    this.interval = null;
  }

  start() {
    if (this.interval) return;
    this.interval = setInterval(() => this.collect(), 5000);
  }

  stop() {
    if (this.interval) {
      clearInterval(this.interval);
      this.interval = null;
    }
  }

  collect() {
    // Collect metrics from various sources
    this.metrics.cpu = process.cpuUsage();
    this.metrics.memory = process.memoryUsage();
    
    // Example AI-specific metrics
    metrics.track('system.cpu_usage', this.metrics.cpu.user);
    metrics.track('system.memory_usage', this.metrics.memory.rss);
  }
}

module.exports = MetricsCollector;