import { createHmac } from 'crypto';
import { v4 as uuidv4 } from 'uuid';
import { EnhancementDatabase } from './database/enhancement-database';
import { EnhancementManager } from './enhancement-manager';

export class EnhancementService {
  static instance = null;

  static getInstance() {
    if (!this.instance) {
      this.instance = new EnhancementService();
    }
    return this.instance;
  }

  database = EnhancementDatabase.getInstance();

  async createEnhancementPlan(planData) {
    // Generate a unique hash for this plan
    const planHash = this._generateHash(planData);

    // Check if plan already exists
    const existing = await this.database.getEnhancementByHash(planHash);
    if (existing) {
      return existing;
    }

    // Create new plan
    const newPlan = {
      ...planData,
      hash: planHash,
      timestamp: new Date().toISOString(),
      status: 'pending'
    };

    // Save to database
    const result = await this.database.saveEnhancement(newPlan);

    // Notify manager
    EnhancementManager.getInstance().notifyPlanCreated(newPlan);

    return result;
  }

  _generateHash(data) {
    // Use a secure hash algorithm
    return createHmac('sha256', process.env.SECRET_KEY || 'default-secret')
      .update(JSON.stringify(data))
      .digest('hex');
  }
}
