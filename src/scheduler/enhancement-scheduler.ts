export default class EnhancementScheduler {
  static instance = null;

  static getInstance() {
    if (!this.instance) {
      this.instance = new EnhancementScheduler();
    }
    return this.instance;
  }

  // Cron-style scheduling patterns
  static CRON_PATTERNS = {
    daily: '0 0 * * *', // Every day at midnight
    hourly: '0 * * * *', // Every hour
    weekly: '0 0 * * 0', // Every Sunday at midnight
    monthly: '0 0 1 * *', // First day of every month
    // Custom intervals
    thirtyMinutes: '0 */30 * * *', // Every 30 minutes
    fiveMinutes: '0 */5 * * *', // Every 5 minutes
    minute: '* * * * *' // Every minute
  };

  constructor() {
    this.jobs = {};
    this.scheduler = null;
    this.isRunning = false;
  }

  async startScheduler() {
    if (this.isRunning) {
      return;
    }

    // Initialize scheduler
    this.scheduler = require('node-cron');
    this.isRunning = true;

    // Start all existing jobs
    await this._startAllJobs();

    // Set up error handling
    process.on('uncaughtException', this._handleSchedulerError.bind(this));
    process.on('unhandledRejection', this._handleSchedulerError.bind(this));
  }

  async stopScheduler() {
    if (!this.isRunning) {
      return;
    }

    this.isRunning = false;

    // Stop all jobs
    await this._stopAllJobs();

    // Clean up error handlers
    process.removeListener('uncaughtException', this._handleSchedulerError.bind(this));
    process.removeListener('unhandledRejection', this._handleSchedulerError.bind(this));

    this.scheduler = null;
  }

  _handleSchedulerError(error) {
    console.error('Scheduler encountered an error:', error);
    // Handle error appropriately
  }

  async _startAllJobs() {
    // Start each job
    Object.values(this.jobs).forEach(job => {
      job.resume();
    });
  }

  async _stopAllJobs() {
    // Stop each job
    Object.values(this.jobs).forEach(job => {
      job.pause();
    });
  }

  async scheduleJob(name, pattern, callback, timezone = 'UTC') {
    if (!this.isRunning) {
      throw new Error('Scheduler is not running');
    }

    if (this.jobs[name]) {
      throw new Error(`Job with name '${name}' already exists`);
    }

    try {
      const job = this.scheduler.schedule(pattern, async () => {
        try {
          await callback();
        } catch (error) {
          console.error(`Job '${name}' failed:`, error);
          // Handle job-specific error
        }
      }, {
        timezone: timezone,
        scheduled: true,
        name: name
      });

      this.jobs[name] = job;
      return job;
    } catch (error) {
      console.error(`Failed to schedule job '${name}':`, error);
      throw error;
    }
  }

  getJob(name) {
    return this.jobs[name];
  }

  async runJobNow(name) {
    const job = this.jobs[name];
    if (job) {
      await job.run();
    } else {
      throw new Error(`Job with name '${name}' not found`);
    }
  }

  listJobs() {
    return Object.keys(this.jobs);
  }

  async deleteJob(name) {
    const job = this.jobs[name];
    if (job) {
      job.stop();
      delete this.jobs[name];
      return true;
    }
    return false;
  }
}
