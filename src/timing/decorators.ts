import { TimingManager, TimingContext } from './timing';

export class TimingDecorator {
  static async timeOperation(name: string, target: any, propertyKey: string, descriptor: PropertyDescriptor): Promise<void> {
    const original = descriptor.value;

    descriptor.value = async function (...args: any[]): Promise<any> {
      const context = TimingManager.instance.createContext(name || propertyKey);
      try {
        return await context.runAsync(() => original.apply(this, args));
      } catch (error) {
        throw error;
      }
    };
  }

  static async timeClass(target: Function): Promise<void> {
    for (const key of Object.getOwnPropertyNames(target.prototype)) {
      if (typeof target.prototype[key] === 'function' && key !== 'constructor') {
        TimingDecorator.timeOperation(key, target, key, Object.getOwnPropertyDescriptor(target.prototype, key)!);
      }
    }
  }
}