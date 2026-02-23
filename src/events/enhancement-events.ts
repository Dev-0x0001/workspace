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

export var EnhancementEvents = /*#__PURE__*/function () {
  function EnhancementEvents() {
    _classCallCheck(this, EnhancementEvents);
    _defineProperty(this, "_listeners", {});
  }

  _createClass(EnhancementEvents, [
    {
      key: "on",
      value: function on(event, callback) {
        if (!this._listeners[event]) {
          this._listeners[event] = [];
        }
        this._listeners[event].push(callback);
        return this;
      }
    },
    {
      key: "emit",
      value: function emit(event, data) {
        if (this._listeners[event]) {
          this._listeners[event].forEach(function (callback) {
            callback(data);
          });
        }
        return this;
      }
    },
    {
      key: "off",
      value: function off(event, callback) {
        if (this._listeners[event]) {
          this._listeners[event] = this._listeners[event].filter(function (cb) {
            return cb !== callback;
          });
        }
        return this;
      }
    }
  ]);

  return EnhancementEvents;
}();
