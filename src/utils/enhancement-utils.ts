'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Invalid attempt to construct private class field");
  }
}

function _defineProperty(obj, key, value) {
  if (key in obj) {
    Object.defineProperty(obj, key, {
      value: value,
      enumerable: true,
      configurable: true,
      writable: true
    });
  } else {
    obj[key] = value;
  }
  return obj;
}

// Utility functions for system enhancement
export var EnhancementUtils = /*#__PURE__*/function () {
  function EnhancementUtils() {
    _classCallCheck(this, EnhancementUtils);
    _defineProperty(this, "_metrics", {});
  }

  _createClass(EnhancementUtils, [
    {
      key: "trackMetric",
      value: function trackMetric(category, name, value, metadata = {}) {
        if (!this._metrics[category]) {
          this._metrics[category] = {};
        }
        if (!this._metrics[category][name]) {
          this._metrics[category][name] = [];
        }
        this._metrics[category][name].push({
          value: value,
          metadata: metadata,
          timestamp: new Date().toISOString()
        });
        return this;
      }
    },
    {
      key: "getMetrics",
      value: function getMetrics(category = null, name = null) {
        if (category && name) {
          return this._metrics[category]?.[name] || [];
        } else if (category) {
          return this._metrics[category] || {};
        }
        return this._metrics;
      }
    },
    {
      key: "logState",
      value: function logState(state, level = 'info') {
        const timestamp = new Date().toISOString();
        console[level](`Enhancement System State - ${timestamp}`);
        console[level](JSON.stringify(state, null, 2));
        return this;
      }
    }
  ]);

  return EnhancementUtils;
}();
