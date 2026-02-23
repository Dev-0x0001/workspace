const { describe, it, expect } = require('mocha');
const { add } = require('../src/math');

describe('Addition tests', () => {
  it('should add two numbers', () => {
    expect(add(2, 3)).to.equal(5);
  });

  it('should handle negative numbers', () => {
    expect(add(-2, 3)).to.equal(1);
    expect(add(2, -3)).to.equal(-1);
  });

  it('should return zero when adding zero', () => {
    expect(add(0, 5)).to.equal(5);
    expect(add(5, 0)).to.equal(5);
    expect(add(0, 0)).to.equal(0);
  });
}