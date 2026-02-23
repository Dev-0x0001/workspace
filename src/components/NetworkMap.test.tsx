export default function NetworkMapTests() {
  // Test 1: Basic rendering
  it('renders the network map', () => {
    render(<NetworkMap />);
    expect(screen.getByTestId('network-map')).toBeInTheDocument();
  });

  // Test 2: Host discovery
  it('displays discovered hosts', async () => {
    const mockHosts = [{ip: '192.168.1.1', name: 'Router'}];
    render(<NetworkMap hosts={mockHosts} />);
    expect(screen.getByText('192.168.1.1')).toBeInTheDocument();
  });

  // Test 3: Port scanning
  it('scans ports on host click', async () => {
    const mockScan = jest.fn();
    render(<NetworkMap onPortScan={mockScan} />);
    fireEvent.click(screen.getByText('Scan Ports'));
    expect(mockScan).toHaveBeenCalled();
  });
}
