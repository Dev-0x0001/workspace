const { render, screen, fireEvent } = require('@testing-library/react');
const MyComponent = require('../../../src/components/MyComponent').default;

describe('MyComponent Integration', () => {
  it('should handle form submission and update state', async () => {
    render(<MyComponent />);
    // Arrange
    const email = 'test@example.com';
    const password = 'password123';
    
    // Act
    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: email } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: password } });
    fireEvent.click(screen.getByText(/submit/i));
    
    // Assert
    expect(screen.getByText(/welcome, test/i)).toBeInTheDocument();
  });
});