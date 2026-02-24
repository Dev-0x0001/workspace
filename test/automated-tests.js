// Automated Tests

const chai = require('chai');
const expect = chai.expect;

describe('Test Suite', function() {
    it('should pass basic test', function() {
        expect(true).to.be.true;
    });

    it('should calculate correctly', function() {
        expect(2 + 2).to.equal(4);
    });
};