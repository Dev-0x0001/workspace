import { EnhancementManager } from './src/enhancement-manager';
import config from './config/enhancement-config';

// Initialize the enhancement manager
const enhancementManager = new EnhancementManager(config);

// Start the enhancement system
enhancementManager.start();

export { enhancementManager };