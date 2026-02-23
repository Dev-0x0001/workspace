export default class LogHandler {
  static levels = {
    'error': 0,
    'warn': 1,
    'info': 2,
    'debug': 3,
    'trace': 4
  };

  constructor(options = {}) {
    this.options = {
      level: 'info',
      ...options
    };
    this.transports = [];
    this._setupDefaultTransports();
  }

  _setupDefaultTransports() {
    // Console transport
    this.transports.push({
      type: 'console',
      level: this.options.level,
      formatter: this._formatLog.bind(this)
    });

    // File transport (development only)
    if (process.env.NODE_ENV !== 'production') {
      this.transports.push({
        type: 'file',
        level: 'debug',
        filename: 'logs/enhancement.log',
        formatter: this._formatFileLog.bind(this)
      });
    }
  }

  _formatLog(level, message, meta) {
    return `${new Date().toISOString()} [${level.toUpperCase()}] ${message}`;
  }

  _formatFileLog(level, message, meta) {
    return JSON.stringify({
      timestamp: new Date().toISOString(),
      level, 
      message, 
      meta: { ...meta, pid: process.pid },
    });
  }

  log(level, message, meta = {}) {
    const logLevel = LogHandler.levels[level];
    const effectiveLevel = LogHandler.levels[this.options.level];

    if (logLevel >= effectiveLevel) {
      this.transports.forEach(transport => {
        if (logLevel >= LogHandler.levels[transport.level]) {
          const formatted = this[transport.formatter].bind(this)(
            level, message, meta
          );
          console.log(formatted); // This would be replaced with actual transport
        }
      });
    }
  }

  // Convenience methods
  error(message, meta = {}) {
    this.log('error', message, meta);
  }

  warn(message, meta = {}) {
    this.log('warn', message, meta);
  }

  info(message, meta = {}) {
    this.log('info', message, meta);
  }

  debug(message, meta = {}) {
    this.log('debug', message, meta);
  }

  trace(message, meta = {}) {
    this.log('trace', message, meta);
  }
}
