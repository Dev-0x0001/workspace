export default class EnhancementDatabase {
  static instance = null;

  static getInstance() {
    if (!this.instance) {
      this.instance = new EnhancementDatabase();
    }
    return this.instance;
  }

  constructor() {
    this.collections = {};
    this.connection = null;
    this.isConnected = false;
  }

  async connect(uri, options = {}) {
    if (this.isConnecting || this.isConnected) {
      return this;
    }

    this.isConnecting = true;

    try {
      // In a real implementation, connect to database
      // This is a simulation for demonstration
      this.connection = { uri, options };
      this.isConnected = true;
      this.isConnecting = false;

      await this._initializeCollections();

      return this;
    } catch (error) {
      this.isConnecting = false;
      throw error;
    }
  }

  async _initializeCollections() {
    // Define collections
    this.collections.metrics = this.connection.db.collection('metrics');
    this.collections.enhancements = this.connection.db.collection('enhancements');
    this.collections.state = this.connection.db.collection('state');
    
    // Create indexes if needed
    await this._createIndexes();
  }

  async _createIndexes() {
    // Create index on metrics collection
    await this.collections.metrics.createIndex({
      category: 1,
      name: 1,
      timestamp: 1
    }, { unique: false });

    // Create index on enhancements
    await this.collections.enhancements.createIndex({
      aspect: 1,
      timestamp: -1
    }, { unique: false });
  }

  async saveMetric(category, name, value, metadata = {}) {
    if (!this.isConnected) {
      throw new Error('Database not connected');
    }

    const metric = {
      category,
      name,
      value,
      metadata,
      timestamp: new Date().toISOString()
    };

    await this.collections.metrics.insertOne(metric);
    return metric;
  }

  async saveEnhancement(record) {
    if (!this.isConnected) {
      throw new Error('Database not connected');
    }

    await this.collections.enhancements.insertOne(record);
    return record;
  }

  async updateState(newState) {
    if (!this.isConnected) {
      throw new Error('Database not connected');
    }

    const result = await this.collections.state.updateOne(
      {},
      { $set: newState },
      { upsert: true }
    );

    return result;
  }

  async getState() {
    if (!this.isConnected) {
      throw new Error('Database not connected');
    }

    const doc = await this.collections.state.findOne();
    return doc || {};
  }

  async getEnhancementByHash(hash) {
    if (!this.isConnected) {
      throw new Error('Database not connected');
    }

    const doc = await this.collections.enhancements.findOne({
      hash: hash
    });

    return doc;
  }
}
