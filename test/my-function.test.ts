import { myFunction } from '../src/index';

describe('myFunction', () => {
  it('should return correct result', () => {
    expect(myFunction(2, 3)).toBe(5);
  });
});