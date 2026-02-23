const metrics = {
  performance: ['response_time', 'throughput', 'error_rate', 'resource_utilization'],
  security: ['vulnerability_count', 'penetration_test', 'compliance', 'incident_response'],
  efficiency: ['process_cycle_time', 'automation_coverage', 'manual_effort', 'cost_per_unit'],
};

// Review intervals in milliseconds
const intervals = {
  monthly: 30 * 24 * 60 * 60 * 1000,
  quarterly: 90 * 24 * 60 * 60 * 1000,
  biAnnual: 180 * 24 * 60 * 60 * 1000,
};

export { metrics, intervals };