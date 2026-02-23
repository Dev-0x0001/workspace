const auditConfig = {
  scanFrequency: 'weekly',
  pentestFrequency: 'quarterly',
  reportRetention: 365,
  severityThreshold: 5,
  // 1=Low, 5=Critical
  auditScope: ['app', 'api', 'database'],
};