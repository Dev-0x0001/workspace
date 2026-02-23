import { TimingManager } from '../timing';

export class PerformanceTracker {
  static async track<T>(name: string, fn: () => Promise<T>): Promise<T> {
    return TimingManager.instance.runAsync(name, fn);
  }
}

export function track<T>(fn: () => Promise<T>): Promise<T> {
  return PerformanceTracker.track(fn.name, fn);
}