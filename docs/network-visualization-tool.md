## Network Visualization Tool

A comprehensive network visualization and management solution.

### Features

#### Core Features
- [x] Local network scanning
- [x] Host discovery
- [x] Interactive visualization

#### Host Management
- [x] Port scanning
- [x] OS fingerprinting
- [x] Status monitoring

#### Visualization
- [x] Topology mapping
- [x] Color-coded status indicators
- [x] Zoom and pan support

### Usage

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build production
npm run build
```

### API Reference

#### Host Object
```ts
interface Host {
  id: string;
  ip: string;
  mac: string;
  name: string;
  status: 'online' | 'offline' | 'unknown';
  ports: Port[];
}

interface Port {
  number: number;
  protocol: 'tcp' | 'udp';
  state: 'open' | 'closed' | 'filtered';
}
```

### Development

Run the development server at `http://localhost:3000`

### License
MIT License