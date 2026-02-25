describe('core module tests', () => {
  describe('input validation', () => {
    it('should throw error for invalid input type', () => {
      expect(() => validateInput('not an object')).toThrow(Error);
    });

    it('should throw error for missing required field', () => {
      expect(() => validateInput({ id: '123' })).toThrow(/Missing required field/);
    });

    it('should throw error for incomplete object', () => {
      expect(() => validateInput({})).toThrow(/Missing required field/);
    });

    it('should throw error for invalid ID format', () => {
      expect(() => validateInput({ id: 'invalid-id', name: 'test' })).toThrow(/ID has invalid format/);
    });

    it('should throw error for numeric ID', () => {
      expect(() => validateInput({ id: 123, name: 'test' })).toThrow(/ID must be a string/);
    });

    it('should throw error for short name', () => {
      expect(() => validateInput({ id: '123', name: 'a' })).toThrow(/Name must be between/);
    });

    it('should throw error for long name', () => {
      expect(() => validateInput({ id: '123', name: 'a'.repeat(101) })).toThrow(/Name must be between/);
    });

    it('should pass validation with valid input', () => {
      expect(() => validateInput({
        id: 'abc-123',
        name: 'valid item',
      })).not.toThrow();
    });
  });

  describe('processing logic', () => {
    it('should process data successfully', () => {
      const input = {
        id: '123',
        name: 'test item',
        processedAt: new Date().toISOString(),
      };

      return processCoreLogic(input).then(result => {
        expect(result.processed).toBe(true);
        expect(result.timestamp).toBeDefined();
      });
    });

    it('should throw error when processedAt is missing', () => {
      expect(() => processCoreLogic({
        id: '123',
        name: 'test item',
      })).toThrow(/Processed date is required/);
    });
  });
});