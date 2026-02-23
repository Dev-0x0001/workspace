import { useState, useEffect } from 'react';
import { TimingManager } from '../timing';

export function useTiming(name: string): { duration: number, isLoading: boolean, error: Error | null } {
  const [duration, setDuration] = useState<number>(0);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);

  const run = async (fn: () => Promise<any>): Promise<any> => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await TimingManager.instance.runAsync(name, fn);
      setDuration(result.duration);
      return result;
    } catch (err) {
      setError(err as Error);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  return { duration, isLoading, error, run };
}