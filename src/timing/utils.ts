import { TimingManager } from './timing';

export async function timeFunction<T>(name: string, fn: () => Promise<T>): Promise<T> {
  return TimingManager.instance.runAsync(name, fn);
}

export function time<T>(fn: () => Promise<T>): Promise<T> {
  return timeFunction(fn.name, fn);
}