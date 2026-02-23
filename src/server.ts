import { createServer } from 'http';
import express from 'express';
import cors from 'cors';
import morgan from 'morgan';
import { json as jsonParser } from 'body-parser';
import { createAdapterFactory } from '@hapi/adapter';

const app = express();
const server = createServer(app);

// Configure CORS
app.use(cors({
  origin: '*', // In production, should restrict this
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true
}));

// Logging middleware
app.use(morgan('combined', {
  skip: function (req, res) {
    return res.statusCode < 400;
  }
}));

// JSON parsing
app.use(jsonParser({
  limit: '50mb' // Adjust based on expected payload size
}));

// Router setup
const router = express.Router();
app.use('/api', router);

// Health check
router.get('/health', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    timestamp: new Date().toISOString()
  });
});

// Metrics endpoint
router.get('/metrics', (req, res) => {
  res.status(200).json({
    metrics: MetricStore.getInstance().getMetrics(),
    timestamp: new Date().toISOString()
  });
});

// Logs endpoint
router.get('/logs', (req, res) => {
  // Implementation for log retrieval
  res.status(501).json({
    error: 'Not implemented'
  });
});

// Enhancement status
router.get('/enhancement/status', (req, res) => {
  res.status(200).json({
    status: 'active',
    lastRun: EnhancementManager.getInstance().getLastEnhancementResults(),
    timestamp: new Date().toISOString()
  });
});

// Start server
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
