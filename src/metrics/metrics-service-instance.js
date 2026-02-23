const MetricsService = require('../services/metrics-service');

const metricsService = new MetricsService();
metricsService.startCollection();

module.exports = metricsService;