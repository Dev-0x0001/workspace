export default {
  enhancement: {
    enabled: true,
    autoRun: true,
    checkFrequency: 'daily',
    environment: process.env.NODE_ENV || 'development',
    maxRetries: 3,
    retryDelay: 5000,
    // Performance targets
    performance: {
      maxResponseTime: 500, // milliseconds
      minThroughput: 100, // requests per second
    },
    // Security targets
    security: {
      vulnerabilitySeverityThreshold: 'medium',
      penetrationTestScore: 85,
    },
    // Efficiency targets
    efficiency: {
      maxCpuUsage: 80, // percent
      maxMemoryUsage: 85, // percent
    }
  }
};