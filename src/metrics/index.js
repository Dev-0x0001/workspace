const collector = require('./collector');

const metrics = {
  track(key, value) {
    // In a real system, this would send metrics to a collection service
    console.log(`Metric ${key}: ${value}`);
  }
};

module.exports = metrics;