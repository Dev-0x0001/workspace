import { EnhancementEvents } from './events/enhancement-events';
import { EnhancementManager } from './enhancement-manager';
import { ContinuousEnhancement } from './continuous-enhancement';
import { StateManager } from './state-manager';
import { MetricStore } from './metric-store';
import { LogHandler } from './logging/log-handler';
import { EnhancementAnalytics } from './analytics/enhancement-analytics';
import { PerformanceTracker } from './performance-tracker';

// Initialize core services
export const enhancementManager = new EnhancementManager();
export const continuousEnhancement = new ContinuousEnhancement();
export const stateManager = new StateManager();
export const metricStore = new MetricStore();
export const logHandler = new LogHandler();
export const enhancementAnalytics = new EnhancementAnalytics();
export const performanceTracker = new PerformanceTracker();
export const enhancementEvents = new EnhancementEvents();
