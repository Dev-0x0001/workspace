export default class StateManager {
  static instance = null;
  
  static getInstance() {
    if (!this.instance) {
      this.instance = new StateManager();
    }
    return this.instance;
  }

  constructor() {
    this.state = {
      enhancement: {
        lastRun: null,
        currentPlan: null,
        status: 'inactive',
        // Add more state properties
      }
    };
  }

  updateState(newState) {
    // Merge new state with existing
    this.state = { ...this.state, ...newState };
    this._persistState();
    return this.state;
  }

  _persistState() {
    // In a real system, this would persist state to storage
    // For demonstration, we'll just log it
    console.log('State updated:', this.state);
  }

  getState() {
    return this.state;
  }
}
