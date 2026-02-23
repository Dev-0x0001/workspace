export class TimingContext {
  private startTime: number;
  private duration: number = 0;
  private isActive: boolean = false;

  constructor(private name: string, private parent: TimingContext | null = null) {
    this.startTime = performance.now();
    this.isActive = true;
  }

  public async runAsync<T>(fn: () => Promise<T>): Promise<T> {
    if (!this.isActive) {
      throw new Error(`Timing context '${this.name}' is not active`);
    }

    try {
      const result = await fn();
      this.duration = performance.now() - this.startTime;
      return result;
    } catch (error) {
      this.duration = performance.now() - this.startTime;
      throw error;
    }
  }

  public getDuration(): number {
    if (this.isActive) {
      this.duration = performance.now() - this.startTime;
      this.isActive = false;
    }
    return this.duration;
  }
}

export class TimingManager {
  private contexts: Map<string, TimingContext> = new Map();
  private results: Map<string, { duration: number, timestamp: Date }> = new Map();

  public static instance: TimingManager;

  public constructor() {
    if (TimingManager.instance) {
      return TimingManager.instance;
    }
    TimingManager.instance = this;
  }

  public createContext(name: string, parent: TimingContext | null = null): TimingContext {
    const context = new TimingContext(name, parent);
    this.contexts.set(name, context);
    return context;
  }

  public async runAsync<T>(name: string, fn: () => Promise<T>): Promise<T> {
    const context = this.createContext(name);
    try {
      const result = await context.runAsync(fn);
      this.recordResult(name, context.getDuration());
      return result;
    } catch (error) {
      this.recordResult(name, context.getDuration(), true);
      throw error;
    }
  }

  private recordResult(name: string, duration: number, isError: boolean = false): void {
    this.results.set(name, {
      duration,
      timestamp: new Date(),
      isError,
    });
  }

  public getResults(): Map<string, { duration: number, timestamp: Date, isError: boolean }> {
    return new Map(this.results);
  }

  public getAverageDuration(name: string): number {
    const results = this.results.get(name);
    if (!results) {
      return 0;
    }
    return results.duration;
  }
}

// Usage example
export async function exampleUsage() {
  return TimingManager.instance.runAsync('example-task', async () => {
    // Simulate work
    await new Promise(resolve => setTimeout(resolve, 50));
    return 'completed';
  });
}

// Hook for periodic reporting
setInterval(() => {
  const results = TimingManager.instance.getResults();
  if (results.size > 0) {
    console.log('Timing results:', Object.fromEntries(results));
  }
}, 60000);