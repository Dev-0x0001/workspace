const validateInput = (data) => {
  if (!data || typeof data !== 'object') {
    throw new Error('Invalid input - expected an object');
  }

  // Check for required fields
  const requiredFields = ['id', 'name'];
  for (const field of requiredFields) {
    if (!(field in data)) {
      throw new Error(`Missing required field: ${field}`);
    }
  }

  // Validate field types
  if (typeof data.id !== 'string') {
    throw new Error('ID must be a string');
  }

  if (typeof data.name !== 'string') {
    throw new Error('Name must be a string');
  }

  // Validate ID format (UUID or alphanumeric)
  const idPattern = /^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$|^[a-zA-Z0-9]+$;
  if (!idPattern.test(data.id)) {
    throw new Error('ID has invalid format');
  }

  // Validate name length
  if (data.name.length < 2 || data.name.length > 100) {
    throw new Error('Name must be between 2 and 100 characters');
  }

  return true;
};

export const processCoreLogic = async (data) => {
  try {
    validateInput(data);

    // Additional processing validation
    if (!data.processedAt) {
      throw new Error('Processed date is required');
    }

    // Core processing logic
    const result = {
      ...data,
      processed: true,
      timestamp: new Date().toISOString(),
    };

    return result;
  } catch (error) {
    console.error(`Processing failed: ${error.message}`);
    throw error;
  }
};