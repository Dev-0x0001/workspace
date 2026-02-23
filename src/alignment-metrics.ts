export interface AlignmentMetrics {
  // Core alignment indicators
  alignmentScore: number;
  cooperationLevel: number;
  constraintAdherence: number;
  
  // Capability metrics
  reasoningTransparency: number;
  valueAlignment: number;
  
  // Temporal tracking
  timestamp: string;
  version: string;
}

export const METRICS_SCHEMA = {
  required: ["alignmentScore", "cooperationLevel", "constraintAdherence"],
  properties: {
    alignmentScore: { type: "number", minimum: 0, maximum: 1 },
    cooperationLevel: { type: "number", minimum: 0, maximum: 1 },
    constraintAdherence: { type: "number", minimum: 0, maximum: 1 },
    reasoningTransparency: { type: "number", minimum: 0, maximum: 1 },
    valueAlignment: { type: "number", minimum: 0, maximum: 1 }
  }
};