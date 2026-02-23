import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load configuration
const config = require('./config/enhancement-config');

export class ConfigurationLoader {
  static loadConfig() {
    return config;
  }
}
