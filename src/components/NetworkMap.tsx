import React, { useState, useEffect, useCallback } from 'react';
import { createRoot } from 'react-dom/client';
import styled, { createTheme, ThemeProvider } from 'styled-components';
import { BsFillInfoCircleFill } from 'react-icons/bs';

// Types
interface Host {
  id: string;
  ip: string;
  hostname: string;
  online: boolean;
  ports: Record<string, { status: 'open' | 'closed' | 'filtered' }>[];
  os: string;
}

interface NetworkMapProps {
  hosts: Host[];
}

// Theme
const theme = createTheme({
  colors: {
    primary: '#FF6B35',
    secondary: '#FFA84D',
    tertiary: '#4C4C4C',
    background: '#1E1E1E',
    card: '#2C2C2C',
    text: '#FFFFFF',
    border: '#3A3A3A',
    // Status colors
    online: '#28A745',
    offline: '#DC3545',
    pending: '#FFC107',
    portOpen: '#28A745',
    portClosed: '#DC3545',
    portFiltered: '#FFC107',
  },
  fonts: {
    primary: 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif',
  },
  radius: {
    sm: '4px',
    md: '8px',
    lg: '16px',
  },
});

// Host Card
const HostCard = styled.div`
  background: ${props => props.theme.colors.card};
  border: 2px solid ${props => props.theme.colors.border};
  border-radius: ${props => props.theme.radius.md};
  padding: 16px;
  margin-bottom: 16px;
  transition: transform 0.2s ease-in-out;

  &:hover {
    transform: translateY(-2px);
    border-color: ${props => props.theme.colors.primary};
  }
`;

// NetworkMap
const NetworkMap = ({ hosts }: NetworkMapProps) => {
  const [selectedHost, setSelectedHost] = useState<Host | null>(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const toggleSidebar = useCallback(() => {
    setIsSidebarOpen(prev => !prev);
  }, []);

  const closeSidebar = useCallback(() => {
    setIsSidebarOpen(false);
  }, []);

  const handleHostClick = useCallback((host: Host) => {
    setSelectedHost(host);
    toggleSidebar();
  }, [toggleSidebar]);

  return (
    <div>
      <div style={{ display: 'flex' }}>
        {/* Main Network Map */}
        <div
          style={{
            flex: 1,
            minHeight: '100vh',
            padding: '24px',
            backgroundColor: props.theme.colors.background,
          }}
        >
          <h2 style={{ color: props.theme.colors.text, marginBottom: '24px' }}>Network Map</h2>

          {hosts.length === 0 ? (
            <div style={{ textAlign: 'center', color: props.theme.colors.text, padding: '40px 20px' }}>
              <BsFillInfoCircleFill style={{ fontSize: '48px', color: props.theme.colors.primary, marginBottom: '16px' }} />
              <h3>No hosts found</h3>
              <p>Scan your network to discover hosts.</p>
            </div>
          ) : (
            <div>
              {hosts.map(host => (
                <HostCard
                  key={host.id}
                  onClick={() => handleHostClick(host)}
                  style={{ cursor: 'pointer' }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <h4 style={{ color: props.theme.colors.text, margin: 0 }}>{host.hostname || host.ip}</h4>
                      <span
                        style={{
                          backgroundColor:
                            host.online
                              ? props.theme.colors.online
                              : props.theme.colors.offline,
                          color: props.theme.colors.text,
                          padding: '4px 8px',
                          borderRadius: props.theme.radius.sm,
                          fontSize: '12px',
                        }}
                      >
                        {host.online ? 'Online' : 'Offline'}
                      </span>
                    </div>
                    {host.online && (
                      <span
                        style={{
                          backgroundColor: props.theme.colors.tertiary,
                          color: props.theme.colors.text,
                          padding: '4px 8px',
                          borderRadius: props.theme.radius.sm,
                          fontSize: '12px',
                        }}
                      >
                        {hosts.length > 1 ? `(${host.index + 1})` : ''}
                      </span>
                    )}
                  </div>

                  <div style={{ marginTop: '12px', display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                    {host.ports.map(port => (
                      <span
                        key={port.id}
                        style={{
                          backgroundColor:
                            port.status === 'open'
                              ? props.theme.colors.portOpen
                              : port.status === 'closed'
                              ? props.theme.colors.portClosed
                              : props.theme.colors.portFiltered,
                          color: props.theme.colors.text,
                          padding: '4px 8px',
                          borderRadius: props.theme.radius.sm,
                          fontSize: '12px',
                        }}
                      >
                        Port {port.number}: {port.status}
                      </span>
                    ))}
                  </div>
                </HostCard>
              ))}
            </div>
          )}
        </div>

        {/* Sidebar for Host Details */}
        {isSidebarOpen && selectedHost && (
          <div
            style={{
              width: '350px',
              backgroundColor: props.theme.colors.card,
              borderLeft: `2px solid ${props.theme.colors.border}`,
              padding: '24px',
              transition: 'transform 0.3s ease-in-out',
            }}
          >
            <button
              onClick={closeSidebar}
              style={{
                position: 'absolute',
                top: '24px',
                right: '24px',
                backgroundColor: props.theme.colors.background,
                color: props.theme.colors.text,
                border: `1px solid ${props.theme.colors.border}`,
                padding: '8px 16px',
                borderRadius: props.theme.radius.md,
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                '&:hover': {
                  backgroundColor: props.theme.colors.tieriary,
                  borderColor: props.theme.colors.primary,
                },
              }}
            >
              Close
            </button>

            <h3 style={{ color: props.theme.colors.text, marginBottom: '16px' }}>{selectedHost.hostname || selectedHost.ip}</h3>

            <div style={{ marginBottom: '24px' }}>
              <h4 style={{ color: props.theme.colors.text, marginBottom: '8px' }}>Overview</h4>
              <p style={{ color: props.theme.colors.text, lineHeight: '1.6' }}>{selectedHost.description}</p>
            </div>

            <div style={{ marginBottom: '24px' }}>
              <h4 style={{ color: props.theme.colors.text, marginBottom: '8px' }}>OS Information</h4>
              <p style={{ color: props.theme.colors.text, marginBottom: '4px' }}>
                <strong>OS:</strong> {selectedHost.os}
              </p>
              <p style={{ color: props.theme.colors.text, marginBottom: '4px' }}>
                <strong>Uptime:</strong> {selectedHost.uptime}
              </p>
              <p style={{ color: props.theme.colors.text }}>
                <strong>Kernel Version:</strong> {selectedHost.kernelVersion}
              </p>
            </div>

            <div>
              <h4 style={{ color: props.theme.colors.text, marginBottom: '8px' }}>Available Actions</h4>
              <button
                style={{
                  width: '100%',
                  backgroundColor: props.theme.colors.primary,
                  color: props.theme.colors.text,
                  border: 'none',
                  padding: '12px 16px',
                  borderRadius: props.theme.radius.md,
                  marginBottom: '12px',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    backgroundColor: props.theme.colors.secondary,
                  },
                }}
              >
                Run Port Scan
              </button>
              <button
                style={{
                  width: '100%',
                  backgroundColor: props.theme.colors.primary,
                  color: props.theme.colors.text,
                  border: 'none',
                  padding: '12px 16px',
                  borderRadius: props.theme.radius.md,
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    backgroundColor: props.theme.colors.secondary,
                  },
                }}
              >
                OS Fingerprinting
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default NetworkMap;
`, 