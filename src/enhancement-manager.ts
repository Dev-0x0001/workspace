import ContinuousEnhancement from './continuous-enhancement';

// Configuration for the enhancement system
const ENHANCEMENT_CONFIG = {
  autoEnhance: true,
  checkInterval: 24 * 60 * 60 * 1000, // 24 hours
  maxRetries: 3,
  retryDelay: 5000,
  // Add configuration for different environments
  environments: {
    production: { checkInterval: 12 * 60 * 60 * 1000 }, // 12 hours
    development: { checkInterval: 60 * 60 * 1000 } // 1 hour
  }
};

// Global enhancement manager
export class EnhancementManager {
  static instance = null;
  config = ENHANCEMENT_CONFIG;
  enhancementService = null;

  static getInstance() {
    if (!this.instance) {
      this.instance = new EnhancementManager();
    }
    return this.instance;
  }

  constructor(config = {}) {
    this.config = { ...this.config, ...config };
    this.enhancementService = new ContinuousEnhancement({
      autoEnhance: this.config.autoEnhance
    });
  }

  async start() {
    if (this.config.autoEnhance) {
      this._startAutoEnhancement();
    }
  }

  _startAutoEnhancement() {
    // Start initial enhancement
    this._runEnhancement()
      .catch(console.error);

    // Set interval for periodic checks
    this.intervalId = setInterval(() => {
      this._runEnhancement()
        .catch(console.error);
    }, this.config.checkInterval);
  }

  async _runEnhancement() {
    try {
      if (!this.enhancementService.isEnhancing) {
        await this.enhancementService.startEnhancement('all');
      }
    } catch (error) {
      console.error('Automatic enhancement failed:', error);
      // Handle retry logic
    }
  }

  // Method to manually trigger enhancement
  async triggerEnhancement(aspect = 'all') {
    return this.enhancementService.startEnhancement(aspect);
  }

  // Method to get last enhancement results
  getLastEnhancementResults() {
    return this.enhancementService.lastEnhancement;
  }

  // Cleanup on stop
  stop() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  }
}

// Export the instance
export default EnhancementManager.getInstance();