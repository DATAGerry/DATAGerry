/*!
  * CMDB Frontend v1.0.0 (https://github.com/NETHINKS/netcmdb_frontend#readme)
  * @Copyright 2018 undefined
  * @Licensed under MIT (https://github.com/NETHINKS/netcmdb_frontend#readme)
  */
(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? factory(require('jquery')) :
  typeof define === 'function' && define.amd ? define(['jquery'], factory) :
  (factory(global.jQuery));
}(this, (function ($) { 'use strict';

  $ = $ && $.hasOwnProperty('default') ? $['default'] : $;

  /*
   * Error error_code
   * based on https://codepen.io/Ahmed_B_Hameed/pen/LkqNmp
   */
  (function ($$$1, global, undefined) {

    $$$1.error_code = {
      defaults: {
        thirdDigit: 4,
        secondDigit: 0,
        firstDigit: 4
      }
    };

    $$$1.fn.error_code = function (opt) {
      var code = $$$1.extend({}, $$$1.error_code.defaults, opt);
      var error_target = this;

      this.randomNum = function () {

        return Math.floor(Math.random() * 9) + 1;
      };

      var loop1,
          loop2,
          loop3,
          time = 30,
          i = 0;
      var selector3 = $$$1('.thirdDigit', this);
      var selector2 = $$$1('.secondDigit', this);
      var selector1 = $$$1('.firstDigit', this);
      this.loop3 = setInterval(function () {

        if (i > 40) {
          clearInterval(loop3);
          selector3.text(code.thirdDigit);
        } else {
          selector3.text(error_target.randomNum());
          i++;
        }
      }, time);
      this.loop2 = setInterval(function () {

        if (i > 80) {
          clearInterval(loop2);
          selector2.text(code.secondDigit);
        } else {
          selector2.text(error_target.randomNum());
          i++;
        }
      }, time);
      this.loop1 = setInterval(function () {

        if (i > 100) {
          clearInterval(loop1);
          selector1.text(code.firstDigit);
        } else {
          selector1.text(error_target.randomNum());
          i++;
        }
      }, time);
    };

    if (global.module && global.module.exports) {
      module.exports = $$$1.fn.error_code;
    }
  })(jQuery, window || global);

  (function () {
    var AjaxMonitor,
        Bar,
        DocumentMonitor,
        ElementMonitor,
        ElementTracker,
        EventLagMonitor,
        Evented,
        Events,
        NoTargetError,
        Pace,
        RequestIntercept,
        SOURCE_KEYS,
        Scaler,
        SocketRequestTracker,
        XHRRequestTracker,
        animation,
        avgAmplitude,
        bar,
        cancelAnimation,
        cancelAnimationFrame,
        defaultOptions,
        _extend,
        extendNative,
        getFromDOM,
        getIntercept,
        handlePushState,
        ignoreStack,
        init,
        now,
        options,
        requestAnimationFrame,
        result,
        runAnimation,
        scalers,
        shouldIgnoreURL,
        shouldTrack,
        source,
        sources,
        uniScaler,
        _WebSocket,
        _XDomainRequest,
        _XMLHttpRequest,
        _i,
        _intercept,
        _len,
        _pushState,
        _ref,
        _ref1,
        _replaceState,
        __slice = [].slice,
        __hasProp = {}.hasOwnProperty,
        __extends = function __extends(child, parent) {
      for (var key in parent) {
        if (__hasProp.call(parent, key)) child[key] = parent[key];
      }

      function ctor() {
        this.constructor = child;
      }

      ctor.prototype = parent.prototype;
      child.prototype = new ctor();
      child.__super__ = parent.prototype;
      return child;
    },
        __indexOf = [].indexOf || function (item) {
      for (var i = 0, l = this.length; i < l; i++) {
        if (i in this && this[i] === item) return i;
      }

      return -1;
    };

    defaultOptions = {
      catchupTime: 100,
      initialRate: .03,
      minTime: 250,
      ghostTime: 100,
      maxProgressPerFrame: 20,
      easeFactor: 1.25,
      startOnPageLoad: true,
      restartOnPushState: true,
      restartOnRequestAfter: 500,
      target: 'body',
      elements: {
        checkInterval: 100,
        selectors: ['body']
      },
      eventLag: {
        minSamples: 10,
        sampleCount: 3,
        lagThreshold: 3
      },
      ajax: {
        trackMethods: ['GET'],
        trackWebSockets: true,
        ignoreURLs: []
      }
    };

    now = function now() {
      var _ref;

      return (_ref = typeof performance !== "undefined" && performance !== null ? typeof performance.now === "function" ? performance.now() : void 0 : void 0) != null ? _ref : +new Date();
    };

    requestAnimationFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame || window.webkitRequestAnimationFrame || window.msRequestAnimationFrame;
    cancelAnimationFrame = window.cancelAnimationFrame || window.mozCancelAnimationFrame;

    if (requestAnimationFrame == null) {
      requestAnimationFrame = function requestAnimationFrame(fn) {
        return setTimeout(fn, 50);
      };

      cancelAnimationFrame = function cancelAnimationFrame(id) {
        return clearTimeout(id);
      };
    }

    runAnimation = function runAnimation(fn) {
      var last, _tick;

      last = now();

      _tick = function tick() {
        var diff;
        diff = now() - last;

        if (diff >= 33) {
          last = now();
          return fn(diff, function () {
            return requestAnimationFrame(_tick);
          });
        } else {
          return setTimeout(_tick, 33 - diff);
        }
      };

      return _tick();
    };

    result = function result() {
      var args, key, obj;
      obj = arguments[0], key = arguments[1], args = 3 <= arguments.length ? __slice.call(arguments, 2) : [];

      if (typeof obj[key] === 'function') {
        return obj[key].apply(obj, args);
      } else {
        return obj[key];
      }
    };

    _extend = function extend() {
      var key, out, source, sources, val, _i, _len;

      out = arguments[0], sources = 2 <= arguments.length ? __slice.call(arguments, 1) : [];

      for (_i = 0, _len = sources.length; _i < _len; _i++) {
        source = sources[_i];

        if (source) {
          for (key in source) {
            if (!__hasProp.call(source, key)) continue;
            val = source[key];

            if (out[key] != null && typeof out[key] === 'object' && val != null && typeof val === 'object') {
              _extend(out[key], val);
            } else {
              out[key] = val;
            }
          }
        }
      }

      return out;
    };

    avgAmplitude = function avgAmplitude(arr) {
      var count, sum, v, _i, _len;

      sum = count = 0;

      for (_i = 0, _len = arr.length; _i < _len; _i++) {
        v = arr[_i];
        sum += Math.abs(v);
        count++;
      }

      return sum / count;
    };

    getFromDOM = function getFromDOM(key, json) {
      var data, e, el;

      if (key == null) {
        key = 'options';
      }

      if (json == null) {
        json = true;
      }

      el = document.querySelector("[data-pace-" + key + "]");

      if (!el) {
        return;
      }

      data = el.getAttribute("data-pace-" + key);

      if (!json) {
        return data;
      }

      try {
        return JSON.parse(data);
      } catch (_error) {
        e = _error;
        return typeof console !== "undefined" && console !== null ? console.error("Error parsing inline pace options", e) : void 0;
      }
    };

    Evented = function () {
      function Evented() {}

      Evented.prototype.on = function (event, handler, ctx, once) {
        var _base;

        if (once == null) {
          once = false;
        }

        if (this.bindings == null) {
          this.bindings = {};
        }

        if ((_base = this.bindings)[event] == null) {
          _base[event] = [];
        }

        return this.bindings[event].push({
          handler: handler,
          ctx: ctx,
          once: once
        });
      };

      Evented.prototype.once = function (event, handler, ctx) {
        return this.on(event, handler, ctx, true);
      };

      Evented.prototype.off = function (event, handler) {
        var i, _ref, _results;

        if (((_ref = this.bindings) != null ? _ref[event] : void 0) == null) {
          return;
        }

        if (handler == null) {
          return delete this.bindings[event];
        } else {
          i = 0;
          _results = [];

          while (i < this.bindings[event].length) {
            if (this.bindings[event][i].handler === handler) {
              _results.push(this.bindings[event].splice(i, 1));
            } else {
              _results.push(i++);
            }
          }

          return _results;
        }
      };

      Evented.prototype.trigger = function () {
        var args, ctx, event, handler, i, once, _ref, _ref1, _results;

        event = arguments[0], args = 2 <= arguments.length ? __slice.call(arguments, 1) : [];

        if ((_ref = this.bindings) != null ? _ref[event] : void 0) {
          i = 0;
          _results = [];

          while (i < this.bindings[event].length) {
            _ref1 = this.bindings[event][i], handler = _ref1.handler, ctx = _ref1.ctx, once = _ref1.once;
            handler.apply(ctx != null ? ctx : this, args);

            if (once) {
              _results.push(this.bindings[event].splice(i, 1));
            } else {
              _results.push(i++);
            }
          }

          return _results;
        }
      };

      return Evented;
    }();

    Pace = window.Pace || {};
    window.Pace = Pace;

    _extend(Pace, Evented.prototype);

    options = Pace.options = _extend({}, defaultOptions, window.paceOptions, getFromDOM());
    _ref = ['ajax', 'document', 'eventLag', 'elements'];

    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      source = _ref[_i];

      if (options[source] === true) {
        options[source] = defaultOptions[source];
      }
    }

    NoTargetError = function (_super) {
      __extends(NoTargetError, _super);

      function NoTargetError() {
        _ref1 = NoTargetError.__super__.constructor.apply(this, arguments);
        return _ref1;
      }

      return NoTargetError;
    }(Error);

    Bar = function () {
      function Bar() {
        this.progress = 0;
      }

      Bar.prototype.getElement = function () {
        var targetElement;

        if (this.el == null) {
          targetElement = document.querySelector(options.target);

          if (!targetElement) {
            throw new NoTargetError();
          }

          this.el = document.createElement('div');
          this.el.className = "pace pace-active";
          document.body.className = document.body.className.replace(/pace-done/g, '');
          document.body.className += ' pace-running';
          this.el.innerHTML = '<div class="pace-progress">\n  <div class="pace-progress-inner"></div>\n</div>\n<div class="pace-activity"></div>';

          if (targetElement.firstChild != null) {
            targetElement.insertBefore(this.el, targetElement.firstChild);
          } else {
            targetElement.appendChild(this.el);
          }
        }

        return this.el;
      };

      Bar.prototype.finish = function () {
        var el;
        el = this.getElement();
        el.className = el.className.replace('pace-active', '');
        el.className += ' pace-inactive';
        document.body.className = document.body.className.replace('pace-running', '');
        return document.body.className += ' pace-done';
      };

      Bar.prototype.update = function (prog) {
        this.progress = prog;
        return this.render();
      };

      Bar.prototype.destroy = function () {
        try {
          this.getElement().parentNode.removeChild(this.getElement());
        } catch (_error) {
          NoTargetError = _error;
        }

        return this.el = void 0;
      };

      Bar.prototype.render = function () {
        var el, key, progressStr, transform, _j, _len1, _ref2;

        if (document.querySelector(options.target) == null) {
          return false;
        }

        el = this.getElement();
        transform = "translate3d(" + this.progress + "%, 0, 0)";
        _ref2 = ['webkitTransform', 'msTransform', 'transform'];

        for (_j = 0, _len1 = _ref2.length; _j < _len1; _j++) {
          key = _ref2[_j];
          el.children[0].style[key] = transform;
        }

        if (!this.lastRenderedProgress || this.lastRenderedProgress | 0 !== this.progress | 0) {
          el.children[0].setAttribute('data-progress-text', "" + (this.progress | 0) + "%");

          if (this.progress >= 100) {
            progressStr = '99';
          } else {
            progressStr = this.progress < 10 ? "0" : "";
            progressStr += this.progress | 0;
          }

          el.children[0].setAttribute('data-progress', "" + progressStr);
        }

        return this.lastRenderedProgress = this.progress;
      };

      Bar.prototype.done = function () {
        return this.progress >= 100;
      };

      return Bar;
    }();

    Events = function () {
      function Events() {
        this.bindings = {};
      }

      Events.prototype.trigger = function (name, val) {
        var binding, _j, _len1, _ref2, _results;

        if (this.bindings[name] != null) {
          _ref2 = this.bindings[name];
          _results = [];

          for (_j = 0, _len1 = _ref2.length; _j < _len1; _j++) {
            binding = _ref2[_j];

            _results.push(binding.call(this, val));
          }

          return _results;
        }
      };

      Events.prototype.on = function (name, fn) {
        var _base;

        if ((_base = this.bindings)[name] == null) {
          _base[name] = [];
        }

        return this.bindings[name].push(fn);
      };

      return Events;
    }();

    _XMLHttpRequest = window.XMLHttpRequest;
    _XDomainRequest = window.XDomainRequest;
    _WebSocket = window.WebSocket;

    extendNative = function extendNative(to, from) {
      var key, _results;

      _results = [];

      for (key in from.prototype) {
        try {
          if (to[key] == null && typeof from[key] !== 'function') {
            if (typeof Object.defineProperty === 'function') {
              _results.push(Object.defineProperty(to, key, {
                get: function get() {
                  return from.prototype[key];
                },
                configurable: true,
                enumerable: true
              }));
            } else {
              _results.push(to[key] = from.prototype[key]);
            }
          } else {
            _results.push(void 0);
          }
        } catch (_error) {
        }
      }

      return _results;
    };

    ignoreStack = [];

    Pace.ignore = function () {
      var args, fn, ret;
      fn = arguments[0], args = 2 <= arguments.length ? __slice.call(arguments, 1) : [];
      ignoreStack.unshift('ignore');
      ret = fn.apply(null, args);
      ignoreStack.shift();
      return ret;
    };

    Pace.track = function () {
      var args, fn, ret;
      fn = arguments[0], args = 2 <= arguments.length ? __slice.call(arguments, 1) : [];
      ignoreStack.unshift('track');
      ret = fn.apply(null, args);
      ignoreStack.shift();
      return ret;
    };

    shouldTrack = function shouldTrack(method) {
      var _ref2;

      if (method == null) {
        method = 'GET';
      }

      if (ignoreStack[0] === 'track') {
        return 'force';
      }

      if (!ignoreStack.length && options.ajax) {
        if (method === 'socket' && options.ajax.trackWebSockets) {
          return true;
        } else if (_ref2 = method.toUpperCase(), __indexOf.call(options.ajax.trackMethods, _ref2) >= 0) {
          return true;
        }
      }

      return false;
    };

    RequestIntercept = function (_super) {
      __extends(RequestIntercept, _super);

      function RequestIntercept() {
        var monitorXHR,
            _this = this;

        RequestIntercept.__super__.constructor.apply(this, arguments);

        monitorXHR = function monitorXHR(req) {
          var _open;

          _open = req.open;
          return req.open = function (type, url, async) {
            if (shouldTrack(type)) {
              _this.trigger('request', {
                type: type,
                url: url,
                request: req
              });
            }

            return _open.apply(req, arguments);
          };
        };

        window.XMLHttpRequest = function (flags) {
          var req;
          req = new _XMLHttpRequest(flags);
          monitorXHR(req);
          return req;
        };

        try {
          extendNative(window.XMLHttpRequest, _XMLHttpRequest);
        } catch (_error) {}

        if (_XDomainRequest != null) {
          window.XDomainRequest = function () {
            var req;
            req = new _XDomainRequest();
            monitorXHR(req);
            return req;
          };

          try {
            extendNative(window.XDomainRequest, _XDomainRequest);
          } catch (_error) {}
        }

        if (_WebSocket != null && options.ajax.trackWebSockets) {
          window.WebSocket = function (url, protocols) {
            var req;

            if (protocols != null) {
              req = new _WebSocket(url, protocols);
            } else {
              req = new _WebSocket(url);
            }

            if (shouldTrack('socket')) {
              _this.trigger('request', {
                type: 'socket',
                url: url,
                protocols: protocols,
                request: req
              });
            }

            return req;
          };

          try {
            extendNative(window.WebSocket, _WebSocket);
          } catch (_error) {}
        }
      }

      return RequestIntercept;
    }(Events);

    _intercept = null;

    getIntercept = function getIntercept() {
      if (_intercept == null) {
        _intercept = new RequestIntercept();
      }

      return _intercept;
    };

    shouldIgnoreURL = function shouldIgnoreURL(url) {
      var pattern, _j, _len1, _ref2;

      _ref2 = options.ajax.ignoreURLs;

      for (_j = 0, _len1 = _ref2.length; _j < _len1; _j++) {
        pattern = _ref2[_j];

        if (typeof pattern === 'string') {
          if (url.indexOf(pattern) !== -1) {
            return true;
          }
        } else {
          if (pattern.test(url)) {
            return true;
          }
        }
      }

      return false;
    };

    getIntercept().on('request', function (_arg) {
      var after, args, request, type, url;
      type = _arg.type, request = _arg.request, url = _arg.url;

      if (shouldIgnoreURL(url)) {
        return;
      }

      if (!Pace.running && (options.restartOnRequestAfter !== false || shouldTrack(type) === 'force')) {
        args = arguments;
        after = options.restartOnRequestAfter || 0;

        if (typeof after === 'boolean') {
          after = 0;
        }

        return setTimeout(function () {
          var stillActive, _j, _len1, _ref2, _ref3, _results;

          if (type === 'socket') {
            stillActive = request.readyState < 2;
          } else {
            stillActive = 0 < (_ref2 = request.readyState) && _ref2 < 4;
          }

          if (stillActive) {
            Pace.restart();
            _ref3 = Pace.sources;
            _results = [];

            for (_j = 0, _len1 = _ref3.length; _j < _len1; _j++) {
              source = _ref3[_j];

              if (source instanceof AjaxMonitor) {
                source.watch.apply(source, args);
                break;
              } else {
                _results.push(void 0);
              }
            }

            return _results;
          }
        }, after);
      }
    });

    AjaxMonitor = function () {
      function AjaxMonitor() {
        var _this = this;

        this.elements = [];
        getIntercept().on('request', function () {
          return _this.watch.apply(_this, arguments);
        });
      }

      AjaxMonitor.prototype.watch = function (_arg) {
        var request, tracker, type, url;
        type = _arg.type, request = _arg.request, url = _arg.url;

        if (shouldIgnoreURL(url)) {
          return;
        }

        if (type === 'socket') {
          tracker = new SocketRequestTracker(request);
        } else {
          tracker = new XHRRequestTracker(request);
        }

        return this.elements.push(tracker);
      };

      return AjaxMonitor;
    }();

    XHRRequestTracker = function () {
      function XHRRequestTracker(request) {
        var event,
            _j,
            _len1,
            _onreadystatechange,
            _ref2,
            _this = this;

        this.progress = 0;

        if (window.ProgressEvent != null) {
          request.addEventListener('progress', function (evt) {
            if (evt.lengthComputable) {
              return _this.progress = 100 * evt.loaded / evt.total;
            } else {
              return _this.progress = _this.progress + (100 - _this.progress) / 2;
            }
          }, false);
          _ref2 = ['load', 'abort', 'timeout', 'error'];

          for (_j = 0, _len1 = _ref2.length; _j < _len1; _j++) {
            event = _ref2[_j];
            request.addEventListener(event, function () {
              return _this.progress = 100;
            }, false);
          }
        } else {
          _onreadystatechange = request.onreadystatechange;

          request.onreadystatechange = function () {
            var _ref3;

            if ((_ref3 = request.readyState) === 0 || _ref3 === 4) {
              _this.progress = 100;
            } else if (request.readyState === 3) {
              _this.progress = 50;
            }

            return typeof _onreadystatechange === "function" ? _onreadystatechange.apply(null, arguments) : void 0;
          };
        }
      }

      return XHRRequestTracker;
    }();

    SocketRequestTracker = function () {
      function SocketRequestTracker(request) {
        var event,
            _j,
            _len1,
            _ref2,
            _this = this;

        this.progress = 0;
        _ref2 = ['error', 'open'];

        for (_j = 0, _len1 = _ref2.length; _j < _len1; _j++) {
          event = _ref2[_j];
          request.addEventListener(event, function () {
            return _this.progress = 100;
          }, false);
        }
      }

      return SocketRequestTracker;
    }();

    ElementMonitor = function () {
      function ElementMonitor(options) {
        var selector, _j, _len1, _ref2;

        if (options == null) {
          options = {};
        }

        this.elements = [];

        if (options.selectors == null) {
          options.selectors = [];
        }

        _ref2 = options.selectors;

        for (_j = 0, _len1 = _ref2.length; _j < _len1; _j++) {
          selector = _ref2[_j];
          this.elements.push(new ElementTracker(selector));
        }
      }

      return ElementMonitor;
    }();

    ElementTracker = function () {
      function ElementTracker(selector) {
        this.selector = selector;
        this.progress = 0;
        this.check();
      }

      ElementTracker.prototype.check = function () {
        var _this = this;

        if (document.querySelector(this.selector)) {
          return this.done();
        } else {
          return setTimeout(function () {
            return _this.check();
          }, options.elements.checkInterval);
        }
      };

      ElementTracker.prototype.done = function () {
        return this.progress = 100;
      };

      return ElementTracker;
    }();

    DocumentMonitor = function () {
      DocumentMonitor.prototype.states = {
        loading: 0,
        interactive: 50,
        complete: 100
      };

      function DocumentMonitor() {
        var _onreadystatechange,
            _ref2,
            _this = this;

        this.progress = (_ref2 = this.states[document.readyState]) != null ? _ref2 : 100;
        _onreadystatechange = document.onreadystatechange;

        document.onreadystatechange = function () {
          if (_this.states[document.readyState] != null) {
            _this.progress = _this.states[document.readyState];
          }

          return typeof _onreadystatechange === "function" ? _onreadystatechange.apply(null, arguments) : void 0;
        };
      }

      return DocumentMonitor;
    }();

    EventLagMonitor = function () {
      function EventLagMonitor() {
        var avg,
            interval,
            last,
            points,
            samples,
            _this = this;

        this.progress = 0;
        avg = 0;
        samples = [];
        points = 0;
        last = now();
        interval = setInterval(function () {
          var diff;
          diff = now() - last - 50;
          last = now();
          samples.push(diff);

          if (samples.length > options.eventLag.sampleCount) {
            samples.shift();
          }

          avg = avgAmplitude(samples);

          if (++points >= options.eventLag.minSamples && avg < options.eventLag.lagThreshold) {
            _this.progress = 100;
            return clearInterval(interval);
          } else {
            return _this.progress = 100 * (3 / (avg + 3));
          }
        }, 50);
      }

      return EventLagMonitor;
    }();

    Scaler = function () {
      function Scaler(source) {
        this.source = source;
        this.last = this.sinceLastUpdate = 0;
        this.rate = options.initialRate;
        this.catchup = 0;
        this.progress = this.lastProgress = 0;

        if (this.source != null) {
          this.progress = result(this.source, 'progress');
        }
      }

      Scaler.prototype.tick = function (frameTime, val) {
        var scaling;

        if (val == null) {
          val = result(this.source, 'progress');
        }

        if (val >= 100) {
          this.done = true;
        }

        if (val === this.last) {
          this.sinceLastUpdate += frameTime;
        } else {
          if (this.sinceLastUpdate) {
            this.rate = (val - this.last) / this.sinceLastUpdate;
          }

          this.catchup = (val - this.progress) / options.catchupTime;
          this.sinceLastUpdate = 0;
          this.last = val;
        }

        if (val > this.progress) {
          this.progress += this.catchup * frameTime;
        }

        scaling = 1 - Math.pow(this.progress / 100, options.easeFactor);
        this.progress += scaling * this.rate * frameTime;
        this.progress = Math.min(this.lastProgress + options.maxProgressPerFrame, this.progress);
        this.progress = Math.max(0, this.progress);
        this.progress = Math.min(100, this.progress);
        this.lastProgress = this.progress;
        return this.progress;
      };

      return Scaler;
    }();

    sources = null;
    scalers = null;
    bar = null;
    uniScaler = null;
    animation = null;
    cancelAnimation = null;
    Pace.running = false;

    handlePushState = function handlePushState() {
      if (options.restartOnPushState) {
        return Pace.restart();
      }
    };

    if (window.history.pushState != null) {
      _pushState = window.history.pushState;

      window.history.pushState = function () {
        handlePushState();
        return _pushState.apply(window.history, arguments);
      };
    }

    if (window.history.replaceState != null) {
      _replaceState = window.history.replaceState;

      window.history.replaceState = function () {
        handlePushState();
        return _replaceState.apply(window.history, arguments);
      };
    }

    SOURCE_KEYS = {
      ajax: AjaxMonitor,
      elements: ElementMonitor,
      document: DocumentMonitor,
      eventLag: EventLagMonitor
    };
    (init = function init() {
      var type, _j, _k, _len1, _len2, _ref2, _ref3, _ref4;

      Pace.sources = sources = [];
      _ref2 = ['ajax', 'elements', 'document', 'eventLag'];

      for (_j = 0, _len1 = _ref2.length; _j < _len1; _j++) {
        type = _ref2[_j];

        if (options[type] !== false) {
          sources.push(new SOURCE_KEYS[type](options[type]));
        }
      }

      _ref4 = (_ref3 = options.extraSources) != null ? _ref3 : [];

      for (_k = 0, _len2 = _ref4.length; _k < _len2; _k++) {
        source = _ref4[_k];
        sources.push(new source(options));
      }

      Pace.bar = bar = new Bar();
      scalers = [];
      return uniScaler = new Scaler();
    })();

    Pace.stop = function () {
      Pace.trigger('stop');
      Pace.running = false;
      bar.destroy();
      cancelAnimation = true;

      if (animation != null) {
        if (typeof cancelAnimationFrame === "function") {
          cancelAnimationFrame(animation);
        }

        animation = null;
      }

      return init();
    };

    Pace.restart = function () {
      Pace.trigger('restart');
      Pace.stop();
      return Pace.start();
    };

    Pace.go = function () {
      var start;
      Pace.running = true;
      bar.render();
      start = now();
      cancelAnimation = false;
      return animation = runAnimation(function (frameTime, enqueueNextFrame) {
        var avg, count, done, element, elements, i, j, remaining, scaler, scalerList, sum, _j, _k, _len1, _len2, _ref2;

        remaining = 100 - bar.progress;
        count = sum = 0;
        done = true;

        for (i = _j = 0, _len1 = sources.length; _j < _len1; i = ++_j) {
          source = sources[i];
          scalerList = scalers[i] != null ? scalers[i] : scalers[i] = [];
          elements = (_ref2 = source.elements) != null ? _ref2 : [source];

          for (j = _k = 0, _len2 = elements.length; _k < _len2; j = ++_k) {
            element = elements[j];
            scaler = scalerList[j] != null ? scalerList[j] : scalerList[j] = new Scaler(element);
            done &= scaler.done;

            if (scaler.done) {
              continue;
            }

            count++;
            sum += scaler.tick(frameTime);
          }
        }

        avg = sum / count;
        bar.update(uniScaler.tick(frameTime, avg));

        if (bar.done() || done || cancelAnimation) {
          bar.update(100);
          Pace.trigger('done');
          return setTimeout(function () {
            bar.finish();
            Pace.running = false;
            return Pace.trigger('hide');
          }, Math.max(options.ghostTime, Math.max(options.minTime - (now() - start), 0)));
        } else {
          return enqueueNextFrame();
        }
      });
    };

    Pace.start = function (_options) {
      _extend(options, _options);

      Pace.running = true;

      try {
        bar.render();
      } catch (_error) {
        NoTargetError = _error;
      }

      if (!document.querySelector('.pace')) {
        return setTimeout(Pace.start, 50);
      } else {
        Pace.trigger('start');
        return Pace.go();
      }
    };

    if (typeof define === 'function' && define.amd) {
      define(['pace'], function () {
        return Pace;
      });
    } else if (typeof exports === 'object') {
      module.exports = Pace;
    } else {
      if (options.startOnPageLoad) {
        Pace.start();
      }
    }
  })();

  /*! jQuery-QuickSearch - v2.4.0 - 2017-08-15
  * https://deuxhuithuit.github.io/quicksearch/
  * Copyright (c) 2013 Deux Huit Huit, Rik Lomas.
  * Copyright (c) 2017 Deux Huit Huit (https://deuxhuithuit.com/);
  * License MIT http://deuxhuithuit.mit-license.org */
  (function ($$$1, global, undefined) {

    $$$1.quicksearch = {
      defaults: {
        delay: 100,
        selector: null,
        stripeRows: null,
        loader: null,
        caseSensitive: false,
        noResults: '',
        matchedResultsCount: 0,
        keyCode: false,
        bind: 'keyup search input',
        resetBind: 'reset',
        removeDiacritics: false,
        minValLength: 0,
        onBefore: $$$1.noop,
        onAfter: $$$1.noop,
        onValTooSmall: $$$1.noop,
        onNoResultFound: null,
        show: function show() {
          $$$1(this).show();
        },
        hide: function hide() {
          $$$1(this).hide();
        },
        prepareQuery: function prepareQuery(val) {
          return val.toLowerCase().split(' ');
        },
        testQuery: function testQuery(query, txt, _row) {
          for (var i = 0; i < query.length; i += 1) {
            if (txt.indexOf(query[i]) === -1) {
              return false;
            }
          }

          return true;
        }
      },
      diacriticsRemovalMap: [{
        'base': 'A',
        'letters': /[\u0041\u24B6\uFF21\u00C0\u00C1\u00C2\u1EA6\u1EA4\u1EAA\u1EA8\u00C3\u0100\u0102\u1EB0\u1EAE\u1EB4\u1EB2\u0226\u01E0\u00C4\u01DE\u1EA2\u00C5\u01FA\u01CD\u0200\u0202\u1EA0\u1EAC\u1EB6\u1E00\u0104\u023A\u2C6F]/g
      }, {
        'base': 'AA',
        'letters': /[\uA732]/g
      }, {
        'base': 'AE',
        'letters': /[\u00C6\u01FC\u01E2]/g
      }, {
        'base': 'AO',
        'letters': /[\uA734]/g
      }, {
        'base': 'AU',
        'letters': /[\uA736]/g
      }, {
        'base': 'AV',
        'letters': /[\uA738\uA73A]/g
      }, {
        'base': 'AY',
        'letters': /[\uA73C]/g
      }, {
        'base': 'B',
        'letters': /[\u0042\u24B7\uFF22\u1E02\u1E04\u1E06\u0243\u0182\u0181]/g
      }, {
        'base': 'C',
        'letters': /[\u0043\u24B8\uFF23\u0106\u0108\u010A\u010C\u00C7\u1E08\u0187\u023B\uA73E]/g
      }, {
        'base': 'D',
        'letters': /[\u0044\u24B9\uFF24\u1E0A\u010E\u1E0C\u1E10\u1E12\u1E0E\u0110\u018B\u018A\u0189\uA779]/g
      }, {
        'base': 'DZ',
        'letters': /[\u01F1\u01C4]/g
      }, {
        'base': 'Dz',
        'letters': /[\u01F2\u01C5]/g
      }, {
        'base': 'E',
        'letters': /[\u0045\u24BA\uFF25\u00C8\u00C9\u00CA\u1EC0\u1EBE\u1EC4\u1EC2\u1EBC\u0112\u1E14\u1E16\u0114\u0116\u00CB\u1EBA\u011A\u0204\u0206\u1EB8\u1EC6\u0228\u1E1C\u0118\u1E18\u1E1A\u0190\u018E]/g
      }, {
        'base': 'F',
        'letters': /[\u0046\u24BB\uFF26\u1E1E\u0191\uA77B]/g
      }, {
        'base': 'G',
        'letters': /[\u0047\u24BC\uFF27\u01F4\u011C\u1E20\u011E\u0120\u01E6\u0122\u01E4\u0193\uA7A0\uA77D\uA77E]/g
      }, {
        'base': 'H',
        'letters': /[\u0048\u24BD\uFF28\u0124\u1E22\u1E26\u021E\u1E24\u1E28\u1E2A\u0126\u2C67\u2C75\uA78D]/g
      }, {
        'base': 'I',
        'letters': /[\u0049\u24BE\uFF29\u00CC\u00CD\u00CE\u0128\u012A\u012C\u0130\u00CF\u1E2E\u1EC8\u01CF\u0208\u020A\u1ECA\u012E\u1E2C\u0197]/g
      }, {
        'base': 'J',
        'letters': /[\u004A\u24BF\uFF2A\u0134\u0248]/g
      }, {
        'base': 'K',
        'letters': /[\u004B\u24C0\uFF2B\u1E30\u01E8\u1E32\u0136\u1E34\u0198\u2C69\uA740\uA742\uA744\uA7A2]/g
      }, {
        'base': 'L',
        'letters': /[\u004C\u24C1\uFF2C\u013F\u0139\u013D\u1E36\u1E38\u013B\u1E3C\u1E3A\u0141\u023D\u2C62\u2C60\uA748\uA746\uA780]/g
      }, {
        'base': 'LJ',
        'letters': /[\u01C7]/g
      }, {
        'base': 'Lj',
        'letters': /[\u01C8]/g
      }, {
        'base': 'M',
        'letters': /[\u004D\u24C2\uFF2D\u1E3E\u1E40\u1E42\u2C6E\u019C]/g
      }, {
        'base': 'N',
        'letters': /[\u004E\u24C3\uFF2E\u01F8\u0143\u00D1\u1E44\u0147\u1E46\u0145\u1E4A\u1E48\u0220\u019D\uA790\uA7A4]/g
      }, {
        'base': 'NJ',
        'letters': /[\u01CA]/g
      }, {
        'base': 'Nj',
        'letters': /[\u01CB]/g
      }, {
        'base': 'O',
        'letters': /[\u004F\u24C4\uFF2F\u00D2\u00D3\u00D4\u1ED2\u1ED0\u1ED6\u1ED4\u00D5\u1E4C\u022C\u1E4E\u014C\u1E50\u1E52\u014E\u022E\u0230\u00D6\u022A\u1ECE\u0150\u01D1\u020C\u020E\u01A0\u1EDC\u1EDA\u1EE0\u1EDE\u1EE2\u1ECC\u1ED8\u01EA\u01EC\u00D8\u01FE\u0186\u019F\uA74A\uA74C]/g
      }, {
        'base': 'OI',
        'letters': /[\u01A2]/g
      }, {
        'base': 'OO',
        'letters': /[\uA74E]/g
      }, {
        'base': 'OU',
        'letters': /[\u0222]/g
      }, {
        'base': 'P',
        'letters': /[\u0050\u24C5\uFF30\u1E54\u1E56\u01A4\u2C63\uA750\uA752\uA754]/g
      }, {
        'base': 'Q',
        'letters': /[\u0051\u24C6\uFF31\uA756\uA758\u024A]/g
      }, {
        'base': 'R',
        'letters': /[\u0052\u24C7\uFF32\u0154\u1E58\u0158\u0210\u0212\u1E5A\u1E5C\u0156\u1E5E\u024C\u2C64\uA75A\uA7A6\uA782]/g
      }, {
        'base': 'S',
        'letters': /[\u0053\u24C8\uFF33\u1E9E\u015A\u1E64\u015C\u1E60\u0160\u1E66\u1E62\u1E68\u0218\u015E\u2C7E\uA7A8\uA784]/g
      }, {
        'base': 'T',
        'letters': /[\u0054\u24C9\uFF34\u1E6A\u0164\u1E6C\u021A\u0162\u1E70\u1E6E\u0166\u01AC\u01AE\u023E\uA786]/g
      }, {
        'base': 'TZ',
        'letters': /[\uA728]/g
      }, {
        'base': 'U',
        'letters': /[\u0055\u24CA\uFF35\u00D9\u00DA\u00DB\u0168\u1E78\u016A\u1E7A\u016C\u00DC\u01DB\u01D7\u01D5\u01D9\u1EE6\u016E\u0170\u01D3\u0214\u0216\u01AF\u1EEA\u1EE8\u1EEE\u1EEC\u1EF0\u1EE4\u1E72\u0172\u1E76\u1E74\u0244]/g
      }, {
        'base': 'V',
        'letters': /[\u0056\u24CB\uFF36\u1E7C\u1E7E\u01B2\uA75E\u0245]/g
      }, {
        'base': 'VY',
        'letters': /[\uA760]/g
      }, {
        'base': 'W',
        'letters': /[\u0057\u24CC\uFF37\u1E80\u1E82\u0174\u1E86\u1E84\u1E88\u2C72]/g
      }, {
        'base': 'X',
        'letters': /[\u0058\u24CD\uFF38\u1E8A\u1E8C]/g
      }, {
        'base': 'Y',
        'letters': /[\u0059\u24CE\uFF39\u1EF2\u00DD\u0176\u1EF8\u0232\u1E8E\u0178\u1EF6\u1EF4\u01B3\u024E\u1EFE]/g
      }, {
        'base': 'Z',
        'letters': /[\u005A\u24CF\uFF3A\u0179\u1E90\u017B\u017D\u1E92\u1E94\u01B5\u0224\u2C7F\u2C6B\uA762]/g
      }, {
        'base': 'a',
        'letters': /[\u0061\u24D0\uFF41\u1E9A\u00E0\u00E1\u00E2\u1EA7\u1EA5\u1EAB\u1EA9\u00E3\u0101\u0103\u1EB1\u1EAF\u1EB5\u1EB3\u0227\u01E1\u00E4\u01DF\u1EA3\u00E5\u01FB\u01CE\u0201\u0203\u1EA1\u1EAD\u1EB7\u1E01\u0105\u2C65\u0250]/g
      }, {
        'base': 'aa',
        'letters': /[\uA733]/g
      }, {
        'base': 'ae',
        'letters': /[\u00E6\u01FD\u01E3]/g
      }, {
        'base': 'ao',
        'letters': /[\uA735]/g
      }, {
        'base': 'au',
        'letters': /[\uA737]/g
      }, {
        'base': 'av',
        'letters': /[\uA739\uA73B]/g
      }, {
        'base': 'ay',
        'letters': /[\uA73D]/g
      }, {
        'base': 'b',
        'letters': /[\u0062\u24D1\uFF42\u1E03\u1E05\u1E07\u0180\u0183\u0253]/g
      }, {
        'base': 'c',
        'letters': /[\u0063\u24D2\uFF43\u0107\u0109\u010B\u010D\u00E7\u1E09\u0188\u023C\uA73F\u2184]/g
      }, {
        'base': 'd',
        'letters': /[\u0064\u24D3\uFF44\u1E0B\u010F\u1E0D\u1E11\u1E13\u1E0F\u0111\u018C\u0256\u0257\uA77A]/g
      }, {
        'base': 'dz',
        'letters': /[\u01F3\u01C6]/g
      }, {
        'base': 'e',
        'letters': /[\u0065\u24D4\uFF45\u00E8\u00E9\u00EA\u1EC1\u1EBF\u1EC5\u1EC3\u1EBD\u0113\u1E15\u1E17\u0115\u0117\u00EB\u1EBB\u011B\u0205\u0207\u1EB9\u1EC7\u0229\u1E1D\u0119\u1E19\u1E1B\u0247\u025B\u01DD]/g
      }, {
        'base': 'f',
        'letters': /[\u0066\u24D5\uFF46\u1E1F\u0192\uA77C]/g
      }, {
        'base': 'g',
        'letters': /[\u0067\u24D6\uFF47\u01F5\u011D\u1E21\u011F\u0121\u01E7\u0123\u01E5\u0260\uA7A1\u1D79\uA77F]/g
      }, {
        'base': 'h',
        'letters': /[\u0068\u24D7\uFF48\u0125\u1E23\u1E27\u021F\u1E25\u1E29\u1E2B\u1E96\u0127\u2C68\u2C76\u0265]/g
      }, {
        'base': 'hv',
        'letters': /[\u0195]/g
      }, {
        'base': 'i',
        'letters': /[\u0069\u24D8\uFF49\u00EC\u00ED\u00EE\u0129\u012B\u012D\u00EF\u1E2F\u1EC9\u01D0\u0209\u020B\u1ECB\u012F\u1E2D\u0268\u0131]/g
      }, {
        'base': 'j',
        'letters': /[\u006A\u24D9\uFF4A\u0135\u01F0\u0249]/g
      }, {
        'base': 'k',
        'letters': /[\u006B\u24DA\uFF4B\u1E31\u01E9\u1E33\u0137\u1E35\u0199\u2C6A\uA741\uA743\uA745\uA7A3]/g
      }, {
        'base': 'l',
        'letters': /[\u006C\u24DB\uFF4C\u0140\u013A\u013E\u1E37\u1E39\u013C\u1E3D\u1E3B\u017F\u0142\u019A\u026B\u2C61\uA749\uA781\uA747]/g
      }, {
        'base': 'lj',
        'letters': /[\u01C9]/g
      }, {
        'base': 'm',
        'letters': /[\u006D\u24DC\uFF4D\u1E3F\u1E41\u1E43\u0271\u026F]/g
      }, {
        'base': 'n',
        'letters': /[\u006E\u24DD\uFF4E\u01F9\u0144\u00F1\u1E45\u0148\u1E47\u0146\u1E4B\u1E49\u019E\u0272\u0149\uA791\uA7A5]/g
      }, {
        'base': 'nj',
        'letters': /[\u01CC]/g
      }, {
        'base': 'o',
        'letters': /[\u006F\u24DE\uFF4F\u00F2\u00F3\u00F4\u1ED3\u1ED1\u1ED7\u1ED5\u00F5\u1E4D\u022D\u1E4F\u014D\u1E51\u1E53\u014F\u022F\u0231\u00F6\u022B\u1ECF\u0151\u01D2\u020D\u020F\u01A1\u1EDD\u1EDB\u1EE1\u1EDF\u1EE3\u1ECD\u1ED9\u01EB\u01ED\u00F8\u01FF\u0254\uA74B\uA74D\u0275]/g
      }, {
        'base': 'oi',
        'letters': /[\u01A3]/g
      }, {
        'base': 'ou',
        'letters': /[\u0223]/g
      }, {
        'base': 'oo',
        'letters': /[\uA74F]/g
      }, {
        'base': 'p',
        'letters': /[\u0070\u24DF\uFF50\u1E55\u1E57\u01A5\u1D7D\uA751\uA753\uA755]/g
      }, {
        'base': 'q',
        'letters': /[\u0071\u24E0\uFF51\u024B\uA757\uA759]/g
      }, {
        'base': 'r',
        'letters': /[\u0072\u24E1\uFF52\u0155\u1E59\u0159\u0211\u0213\u1E5B\u1E5D\u0157\u1E5F\u024D\u027D\uA75B\uA7A7\uA783]/g
      }, {
        'base': 's',
        'letters': /[\u0073\u24E2\uFF53\u00DF\u015B\u1E65\u015D\u1E61\u0161\u1E67\u1E63\u1E69\u0219\u015F\u023F\uA7A9\uA785\u1E9B]/g
      }, {
        'base': 't',
        'letters': /[\u0074\u24E3\uFF54\u1E6B\u1E97\u0165\u1E6D\u021B\u0163\u1E71\u1E6F\u0167\u01AD\u0288\u2C66\uA787]/g
      }, {
        'base': 'tz',
        'letters': /[\uA729]/g
      }, {
        'base': 'u',
        'letters': /[\u0075\u24E4\uFF55\u00F9\u00FA\u00FB\u0169\u1E79\u016B\u1E7B\u016D\u00FC\u01DC\u01D8\u01D6\u01DA\u1EE7\u016F\u0171\u01D4\u0215\u0217\u01B0\u1EEB\u1EE9\u1EEF\u1EED\u1EF1\u1EE5\u1E73\u0173\u1E77\u1E75\u0289]/g
      }, {
        'base': 'v',
        'letters': /[\u0076\u24E5\uFF56\u1E7D\u1E7F\u028B\uA75F\u028C]/g
      }, {
        'base': 'vy',
        'letters': /[\uA761]/g
      }, {
        'base': 'w',
        'letters': /[\u0077\u24E6\uFF57\u1E81\u1E83\u0175\u1E87\u1E85\u1E98\u1E89\u2C73]/g
      }, {
        'base': 'x',
        'letters': /[\u0078\u24E7\uFF58\u1E8B\u1E8D]/g
      }, {
        'base': 'y',
        'letters': /[\u0079\u24E8\uFF59\u1EF3\u00FD\u0177\u1EF9\u0233\u1E8F\u00FF\u1EF7\u1E99\u1EF5\u01B4\u024F\u1EFF]/g
      }, {
        'base': 'z',
        'letters': /[\u007A\u24E9\uFF5A\u017A\u1E91\u017C\u017E\u1E93\u1E95\u01B6\u0225\u0240\u2C6C\uA763]/g
      }]
    };

    $$$1.fn.quicksearch = function (target, opt) {
      this.removeDiacritics = function (str) {
        var changes = $$$1.quicksearch.diacriticsRemovalMap;

        for (var i = 0; i < changes.length; i++) {
          str = str.replace(changes[i].letters, changes[i].base);
        }

        return str;
      };

      var timeout,
          cache,
          rowcache,
          jq_results,
          val = '',
          last_val = '',
          self = this,
          options = $$$1.extend({}, $$$1.quicksearch.defaults, opt); // Assure selectors

      options.noResults = !options.noResults ? $$$1() : $$$1(options.noResults);
      options.loader = !options.loader ? $$$1() : $$$1(options.loader);

      this.go = function () {
        var i = 0,
            len = 0,
            numMatchedRows = 0,
            noresults = true,
            query,
            val_empty = val.replace(' ', '').length === 0;

        if (options.removeDiacritics) {
          val = self.removeDiacritics(val);
        }

        query = options.prepareQuery(val);

        for (i = 0, len = rowcache.length; i < len; i++) {
          if (query.length > 0 && query[0].length < options.minValLength) {
            options.show.apply(rowcache[i]);
            noresults = false;
            numMatchedRows++;
          } else if (val_empty || options.testQuery(query, cache[i], rowcache[i])) {
            options.show.apply(rowcache[i]);
            noresults = false;
            numMatchedRows++;
          } else {
            options.hide.apply(rowcache[i]);
          }
        }

        if (noresults) {
          if ($$$1.isFunction(options.onNoResultFound)) {
            options.onNoResultFound(this);
          } else {
            this.results(false);
          }
        } else {
          this.results(true);
          this.stripe();
        }

        this.matchedResultsCount = numMatchedRows;
        this.loader(false);
        options.onAfter.call(this);
        last_val = val;
        return this;
      };
      /*
       * External API so that users can perform search programatically.
       * */


      this.search = function (submittedVal) {
        val = submittedVal;
        self.trigger();
      };
      /*
       * External API so that users can perform search programatically.
       * */


      this.reset = function () {
        val = '';
        this.loader(true);
        options.onBefore.call(this);
        global.clearTimeout(timeout);
        timeout = global.setTimeout(function () {
          self.go();
        }, options.delay);
      };
      /*
       * External API to get the number of matched results as seen in
       * https://github.com/ruiz107/quicksearch/commit/f78dc440b42d95ce9caed1d087174dd4359982d6
       * */


      this.currentMatchedResults = function () {
        return this.matchedResultsCount;
      };

      this.stripe = function () {
        if (typeof options.stripeRows === "object" && options.stripeRows !== null) {
          var joined = options.stripeRows.join(' ');
          var stripeRows_length = options.stripeRows.length;
          jq_results.not(':hidden').each(function (i) {
            $$$1(this).removeClass(joined).addClass(options.stripeRows[i % stripeRows_length]);
          });
        }

        return this;
      };

      this.strip_html = function (input) {
        var output = input.replace(new RegExp('<[^<]+\\>', 'g'), ' ');

        if (!options.caseSensitive) {
          output = output.toLowerCase();
        }

        output = $$$1.trim(output);
        return output;
      };

      this.results = function (bool) {
        if (!!options.noResults.length) {
          options.noResults[bool ? 'hide' : 'show']();
        }

        return this;
      };

      this.loader = function (bool) {
        if (!!options.loader.length) {
          options.loader[bool ? 'show' : 'hide']();
        }

        return this;
      };

      this.cache = function (doRedraw) {
        doRedraw = typeof doRedraw === "undefined" ? true : doRedraw;
        jq_results = $$$1(target).not(options.noResults);

        if (typeof options.selector === "string") {
          cache = jq_results.map(function () {
            return $$$1(this).find(options.selector).map(function () {
              var temp = self.strip_html(this.innerHTML);
              return options.removeDiacritics ? self.removeDiacritics(temp) : temp;
            }).get().join(" ");
          });
        } else {
          cache = jq_results.map(function () {
            var temp = self.strip_html(this.innerHTML);
            return options.removeDiacritics ? self.removeDiacritics(temp) : temp;
          });
        }

        rowcache = jq_results.map(function () {
          return this;
        });
        /*
         * Modified fix for sync-ing "val".
         * Original fix https://github.com/michaellwest/quicksearch/commit/4ace4008d079298a01f97f885ba8fa956a9703d1
         * */

        val = val || this.val() || "";

        if (doRedraw) {
          this.go();
        }

        return this;
      };

      this.trigger = function () {
        if (val.length < options.minValLength && val.length > last_val.length || val.length < options.minValLength - 1 && val.length < last_val.length) {
          options.onValTooSmall.call(this, val);
          self.go();
        } else {
          this.loader(true);
          options.onBefore.call(this);
          global.clearTimeout(timeout);
          timeout = global.setTimeout(function () {
            self.go();
          }, options.delay);
        }

        return this;
      };

      this.cache();
      this.stripe();
      this.loader(false);
      return this.each(function () {
        $$$1(this).on(options.bind, function (e) {
          if (options.keyCode) {
            var keycode = e.keyCode || e.which;

            if (keycode === options.keyCode) {
              val = $$$1(this).val();
              self.trigger();
            }
          } else {
            val = $$$1(this).val();
            self.trigger();
          }
        });
        $$$1(this).on(options.resetBind, function () {
          val = '';
          self.reset();
        });
      });
    }; // node export


    if (global.module && global.module.exports) {
      module.exports = $$$1.fn.quicksearch;
    }
  })(jQuery, window || global);

  /*
   * This combined file was created by the DataTables downloader builder:
   *   https://datatables.net/download
   *
   * To rebuild or modify this file with the latest versions of the included
   * software please visit:
   *   https://datatables.net/download/#bs4/dt-1.10.18/r-2.2.2
   *
   * Included libraries:
   *   DataTables 1.10.18, Responsive 2.2.2
   */

  /*! DataTables 1.10.18
   * ©2008-2018 SpryMedia Ltd - datatables.net/license
   */

  /**
   * @summary     DataTables
   * @description Paginate, search and order HTML tables
   * @version     1.10.18
   * @file        jquery.dataTables.js
   * @author      SpryMedia Ltd
   * @contact     www.datatables.net
   * @copyright   Copyright 2008-2018 SpryMedia Ltd.
   *
   * This source file is free software, available under the following license:
   *   MIT license - http://datatables.net/license
   *
   * This source file is distributed in the hope that it will be useful, but
   * WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
   * or FITNESS FOR A PARTICULAR PURPOSE. See the license files for details.
   *
   * For details please refer to: http://www.datatables.net
   */

  /*jslint evil: true, undef: true, browser: true */

  /*globals $,require,jQuery,define,_selector_run,_selector_opts,_selector_first,_selector_row_indexes,_ext,_Api,_api_register,_api_registerPlural,_re_new_lines,_re_html,_re_formatted_numeric,_re_escape_regex,_empty,_intVal,_numToDecimal,_isNumber,_isHtml,_htmlNumeric,_pluck,_pluck_order,_range,_stripHtml,_unique,_fnBuildAjax,_fnAjaxUpdate,_fnAjaxParameters,_fnAjaxUpdateDraw,_fnAjaxDataSrc,_fnAddColumn,_fnColumnOptions,_fnAdjustColumnSizing,_fnVisibleToColumnIndex,_fnColumnIndexToVisible,_fnVisbleColumns,_fnGetColumns,_fnColumnTypes,_fnApplyColumnDefs,_fnHungarianMap,_fnCamelToHungarian,_fnLanguageCompat,_fnBrowserDetect,_fnAddData,_fnAddTr,_fnNodeToDataIndex,_fnNodeToColumnIndex,_fnGetCellData,_fnSetCellData,_fnSplitObjNotation,_fnGetObjectDataFn,_fnSetObjectDataFn,_fnGetDataMaster,_fnClearTable,_fnDeleteIndex,_fnInvalidate,_fnGetRowElements,_fnCreateTr,_fnBuildHead,_fnDrawHead,_fnDraw,_fnReDraw,_fnAddOptionsHtml,_fnDetectHeader,_fnGetUniqueThs,_fnFeatureHtmlFilter,_fnFilterComplete,_fnFilterCustom,_fnFilterColumn,_fnFilter,_fnFilterCreateSearch,_fnEscapeRegex,_fnFilterData,_fnFeatureHtmlInfo,_fnUpdateInfo,_fnInfoMacros,_fnInitialise,_fnInitComplete,_fnLengthChange,_fnFeatureHtmlLength,_fnFeatureHtmlPaginate,_fnPageChange,_fnFeatureHtmlProcessing,_fnProcessingDisplay,_fnFeatureHtmlTable,_fnScrollDraw,_fnApplyToChildren,_fnCalculateColumnWidths,_fnThrottle,_fnConvertToWidth,_fnGetWidestNode,_fnGetMaxLenString,_fnStringToCss,_fnSortFlatten,_fnSort,_fnSortAria,_fnSortListener,_fnSortAttachListener,_fnSortingClasses,_fnSortData,_fnSaveState,_fnLoadState,_fnSettingsFromNode,_fnLog,_fnMap,_fnBindAction,_fnCallbackReg,_fnCallbackFire,_fnLengthOverflow,_fnRenderer,_fnDataSource,_fnRowAttributes*/
  (function (factory) {

    if (typeof define === 'function' && define.amd) {
      // AMD
      define(['jquery'], function ($$$1) {
        return factory($$$1, window, document);
      });
    } else if (typeof exports === 'object') {
      // CommonJS
      module.exports = function (root, $$$1) {
        if (!root) {
          // CommonJS environments without a window global must pass a
          // root. This will give an error otherwise
          root = window;
        }

        if (!$$$1) {
          $$$1 = typeof window !== 'undefined' ? // jQuery's factory checks for a global window
          require('jquery') : require('jquery')(root);
        }

        return factory($$$1, root, root.document);
      };
    } else {
      // Browser
      factory(jQuery, window, document);
    }
  })(function ($$$1, window, document, undefined) {
    /**
     * DataTables is a plug-in for the jQuery Javascript library. It is a highly
     * flexible tool, based upon the foundations of progressive enhancement,
     * which will add advanced interaction controls to any HTML table. For a
     * full list of features please refer to
     * [DataTables.net](href="http://datatables.net).
     *
     * Note that the `DataTable` object is not a global variable but is aliased
     * to `jQuery.fn.DataTable` and `jQuery.fn.dataTable` through which it may
     * be  accessed.
     *
     *  @class
     *  @param {object} [init={}] Configuration object for DataTables. Options
     *    are defined by {@link DataTable.defaults}
     *  @requires jQuery 1.7+
     *
     *  @example
     *    // Basic initialisation
     *    $(document).ready( function {
     *      $('#example').dataTable();
     *    } );
     *
     *  @example
     *    // Initialisation with configuration options - in this case, disable
     *    // pagination and sorting.
     *    $(document).ready( function {
     *      $('#example').dataTable( {
     *        "paginate": false,
     *        "sort": false
     *      } );
     *    } );
     */

    var DataTable = function DataTable(options) {
      /**
       * Perform a jQuery selector action on the table's TR elements (from the tbody) and
       * return the resulting jQuery object.
       *  @param {string|node|jQuery} sSelector jQuery selector or node collection to act on
       *  @param {object} [oOpts] Optional parameters for modifying the rows to be included
       *  @param {string} [oOpts.filter=none] Select TR elements that meet the current filter
       *    criterion ("applied") or all TR elements (i.e. no filter).
       *  @param {string} [oOpts.order=current] Order of the TR elements in the processed array.
       *    Can be either 'current', whereby the current sorting of the table is used, or
       *    'original' whereby the original order the data was read into the table is used.
       *  @param {string} [oOpts.page=all] Limit the selection to the currently displayed page
       *    ("current") or not ("all"). If 'current' is given, then order is assumed to be
       *    'current' and filter is 'applied', regardless of what they might be given as.
       *  @returns {object} jQuery object, filtered by the given selector.
       *  @dtopt API
       *  @deprecated Since v1.10
       *
       *  @example
       *    $(document).ready(function() {
       *      var oTable = $('#example').dataTable();
       *
       *      // Highlight every second row
       *      oTable.$('tr:odd').css('backgroundColor', 'blue');
       *    } );
       *
       *  @example
       *    $(document).ready(function() {
       *      var oTable = $('#example').dataTable();
       *
       *      // Filter to rows with 'Webkit' in them, add a background colour and then
       *      // remove the filter, thus highlighting the 'Webkit' rows only.
       *      oTable.fnFilter('Webkit');
       *      oTable.$('tr', {"search": "applied"}).css('backgroundColor', 'blue');
       *      oTable.fnFilter('');
       *    } );
       */
      this.$ = function (sSelector, oOpts) {
        return this.api(true).$(sSelector, oOpts);
      };
      /**
       * Almost identical to $ in operation, but in this case returns the data for the matched
       * rows - as such, the jQuery selector used should match TR row nodes or TD/TH cell nodes
       * rather than any descendants, so the data can be obtained for the row/cell. If matching
       * rows are found, the data returned is the original data array/object that was used to
       * create the row (or a generated array if from a DOM source).
       *
       * This method is often useful in-combination with $ where both functions are given the
       * same parameters and the array indexes will match identically.
       *  @param {string|node|jQuery} sSelector jQuery selector or node collection to act on
       *  @param {object} [oOpts] Optional parameters for modifying the rows to be included
       *  @param {string} [oOpts.filter=none] Select elements that meet the current filter
       *    criterion ("applied") or all elements (i.e. no filter).
       *  @param {string} [oOpts.order=current] Order of the data in the processed array.
       *    Can be either 'current', whereby the current sorting of the table is used, or
       *    'original' whereby the original order the data was read into the table is used.
       *  @param {string} [oOpts.page=all] Limit the selection to the currently displayed page
       *    ("current") or not ("all"). If 'current' is given, then order is assumed to be
       *    'current' and filter is 'applied', regardless of what they might be given as.
       *  @returns {array} Data for the matched elements. If any elements, as a result of the
       *    selector, were not TR, TD or TH elements in the DataTable, they will have a null
       *    entry in the array.
       *  @dtopt API
       *  @deprecated Since v1.10
       *
       *  @example
       *    $(document).ready(function() {
       *      var oTable = $('#example').dataTable();
       *
       *      // Get the data from the first row in the table
       *      var data = oTable._('tr:first');
       *
       *      // Do something useful with the data
       *      alert( "First cell is: "+data[0] );
       *    } );
       *
       *  @example
       *    $(document).ready(function() {
       *      var oTable = $('#example').dataTable();
       *
       *      // Filter to 'Webkit' and get all data for
       *      oTable.fnFilter('Webkit');
       *      var data = oTable._('tr', {"search": "applied"});
       *
       *      // Do something with the data
       *      alert( data.length+" rows matched the search" );
       *    } );
       */


      this._ = function (sSelector, oOpts) {
        return this.api(true).rows(sSelector, oOpts).data();
      };
      /**
       * Create a DataTables Api instance, with the currently selected tables for
       * the Api's context.
       * @param {boolean} [traditional=false] Set the API instance's context to be
       *   only the table referred to by the `DataTable.ext.iApiIndex` option, as was
       *   used in the API presented by DataTables 1.9- (i.e. the traditional mode),
       *   or if all tables captured in the jQuery object should be used.
       * @return {DataTables.Api}
       */


      this.api = function (traditional) {
        return traditional ? new _Api2(_fnSettingsFromNode(this[_ext.iApiIndex])) : new _Api2(this);
      };
      /**
       * Add a single new row or multiple rows of data to the table. Please note
       * that this is suitable for client-side processing only - if you are using
       * server-side processing (i.e. "bServerSide": true), then to add data, you
       * must add it to the data source, i.e. the server-side, through an Ajax call.
       *  @param {array|object} data The data to be added to the table. This can be:
       *    <ul>
       *      <li>1D array of data - add a single row with the data provided</li>
       *      <li>2D array of arrays - add multiple rows in a single call</li>
       *      <li>object - data object when using <i>mData</i></li>
       *      <li>array of objects - multiple data objects when using <i>mData</i></li>
       *    </ul>
       *  @param {bool} [redraw=true] redraw the table or not
       *  @returns {array} An array of integers, representing the list of indexes in
       *    <i>aoData</i> ({@link DataTable.models.oSettings}) that have been added to
       *    the table.
       *  @dtopt API
       *  @deprecated Since v1.10
       *
       *  @example
       *    // Global var for counter
       *    var giCount = 2;
       *
       *    $(document).ready(function() {
       *      $('#example').dataTable();
       *    } );
       *
       *    function fnClickAddRow() {
       *      $('#example').dataTable().fnAddData( [
       *        giCount+".1",
       *        giCount+".2",
       *        giCount+".3",
       *        giCount+".4" ]
       *      );
       *
       *      giCount++;
       *    }
       */


      this.fnAddData = function (data, redraw) {
        var api = this.api(true);
        /* Check if we want to add multiple rows or not */

        var rows = $$$1.isArray(data) && ($$$1.isArray(data[0]) || $$$1.isPlainObject(data[0])) ? api.rows.add(data) : api.row.add(data);

        if (redraw === undefined || redraw) {
          api.draw();
        }

        return rows.flatten().toArray();
      };
      /**
       * This function will make DataTables recalculate the column sizes, based on the data
       * contained in the table and the sizes applied to the columns (in the DOM, CSS or
       * through the sWidth parameter). This can be useful when the width of the table's
       * parent element changes (for example a window resize).
       *  @param {boolean} [bRedraw=true] Redraw the table or not, you will typically want to
       *  @dtopt API
       *  @deprecated Since v1.10
       *
       *  @example
       *    $(document).ready(function() {
       *      var oTable = $('#example').dataTable( {
       *        "sScrollY": "200px",
       *        "bPaginate": false
       *      } );
       *
       *      $(window).on('resize', function () {
       *        oTable.fnAdjustColumnSizing();
       *      } );
       *    } );
       */


      this.fnAdjustColumnSizing = function (bRedraw) {
        var api = this.api(true).columns.adjust();
        var settings = api.settings()[0];
        var scroll = settings.oScroll;

        if (bRedraw === undefined || bRedraw) {
          api.draw(false);
        } else if (scroll.sX !== "" || scroll.sY !== "") {
          /* If not redrawing, but scrolling, we want to apply the new column sizes anyway */
          _fnScrollDraw(settings);
        }
      };
      /**
       * Quickly and simply clear a table
       *  @param {bool} [bRedraw=true] redraw the table or not
       *  @dtopt API
       *  @deprecated Since v1.10
       *
       *  @example
       *    $(document).ready(function() {
       *      var oTable = $('#example').dataTable();
       *
       *      // Immediately 'nuke' the current rows (perhaps waiting for an Ajax callback...)
       *      oTable.fnClearTable();
       *    } );
       */


      this.fnClearTable = function (bRedraw) {
        var api = this.api(true).clear();

        if (bRedraw === undefined || bRedraw) {
          api.draw();
        }
      };
      /**
       * The exact opposite of 'opening' a row, this function will close any rows which
       * are currently 'open'.
       *  @param {node} nTr the table row to 'close'
       *  @returns {int} 0 on success, or 1 if failed (can't find the row)
       *  @dtopt API
       *  @deprecated Since v1.10
       *
       *  @example
       *    $(document).ready(function() {
       *      var oTable;
       *
       *      // 'open' an information row when a row is clicked on
       *      $('#example tbody tr').click( function () {
       *        if ( oTable.fnIsOpen(this) ) {
       *          oTable.fnClose( this );
       *        } else {
       *          oTable.fnOpen( this, "Temporary row opened", "info_row" );
       *        }
       *      } );
       *
       *      oTable = $('#example').dataTable();
       *    } );
       */


      this.fnClose = function (nTr) {
        this.api(true).row(nTr).child.hide();
      };
      /**
       * Remove a row for the table
       *  @param {mixed} target The index of the row from aoData to be deleted, or
       *    the TR element you want to delete
       *  @param {function|null} [callBack] Callback function
       *  @param {bool} [redraw=true] Redraw the table or not
       *  @returns {array} The row that was deleted
       *  @dtopt API
       *  @deprecated Since v1.10
       *
       *  @example
       *    $(document).ready(function() {
       *      var oTable = $('#example').dataTable();
       *
       *      // Immediately remove the first row
       *      oTable.fnDeleteRow( 0 );
       *    } );
       */


      this.fnDeleteRow = function (target, callback, redraw) {
        var api = this.api(true);
        var rows = api.rows(target);
        var settings = rows.settings()[0];
        var data = settings.aoData[rows[0][0]];
        rows.remove();

        if (callback) {
          callback.call(this, settings, data);
        }

        if (redraw === undefined || redraw) {
          api.draw();
        }

        return data;
      };
      /**
       * Restore the table to it's original state in the DOM by removing all of DataTables
       * enhancements, alterations to the DOM structure of the table and event listeners.
       *  @param {boolean} [remove=false] Completely remove the table from the DOM
       *  @dtopt API
       *  @deprecated Since v1.10
       *
       *  @example
       *    $(document).ready(function() {
       *      // This example is fairly pointless in reality, but shows how fnDestroy can be used
       *      var oTable = $('#example').dataTable();
       *      oTable.fnDestroy();
       *    } );
       */


      this.fnDestroy = function (remove) {
        this.api(true).destroy(remove);
      };
      /**
       * Redraw the table
       *  @param {bool} [complete=true] Re-filter and resort (if enabled) the table before the draw.
       *  @dtopt API
       *  @deprecated Since v1.10
       *
       *  @example
       *    $(document).ready(function() {
       *      var oTable = $('#example').dataTable();
       *
       *      // Re-draw the table - you wouldn't want to do it here, but it's an example :-)
       *      oTable.fnDraw();
       *    } );
       */


      this.fnDraw = function (complete) {
        // Note that this isn't an exact match to the old call to _fnDraw - it takes
        // into account the new data, but can hold position.
        this.api(true).draw(complete);
      };
      /**
       * Filter the input based on data
       *  @param {string} sInput String to filter the table on
       *  @param {int|null} [iColumn] Column to limit filtering to
       *  @param {bool} [bRegex=false] Treat as regular expression or not
       *  @param {bool} [bSmart=true] Perform smart filtering or not
       *  @param {bool} [bShowGlobal=true] Show the input global filter in it's input box(es)
       *  @param {bool} [bCaseInsensitive=true] Do case-insensitive matching (true) or not (false)
       *  @dtopt API
       *  @deprecated Since v1.10
       *
       *  @example
       *    $(document).ready(function() {
       *      var oTable = $('#example').dataTable();
       *
       *      // Sometime later - filter...
       *      oTable.fnFilter( 'test string' );
       *    } );
       */


      this.fnFilter = function (sInput, iColumn, bRegex, bSmart, bShowGlobal, bCaseInsensitive) {
        var api = this.api(true);

        if (iColumn === null || iColumn === undefined) {
          api.search(sInput, bRegex, bSmart, bCaseInsensitive);
        } else {
          api.column(iColumn).search(sInput, bRegex, bSmart, bCaseInsensitive);
        }

        api.draw();
      };
      /**
       * Get the data for the whole table, an individual row or an individual cell based on the
       * provided parameters.
       *  @param {int|node} [src] A TR row node, TD/TH cell node or an integer. If given as
       *    a TR node then the data source for the whole row will be returned. If given as a
       *    TD/TH cell node then iCol will be automatically calculated and the data for the
       *    cell returned. If given as an integer, then this is treated as the aoData internal
       *    data index for the row (see fnGetPosition) and the data for that row used.
       *  @param {int} [col] Optional column index that you want the data of.
       *  @returns {array|object|string} If mRow is undefined, then the data for all rows is
       *    returned. If mRow is defined, just data for that row, and is iCol is
       *    defined, only data for the designated cell is returned.
       *  @dtopt API
       *  @deprecated Since v1.10
       *
       *  @example
       *    // Row data
       *    $(document).ready(function() {
       *      oTable = $('#example').dataTable();
       *
       *      oTable.$('tr').click( function () {
       *        var data = oTable.fnGetData( this );
       *        // ... do something with the array / object of data for the row
       *      } );
       *    } );
       *
       *  @example
       *    // Individual cell data
       *    $(document).ready(function() {
       *      oTable = $('#example').dataTable();
       *
       *      oTable.$('td').click( function () {
       *        var sData = oTable.fnGetData( this );
       *        alert( 'The cell clicked on had the value of '+sData );
       *      } );
       *    } );
       */


      this.fnGetData = function (src, col) {
        var api = this.api(true);

        if (src !== undefined) {
          var type = src.nodeName ? src.nodeName.toLowerCase() : '';
          return col !== undefined || type == 'td' || type == 'th' ? api.cell(src, col).data() : api.row(src).data() || null;
        }

        return api.data().toArray();
      };
      /**
       * Get an array of the TR nodes that are used in the table's body. Note that you will
       * typically want to use the '$' API method in preference to this as it is more
       * flexible.
       *  @param {int} [iRow] Optional row index for the TR element you want
       *  @returns {array|node} If iRow is undefined, returns an array of all TR elements
       *    in the table's body, or iRow is defined, just the TR element requested.
       *  @dtopt API
       *  @deprecated Since v1.10
       *
       *  @example
       *    $(document).ready(function() {
       *      var oTable = $('#example').dataTable();
       *
       *      // Get the nodes from the table
       *      var nNodes = oTable.fnGetNodes( );
       *    } );
       */


      this.fnGetNodes = function (iRow) {
        var api = this.api(true);
        return iRow !== undefined ? api.row(iRow).node() : api.rows().nodes().flatten().toArray();
      };
      /**
       * Get the array indexes of a particular cell from it's DOM element
       * and column index including hidden columns
       *  @param {node} node this can either be a TR, TD or TH in the table's body
       *  @returns {int} If nNode is given as a TR, then a single index is returned, or
       *    if given as a cell, an array of [row index, column index (visible),
       *    column index (all)] is given.
       *  @dtopt API
       *  @deprecated Since v1.10
       *
       *  @example
       *    $(document).ready(function() {
       *      $('#example tbody td').click( function () {
       *        // Get the position of the current data from the node
       *        var aPos = oTable.fnGetPosition( this );
       *
       *        // Get the data array for this row
       *        var aData = oTable.fnGetData( aPos[0] );
       *
       *        // Update the data array and return the value
       *        aData[ aPos[1] ] = 'clicked';
       *        this.innerHTML = 'clicked';
       *      } );
       *
       *      // Init DataTables
       *      oTable = $('#example').dataTable();
       *    } );
       */


      this.fnGetPosition = function (node) {
        var api = this.api(true);
        var nodeName = node.nodeName.toUpperCase();

        if (nodeName == 'TR') {
          return api.row(node).index();
        } else if (nodeName == 'TD' || nodeName == 'TH') {
          var cell = api.cell(node).index();
          return [cell.row, cell.columnVisible, cell.column];
        }

        return null;
      };
      /**
       * Check to see if a row is 'open' or not.
       *  @param {node} nTr the table row to check
       *  @returns {boolean} true if the row is currently open, false otherwise
       *  @dtopt API
       *  @deprecated Since v1.10
       *
       *  @example
       *    $(document).ready(function() {
       *      var oTable;
       *
       *      // 'open' an information row when a row is clicked on
       *      $('#example tbody tr').click( function () {
       *        if ( oTable.fnIsOpen(this) ) {
       *          oTable.fnClose( this );
       *        } else {
       *          oTable.fnOpen( this, "Temporary row opened", "info_row" );
       *        }
       *      } );
       *
       *      oTable = $('#example').dataTable();
       *    } );
       */


      this.fnIsOpen = function (nTr) {
        return this.api(true).row(nTr).child.isShown();
      };
      /**
       * This function will place a new row directly after a row which is currently
       * on display on the page, with the HTML contents that is passed into the
       * function. This can be used, for example, to ask for confirmation that a
       * particular record should be deleted.
       *  @param {node} nTr The table row to 'open'
       *  @param {string|node|jQuery} mHtml The HTML to put into the row
       *  @param {string} sClass Class to give the new TD cell
       *  @returns {node} The row opened. Note that if the table row passed in as the
       *    first parameter, is not found in the table, this method will silently
       *    return.
       *  @dtopt API
       *  @deprecated Since v1.10
       *
       *  @example
       *    $(document).ready(function() {
       *      var oTable;
       *
       *      // 'open' an information row when a row is clicked on
       *      $('#example tbody tr').click( function () {
       *        if ( oTable.fnIsOpen(this) ) {
       *          oTable.fnClose( this );
       *        } else {
       *          oTable.fnOpen( this, "Temporary row opened", "info_row" );
       *        }
       *      } );
       *
       *      oTable = $('#example').dataTable();
       *    } );
       */


      this.fnOpen = function (nTr, mHtml, sClass) {
        return this.api(true).row(nTr).child(mHtml, sClass).show().child()[0];
      };
      /**
       * Change the pagination - provides the internal logic for pagination in a simple API
       * function. With this function you can have a DataTables table go to the next,
       * previous, first or last pages.
       *  @param {string|int} mAction Paging action to take: "first", "previous", "next" or "last"
       *    or page number to jump to (integer), note that page 0 is the first page.
       *  @param {bool} [bRedraw=true] Redraw the table or not
       *  @dtopt API
       *  @deprecated Since v1.10
       *
       *  @example
       *    $(document).ready(function() {
       *      var oTable = $('#example').dataTable();
       *      oTable.fnPageChange( 'next' );
       *    } );
       */


      this.fnPageChange = function (mAction, bRedraw) {
        var api = this.api(true).page(mAction);

        if (bRedraw === undefined || bRedraw) {
          api.draw(false);
        }
      };
      /**
       * Show a particular column
       *  @param {int} iCol The column whose display should be changed
       *  @param {bool} bShow Show (true) or hide (false) the column
       *  @param {bool} [bRedraw=true] Redraw the table or not
       *  @dtopt API
       *  @deprecated Since v1.10
       *
       *  @example
       *    $(document).ready(function() {
       *      var oTable = $('#example').dataTable();
       *
       *      // Hide the second column after initialisation
       *      oTable.fnSetColumnVis( 1, false );
       *    } );
       */


      this.fnSetColumnVis = function (iCol, bShow, bRedraw) {
        var api = this.api(true).column(iCol).visible(bShow);

        if (bRedraw === undefined || bRedraw) {
          api.columns.adjust().draw();
        }
      };
      /**
       * Get the settings for a particular table for external manipulation
       *  @returns {object} DataTables settings object. See
       *    {@link DataTable.models.oSettings}
       *  @dtopt API
       *  @deprecated Since v1.10
       *
       *  @example
       *    $(document).ready(function() {
       *      var oTable = $('#example').dataTable();
       *      var oSettings = oTable.fnSettings();
       *
       *      // Show an example parameter from the settings
       *      alert( oSettings._iDisplayStart );
       *    } );
       */


      this.fnSettings = function () {
        return _fnSettingsFromNode(this[_ext.iApiIndex]);
      };
      /**
       * Sort the table by a particular column
       *  @param {int} iCol the data index to sort on. Note that this will not match the
       *    'display index' if you have hidden data entries
       *  @dtopt API
       *  @deprecated Since v1.10
       *
       *  @example
       *    $(document).ready(function() {
       *      var oTable = $('#example').dataTable();
       *
       *      // Sort immediately with columns 0 and 1
       *      oTable.fnSort( [ [0,'asc'], [1,'asc'] ] );
       *    } );
       */


      this.fnSort = function (aaSort) {
        this.api(true).order(aaSort).draw();
      };
      /**
       * Attach a sort listener to an element for a given column
       *  @param {node} nNode the element to attach the sort listener to
       *  @param {int} iColumn the column that a click on this node will sort on
       *  @param {function} [fnCallback] callback function when sort is run
       *  @dtopt API
       *  @deprecated Since v1.10
       *
       *  @example
       *    $(document).ready(function() {
       *      var oTable = $('#example').dataTable();
       *
       *      // Sort on column 1, when 'sorter' is clicked on
       *      oTable.fnSortListener( document.getElementById('sorter'), 1 );
       *    } );
       */


      this.fnSortListener = function (nNode, iColumn, fnCallback) {
        this.api(true).order.listener(nNode, iColumn, fnCallback);
      };
      /**
       * Update a table cell or row - this method will accept either a single value to
       * update the cell with, an array of values with one element for each column or
       * an object in the same format as the original data source. The function is
       * self-referencing in order to make the multi column updates easier.
       *  @param {object|array|string} mData Data to update the cell/row with
       *  @param {node|int} mRow TR element you want to update or the aoData index
       *  @param {int} [iColumn] The column to update, give as null or undefined to
       *    update a whole row.
       *  @param {bool} [bRedraw=true] Redraw the table or not
       *  @param {bool} [bAction=true] Perform pre-draw actions or not
       *  @returns {int} 0 on success, 1 on error
       *  @dtopt API
       *  @deprecated Since v1.10
       *
       *  @example
       *    $(document).ready(function() {
       *      var oTable = $('#example').dataTable();
       *      oTable.fnUpdate( 'Example update', 0, 0 ); // Single cell
       *      oTable.fnUpdate( ['a', 'b', 'c', 'd', 'e'], $('tbody tr')[0] ); // Row
       *    } );
       */


      this.fnUpdate = function (mData, mRow, iColumn, bRedraw, bAction) {
        var api = this.api(true);

        if (iColumn === undefined || iColumn === null) {
          api.row(mRow).data(mData);
        } else {
          api.cell(mRow, iColumn).data(mData);
        }

        if (bAction === undefined || bAction) {
          api.columns.adjust();
        }

        if (bRedraw === undefined || bRedraw) {
          api.draw();
        }

        return 0;
      };
      /**
       * Provide a common method for plug-ins to check the version of DataTables being used, in order
       * to ensure compatibility.
       *  @param {string} sVersion Version string to check for, in the format "X.Y.Z". Note that the
       *    formats "X" and "X.Y" are also acceptable.
       *  @returns {boolean} true if this version of DataTables is greater or equal to the required
       *    version, or false if this version of DataTales is not suitable
       *  @method
       *  @dtopt API
       *  @deprecated Since v1.10
       *
       *  @example
       *    $(document).ready(function() {
       *      var oTable = $('#example').dataTable();
       *      alert( oTable.fnVersionCheck( '1.9.0' ) );
       *    } );
       */


      this.fnVersionCheck = _ext.fnVersionCheck;

      var _that = this;

      var emptyInit = options === undefined;
      var len = this.length;

      if (emptyInit) {
        options = {};
      }

      this.oApi = this.internal = _ext.internal; // Extend with old style plug-in API methods

      for (var fn in DataTable.ext.internal) {
        if (fn) {
          this[fn] = _fnExternApiFunc(fn);
        }
      }

      this.each(function () {
        // For each initialisation we want to give it a clean initialisation
        // object that can be bashed around
        var o = {};
        var oInit = len > 1 ? // optimisation for single table case
        _fnExtend(o, options, true) : options;
        /*global oInit,_that,emptyInit*/

        var i = 0,
            iLen;
        var sId = this.getAttribute('id');
        var bInitHandedOff = false;
        var defaults = DataTable.defaults;
        var $this = $$$1(this);
        /* Sanity check */

        if (this.nodeName.toLowerCase() != 'table') {
          _fnLog(null, 0, 'Non-table node initialisation (' + this.nodeName + ')', 2);

          return;
        }
        /* Backwards compatibility for the defaults */


        _fnCompatOpts(defaults);

        _fnCompatCols(defaults.column);
        /* Convert the camel-case defaults to Hungarian */


        _fnCamelToHungarian(defaults, defaults, true);

        _fnCamelToHungarian(defaults.column, defaults.column, true);
        /* Setting up the initialisation object */


        _fnCamelToHungarian(defaults, $$$1.extend(oInit, $this.data()));
        /* Check to see if we are re-initialising a table */


        var allSettings = DataTable.settings;

        for (i = 0, iLen = allSettings.length; i < iLen; i++) {
          var s = allSettings[i];
          /* Base check on table node */

          if (s.nTable == this || s.nTHead && s.nTHead.parentNode == this || s.nTFoot && s.nTFoot.parentNode == this) {
            var bRetrieve = oInit.bRetrieve !== undefined ? oInit.bRetrieve : defaults.bRetrieve;
            var bDestroy = oInit.bDestroy !== undefined ? oInit.bDestroy : defaults.bDestroy;

            if (emptyInit || bRetrieve) {
              return s.oInstance;
            } else if (bDestroy) {
              s.oInstance.fnDestroy();
              break;
            } else {
              _fnLog(s, 0, 'Cannot reinitialise DataTable', 3);

              return;
            }
          }
          /* If the element we are initialising has the same ID as a table which was previously
           * initialised, but the table nodes don't match (from before) then we destroy the old
           * instance by simply deleting it. This is under the assumption that the table has been
           * destroyed by other methods. Anyone using non-id selectors will need to do this manually
           */


          if (s.sTableId == this.id) {
            allSettings.splice(i, 1);
            break;
          }
        }
        /* Ensure the table has an ID - required for accessibility */


        if (sId === null || sId === "") {
          sId = "DataTables_Table_" + DataTable.ext._unique++;
          this.id = sId;
        }
        /* Create the settings object for this table and set some of the default parameters */


        var oSettings = $$$1.extend(true, {}, DataTable.models.oSettings, {
          "sDestroyWidth": $this[0].style.width,
          "sInstance": sId,
          "sTableId": sId
        });
        oSettings.nTable = this;
        oSettings.oApi = _that.internal;
        oSettings.oInit = oInit;
        allSettings.push(oSettings); // Need to add the instance after the instance after the settings object has been added
        // to the settings array, so we can self reference the table instance if more than one

        oSettings.oInstance = _that.length === 1 ? _that : $this.dataTable(); // Backwards compatibility, before we apply all the defaults

        _fnCompatOpts(oInit);

        _fnLanguageCompat(oInit.oLanguage); // If the length menu is given, but the init display length is not, use the length menu


        if (oInit.aLengthMenu && !oInit.iDisplayLength) {
          oInit.iDisplayLength = $$$1.isArray(oInit.aLengthMenu[0]) ? oInit.aLengthMenu[0][0] : oInit.aLengthMenu[0];
        } // Apply the defaults and init options to make a single init object will all
        // options defined from defaults and instance options.


        oInit = _fnExtend($$$1.extend(true, {}, defaults), oInit); // Map the initialisation options onto the settings object

        _fnMap(oSettings.oFeatures, oInit, ["bPaginate", "bLengthChange", "bFilter", "bSort", "bSortMulti", "bInfo", "bProcessing", "bAutoWidth", "bSortClasses", "bServerSide", "bDeferRender"]);

        _fnMap(oSettings, oInit, ["asStripeClasses", "ajax", "fnServerData", "fnFormatNumber", "sServerMethod", "aaSorting", "aaSortingFixed", "aLengthMenu", "sPaginationType", "sAjaxSource", "sAjaxDataProp", "iStateDuration", "sDom", "bSortCellsTop", "iTabIndex", "fnStateLoadCallback", "fnStateSaveCallback", "renderer", "searchDelay", "rowId", ["iCookieDuration", "iStateDuration"], // backwards compat
        ["oSearch", "oPreviousSearch"], ["aoSearchCols", "aoPreSearchCols"], ["iDisplayLength", "_iDisplayLength"]]);

        _fnMap(oSettings.oScroll, oInit, [["sScrollX", "sX"], ["sScrollXInner", "sXInner"], ["sScrollY", "sY"], ["bScrollCollapse", "bCollapse"]]);

        _fnMap(oSettings.oLanguage, oInit, "fnInfoCallback");
        /* Callback functions which are array driven */


        _fnCallbackReg(oSettings, 'aoDrawCallback', oInit.fnDrawCallback, 'user');

        _fnCallbackReg(oSettings, 'aoServerParams', oInit.fnServerParams, 'user');

        _fnCallbackReg(oSettings, 'aoStateSaveParams', oInit.fnStateSaveParams, 'user');

        _fnCallbackReg(oSettings, 'aoStateLoadParams', oInit.fnStateLoadParams, 'user');

        _fnCallbackReg(oSettings, 'aoStateLoaded', oInit.fnStateLoaded, 'user');

        _fnCallbackReg(oSettings, 'aoRowCallback', oInit.fnRowCallback, 'user');

        _fnCallbackReg(oSettings, 'aoRowCreatedCallback', oInit.fnCreatedRow, 'user');

        _fnCallbackReg(oSettings, 'aoHeaderCallback', oInit.fnHeaderCallback, 'user');

        _fnCallbackReg(oSettings, 'aoFooterCallback', oInit.fnFooterCallback, 'user');

        _fnCallbackReg(oSettings, 'aoInitComplete', oInit.fnInitComplete, 'user');

        _fnCallbackReg(oSettings, 'aoPreDrawCallback', oInit.fnPreDrawCallback, 'user');

        oSettings.rowIdFn = _fnGetObjectDataFn(oInit.rowId);
        /* Browser support detection */

        _fnBrowserDetect(oSettings);

        var oClasses = oSettings.oClasses;
        $$$1.extend(oClasses, DataTable.ext.classes, oInit.oClasses);
        $this.addClass(oClasses.sTable);

        if (oSettings.iInitDisplayStart === undefined) {
          /* Display start point, taking into account the save saving */
          oSettings.iInitDisplayStart = oInit.iDisplayStart;
          oSettings._iDisplayStart = oInit.iDisplayStart;
        }

        if (oInit.iDeferLoading !== null) {
          oSettings.bDeferLoading = true;
          var tmp = $$$1.isArray(oInit.iDeferLoading);
          oSettings._iRecordsDisplay = tmp ? oInit.iDeferLoading[0] : oInit.iDeferLoading;
          oSettings._iRecordsTotal = tmp ? oInit.iDeferLoading[1] : oInit.iDeferLoading;
        }
        /* Language definitions */


        var oLanguage = oSettings.oLanguage;
        $$$1.extend(true, oLanguage, oInit.oLanguage);

        if (oLanguage.sUrl) {
          /* Get the language definitions from a file - because this Ajax call makes the language
           * get async to the remainder of this function we use bInitHandedOff to indicate that
           * _fnInitialise will be fired by the returned Ajax handler, rather than the constructor
           */
          $$$1.ajax({
            dataType: 'json',
            url: oLanguage.sUrl,
            success: function success(json) {
              _fnLanguageCompat(json);

              _fnCamelToHungarian(defaults.oLanguage, json);

              $$$1.extend(true, oLanguage, json);

              _fnInitialise(oSettings);
            },
            error: function error() {
              // Error occurred loading language file, continue on as best we can
              _fnInitialise(oSettings);
            }
          });
          bInitHandedOff = true;
        }
        /*
         * Stripes
         */


        if (oInit.asStripeClasses === null) {
          oSettings.asStripeClasses = [oClasses.sStripeOdd, oClasses.sStripeEven];
        }
        /* Remove row stripe classes if they are already on the table row */


        var stripeClasses = oSettings.asStripeClasses;
        var rowOne = $this.children('tbody').find('tr').eq(0);

        if ($$$1.inArray(true, $$$1.map(stripeClasses, function (el, i) {
          return rowOne.hasClass(el);
        })) !== -1) {
          $$$1('tbody tr', this).removeClass(stripeClasses.join(' '));
          oSettings.asDestroyStripes = stripeClasses.slice();
        }
        /*
         * Columns
         * See if we should load columns automatically or use defined ones
         */


        var anThs = [];
        var aoColumnsInit;
        var nThead = this.getElementsByTagName('thead');

        if (nThead.length !== 0) {
          _fnDetectHeader(oSettings.aoHeader, nThead[0]);

          anThs = _fnGetUniqueThs(oSettings);
        }
        /* If not given a column array, generate one with nulls */


        if (oInit.aoColumns === null) {
          aoColumnsInit = [];

          for (i = 0, iLen = anThs.length; i < iLen; i++) {
            aoColumnsInit.push(null);
          }
        } else {
          aoColumnsInit = oInit.aoColumns;
        }
        /* Add the columns */


        for (i = 0, iLen = aoColumnsInit.length; i < iLen; i++) {
          _fnAddColumn(oSettings, anThs ? anThs[i] : null);
        }
        /* Apply the column definitions */


        _fnApplyColumnDefs(oSettings, oInit.aoColumnDefs, aoColumnsInit, function (iCol, oDef) {
          _fnColumnOptions(oSettings, iCol, oDef);
        });
        /* HTML5 attribute detection - build an mData object automatically if the
         * attributes are found
         */


        if (rowOne.length) {
          var a = function a(cell, name) {
            return cell.getAttribute('data-' + name) !== null ? name : null;
          };

          $$$1(rowOne[0]).children('th, td').each(function (i, cell) {
            var col = oSettings.aoColumns[i];

            if (col.mData === i) {
              var sort = a(cell, 'sort') || a(cell, 'order');
              var filter = a(cell, 'filter') || a(cell, 'search');

              if (sort !== null || filter !== null) {
                col.mData = {
                  _: i + '.display',
                  sort: sort !== null ? i + '.@data-' + sort : undefined,
                  type: sort !== null ? i + '.@data-' + sort : undefined,
                  filter: filter !== null ? i + '.@data-' + filter : undefined
                };

                _fnColumnOptions(oSettings, i);
              }
            }
          });
        }

        var features = oSettings.oFeatures;

        var loadedInit = function loadedInit() {
          /*
           * Sorting
           * @todo For modularisation (1.11) this needs to do into a sort start up handler
           */
          // If aaSorting is not defined, then we use the first indicator in asSorting
          // in case that has been altered, so the default sort reflects that option
          if (oInit.aaSorting === undefined) {
            var sorting = oSettings.aaSorting;

            for (i = 0, iLen = sorting.length; i < iLen; i++) {
              sorting[i][1] = oSettings.aoColumns[i].asSorting[0];
            }
          }
          /* Do a first pass on the sorting classes (allows any size changes to be taken into
           * account, and also will apply sorting disabled classes if disabled
           */


          _fnSortingClasses(oSettings);

          if (features.bSort) {
            _fnCallbackReg(oSettings, 'aoDrawCallback', function () {
              if (oSettings.bSorted) {
                var aSort = _fnSortFlatten(oSettings);

                var sortedColumns = {};
                $$$1.each(aSort, function (i, val) {
                  sortedColumns[val.src] = val.dir;
                });

                _fnCallbackFire(oSettings, null, 'order', [oSettings, aSort, sortedColumns]);

                _fnSortAria(oSettings);
              }
            });
          }

          _fnCallbackReg(oSettings, 'aoDrawCallback', function () {
            if (oSettings.bSorted || _fnDataSource(oSettings) === 'ssp' || features.bDeferRender) {
              _fnSortingClasses(oSettings);
            }
          }, 'sc');
          /*
           * Final init
           * Cache the header, body and footer as required, creating them if needed
           */
          // Work around for Webkit bug 83867 - store the caption-side before removing from doc


          var captions = $this.children('caption').each(function () {
            this._captionSide = $$$1(this).css('caption-side');
          });
          var thead = $this.children('thead');

          if (thead.length === 0) {
            thead = $$$1('<thead/>').appendTo($this);
          }

          oSettings.nTHead = thead[0];
          var tbody = $this.children('tbody');

          if (tbody.length === 0) {
            tbody = $$$1('<tbody/>').appendTo($this);
          }

          oSettings.nTBody = tbody[0];
          var tfoot = $this.children('tfoot');

          if (tfoot.length === 0 && captions.length > 0 && (oSettings.oScroll.sX !== "" || oSettings.oScroll.sY !== "")) {
            // If we are a scrolling table, and no footer has been given, then we need to create
            // a tfoot element for the caption element to be appended to
            tfoot = $$$1('<tfoot/>').appendTo($this);
          }

          if (tfoot.length === 0 || tfoot.children().length === 0) {
            $this.addClass(oClasses.sNoFooter);
          } else if (tfoot.length > 0) {
            oSettings.nTFoot = tfoot[0];

            _fnDetectHeader(oSettings.aoFooter, oSettings.nTFoot);
          }
          /* Check if there is data passing into the constructor */


          if (oInit.aaData) {
            for (i = 0; i < oInit.aaData.length; i++) {
              _fnAddData(oSettings, oInit.aaData[i]);
            }
          } else if (oSettings.bDeferLoading || _fnDataSource(oSettings) == 'dom') {
            /* Grab the data from the page - only do this when deferred loading or no Ajax
             * source since there is no point in reading the DOM data if we are then going
             * to replace it with Ajax data
             */
            _fnAddTr(oSettings, $$$1(oSettings.nTBody).children('tr'));
          }
          /* Copy the data index array */


          oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
          /* Initialisation complete - table can be drawn */

          oSettings.bInitialised = true;
          /* Check if we need to initialise the table (it might not have been handed off to the
           * language processor)
           */

          if (bInitHandedOff === false) {
            _fnInitialise(oSettings);
          }
        };
        /* Must be done after everything which can be overridden by the state saving! */


        if (oInit.bStateSave) {
          features.bStateSave = true;

          _fnCallbackReg(oSettings, 'aoDrawCallback', _fnSaveState, 'state_save');

          _fnLoadState(oSettings, oInit, loadedInit);
        } else {
          loadedInit();
        }
      });
      _that = null;
      return this;
    };
    /*
     * It is useful to have variables which are scoped locally so only the
     * DataTables functions can access them and they don't leak into global space.
     * At the same time these functions are often useful over multiple files in the
     * core and API, so we list, or at least document, all variables which are used
     * by DataTables as private variables here. This also ensures that there is no
     * clashing of variable names and that they can easily referenced for reuse.
     */
    // Defined else where
    //  _selector_run
    //  _selector_opts
    //  _selector_first
    //  _selector_row_indexes


    var _ext; // DataTable.ext


    var _Api2; // DataTable.Api


    var _api_register; // DataTable.Api.register


    var _api_registerPlural; // DataTable.Api.registerPlural


    var _re_dic = {};
    var _re_new_lines = /[\r\n]/g;
    var _re_html = /<.*?>/g; // This is not strict ISO8601 - Date.parse() is quite lax, although
    // implementations differ between browsers.

    var _re_date = /^\d{2,4}[\.\/\-]\d{1,2}[\.\/\-]\d{1,2}([T ]{1}\d{1,2}[:\.]\d{2}([\.:]\d{2})?)?$/; // Escape regular expression special characters

    var _re_escape_regex = new RegExp('(\\' + ['/', '.', '*', '+', '?', '|', '(', ')', '[', ']', '{', '}', '\\', '$', '^', '-'].join('|\\') + ')', 'g'); // http://en.wikipedia.org/wiki/Foreign_exchange_market
    // - \u20BD - Russian ruble.
    // - \u20a9 - South Korean Won
    // - \u20BA - Turkish Lira
    // - \u20B9 - Indian Rupee
    // - R - Brazil (R$) and South Africa
    // - fr - Swiss Franc
    // - kr - Swedish krona, Norwegian krone and Danish krone
    // - \u2009 is thin space and \u202F is narrow no-break space, both used in many
    // - Ƀ - Bitcoin
    // - Ξ - Ethereum
    //   standards as thousands separators.


    var _re_formatted_numeric = /[',$£€¥%\u2009\u202F\u20BD\u20a9\u20BArfkɃΞ]/gi;

    var _empty = function _empty(d) {
      return !d || d === true || d === '-' ? true : false;
    };

    var _intVal = function _intVal(s) {
      var integer = parseInt(s, 10);
      return !isNaN(integer) && isFinite(s) ? integer : null;
    }; // Convert from a formatted number with characters other than `.` as the
    // decimal place, to a Javascript number


    var _numToDecimal = function _numToDecimal(num, decimalPoint) {
      // Cache created regular expressions for speed as this function is called often
      if (!_re_dic[decimalPoint]) {
        _re_dic[decimalPoint] = new RegExp(_fnEscapeRegex(decimalPoint), 'g');
      }

      return typeof num === 'string' && decimalPoint !== '.' ? num.replace(/\./g, '').replace(_re_dic[decimalPoint], '.') : num;
    };

    var _isNumber = function _isNumber(d, decimalPoint, formatted) {
      var strType = typeof d === 'string'; // If empty return immediately so there must be a number if it is a
      // formatted string (this stops the string "k", or "kr", etc being detected
      // as a formatted number for currency

      if (_empty(d)) {
        return true;
      }

      if (decimalPoint && strType) {
        d = _numToDecimal(d, decimalPoint);
      }

      if (formatted && strType) {
        d = d.replace(_re_formatted_numeric, '');
      }

      return !isNaN(parseFloat(d)) && isFinite(d);
    }; // A string without HTML in it can be considered to be HTML still


    var _isHtml = function _isHtml(d) {
      return _empty(d) || typeof d === 'string';
    };

    var _htmlNumeric = function _htmlNumeric(d, decimalPoint, formatted) {
      if (_empty(d)) {
        return true;
      }

      var html = _isHtml(d);

      return !html ? null : _isNumber(_stripHtml(d), decimalPoint, formatted) ? true : null;
    };

    var _pluck = function _pluck(a, prop, prop2) {
      var out = [];
      var i = 0,
          ien = a.length; // Could have the test in the loop for slightly smaller code, but speed
      // is essential here

      if (prop2 !== undefined) {
        for (; i < ien; i++) {
          if (a[i] && a[i][prop]) {
            out.push(a[i][prop][prop2]);
          }
        }
      } else {
        for (; i < ien; i++) {
          if (a[i]) {
            out.push(a[i][prop]);
          }
        }
      }

      return out;
    }; // Basically the same as _pluck, but rather than looping over `a` we use `order`
    // as the indexes to pick from `a`


    var _pluck_order = function _pluck_order(a, order, prop, prop2) {
      var out = [];
      var i = 0,
          ien = order.length; // Could have the test in the loop for slightly smaller code, but speed
      // is essential here

      if (prop2 !== undefined) {
        for (; i < ien; i++) {
          if (a[order[i]][prop]) {
            out.push(a[order[i]][prop][prop2]);
          }
        }
      } else {
        for (; i < ien; i++) {
          out.push(a[order[i]][prop]);
        }
      }

      return out;
    };

    var _range = function _range(len, start) {
      var out = [];
      var end;

      if (start === undefined) {
        start = 0;
        end = len;
      } else {
        end = start;
        start = len;
      }

      for (var i = start; i < end; i++) {
        out.push(i);
      }

      return out;
    };

    var _removeEmpty = function _removeEmpty(a) {
      var out = [];

      for (var i = 0, ien = a.length; i < ien; i++) {
        if (a[i]) {
          // careful - will remove all falsy values!
          out.push(a[i]);
        }
      }

      return out;
    };

    var _stripHtml = function _stripHtml(d) {
      return d.replace(_re_html, '');
    };
    /**
     * Determine if all values in the array are unique. This means we can short
     * cut the _unique method at the cost of a single loop. A sorted array is used
     * to easily check the values.
     *
     * @param  {array} src Source array
     * @return {boolean} true if all unique, false otherwise
     * @ignore
     */


    var _areAllUnique = function _areAllUnique(src) {
      if (src.length < 2) {
        return true;
      }

      var sorted = src.slice().sort();
      var last = sorted[0];

      for (var i = 1, ien = sorted.length; i < ien; i++) {
        if (sorted[i] === last) {
          return false;
        }

        last = sorted[i];
      }

      return true;
    };
    /**
     * Find the unique elements in a source array.
     *
     * @param  {array} src Source array
     * @return {array} Array of unique items
     * @ignore
     */


    var _unique = function _unique(src) {
      if (_areAllUnique(src)) {
        return src.slice();
      } // A faster unique method is to use object keys to identify used values,
      // but this doesn't work with arrays or objects, which we must also
      // consider. See jsperf.com/compare-array-unique-versions/4 for more
      // information.


      var out = [],
          val,
          i,
          ien = src.length,
          j,
          k = 0;

      again: for (i = 0; i < ien; i++) {
        val = src[i];

        for (j = 0; j < k; j++) {
          if (out[j] === val) {
            continue again;
          }
        }

        out.push(val);
        k++;
      }

      return out;
    };
    /**
     * DataTables utility methods
     * 
     * This namespace provides helper methods that DataTables uses internally to
     * create a DataTable, but which are not exclusively used only for DataTables.
     * These methods can be used by extension authors to save the duplication of
     * code.
     *
     *  @namespace
     */


    DataTable.util = {
      /**
       * Throttle the calls to a function. Arguments and context are maintained
       * for the throttled function.
       *
       * @param {function} fn Function to be called
       * @param {integer} freq Call frequency in mS
       * @return {function} Wrapped function
       */
      throttle: function throttle(fn, freq) {
        var frequency = freq !== undefined ? freq : 200,
            last,
            timer;
        return function () {
          var that = this,
              now = +new Date(),
              args = arguments;

          if (last && now < last + frequency) {
            clearTimeout(timer);
            timer = setTimeout(function () {
              last = undefined;
              fn.apply(that, args);
            }, frequency);
          } else {
            last = now;
            fn.apply(that, args);
          }
        };
      },

      /**
       * Escape a string such that it can be used in a regular expression
       *
       *  @param {string} val string to escape
       *  @returns {string} escaped string
       */
      escapeRegex: function escapeRegex(val) {
        return val.replace(_re_escape_regex, '\\$1');
      }
    };
    /**
     * Create a mapping object that allows camel case parameters to be looked up
     * for their Hungarian counterparts. The mapping is stored in a private
     * parameter called `_hungarianMap` which can be accessed on the source object.
     *  @param {object} o
     *  @memberof DataTable#oApi
     */

    function _fnHungarianMap(o) {
      var hungarian = 'a aa ai ao as b fn i m o s ',
          match,
          newKey,
          map = {};
      $$$1.each(o, function (key, val) {
        match = key.match(/^([^A-Z]+?)([A-Z])/);

        if (match && hungarian.indexOf(match[1] + ' ') !== -1) {
          newKey = key.replace(match[0], match[2].toLowerCase());
          map[newKey] = key;

          if (match[1] === 'o') {
            _fnHungarianMap(o[key]);
          }
        }
      });
      o._hungarianMap = map;
    }
    /**
     * Convert from camel case parameters to Hungarian, based on a Hungarian map
     * created by _fnHungarianMap.
     *  @param {object} src The model object which holds all parameters that can be
     *    mapped.
     *  @param {object} user The object to convert from camel case to Hungarian.
     *  @param {boolean} force When set to `true`, properties which already have a
     *    Hungarian value in the `user` object will be overwritten. Otherwise they
     *    won't be.
     *  @memberof DataTable#oApi
     */


    function _fnCamelToHungarian(src, user, force) {
      if (!src._hungarianMap) {
        _fnHungarianMap(src);
      }

      var hungarianKey;
      $$$1.each(user, function (key, val) {
        hungarianKey = src._hungarianMap[key];

        if (hungarianKey !== undefined && (force || user[hungarianKey] === undefined)) {
          // For objects, we need to buzz down into the object to copy parameters
          if (hungarianKey.charAt(0) === 'o') {
            // Copy the camelCase options over to the hungarian
            if (!user[hungarianKey]) {
              user[hungarianKey] = {};
            }

            $$$1.extend(true, user[hungarianKey], user[key]);

            _fnCamelToHungarian(src[hungarianKey], user[hungarianKey], force);
          } else {
            user[hungarianKey] = user[key];
          }
        }
      });
    }
    /**
     * Language compatibility - when certain options are given, and others aren't, we
     * need to duplicate the values over, in order to provide backwards compatibility
     * with older language files.
     *  @param {object} oSettings dataTables settings object
     *  @memberof DataTable#oApi
     */


    function _fnLanguageCompat(lang) {
      // Note the use of the Hungarian notation for the parameters in this method as
      // this is called after the mapping of camelCase to Hungarian
      var defaults = DataTable.defaults.oLanguage; // Default mapping

      var defaultDecimal = defaults.sDecimal;

      if (defaultDecimal) {
        _addNumericSort(defaultDecimal);
      }

      if (lang) {
        var zeroRecords = lang.sZeroRecords; // Backwards compatibility - if there is no sEmptyTable given, then use the same as
        // sZeroRecords - assuming that is given.

        if (!lang.sEmptyTable && zeroRecords && defaults.sEmptyTable === "No data available in table") {
          _fnMap(lang, lang, 'sZeroRecords', 'sEmptyTable');
        } // Likewise with loading records


        if (!lang.sLoadingRecords && zeroRecords && defaults.sLoadingRecords === "Loading...") {
          _fnMap(lang, lang, 'sZeroRecords', 'sLoadingRecords');
        } // Old parameter name of the thousands separator mapped onto the new


        if (lang.sInfoThousands) {
          lang.sThousands = lang.sInfoThousands;
        }

        var decimal = lang.sDecimal;

        if (decimal && defaultDecimal !== decimal) {
          _addNumericSort(decimal);
        }
      }
    }
    /**
     * Map one parameter onto another
     *  @param {object} o Object to map
     *  @param {*} knew The new parameter name
     *  @param {*} old The old parameter name
     */


    var _fnCompatMap = function _fnCompatMap(o, knew, old) {
      if (o[knew] !== undefined) {
        o[old] = o[knew];
      }
    };
    /**
     * Provide backwards compatibility for the main DT options. Note that the new
     * options are mapped onto the old parameters, so this is an external interface
     * change only.
     *  @param {object} init Object to map
     */


    function _fnCompatOpts(init) {
      _fnCompatMap(init, 'ordering', 'bSort');

      _fnCompatMap(init, 'orderMulti', 'bSortMulti');

      _fnCompatMap(init, 'orderClasses', 'bSortClasses');

      _fnCompatMap(init, 'orderCellsTop', 'bSortCellsTop');

      _fnCompatMap(init, 'order', 'aaSorting');

      _fnCompatMap(init, 'orderFixed', 'aaSortingFixed');

      _fnCompatMap(init, 'paging', 'bPaginate');

      _fnCompatMap(init, 'pagingType', 'sPaginationType');

      _fnCompatMap(init, 'pageLength', 'iDisplayLength');

      _fnCompatMap(init, 'searching', 'bFilter'); // Boolean initialisation of x-scrolling


      if (typeof init.sScrollX === 'boolean') {
        init.sScrollX = init.sScrollX ? '100%' : '';
      }

      if (typeof init.scrollX === 'boolean') {
        init.scrollX = init.scrollX ? '100%' : '';
      } // Column search objects are in an array, so it needs to be converted
      // element by element


      var searchCols = init.aoSearchCols;

      if (searchCols) {
        for (var i = 0, ien = searchCols.length; i < ien; i++) {
          if (searchCols[i]) {
            _fnCamelToHungarian(DataTable.models.oSearch, searchCols[i]);
          }
        }
      }
    }
    /**
     * Provide backwards compatibility for column options. Note that the new options
     * are mapped onto the old parameters, so this is an external interface change
     * only.
     *  @param {object} init Object to map
     */


    function _fnCompatCols(init) {
      _fnCompatMap(init, 'orderable', 'bSortable');

      _fnCompatMap(init, 'orderData', 'aDataSort');

      _fnCompatMap(init, 'orderSequence', 'asSorting');

      _fnCompatMap(init, 'orderDataType', 'sortDataType'); // orderData can be given as an integer


      var dataSort = init.aDataSort;

      if (typeof dataSort === 'number' && !$$$1.isArray(dataSort)) {
        init.aDataSort = [dataSort];
      }
    }
    /**
     * Browser feature detection for capabilities, quirks
     *  @param {object} settings dataTables settings object
     *  @memberof DataTable#oApi
     */


    function _fnBrowserDetect(settings) {
      // We don't need to do this every time DataTables is constructed, the values
      // calculated are specific to the browser and OS configuration which we
      // don't expect to change between initialisations
      if (!DataTable.__browser) {
        var browser = {};
        DataTable.__browser = browser; // Scrolling feature / quirks detection

        var n = $$$1('<div/>').css({
          position: 'fixed',
          top: 0,
          left: $$$1(window).scrollLeft() * -1,
          // allow for scrolling
          height: 1,
          width: 1,
          overflow: 'hidden'
        }).append($$$1('<div/>').css({
          position: 'absolute',
          top: 1,
          left: 1,
          width: 100,
          overflow: 'scroll'
        }).append($$$1('<div/>').css({
          width: '100%',
          height: 10
        }))).appendTo('body');
        var outer = n.children();
        var inner = outer.children(); // Numbers below, in order, are:
        // inner.offsetWidth, inner.clientWidth, outer.offsetWidth, outer.clientWidth
        //
        // IE6 XP:                           100 100 100  83
        // IE7 Vista:                        100 100 100  83
        // IE 8+ Windows:                     83  83 100  83
        // Evergreen Windows:                 83  83 100  83
        // Evergreen Mac with scrollbars:     85  85 100  85
        // Evergreen Mac without scrollbars: 100 100 100 100
        // Get scrollbar width

        browser.barWidth = outer[0].offsetWidth - outer[0].clientWidth; // IE6/7 will oversize a width 100% element inside a scrolling element, to
        // include the width of the scrollbar, while other browsers ensure the inner
        // element is contained without forcing scrolling

        browser.bScrollOversize = inner[0].offsetWidth === 100 && outer[0].clientWidth !== 100; // In rtl text layout, some browsers (most, but not all) will place the
        // scrollbar on the left, rather than the right.

        browser.bScrollbarLeft = Math.round(inner.offset().left) !== 1; // IE8- don't provide height and width for getBoundingClientRect

        browser.bBounding = n[0].getBoundingClientRect().width ? true : false;
        n.remove();
      }

      $$$1.extend(settings.oBrowser, DataTable.__browser);
      settings.oScroll.iBarWidth = DataTable.__browser.barWidth;
    }
    /**
     * Array.prototype reduce[Right] method, used for browsers which don't support
     * JS 1.6. Done this way to reduce code size, since we iterate either way
     *  @param {object} settings dataTables settings object
     *  @memberof DataTable#oApi
     */


    function _fnReduce(that, fn, init, start, end, inc) {
      var i = start,
          value,
          isSet = false;

      if (init !== undefined) {
        value = init;
        isSet = true;
      }

      while (i !== end) {
        if (!that.hasOwnProperty(i)) {
          continue;
        }

        value = isSet ? fn(value, that[i], i, that) : that[i];
        isSet = true;
        i += inc;
      }

      return value;
    }
    /**
     * Add a column to the list used for the table with default values
     *  @param {object} oSettings dataTables settings object
     *  @param {node} nTh The th element for this column
     *  @memberof DataTable#oApi
     */


    function _fnAddColumn(oSettings, nTh) {
      // Add column to aoColumns array
      var oDefaults = DataTable.defaults.column;
      var iCol = oSettings.aoColumns.length;
      var oCol = $$$1.extend({}, DataTable.models.oColumn, oDefaults, {
        "nTh": nTh ? nTh : document.createElement('th'),
        "sTitle": oDefaults.sTitle ? oDefaults.sTitle : nTh ? nTh.innerHTML : '',
        "aDataSort": oDefaults.aDataSort ? oDefaults.aDataSort : [iCol],
        "mData": oDefaults.mData ? oDefaults.mData : iCol,
        idx: iCol
      });
      oSettings.aoColumns.push(oCol); // Add search object for column specific search. Note that the `searchCols[ iCol ]`
      // passed into extend can be undefined. This allows the user to give a default
      // with only some of the parameters defined, and also not give a default

      var searchCols = oSettings.aoPreSearchCols;
      searchCols[iCol] = $$$1.extend({}, DataTable.models.oSearch, searchCols[iCol]); // Use the default column options function to initialise classes etc

      _fnColumnOptions(oSettings, iCol, $$$1(nTh).data());
    }
    /**
     * Apply options for a column
     *  @param {object} oSettings dataTables settings object
     *  @param {int} iCol column index to consider
     *  @param {object} oOptions object with sType, bVisible and bSearchable etc
     *  @memberof DataTable#oApi
     */


    function _fnColumnOptions(oSettings, iCol, oOptions) {
      var oCol = oSettings.aoColumns[iCol];
      var oClasses = oSettings.oClasses;
      var th = $$$1(oCol.nTh); // Try to get width information from the DOM. We can't get it from CSS
      // as we'd need to parse the CSS stylesheet. `width` option can override

      if (!oCol.sWidthOrig) {
        // Width attribute
        oCol.sWidthOrig = th.attr('width') || null; // Style attribute

        var t = (th.attr('style') || '').match(/width:\s*(\d+[pxem%]+)/);

        if (t) {
          oCol.sWidthOrig = t[1];
        }
      }
      /* User specified column options */


      if (oOptions !== undefined && oOptions !== null) {
        // Backwards compatibility
        _fnCompatCols(oOptions); // Map camel case parameters to their Hungarian counterparts


        _fnCamelToHungarian(DataTable.defaults.column, oOptions);
        /* Backwards compatibility for mDataProp */


        if (oOptions.mDataProp !== undefined && !oOptions.mData) {
          oOptions.mData = oOptions.mDataProp;
        }

        if (oOptions.sType) {
          oCol._sManualType = oOptions.sType;
        } // `class` is a reserved word in Javascript, so we need to provide
        // the ability to use a valid name for the camel case input


        if (oOptions.className && !oOptions.sClass) {
          oOptions.sClass = oOptions.className;
        }

        if (oOptions.sClass) {
          th.addClass(oOptions.sClass);
        }

        $$$1.extend(oCol, oOptions);

        _fnMap(oCol, oOptions, "sWidth", "sWidthOrig");
        /* iDataSort to be applied (backwards compatibility), but aDataSort will take
         * priority if defined
         */


        if (oOptions.iDataSort !== undefined) {
          oCol.aDataSort = [oOptions.iDataSort];
        }

        _fnMap(oCol, oOptions, "aDataSort");
      }
      /* Cache the data get and set functions for speed */


      var mDataSrc = oCol.mData;

      var mData = _fnGetObjectDataFn(mDataSrc);

      var mRender = oCol.mRender ? _fnGetObjectDataFn(oCol.mRender) : null;

      var attrTest = function attrTest(src) {
        return typeof src === 'string' && src.indexOf('@') !== -1;
      };

      oCol._bAttrSrc = $$$1.isPlainObject(mDataSrc) && (attrTest(mDataSrc.sort) || attrTest(mDataSrc.type) || attrTest(mDataSrc.filter));
      oCol._setter = null;

      oCol.fnGetData = function (rowData, type, meta) {
        var innerData = mData(rowData, type, undefined, meta);
        return mRender && type ? mRender(innerData, type, rowData, meta) : innerData;
      };

      oCol.fnSetData = function (rowData, val, meta) {
        return _fnSetObjectDataFn(mDataSrc)(rowData, val, meta);
      }; // Indicate if DataTables should read DOM data as an object or array
      // Used in _fnGetRowElements


      if (typeof mDataSrc !== 'number') {
        oSettings._rowReadObject = true;
      }
      /* Feature sorting overrides column specific when off */


      if (!oSettings.oFeatures.bSort) {
        oCol.bSortable = false;
        th.addClass(oClasses.sSortableNone); // Have to add class here as order event isn't called
      }
      /* Check that the class assignment is correct for sorting */


      var bAsc = $$$1.inArray('asc', oCol.asSorting) !== -1;
      var bDesc = $$$1.inArray('desc', oCol.asSorting) !== -1;

      if (!oCol.bSortable || !bAsc && !bDesc) {
        oCol.sSortingClass = oClasses.sSortableNone;
        oCol.sSortingClassJUI = "";
      } else if (bAsc && !bDesc) {
        oCol.sSortingClass = oClasses.sSortableAsc;
        oCol.sSortingClassJUI = oClasses.sSortJUIAscAllowed;
      } else if (!bAsc && bDesc) {
        oCol.sSortingClass = oClasses.sSortableDesc;
        oCol.sSortingClassJUI = oClasses.sSortJUIDescAllowed;
      } else {
        oCol.sSortingClass = oClasses.sSortable;
        oCol.sSortingClassJUI = oClasses.sSortJUI;
      }
    }
    /**
     * Adjust the table column widths for new data. Note: you would probably want to
     * do a redraw after calling this function!
     *  @param {object} settings dataTables settings object
     *  @memberof DataTable#oApi
     */


    function _fnAdjustColumnSizing(settings) {
      /* Not interested in doing column width calculation if auto-width is disabled */
      if (settings.oFeatures.bAutoWidth !== false) {
        var columns = settings.aoColumns;

        _fnCalculateColumnWidths(settings);

        for (var i = 0, iLen = columns.length; i < iLen; i++) {
          columns[i].nTh.style.width = columns[i].sWidth;
        }
      }

      var scroll = settings.oScroll;

      if (scroll.sY !== '' || scroll.sX !== '') {
        _fnScrollDraw(settings);
      }

      _fnCallbackFire(settings, null, 'column-sizing', [settings]);
    }
    /**
     * Covert the index of a visible column to the index in the data array (take account
     * of hidden columns)
     *  @param {object} oSettings dataTables settings object
     *  @param {int} iMatch Visible column index to lookup
     *  @returns {int} i the data index
     *  @memberof DataTable#oApi
     */


    function _fnVisibleToColumnIndex(oSettings, iMatch) {
      var aiVis = _fnGetColumns(oSettings, 'bVisible');

      return typeof aiVis[iMatch] === 'number' ? aiVis[iMatch] : null;
    }
    /**
     * Covert the index of an index in the data array and convert it to the visible
     *   column index (take account of hidden columns)
     *  @param {int} iMatch Column index to lookup
     *  @param {object} oSettings dataTables settings object
     *  @returns {int} i the data index
     *  @memberof DataTable#oApi
     */


    function _fnColumnIndexToVisible(oSettings, iMatch) {
      var aiVis = _fnGetColumns(oSettings, 'bVisible');

      var iPos = $$$1.inArray(iMatch, aiVis);
      return iPos !== -1 ? iPos : null;
    }
    /**
     * Get the number of visible columns
     *  @param {object} oSettings dataTables settings object
     *  @returns {int} i the number of visible columns
     *  @memberof DataTable#oApi
     */


    function _fnVisbleColumns(oSettings) {
      var vis = 0; // No reduce in IE8, use a loop for now

      $$$1.each(oSettings.aoColumns, function (i, col) {
        if (col.bVisible && $$$1(col.nTh).css('display') !== 'none') {
          vis++;
        }
      });
      return vis;
    }
    /**
     * Get an array of column indexes that match a given property
     *  @param {object} oSettings dataTables settings object
     *  @param {string} sParam Parameter in aoColumns to look for - typically
     *    bVisible or bSearchable
     *  @returns {array} Array of indexes with matched properties
     *  @memberof DataTable#oApi
     */


    function _fnGetColumns(oSettings, sParam) {
      var a = [];
      $$$1.map(oSettings.aoColumns, function (val, i) {
        if (val[sParam]) {
          a.push(i);
        }
      });
      return a;
    }
    /**
     * Calculate the 'type' of a column
     *  @param {object} settings dataTables settings object
     *  @memberof DataTable#oApi
     */


    function _fnColumnTypes(settings) {
      var columns = settings.aoColumns;
      var data = settings.aoData;
      var types = DataTable.ext.type.detect;
      var i, ien, j, jen, k, ken;
      var col, detectedType, cache; // For each column, spin over the 

      for (i = 0, ien = columns.length; i < ien; i++) {
        col = columns[i];
        cache = [];

        if (!col.sType && col._sManualType) {
          col.sType = col._sManualType;
        } else if (!col.sType) {
          for (j = 0, jen = types.length; j < jen; j++) {
            for (k = 0, ken = data.length; k < ken; k++) {
              // Use a cache array so we only need to get the type data
              // from the formatter once (when using multiple detectors)
              if (cache[k] === undefined) {
                cache[k] = _fnGetCellData(settings, k, i, 'type');
              }

              detectedType = types[j](cache[k], settings); // If null, then this type can't apply to this column, so
              // rather than testing all cells, break out. There is an
              // exception for the last type which is `html`. We need to
              // scan all rows since it is possible to mix string and HTML
              // types

              if (!detectedType && j !== types.length - 1) {
                break;
              } // Only a single match is needed for html type since it is
              // bottom of the pile and very similar to string


              if (detectedType === 'html') {
                break;
              }
            } // Type is valid for all data points in the column - use this
            // type


            if (detectedType) {
              col.sType = detectedType;
              break;
            }
          } // Fall back - if no type was detected, always use string


          if (!col.sType) {
            col.sType = 'string';
          }
        }
      }
    }
    /**
     * Take the column definitions and static columns arrays and calculate how
     * they relate to column indexes. The callback function will then apply the
     * definition found for a column to a suitable configuration object.
     *  @param {object} oSettings dataTables settings object
     *  @param {array} aoColDefs The aoColumnDefs array that is to be applied
     *  @param {array} aoCols The aoColumns array that defines columns individually
     *  @param {function} fn Callback function - takes two parameters, the calculated
     *    column index and the definition for that column.
     *  @memberof DataTable#oApi
     */


    function _fnApplyColumnDefs(oSettings, aoColDefs, aoCols, fn) {
      var i, iLen, j, jLen, k, kLen, def;
      var columns = oSettings.aoColumns; // Column definitions with aTargets

      if (aoColDefs) {
        /* Loop over the definitions array - loop in reverse so first instance has priority */
        for (i = aoColDefs.length - 1; i >= 0; i--) {
          def = aoColDefs[i];
          /* Each definition can target multiple columns, as it is an array */

          var aTargets = def.targets !== undefined ? def.targets : def.aTargets;

          if (!$$$1.isArray(aTargets)) {
            aTargets = [aTargets];
          }

          for (j = 0, jLen = aTargets.length; j < jLen; j++) {
            if (typeof aTargets[j] === 'number' && aTargets[j] >= 0) {
              /* Add columns that we don't yet know about */
              while (columns.length <= aTargets[j]) {
                _fnAddColumn(oSettings);
              }
              /* Integer, basic index */


              fn(aTargets[j], def);
            } else if (typeof aTargets[j] === 'number' && aTargets[j] < 0) {
              /* Negative integer, right to left column counting */
              fn(columns.length + aTargets[j], def);
            } else if (typeof aTargets[j] === 'string') {
              /* Class name matching on TH element */
              for (k = 0, kLen = columns.length; k < kLen; k++) {
                if (aTargets[j] == "_all" || $$$1(columns[k].nTh).hasClass(aTargets[j])) {
                  fn(k, def);
                }
              }
            }
          }
        }
      } // Statically defined columns array


      if (aoCols) {
        for (i = 0, iLen = aoCols.length; i < iLen; i++) {
          fn(i, aoCols[i]);
        }
      }
    }
    /**
     * Add a data array to the table, creating DOM node etc. This is the parallel to
     * _fnGatherData, but for adding rows from a Javascript source, rather than a
     * DOM source.
     *  @param {object} oSettings dataTables settings object
     *  @param {array} aData data array to be added
     *  @param {node} [nTr] TR element to add to the table - optional. If not given,
     *    DataTables will create a row automatically
     *  @param {array} [anTds] Array of TD|TH elements for the row - must be given
     *    if nTr is.
     *  @returns {int} >=0 if successful (index of new aoData entry), -1 if failed
     *  @memberof DataTable#oApi
     */


    function _fnAddData(oSettings, aDataIn, nTr, anTds) {
      /* Create the object for storing information about this new row */
      var iRow = oSettings.aoData.length;
      var oData = $$$1.extend(true, {}, DataTable.models.oRow, {
        src: nTr ? 'dom' : 'data',
        idx: iRow
      });
      oData._aData = aDataIn;
      oSettings.aoData.push(oData);
      var columns = oSettings.aoColumns; // Invalidate the column types as the new data needs to be revalidated

      for (var i = 0, iLen = columns.length; i < iLen; i++) {
        columns[i].sType = null;
      }
      /* Add to the display array */


      oSettings.aiDisplayMaster.push(iRow);
      var id = oSettings.rowIdFn(aDataIn);

      if (id !== undefined) {
        oSettings.aIds[id] = oData;
      }
      /* Create the DOM information, or register it if already present */


      if (nTr || !oSettings.oFeatures.bDeferRender) {
        _fnCreateTr(oSettings, iRow, nTr, anTds);
      }

      return iRow;
    }
    /**
     * Add one or more TR elements to the table. Generally we'd expect to
     * use this for reading data from a DOM sourced table, but it could be
     * used for an TR element. Note that if a TR is given, it is used (i.e.
     * it is not cloned).
     *  @param {object} settings dataTables settings object
     *  @param {array|node|jQuery} trs The TR element(s) to add to the table
     *  @returns {array} Array of indexes for the added rows
     *  @memberof DataTable#oApi
     */


    function _fnAddTr(settings, trs) {
      var row; // Allow an individual node to be passed in

      if (!(trs instanceof $$$1)) {
        trs = $$$1(trs);
      }

      return trs.map(function (i, el) {
        row = _fnGetRowElements(settings, el);
        return _fnAddData(settings, row.data, el, row.cells);
      });
    }
    /**
     * Take a TR element and convert it to an index in aoData
     *  @param {object} oSettings dataTables settings object
     *  @param {node} n the TR element to find
     *  @returns {int} index if the node is found, null if not
     *  @memberof DataTable#oApi
     */


    function _fnNodeToDataIndex(oSettings, n) {
      return n._DT_RowIndex !== undefined ? n._DT_RowIndex : null;
    }
    /**
     * Take a TD element and convert it into a column data index (not the visible index)
     *  @param {object} oSettings dataTables settings object
     *  @param {int} iRow The row number the TD/TH can be found in
     *  @param {node} n The TD/TH element to find
     *  @returns {int} index if the node is found, -1 if not
     *  @memberof DataTable#oApi
     */


    function _fnNodeToColumnIndex(oSettings, iRow, n) {
      return $$$1.inArray(n, oSettings.aoData[iRow].anCells);
    }
    /**
     * Get the data for a given cell from the internal cache, taking into account data mapping
     *  @param {object} settings dataTables settings object
     *  @param {int} rowIdx aoData row id
     *  @param {int} colIdx Column index
     *  @param {string} type data get type ('display', 'type' 'filter' 'sort')
     *  @returns {*} Cell data
     *  @memberof DataTable#oApi
     */


    function _fnGetCellData(settings, rowIdx, colIdx, type) {
      var draw = settings.iDraw;
      var col = settings.aoColumns[colIdx];
      var rowData = settings.aoData[rowIdx]._aData;
      var defaultContent = col.sDefaultContent;
      var cellData = col.fnGetData(rowData, type, {
        settings: settings,
        row: rowIdx,
        col: colIdx
      });

      if (cellData === undefined) {
        if (settings.iDrawError != draw && defaultContent === null) {
          _fnLog(settings, 0, "Requested unknown parameter " + (typeof col.mData == 'function' ? '{function}' : "'" + col.mData + "'") + " for row " + rowIdx + ", column " + colIdx, 4);

          settings.iDrawError = draw;
        }

        return defaultContent;
      } // When the data source is null and a specific data type is requested (i.e.
      // not the original data), we can use default column data


      if ((cellData === rowData || cellData === null) && defaultContent !== null && type !== undefined) {
        cellData = defaultContent;
      } else if (typeof cellData === 'function') {
        // If the data source is a function, then we run it and use the return,
        // executing in the scope of the data object (for instances)
        return cellData.call(rowData);
      }

      if (cellData === null && type == 'display') {
        return '';
      }

      return cellData;
    }
    /**
     * Set the value for a specific cell, into the internal data cache
     *  @param {object} settings dataTables settings object
     *  @param {int} rowIdx aoData row id
     *  @param {int} colIdx Column index
     *  @param {*} val Value to set
     *  @memberof DataTable#oApi
     */


    function _fnSetCellData(settings, rowIdx, colIdx, val) {
      var col = settings.aoColumns[colIdx];
      var rowData = settings.aoData[rowIdx]._aData;
      col.fnSetData(rowData, val, {
        settings: settings,
        row: rowIdx,
        col: colIdx
      });
    } // Private variable that is used to match action syntax in the data property object


    var __reArray = /\[.*?\]$/;
    var __reFn = /\(\)$/;
    /**
     * Split string on periods, taking into account escaped periods
     * @param  {string} str String to split
     * @return {array} Split string
     */

    function _fnSplitObjNotation(str) {
      return $$$1.map(str.match(/(\\.|[^\.])+/g) || [''], function (s) {
        return s.replace(/\\\./g, '.');
      });
    }
    /**
     * Return a function that can be used to get data from a source object, taking
     * into account the ability to use nested objects as a source
     *  @param {string|int|function} mSource The data source for the object
     *  @returns {function} Data get function
     *  @memberof DataTable#oApi
     */


    function _fnGetObjectDataFn(mSource) {
      if ($$$1.isPlainObject(mSource)) {
        /* Build an object of get functions, and wrap them in a single call */
        var o = {};
        $$$1.each(mSource, function (key, val) {
          if (val) {
            o[key] = _fnGetObjectDataFn(val);
          }
        });
        return function (data, type, row, meta) {
          var t = o[type] || o._;
          return t !== undefined ? t(data, type, row, meta) : data;
        };
      } else if (mSource === null) {
        /* Give an empty string for rendering / sorting etc */
        return function (data) {
          // type, row and meta also passed, but not used
          return data;
        };
      } else if (typeof mSource === 'function') {
        return function (data, type, row, meta) {
          return mSource(data, type, row, meta);
        };
      } else if (typeof mSource === 'string' && (mSource.indexOf('.') !== -1 || mSource.indexOf('[') !== -1 || mSource.indexOf('(') !== -1)) {
        /* If there is a . in the source string then the data source is in a
         * nested object so we loop over the data for each level to get the next
         * level down. On each loop we test for undefined, and if found immediately
         * return. This allows entire objects to be missing and sDefaultContent to
         * be used if defined, rather than throwing an error
         */
        var fetchData = function fetchData(data, type, src) {
          var arrayNotation, funcNotation, out, innerSrc;

          if (src !== "") {
            var a = _fnSplitObjNotation(src);

            for (var i = 0, iLen = a.length; i < iLen; i++) {
              // Check if we are dealing with special notation
              arrayNotation = a[i].match(__reArray);
              funcNotation = a[i].match(__reFn);

              if (arrayNotation) {
                // Array notation
                a[i] = a[i].replace(__reArray, ''); // Condition allows simply [] to be passed in

                if (a[i] !== "") {
                  data = data[a[i]];
                }

                out = []; // Get the remainder of the nested object to get

                a.splice(0, i + 1);
                innerSrc = a.join('.'); // Traverse each entry in the array getting the properties requested

                if ($$$1.isArray(data)) {
                  for (var j = 0, jLen = data.length; j < jLen; j++) {
                    out.push(fetchData(data[j], type, innerSrc));
                  }
                } // If a string is given in between the array notation indicators, that
                // is used to join the strings together, otherwise an array is returned


                var join = arrayNotation[0].substring(1, arrayNotation[0].length - 1);
                data = join === "" ? out : out.join(join); // The inner call to fetchData has already traversed through the remainder
                // of the source requested, so we exit from the loop

                break;
              } else if (funcNotation) {
                // Function call
                a[i] = a[i].replace(__reFn, '');
                data = data[a[i]]();
                continue;
              }

              if (data === null || data[a[i]] === undefined) {
                return undefined;
              }

              data = data[a[i]];
            }
          }

          return data;
        };

        return function (data, type) {
          // row and meta also passed, but not used
          return fetchData(data, type, mSource);
        };
      } else {
        /* Array or flat object mapping */
        return function (data, type) {
          // row and meta also passed, but not used
          return data[mSource];
        };
      }
    }
    /**
     * Return a function that can be used to set data from a source object, taking
     * into account the ability to use nested objects as a source
     *  @param {string|int|function} mSource The data source for the object
     *  @returns {function} Data set function
     *  @memberof DataTable#oApi
     */


    function _fnSetObjectDataFn(mSource) {
      if ($$$1.isPlainObject(mSource)) {
        /* Unlike get, only the underscore (global) option is used for for
         * setting data since we don't know the type here. This is why an object
         * option is not documented for `mData` (which is read/write), but it is
         * for `mRender` which is read only.
         */
        return _fnSetObjectDataFn(mSource._);
      } else if (mSource === null) {
        /* Nothing to do when the data source is null */
        return function () {};
      } else if (typeof mSource === 'function') {
        return function (data, val, meta) {
          mSource(data, 'set', val, meta);
        };
      } else if (typeof mSource === 'string' && (mSource.indexOf('.') !== -1 || mSource.indexOf('[') !== -1 || mSource.indexOf('(') !== -1)) {
        /* Like the get, we need to get data from a nested object */
        var setData = function setData(data, val, src) {
          var a = _fnSplitObjNotation(src),
              b;

          var aLast = a[a.length - 1];
          var arrayNotation, funcNotation, o, innerSrc;

          for (var i = 0, iLen = a.length - 1; i < iLen; i++) {
            // Check if we are dealing with an array notation request
            arrayNotation = a[i].match(__reArray);
            funcNotation = a[i].match(__reFn);

            if (arrayNotation) {
              a[i] = a[i].replace(__reArray, '');
              data[a[i]] = []; // Get the remainder of the nested object to set so we can recurse

              b = a.slice();
              b.splice(0, i + 1);
              innerSrc = b.join('.'); // Traverse each entry in the array setting the properties requested

              if ($$$1.isArray(val)) {
                for (var j = 0, jLen = val.length; j < jLen; j++) {
                  o = {};
                  setData(o, val[j], innerSrc);
                  data[a[i]].push(o);
                }
              } else {
                // We've been asked to save data to an array, but it
                // isn't array data to be saved. Best that can be done
                // is to just save the value.
                data[a[i]] = val;
              } // The inner call to setData has already traversed through the remainder
              // of the source and has set the data, thus we can exit here


              return;
            } else if (funcNotation) {
              // Function call
              a[i] = a[i].replace(__reFn, '');
              data = data[a[i]](val);
            } // If the nested object doesn't currently exist - since we are
            // trying to set the value - create it


            if (data[a[i]] === null || data[a[i]] === undefined) {
              data[a[i]] = {};
            }

            data = data[a[i]];
          } // Last item in the input - i.e, the actual set


          if (aLast.match(__reFn)) {
            // Function call
            data = data[aLast.replace(__reFn, '')](val);
          } else {
            // If array notation is used, we just want to strip it and use the property name
            // and assign the value. If it isn't used, then we get the result we want anyway
            data[aLast.replace(__reArray, '')] = val;
          }
        };

        return function (data, val) {
          // meta is also passed in, but not used
          return setData(data, val, mSource);
        };
      } else {
        /* Array or flat object mapping */
        return function (data, val) {
          // meta is also passed in, but not used
          data[mSource] = val;
        };
      }
    }
    /**
     * Return an array with the full table data
     *  @param {object} oSettings dataTables settings object
     *  @returns array {array} aData Master data array
     *  @memberof DataTable#oApi
     */


    function _fnGetDataMaster(settings) {
      return _pluck(settings.aoData, '_aData');
    }
    /**
     * Nuke the table
     *  @param {object} oSettings dataTables settings object
     *  @memberof DataTable#oApi
     */


    function _fnClearTable(settings) {
      settings.aoData.length = 0;
      settings.aiDisplayMaster.length = 0;
      settings.aiDisplay.length = 0;
      settings.aIds = {};
    }
    /**
    * Take an array of integers (index array) and remove a target integer (value - not
    * the key!)
    *  @param {array} a Index array to target
    *  @param {int} iTarget value to find
    *  @memberof DataTable#oApi
    */


    function _fnDeleteIndex(a, iTarget, splice) {
      var iTargetIndex = -1;

      for (var i = 0, iLen = a.length; i < iLen; i++) {
        if (a[i] == iTarget) {
          iTargetIndex = i;
        } else if (a[i] > iTarget) {
          a[i]--;
        }
      }

      if (iTargetIndex != -1 && splice === undefined) {
        a.splice(iTargetIndex, 1);
      }
    }
    /**
     * Mark cached data as invalid such that a re-read of the data will occur when
     * the cached data is next requested. Also update from the data source object.
     *
     * @param {object} settings DataTables settings object
     * @param {int}    rowIdx   Row index to invalidate
     * @param {string} [src]    Source to invalidate from: undefined, 'auto', 'dom'
     *     or 'data'
     * @param {int}    [colIdx] Column index to invalidate. If undefined the whole
     *     row will be invalidated
     * @memberof DataTable#oApi
     *
     * @todo For the modularisation of v1.11 this will need to become a callback, so
     *   the sort and filter methods can subscribe to it. That will required
     *   initialisation options for sorting, which is why it is not already baked in
     */


    function _fnInvalidate(settings, rowIdx, src, colIdx) {
      var row = settings.aoData[rowIdx];
      var i, ien;

      var cellWrite = function cellWrite(cell, col) {
        // This is very frustrating, but in IE if you just write directly
        // to innerHTML, and elements that are overwritten are GC'ed,
        // even if there is a reference to them elsewhere
        while (cell.childNodes.length) {
          cell.removeChild(cell.firstChild);
        }

        cell.innerHTML = _fnGetCellData(settings, rowIdx, col, 'display');
      }; // Are we reading last data from DOM or the data object?


      if (src === 'dom' || (!src || src === 'auto') && row.src === 'dom') {
        // Read the data from the DOM
        row._aData = _fnGetRowElements(settings, row, colIdx, colIdx === undefined ? undefined : row._aData).data;
      } else {
        // Reading from data object, update the DOM
        var cells = row.anCells;

        if (cells) {
          if (colIdx !== undefined) {
            cellWrite(cells[colIdx], colIdx);
          } else {
            for (i = 0, ien = cells.length; i < ien; i++) {
              cellWrite(cells[i], i);
            }
          }
        }
      } // For both row and cell invalidation, the cached data for sorting and
      // filtering is nulled out


      row._aSortData = null;
      row._aFilterData = null; // Invalidate the type for a specific column (if given) or all columns since
      // the data might have changed

      var cols = settings.aoColumns;

      if (colIdx !== undefined) {
        cols[colIdx].sType = null;
      } else {
        for (i = 0, ien = cols.length; i < ien; i++) {
          cols[i].sType = null;
        } // Update DataTables special `DT_*` attributes for the row


        _fnRowAttributes(settings, row);
      }
    }
    /**
     * Build a data source object from an HTML row, reading the contents of the
     * cells that are in the row.
     *
     * @param {object} settings DataTables settings object
     * @param {node|object} TR element from which to read data or existing row
     *   object from which to re-read the data from the cells
     * @param {int} [colIdx] Optional column index
     * @param {array|object} [d] Data source object. If `colIdx` is given then this
     *   parameter should also be given and will be used to write the data into.
     *   Only the column in question will be written
     * @returns {object} Object with two parameters: `data` the data read, in
     *   document order, and `cells` and array of nodes (they can be useful to the
     *   caller, so rather than needing a second traversal to get them, just return
     *   them from here).
     * @memberof DataTable#oApi
     */


    function _fnGetRowElements(settings, row, colIdx, d) {
      var tds = [],
          td = row.firstChild,
          name,
          col,
          i = 0,
          contents,
          columns = settings.aoColumns,
          objectRead = settings._rowReadObject; // Allow the data object to be passed in, or construct

      d = d !== undefined ? d : objectRead ? {} : [];

      var attr = function attr(str, td) {
        if (typeof str === 'string') {
          var idx = str.indexOf('@');

          if (idx !== -1) {
            var attr = str.substring(idx + 1);

            var setter = _fnSetObjectDataFn(str);

            setter(d, td.getAttribute(attr));
          }
        }
      }; // Read data from a cell and store into the data object


      var cellProcess = function cellProcess(cell) {
        if (colIdx === undefined || colIdx === i) {
          col = columns[i];
          contents = $$$1.trim(cell.innerHTML);

          if (col && col._bAttrSrc) {
            var setter = _fnSetObjectDataFn(col.mData._);

            setter(d, contents);
            attr(col.mData.sort, cell);
            attr(col.mData.type, cell);
            attr(col.mData.filter, cell);
          } else {
            // Depending on the `data` option for the columns the data can
            // be read to either an object or an array.
            if (objectRead) {
              if (!col._setter) {
                // Cache the setter function
                col._setter = _fnSetObjectDataFn(col.mData);
              }

              col._setter(d, contents);
            } else {
              d[i] = contents;
            }
          }
        }

        i++;
      };

      if (td) {
        // `tr` element was passed in
        while (td) {
          name = td.nodeName.toUpperCase();

          if (name == "TD" || name == "TH") {
            cellProcess(td);
            tds.push(td);
          }

          td = td.nextSibling;
        }
      } else {
        // Existing row object passed in
        tds = row.anCells;

        for (var j = 0, jen = tds.length; j < jen; j++) {
          cellProcess(tds[j]);
        }
      } // Read the ID from the DOM if present


      var rowNode = row.firstChild ? row : row.nTr;

      if (rowNode) {
        var id = rowNode.getAttribute('id');

        if (id) {
          _fnSetObjectDataFn(settings.rowId)(d, id);
        }
      }

      return {
        data: d,
        cells: tds
      };
    }
    /**
     * Create a new TR element (and it's TD children) for a row
     *  @param {object} oSettings dataTables settings object
     *  @param {int} iRow Row to consider
     *  @param {node} [nTrIn] TR element to add to the table - optional. If not given,
     *    DataTables will create a row automatically
     *  @param {array} [anTds] Array of TD|TH elements for the row - must be given
     *    if nTr is.
     *  @memberof DataTable#oApi
     */


    function _fnCreateTr(oSettings, iRow, nTrIn, anTds) {
      var row = oSettings.aoData[iRow],
          rowData = row._aData,
          cells = [],
          nTr,
          nTd,
          oCol,
          i,
          iLen;

      if (row.nTr === null) {
        nTr = nTrIn || document.createElement('tr');
        row.nTr = nTr;
        row.anCells = cells;
        /* Use a private property on the node to allow reserve mapping from the node
         * to the aoData array for fast look up
         */

        nTr._DT_RowIndex = iRow;
        /* Special parameters can be given by the data source to be used on the row */

        _fnRowAttributes(oSettings, row);
        /* Process each column */


        for (i = 0, iLen = oSettings.aoColumns.length; i < iLen; i++) {
          oCol = oSettings.aoColumns[i];
          nTd = nTrIn ? anTds[i] : document.createElement(oCol.sCellType);
          nTd._DT_CellIndex = {
            row: iRow,
            column: i
          };
          cells.push(nTd); // Need to create the HTML if new, or if a rendering function is defined

          if ((!nTrIn || oCol.mRender || oCol.mData !== i) && (!$$$1.isPlainObject(oCol.mData) || oCol.mData._ !== i + '.display')) {
            nTd.innerHTML = _fnGetCellData(oSettings, iRow, i, 'display');
          }
          /* Add user defined class */


          if (oCol.sClass) {
            nTd.className += ' ' + oCol.sClass;
          } // Visibility - add or remove as required


          if (oCol.bVisible && !nTrIn) {
            nTr.appendChild(nTd);
          } else if (!oCol.bVisible && nTrIn) {
            nTd.parentNode.removeChild(nTd);
          }

          if (oCol.fnCreatedCell) {
            oCol.fnCreatedCell.call(oSettings.oInstance, nTd, _fnGetCellData(oSettings, iRow, i), rowData, iRow, i);
          }
        }

        _fnCallbackFire(oSettings, 'aoRowCreatedCallback', null, [nTr, rowData, iRow, cells]);
      } // Remove once webkit bug 131819 and Chromium bug 365619 have been resolved
      // and deployed


      row.nTr.setAttribute('role', 'row');
    }
    /**
     * Add attributes to a row based on the special `DT_*` parameters in a data
     * source object.
     *  @param {object} settings DataTables settings object
     *  @param {object} DataTables row object for the row to be modified
     *  @memberof DataTable#oApi
     */


    function _fnRowAttributes(settings, row) {
      var tr = row.nTr;
      var data = row._aData;

      if (tr) {
        var id = settings.rowIdFn(data);

        if (id) {
          tr.id = id;
        }

        if (data.DT_RowClass) {
          // Remove any classes added by DT_RowClass before
          var a = data.DT_RowClass.split(' ');
          row.__rowc = row.__rowc ? _unique(row.__rowc.concat(a)) : a;
          $$$1(tr).removeClass(row.__rowc.join(' ')).addClass(data.DT_RowClass);
        }

        if (data.DT_RowAttr) {
          $$$1(tr).attr(data.DT_RowAttr);
        }

        if (data.DT_RowData) {
          $$$1(tr).data(data.DT_RowData);
        }
      }
    }
    /**
     * Create the HTML header for the table
     *  @param {object} oSettings dataTables settings object
     *  @memberof DataTable#oApi
     */


    function _fnBuildHead(oSettings) {
      var i, ien, cell, row, column;
      var thead = oSettings.nTHead;
      var tfoot = oSettings.nTFoot;
      var createHeader = $$$1('th, td', thead).length === 0;
      var classes = oSettings.oClasses;
      var columns = oSettings.aoColumns;

      if (createHeader) {
        row = $$$1('<tr/>').appendTo(thead);
      }

      for (i = 0, ien = columns.length; i < ien; i++) {
        column = columns[i];
        cell = $$$1(column.nTh).addClass(column.sClass);

        if (createHeader) {
          cell.appendTo(row);
        } // 1.11 move into sorting


        if (oSettings.oFeatures.bSort) {
          cell.addClass(column.sSortingClass);

          if (column.bSortable !== false) {
            cell.attr('tabindex', oSettings.iTabIndex).attr('aria-controls', oSettings.sTableId);

            _fnSortAttachListener(oSettings, column.nTh, i);
          }
        }

        if (column.sTitle != cell[0].innerHTML) {
          cell.html(column.sTitle);
        }

        _fnRenderer(oSettings, 'header')(oSettings, cell, column, classes);
      }

      if (createHeader) {
        _fnDetectHeader(oSettings.aoHeader, thead);
      }
      /* ARIA role for the rows */


      $$$1(thead).find('>tr').attr('role', 'row');
      /* Deal with the footer - add classes if required */

      $$$1(thead).find('>tr>th, >tr>td').addClass(classes.sHeaderTH);
      $$$1(tfoot).find('>tr>th, >tr>td').addClass(classes.sFooterTH); // Cache the footer cells. Note that we only take the cells from the first
      // row in the footer. If there is more than one row the user wants to
      // interact with, they need to use the table().foot() method. Note also this
      // allows cells to be used for multiple columns using colspan

      if (tfoot !== null) {
        var cells = oSettings.aoFooter[0];

        for (i = 0, ien = cells.length; i < ien; i++) {
          column = columns[i];
          column.nTf = cells[i].cell;

          if (column.sClass) {
            $$$1(column.nTf).addClass(column.sClass);
          }
        }
      }
    }
    /**
     * Draw the header (or footer) element based on the column visibility states. The
     * methodology here is to use the layout array from _fnDetectHeader, modified for
     * the instantaneous column visibility, to construct the new layout. The grid is
     * traversed over cell at a time in a rows x columns grid fashion, although each
     * cell insert can cover multiple elements in the grid - which is tracks using the
     * aApplied array. Cell inserts in the grid will only occur where there isn't
     * already a cell in that position.
     *  @param {object} oSettings dataTables settings object
     *  @param array {objects} aoSource Layout array from _fnDetectHeader
     *  @param {boolean} [bIncludeHidden=false] If true then include the hidden columns in the calc,
     *  @memberof DataTable#oApi
     */


    function _fnDrawHead(oSettings, aoSource, bIncludeHidden) {
      var i, iLen, j, jLen, k, n, nLocalTr;
      var aoLocal = [];
      var aApplied = [];
      var iColumns = oSettings.aoColumns.length;
      var iRowspan, iColspan;

      if (!aoSource) {
        return;
      }

      if (bIncludeHidden === undefined) {
        bIncludeHidden = false;
      }
      /* Make a copy of the master layout array, but without the visible columns in it */


      for (i = 0, iLen = aoSource.length; i < iLen; i++) {
        aoLocal[i] = aoSource[i].slice();
        aoLocal[i].nTr = aoSource[i].nTr;
        /* Remove any columns which are currently hidden */

        for (j = iColumns - 1; j >= 0; j--) {
          if (!oSettings.aoColumns[j].bVisible && !bIncludeHidden) {
            aoLocal[i].splice(j, 1);
          }
        }
        /* Prep the applied array - it needs an element for each row */


        aApplied.push([]);
      }

      for (i = 0, iLen = aoLocal.length; i < iLen; i++) {
        nLocalTr = aoLocal[i].nTr;
        /* All cells are going to be replaced, so empty out the row */

        if (nLocalTr) {
          while (n = nLocalTr.firstChild) {
            nLocalTr.removeChild(n);
          }
        }

        for (j = 0, jLen = aoLocal[i].length; j < jLen; j++) {
          iRowspan = 1;
          iColspan = 1;
          /* Check to see if there is already a cell (row/colspan) covering our target
           * insert point. If there is, then there is nothing to do.
           */

          if (aApplied[i][j] === undefined) {
            nLocalTr.appendChild(aoLocal[i][j].cell);
            aApplied[i][j] = 1;
            /* Expand the cell to cover as many rows as needed */

            while (aoLocal[i + iRowspan] !== undefined && aoLocal[i][j].cell == aoLocal[i + iRowspan][j].cell) {
              aApplied[i + iRowspan][j] = 1;
              iRowspan++;
            }
            /* Expand the cell to cover as many columns as needed */


            while (aoLocal[i][j + iColspan] !== undefined && aoLocal[i][j].cell == aoLocal[i][j + iColspan].cell) {
              /* Must update the applied array over the rows for the columns */
              for (k = 0; k < iRowspan; k++) {
                aApplied[i + k][j + iColspan] = 1;
              }

              iColspan++;
            }
            /* Do the actual expansion in the DOM */


            $$$1(aoLocal[i][j].cell).attr('rowspan', iRowspan).attr('colspan', iColspan);
          }
        }
      }
    }
    /**
     * Insert the required TR nodes into the table for display
     *  @param {object} oSettings dataTables settings object
     *  @memberof DataTable#oApi
     */


    function _fnDraw(oSettings) {
      /* Provide a pre-callback function which can be used to cancel the draw is false is returned */
      var aPreDraw = _fnCallbackFire(oSettings, 'aoPreDrawCallback', 'preDraw', [oSettings]);

      if ($$$1.inArray(false, aPreDraw) !== -1) {
        _fnProcessingDisplay(oSettings, false);

        return;
      }
      var anRows = [];
      var iRowCount = 0;
      var asStripeClasses = oSettings.asStripeClasses;
      var iStripes = asStripeClasses.length;
      var iOpenRows = oSettings.aoOpenRows.length;
      var oLang = oSettings.oLanguage;
      var iInitDisplayStart = oSettings.iInitDisplayStart;
      var bServerSide = _fnDataSource(oSettings) == 'ssp';
      var aiDisplay = oSettings.aiDisplay;
      oSettings.bDrawing = true;
      /* Check and see if we have an initial draw position from state saving */

      if (iInitDisplayStart !== undefined && iInitDisplayStart !== -1) {
        oSettings._iDisplayStart = bServerSide ? iInitDisplayStart : iInitDisplayStart >= oSettings.fnRecordsDisplay() ? 0 : iInitDisplayStart;
        oSettings.iInitDisplayStart = -1;
      }

      var iDisplayStart = oSettings._iDisplayStart;
      var iDisplayEnd = oSettings.fnDisplayEnd();
      /* Server-side processing draw intercept */

      if (oSettings.bDeferLoading) {
        oSettings.bDeferLoading = false;
        oSettings.iDraw++;

        _fnProcessingDisplay(oSettings, false);
      } else if (!bServerSide) {
        oSettings.iDraw++;
      } else if (!oSettings.bDestroying && !_fnAjaxUpdate(oSettings)) {
        return;
      }

      if (aiDisplay.length !== 0) {
        var iStart = bServerSide ? 0 : iDisplayStart;
        var iEnd = bServerSide ? oSettings.aoData.length : iDisplayEnd;

        for (var j = iStart; j < iEnd; j++) {
          var iDataIndex = aiDisplay[j];
          var aoData = oSettings.aoData[iDataIndex];

          if (aoData.nTr === null) {
            _fnCreateTr(oSettings, iDataIndex);
          }

          var nRow = aoData.nTr;
          /* Remove the old striping classes and then add the new one */

          if (iStripes !== 0) {
            var sStripe = asStripeClasses[iRowCount % iStripes];

            if (aoData._sRowStripe != sStripe) {
              $$$1(nRow).removeClass(aoData._sRowStripe).addClass(sStripe);
              aoData._sRowStripe = sStripe;
            }
          } // Row callback functions - might want to manipulate the row
          // iRowCount and j are not currently documented. Are they at all
          // useful?


          _fnCallbackFire(oSettings, 'aoRowCallback', null, [nRow, aoData._aData, iRowCount, j, iDataIndex]);

          anRows.push(nRow);
          iRowCount++;
        }
      } else {
        /* Table is empty - create a row with an empty message in it */
        var sZero = oLang.sZeroRecords;

        if (oSettings.iDraw == 1 && _fnDataSource(oSettings) == 'ajax') {
          sZero = oLang.sLoadingRecords;
        } else if (oLang.sEmptyTable && oSettings.fnRecordsTotal() === 0) {
          sZero = oLang.sEmptyTable;
        }

        anRows[0] = $$$1('<tr/>', {
          'class': iStripes ? asStripeClasses[0] : ''
        }).append($$$1('<td />', {
          'valign': 'top',
          'colSpan': _fnVisbleColumns(oSettings),
          'class': oSettings.oClasses.sRowEmpty
        }).html(sZero))[0];
      }
      /* Header and footer callbacks */


      _fnCallbackFire(oSettings, 'aoHeaderCallback', 'header', [$$$1(oSettings.nTHead).children('tr')[0], _fnGetDataMaster(oSettings), iDisplayStart, iDisplayEnd, aiDisplay]);

      _fnCallbackFire(oSettings, 'aoFooterCallback', 'footer', [$$$1(oSettings.nTFoot).children('tr')[0], _fnGetDataMaster(oSettings), iDisplayStart, iDisplayEnd, aiDisplay]);

      var body = $$$1(oSettings.nTBody);
      body.children().detach();
      body.append($$$1(anRows));
      /* Call all required callback functions for the end of a draw */

      _fnCallbackFire(oSettings, 'aoDrawCallback', 'draw', [oSettings]);
      /* Draw is complete, sorting and filtering must be as well */


      oSettings.bSorted = false;
      oSettings.bFiltered = false;
      oSettings.bDrawing = false;
    }
    /**
     * Redraw the table - taking account of the various features which are enabled
     *  @param {object} oSettings dataTables settings object
     *  @param {boolean} [holdPosition] Keep the current paging position. By default
     *    the paging is reset to the first page
     *  @memberof DataTable#oApi
     */


    function _fnReDraw(settings, holdPosition) {
      var features = settings.oFeatures,
          sort = features.bSort,
          filter = features.bFilter;

      if (sort) {
        _fnSort(settings);
      }

      if (filter) {
        _fnFilterComplete(settings, settings.oPreviousSearch);
      } else {
        // No filtering, so we want to just use the display master
        settings.aiDisplay = settings.aiDisplayMaster.slice();
      }

      if (holdPosition !== true) {
        settings._iDisplayStart = 0;
      } // Let any modules know about the draw hold position state (used by
      // scrolling internally)


      settings._drawHold = holdPosition;

      _fnDraw(settings);

      settings._drawHold = false;
    }
    /**
     * Add the options to the page HTML for the table
     *  @param {object} oSettings dataTables settings object
     *  @memberof DataTable#oApi
     */


    function _fnAddOptionsHtml(oSettings) {
      var classes = oSettings.oClasses;
      var table = $$$1(oSettings.nTable);
      var holding = $$$1('<div/>').insertBefore(table); // Holding element for speed

      var features = oSettings.oFeatures; // All DataTables are wrapped in a div

      var insert = $$$1('<div/>', {
        id: oSettings.sTableId + '_wrapper',
        'class': classes.sWrapper + (oSettings.nTFoot ? '' : ' ' + classes.sNoFooter)
      });
      oSettings.nHolding = holding[0];
      oSettings.nTableWrapper = insert[0];
      oSettings.nTableReinsertBefore = oSettings.nTable.nextSibling;
      /* Loop over the user set positioning and place the elements as needed */

      var aDom = oSettings.sDom.split('');
      var featureNode, cOption, nNewNode, cNext, sAttr, j;

      for (var i = 0; i < aDom.length; i++) {
        featureNode = null;
        cOption = aDom[i];

        if (cOption == '<') {
          /* New container div */
          nNewNode = $$$1('<div/>')[0];
          /* Check to see if we should append an id and/or a class name to the container */

          cNext = aDom[i + 1];

          if (cNext == "'" || cNext == '"') {
            sAttr = "";
            j = 2;

            while (aDom[i + j] != cNext) {
              sAttr += aDom[i + j];
              j++;
            }
            /* Replace jQuery UI constants @todo depreciated */


            if (sAttr == "H") {
              sAttr = classes.sJUIHeader;
            } else if (sAttr == "F") {
              sAttr = classes.sJUIFooter;
            }
            /* The attribute can be in the format of "#id.class", "#id" or "class" This logic
             * breaks the string into parts and applies them as needed
             */


            if (sAttr.indexOf('.') != -1) {
              var aSplit = sAttr.split('.');
              nNewNode.id = aSplit[0].substr(1, aSplit[0].length - 1);
              nNewNode.className = aSplit[1];
            } else if (sAttr.charAt(0) == "#") {
              nNewNode.id = sAttr.substr(1, sAttr.length - 1);
            } else {
              nNewNode.className = sAttr;
            }

            i += j;
            /* Move along the position array */
          }

          insert.append(nNewNode);
          insert = $$$1(nNewNode);
        } else if (cOption == '>') {
          /* End container div */
          insert = insert.parent();
        } // @todo Move options into their own plugins?
        else if (cOption == 'l' && features.bPaginate && features.bLengthChange) {
            /* Length */
            featureNode = _fnFeatureHtmlLength(oSettings);
          } else if (cOption == 'f' && features.bFilter) {
            /* Filter */
            featureNode = _fnFeatureHtmlFilter(oSettings);
          } else if (cOption == 'r' && features.bProcessing) {
            /* pRocessing */
            featureNode = _fnFeatureHtmlProcessing(oSettings);
          } else if (cOption == 't') {
            /* Table */
            featureNode = _fnFeatureHtmlTable(oSettings);
          } else if (cOption == 'i' && features.bInfo) {
            /* Info */
            featureNode = _fnFeatureHtmlInfo(oSettings);
          } else if (cOption == 'p' && features.bPaginate) {
            /* Pagination */
            featureNode = _fnFeatureHtmlPaginate(oSettings);
          } else if (DataTable.ext.feature.length !== 0) {
            /* Plug-in features */
            var aoFeatures = DataTable.ext.feature;

            for (var k = 0, kLen = aoFeatures.length; k < kLen; k++) {
              if (cOption == aoFeatures[k].cFeature) {
                featureNode = aoFeatures[k].fnInit(oSettings);
                break;
              }
            }
          }
        /* Add to the 2D features array */


        if (featureNode) {
          var aanFeatures = oSettings.aanFeatures;

          if (!aanFeatures[cOption]) {
            aanFeatures[cOption] = [];
          }

          aanFeatures[cOption].push(featureNode);
          insert.append(featureNode);
        }
      }
      /* Built our DOM structure - replace the holding div with what we want */


      holding.replaceWith(insert);
      oSettings.nHolding = null;
    }
    /**
     * Use the DOM source to create up an array of header cells. The idea here is to
     * create a layout grid (array) of rows x columns, which contains a reference
     * to the cell that that point in the grid (regardless of col/rowspan), such that
     * any column / row could be removed and the new grid constructed
     *  @param array {object} aLayout Array to store the calculated layout in
     *  @param {node} nThead The header/footer element for the table
     *  @memberof DataTable#oApi
     */


    function _fnDetectHeader(aLayout, nThead) {
      var nTrs = $$$1(nThead).children('tr');
      var nTr, nCell;
      var i, k, l, iLen, iColShifted, iColumn, iColspan, iRowspan;
      var bUnique;

      var fnShiftCol = function fnShiftCol(a, i, j) {
        var k = a[i];

        while (k[j]) {
          j++;
        }

        return j;
      };

      aLayout.splice(0, aLayout.length);
      /* We know how many rows there are in the layout - so prep it */

      for (i = 0, iLen = nTrs.length; i < iLen; i++) {
        aLayout.push([]);
      }
      /* Calculate a layout array */


      for (i = 0, iLen = nTrs.length; i < iLen; i++) {
        nTr = nTrs[i];
        iColumn = 0;
        /* For every cell in the row... */

        nCell = nTr.firstChild;

        while (nCell) {
          if (nCell.nodeName.toUpperCase() == "TD" || nCell.nodeName.toUpperCase() == "TH") {
            /* Get the col and rowspan attributes from the DOM and sanitise them */
            iColspan = nCell.getAttribute('colspan') * 1;
            iRowspan = nCell.getAttribute('rowspan') * 1;
            iColspan = !iColspan || iColspan === 0 || iColspan === 1 ? 1 : iColspan;
            iRowspan = !iRowspan || iRowspan === 0 || iRowspan === 1 ? 1 : iRowspan;
            /* There might be colspan cells already in this row, so shift our target
             * accordingly
             */

            iColShifted = fnShiftCol(aLayout, i, iColumn);
            /* Cache calculation for unique columns */

            bUnique = iColspan === 1 ? true : false;
            /* If there is col / rowspan, copy the information into the layout grid */

            for (l = 0; l < iColspan; l++) {
              for (k = 0; k < iRowspan; k++) {
                aLayout[i + k][iColShifted + l] = {
                  "cell": nCell,
                  "unique": bUnique
                };
                aLayout[i + k].nTr = nTr;
              }
            }
          }

          nCell = nCell.nextSibling;
        }
      }
    }
    /**
     * Get an array of unique th elements, one for each column
     *  @param {object} oSettings dataTables settings object
     *  @param {node} nHeader automatically detect the layout from this node - optional
     *  @param {array} aLayout thead/tfoot layout from _fnDetectHeader - optional
     *  @returns array {node} aReturn list of unique th's
     *  @memberof DataTable#oApi
     */


    function _fnGetUniqueThs(oSettings, nHeader, aLayout) {
      var aReturn = [];

      if (!aLayout) {
        aLayout = oSettings.aoHeader;

        if (nHeader) {
          aLayout = [];

          _fnDetectHeader(aLayout, nHeader);
        }
      }

      for (var i = 0, iLen = aLayout.length; i < iLen; i++) {
        for (var j = 0, jLen = aLayout[i].length; j < jLen; j++) {
          if (aLayout[i][j].unique && (!aReturn[j] || !oSettings.bSortCellsTop)) {
            aReturn[j] = aLayout[i][j].cell;
          }
        }
      }

      return aReturn;
    }
    /**
     * Create an Ajax call based on the table's settings, taking into account that
     * parameters can have multiple forms, and backwards compatibility.
     *
     * @param {object} oSettings dataTables settings object
     * @param {array} data Data to send to the server, required by
     *     DataTables - may be augmented by developer callbacks
     * @param {function} fn Callback function to run when data is obtained
     */


    function _fnBuildAjax(oSettings, data, fn) {
      // Compatibility with 1.9-, allow fnServerData and event to manipulate
      _fnCallbackFire(oSettings, 'aoServerParams', 'serverParams', [data]); // Convert to object based for 1.10+ if using the old array scheme which can
      // come from server-side processing or serverParams


      if (data && $$$1.isArray(data)) {
        var tmp = {};
        var rbracket = /(.*?)\[\]$/;
        $$$1.each(data, function (key, val) {
          var match = val.name.match(rbracket);

          if (match) {
            // Support for arrays
            var name = match[0];

            if (!tmp[name]) {
              tmp[name] = [];
            }

            tmp[name].push(val.value);
          } else {
            tmp[val.name] = val.value;
          }
        });
        data = tmp;
      }

      var ajaxData;
      var ajax = oSettings.ajax;
      var instance = oSettings.oInstance;

      var callback = function callback(json) {
        _fnCallbackFire(oSettings, null, 'xhr', [oSettings, json, oSettings.jqXHR]);

        fn(json);
      };

      if ($$$1.isPlainObject(ajax) && ajax.data) {
        ajaxData = ajax.data;
        var newData = typeof ajaxData === 'function' ? ajaxData(data, oSettings) : // fn can manipulate data or return
        ajaxData; // an object object or array to merge
        // If the function returned something, use that alone

        data = typeof ajaxData === 'function' && newData ? newData : $$$1.extend(true, data, newData); // Remove the data property as we've resolved it already and don't want
        // jQuery to do it again (it is restored at the end of the function)

        delete ajax.data;
      }

      var baseAjax = {
        "data": data,
        "success": function success(json) {
          var error = json.error || json.sError;

          if (error) {
            _fnLog(oSettings, 0, error);
          }

          oSettings.json = json;
          callback(json);
        },
        "dataType": "json",
        "cache": false,
        "type": oSettings.sServerMethod,
        "error": function error(xhr, _error, thrown) {
          var ret = _fnCallbackFire(oSettings, null, 'xhr', [oSettings, null, oSettings.jqXHR]);

          if ($$$1.inArray(true, ret) === -1) {
            if (_error == "parsererror") {
              _fnLog(oSettings, 0, 'Invalid JSON response', 1);
            } else if (xhr.readyState === 4) {
              _fnLog(oSettings, 0, 'Ajax error', 7);
            }
          }

          _fnProcessingDisplay(oSettings, false);
        }
      }; // Store the data submitted for the API

      oSettings.oAjaxData = data; // Allow plug-ins and external processes to modify the data

      _fnCallbackFire(oSettings, null, 'preXhr', [oSettings, data]);

      if (oSettings.fnServerData) {
        // DataTables 1.9- compatibility
        oSettings.fnServerData.call(instance, oSettings.sAjaxSource, $$$1.map(data, function (val, key) {
          // Need to convert back to 1.9 trad format
          return {
            name: key,
            value: val
          };
        }), callback, oSettings);
      } else if (oSettings.sAjaxSource || typeof ajax === 'string') {
        // DataTables 1.9- compatibility
        oSettings.jqXHR = $$$1.ajax($$$1.extend(baseAjax, {
          url: ajax || oSettings.sAjaxSource
        }));
      } else if (typeof ajax === 'function') {
        // Is a function - let the caller define what needs to be done
        oSettings.jqXHR = ajax.call(instance, data, callback, oSettings);
      } else {
        // Object to extend the base settings
        oSettings.jqXHR = $$$1.ajax($$$1.extend(baseAjax, ajax)); // Restore for next time around

        ajax.data = ajaxData;
      }
    }
    /**
     * Update the table using an Ajax call
     *  @param {object} settings dataTables settings object
     *  @returns {boolean} Block the table drawing or not
     *  @memberof DataTable#oApi
     */


    function _fnAjaxUpdate(settings) {
      if (settings.bAjaxDataGet) {
        settings.iDraw++;

        _fnProcessingDisplay(settings, true);

        _fnBuildAjax(settings, _fnAjaxParameters(settings), function (json) {
          _fnAjaxUpdateDraw(settings, json);
        });

        return false;
      }

      return true;
    }
    /**
     * Build up the parameters in an object needed for a server-side processing
     * request. Note that this is basically done twice, is different ways - a modern
     * method which is used by default in DataTables 1.10 which uses objects and
     * arrays, or the 1.9- method with is name / value pairs. 1.9 method is used if
     * the sAjaxSource option is used in the initialisation, or the legacyAjax
     * option is set.
     *  @param {object} oSettings dataTables settings object
     *  @returns {bool} block the table drawing or not
     *  @memberof DataTable#oApi
     */


    function _fnAjaxParameters(settings) {
      var columns = settings.aoColumns,
          columnCount = columns.length,
          features = settings.oFeatures,
          preSearch = settings.oPreviousSearch,
          preColSearch = settings.aoPreSearchCols,
          i,
          data = [],
          dataProp,
          column,
          columnSearch,
          sort = _fnSortFlatten(settings),
          displayStart = settings._iDisplayStart,
          displayLength = features.bPaginate !== false ? settings._iDisplayLength : -1;

      var param = function param(name, value) {
        data.push({
          'name': name,
          'value': value
        });
      }; // DataTables 1.9- compatible method


      param('sEcho', settings.iDraw);
      param('iColumns', columnCount);
      param('sColumns', _pluck(columns, 'sName').join(','));
      param('iDisplayStart', displayStart);
      param('iDisplayLength', displayLength); // DataTables 1.10+ method

      var d = {
        draw: settings.iDraw,
        columns: [],
        order: [],
        start: displayStart,
        length: displayLength,
        search: {
          value: preSearch.sSearch,
          regex: preSearch.bRegex
        }
      };

      for (i = 0; i < columnCount; i++) {
        column = columns[i];
        columnSearch = preColSearch[i];
        dataProp = typeof column.mData == "function" ? 'function' : column.mData;
        d.columns.push({
          data: dataProp,
          name: column.sName,
          searchable: column.bSearchable,
          orderable: column.bSortable,
          search: {
            value: columnSearch.sSearch,
            regex: columnSearch.bRegex
          }
        });
        param("mDataProp_" + i, dataProp);

        if (features.bFilter) {
          param('sSearch_' + i, columnSearch.sSearch);
          param('bRegex_' + i, columnSearch.bRegex);
          param('bSearchable_' + i, column.bSearchable);
        }

        if (features.bSort) {
          param('bSortable_' + i, column.bSortable);
        }
      }

      if (features.bFilter) {
        param('sSearch', preSearch.sSearch);
        param('bRegex', preSearch.bRegex);
      }

      if (features.bSort) {
        $$$1.each(sort, function (i, val) {
          d.order.push({
            column: val.col,
            dir: val.dir
          });
          param('iSortCol_' + i, val.col);
          param('sSortDir_' + i, val.dir);
        });
        param('iSortingCols', sort.length);
      } // If the legacy.ajax parameter is null, then we automatically decide which
      // form to use, based on sAjaxSource


      var legacy = DataTable.ext.legacy.ajax;

      if (legacy === null) {
        return settings.sAjaxSource ? data : d;
      } // Otherwise, if legacy has been specified then we use that to decide on the
      // form


      return legacy ? data : d;
    }
    /**
     * Data the data from the server (nuking the old) and redraw the table
     *  @param {object} oSettings dataTables settings object
     *  @param {object} json json data return from the server.
     *  @param {string} json.sEcho Tracking flag for DataTables to match requests
     *  @param {int} json.iTotalRecords Number of records in the data set, not accounting for filtering
     *  @param {int} json.iTotalDisplayRecords Number of records in the data set, accounting for filtering
     *  @param {array} json.aaData The data to display on this page
     *  @param {string} [json.sColumns] Column ordering (sName, comma separated)
     *  @memberof DataTable#oApi
     */


    function _fnAjaxUpdateDraw(settings, json) {
      // v1.10 uses camelCase variables, while 1.9 uses Hungarian notation.
      // Support both
      var compat = function compat(old, modern) {
        return json[old] !== undefined ? json[old] : json[modern];
      };

      var data = _fnAjaxDataSrc(settings, json);

      var draw = compat('sEcho', 'draw');
      var recordsTotal = compat('iTotalRecords', 'recordsTotal');
      var recordsFiltered = compat('iTotalDisplayRecords', 'recordsFiltered');

      if (draw) {
        // Protect against out of sequence returns
        if (draw * 1 < settings.iDraw) {
          return;
        }

        settings.iDraw = draw * 1;
      }

      _fnClearTable(settings);

      settings._iRecordsTotal = parseInt(recordsTotal, 10);
      settings._iRecordsDisplay = parseInt(recordsFiltered, 10);

      for (var i = 0, ien = data.length; i < ien; i++) {
        _fnAddData(settings, data[i]);
      }

      settings.aiDisplay = settings.aiDisplayMaster.slice();
      settings.bAjaxDataGet = false;

      _fnDraw(settings);

      if (!settings._bInitComplete) {
        _fnInitComplete(settings, json);
      }

      settings.bAjaxDataGet = true;

      _fnProcessingDisplay(settings, false);
    }
    /**
     * Get the data from the JSON data source to use for drawing a table. Using
     * `_fnGetObjectDataFn` allows the data to be sourced from a property of the
     * source object, or from a processing function.
     *  @param {object} oSettings dataTables settings object
     *  @param  {object} json Data source object / array from the server
     *  @return {array} Array of data to use
     */


    function _fnAjaxDataSrc(oSettings, json) {
      var dataSrc = $$$1.isPlainObject(oSettings.ajax) && oSettings.ajax.dataSrc !== undefined ? oSettings.ajax.dataSrc : oSettings.sAjaxDataProp; // Compatibility with 1.9-.
      // Compatibility with 1.9-. In order to read from aaData, check if the
      // default has been changed, if not, check for aaData

      if (dataSrc === 'data') {
        return json.aaData || json[dataSrc];
      }

      return dataSrc !== "" ? _fnGetObjectDataFn(dataSrc)(json) : json;
    }
    /**
     * Generate the node required for filtering text
     *  @returns {node} Filter control element
     *  @param {object} oSettings dataTables settings object
     *  @memberof DataTable#oApi
     */


    function _fnFeatureHtmlFilter(settings) {
      var classes = settings.oClasses;
      var tableId = settings.sTableId;
      var language = settings.oLanguage;
      var previousSearch = settings.oPreviousSearch;
      var features = settings.aanFeatures;
      var input = '<input type="search" class="' + classes.sFilterInput + '"/>';
      var str = language.sSearch;
      str = str.match(/_INPUT_/) ? str.replace('_INPUT_', input) : str + input;
      var filter = $$$1('<div/>', {
        'id': !features.f ? tableId + '_filter' : null,
        'class': classes.sFilter
      }).append($$$1('<label/>').append(str));

      var searchFn = function searchFn() {
        /* Update all other filter input elements for the new display */
        var n = features.f;
        var val = !this.value ? "" : this.value; // mental IE8 fix :-(

        /* Now do the filter */

        if (val != previousSearch.sSearch) {
          _fnFilterComplete(settings, {
            "sSearch": val,
            "bRegex": previousSearch.bRegex,
            "bSmart": previousSearch.bSmart,
            "bCaseInsensitive": previousSearch.bCaseInsensitive
          }); // Need to redraw, without resorting


          settings._iDisplayStart = 0;

          _fnDraw(settings);
        }
      };

      var searchDelay = settings.searchDelay !== null ? settings.searchDelay : _fnDataSource(settings) === 'ssp' ? 400 : 0;
      var jqFilter = $$$1('input', filter).val(previousSearch.sSearch).attr('placeholder', language.sSearchPlaceholder).on('keyup.DT search.DT input.DT paste.DT cut.DT', searchDelay ? _fnThrottle(searchFn, searchDelay) : searchFn).on('keypress.DT', function (e) {
        /* Prevent form submission */
        if (e.keyCode == 13) {
          return false;
        }
      }).attr('aria-controls', tableId); // Update the input elements whenever the table is filtered

      $$$1(settings.nTable).on('search.dt.DT', function (ev, s) {
        if (settings === s) {
          // IE9 throws an 'unknown error' if document.activeElement is used
          // inside an iframe or frame...
          try {
            if (jqFilter[0] !== document.activeElement) {
              jqFilter.val(previousSearch.sSearch);
            }
          } catch (e) {}
        }
      });
      return filter[0];
    }
    /**
     * Filter the table using both the global filter and column based filtering
     *  @param {object} oSettings dataTables settings object
     *  @param {object} oSearch search information
     *  @param {int} [iForce] force a research of the master array (1) or not (undefined or 0)
     *  @memberof DataTable#oApi
     */


    function _fnFilterComplete(oSettings, oInput, iForce) {
      var oPrevSearch = oSettings.oPreviousSearch;
      var aoPrevSearch = oSettings.aoPreSearchCols;

      var fnSaveFilter = function fnSaveFilter(oFilter) {
        /* Save the filtering values */
        oPrevSearch.sSearch = oFilter.sSearch;
        oPrevSearch.bRegex = oFilter.bRegex;
        oPrevSearch.bSmart = oFilter.bSmart;
        oPrevSearch.bCaseInsensitive = oFilter.bCaseInsensitive;
      };

      var fnRegex = function fnRegex(o) {
        // Backwards compatibility with the bEscapeRegex option
        return o.bEscapeRegex !== undefined ? !o.bEscapeRegex : o.bRegex;
      }; // Resolve any column types that are unknown due to addition or invalidation
      // @todo As per sort - can this be moved into an event handler?


      _fnColumnTypes(oSettings);
      /* In server-side processing all filtering is done by the server, so no point hanging around here */


      if (_fnDataSource(oSettings) != 'ssp') {
        /* Global filter */
        _fnFilter(oSettings, oInput.sSearch, iForce, fnRegex(oInput), oInput.bSmart, oInput.bCaseInsensitive);

        fnSaveFilter(oInput);
        /* Now do the individual column filter */

        for (var i = 0; i < aoPrevSearch.length; i++) {
          _fnFilterColumn(oSettings, aoPrevSearch[i].sSearch, i, fnRegex(aoPrevSearch[i]), aoPrevSearch[i].bSmart, aoPrevSearch[i].bCaseInsensitive);
        }
        /* Custom filtering */


        _fnFilterCustom(oSettings);
      } else {
        fnSaveFilter(oInput);
      }
      /* Tell the draw function we have been filtering */


      oSettings.bFiltered = true;

      _fnCallbackFire(oSettings, null, 'search', [oSettings]);
    }
    /**
     * Apply custom filtering functions
     *  @param {object} oSettings dataTables settings object
     *  @memberof DataTable#oApi
     */


    function _fnFilterCustom(settings) {
      var filters = DataTable.ext.search;
      var displayRows = settings.aiDisplay;
      var row, rowIdx;

      for (var i = 0, ien = filters.length; i < ien; i++) {
        var rows = []; // Loop over each row and see if it should be included

        for (var j = 0, jen = displayRows.length; j < jen; j++) {
          rowIdx = displayRows[j];
          row = settings.aoData[rowIdx];

          if (filters[i](settings, row._aFilterData, rowIdx, row._aData, j)) {
            rows.push(rowIdx);
          }
        } // So the array reference doesn't break set the results into the
        // existing array


        displayRows.length = 0;
        $$$1.merge(displayRows, rows);
      }
    }
    /**
     * Filter the table on a per-column basis
     *  @param {object} oSettings dataTables settings object
     *  @param {string} sInput string to filter on
     *  @param {int} iColumn column to filter
     *  @param {bool} bRegex treat search string as a regular expression or not
     *  @param {bool} bSmart use smart filtering or not
     *  @param {bool} bCaseInsensitive Do case insenstive matching or not
     *  @memberof DataTable#oApi
     */


    function _fnFilterColumn(settings, searchStr, colIdx, regex, smart, caseInsensitive) {
      if (searchStr === '') {
        return;
      }

      var data;
      var out = [];
      var display = settings.aiDisplay;

      var rpSearch = _fnFilterCreateSearch(searchStr, regex, smart, caseInsensitive);

      for (var i = 0; i < display.length; i++) {
        data = settings.aoData[display[i]]._aFilterData[colIdx];

        if (rpSearch.test(data)) {
          out.push(display[i]);
        }
      }

      settings.aiDisplay = out;
    }
    /**
     * Filter the data table based on user input and draw the table
     *  @param {object} settings dataTables settings object
     *  @param {string} input string to filter on
     *  @param {int} force optional - force a research of the master array (1) or not (undefined or 0)
     *  @param {bool} regex treat as a regular expression or not
     *  @param {bool} smart perform smart filtering or not
     *  @param {bool} caseInsensitive Do case insenstive matching or not
     *  @memberof DataTable#oApi
     */


    function _fnFilter(settings, input, force, regex, smart, caseInsensitive) {
      var rpSearch = _fnFilterCreateSearch(input, regex, smart, caseInsensitive);

      var prevSearch = settings.oPreviousSearch.sSearch;
      var displayMaster = settings.aiDisplayMaster;
      var display, invalidated, i;
      var filtered = []; // Need to take account of custom filtering functions - always filter

      if (DataTable.ext.search.length !== 0) {
        force = true;
      } // Check if any of the rows were invalidated


      invalidated = _fnFilterData(settings); // If the input is blank - we just want the full data set

      if (input.length <= 0) {
        settings.aiDisplay = displayMaster.slice();
      } else {
        // New search - start from the master array
        if (invalidated || force || prevSearch.length > input.length || input.indexOf(prevSearch) !== 0 || settings.bSorted // On resort, the display master needs to be
        // re-filtered since indexes will have changed
        ) {
            settings.aiDisplay = displayMaster.slice();
          } // Search the display array


        display = settings.aiDisplay;

        for (i = 0; i < display.length; i++) {
          if (rpSearch.test(settings.aoData[display[i]]._sFilterRow)) {
            filtered.push(display[i]);
          }
        }

        settings.aiDisplay = filtered;
      }
    }
    /**
     * Build a regular expression object suitable for searching a table
     *  @param {string} sSearch string to search for
     *  @param {bool} bRegex treat as a regular expression or not
     *  @param {bool} bSmart perform smart filtering or not
     *  @param {bool} bCaseInsensitive Do case insensitive matching or not
     *  @returns {RegExp} constructed object
     *  @memberof DataTable#oApi
     */


    function _fnFilterCreateSearch(search, regex, smart, caseInsensitive) {
      search = regex ? search : _fnEscapeRegex(search);

      if (smart) {
        /* For smart filtering we want to allow the search to work regardless of
         * word order. We also want double quoted text to be preserved, so word
         * order is important - a la google. So this is what we want to
         * generate:
         * 
         * ^(?=.*?\bone\b)(?=.*?\btwo three\b)(?=.*?\bfour\b).*$
         */
        var a = $$$1.map(search.match(/"[^"]+"|[^ ]+/g) || [''], function (word) {
          if (word.charAt(0) === '"') {
            var m = word.match(/^"(.*)"$/);
            word = m ? m[1] : word;
          }

          return word.replace('"', '');
        });
        search = '^(?=.*?' + a.join(')(?=.*?') + ').*$';
      }

      return new RegExp(search, caseInsensitive ? 'i' : '');
    }
    /**
     * Escape a string such that it can be used in a regular expression
     *  @param {string} sVal string to escape
     *  @returns {string} escaped string
     *  @memberof DataTable#oApi
     */


    var _fnEscapeRegex = DataTable.util.escapeRegex;
    var __filter_div = $$$1('<div>')[0];

    var __filter_div_textContent = __filter_div.textContent !== undefined; // Update the filtering data for each row if needed (by invalidation or first run)


    function _fnFilterData(settings) {
      var columns = settings.aoColumns;
      var column;
      var i, j, ien, jen, filterData, cellData, row;
      var fomatters = DataTable.ext.type.search;
      var wasInvalidated = false;

      for (i = 0, ien = settings.aoData.length; i < ien; i++) {
        row = settings.aoData[i];

        if (!row._aFilterData) {
          filterData = [];

          for (j = 0, jen = columns.length; j < jen; j++) {
            column = columns[j];

            if (column.bSearchable) {
              cellData = _fnGetCellData(settings, i, j, 'filter');

              if (fomatters[column.sType]) {
                cellData = fomatters[column.sType](cellData);
              } // Search in DataTables 1.10 is string based. In 1.11 this
              // should be altered to also allow strict type checking.


              if (cellData === null) {
                cellData = '';
              }

              if (typeof cellData !== 'string' && cellData.toString) {
                cellData = cellData.toString();
              }
            } else {
              cellData = '';
            } // If it looks like there is an HTML entity in the string,
            // attempt to decode it so sorting works as expected. Note that
            // we could use a single line of jQuery to do this, but the DOM
            // method used here is much faster http://jsperf.com/html-decode


            if (cellData.indexOf && cellData.indexOf('&') !== -1) {
              __filter_div.innerHTML = cellData;
              cellData = __filter_div_textContent ? __filter_div.textContent : __filter_div.innerText;
            }

            if (cellData.replace) {
              cellData = cellData.replace(/[\r\n]/g, '');
            }

            filterData.push(cellData);
          }

          row._aFilterData = filterData;
          row._sFilterRow = filterData.join('  ');
          wasInvalidated = true;
        }
      }

      return wasInvalidated;
    }
    /**
     * Convert from the internal Hungarian notation to camelCase for external
     * interaction
     *  @param {object} obj Object to convert
     *  @returns {object} Inverted object
     *  @memberof DataTable#oApi
     */


    function _fnSearchToCamel(obj) {
      return {
        search: obj.sSearch,
        smart: obj.bSmart,
        regex: obj.bRegex,
        caseInsensitive: obj.bCaseInsensitive
      };
    }
    /**
     * Convert from camelCase notation to the internal Hungarian. We could use the
     * Hungarian convert function here, but this is cleaner
     *  @param {object} obj Object to convert
     *  @returns {object} Inverted object
     *  @memberof DataTable#oApi
     */


    function _fnSearchToHung(obj) {
      return {
        sSearch: obj.search,
        bSmart: obj.smart,
        bRegex: obj.regex,
        bCaseInsensitive: obj.caseInsensitive
      };
    }
    /**
     * Generate the node required for the info display
     *  @param {object} oSettings dataTables settings object
     *  @returns {node} Information element
     *  @memberof DataTable#oApi
     */


    function _fnFeatureHtmlInfo(settings) {
      var tid = settings.sTableId,
          nodes = settings.aanFeatures.i,
          n = $$$1('<div/>', {
        'class': settings.oClasses.sInfo,
        'id': !nodes ? tid + '_info' : null
      });

      if (!nodes) {
        // Update display on each draw
        settings.aoDrawCallback.push({
          "fn": _fnUpdateInfo,
          "sName": "information"
        });
        n.attr('role', 'status').attr('aria-live', 'polite'); // Table is described by our info div

        $$$1(settings.nTable).attr('aria-describedby', tid + '_info');
      }

      return n[0];
    }
    /**
     * Update the information elements in the display
     *  @param {object} settings dataTables settings object
     *  @memberof DataTable#oApi
     */


    function _fnUpdateInfo(settings) {
      /* Show information about the table */
      var nodes = settings.aanFeatures.i;

      if (nodes.length === 0) {
        return;
      }

      var lang = settings.oLanguage,
          start = settings._iDisplayStart + 1,
          end = settings.fnDisplayEnd(),
          max = settings.fnRecordsTotal(),
          total = settings.fnRecordsDisplay(),
          out = total ? lang.sInfo : lang.sInfoEmpty;

      if (total !== max) {
        /* Record set after filtering */
        out += ' ' + lang.sInfoFiltered;
      } // Convert the macros


      out += lang.sInfoPostFix;
      out = _fnInfoMacros(settings, out);
      var callback = lang.fnInfoCallback;

      if (callback !== null) {
        out = callback.call(settings.oInstance, settings, start, end, max, total, out);
      }

      $$$1(nodes).html(out);
    }

    function _fnInfoMacros(settings, str) {
      // When infinite scrolling, we are always starting at 1. _iDisplayStart is used only
      // internally
      var formatter = settings.fnFormatNumber,
          start = settings._iDisplayStart + 1,
          len = settings._iDisplayLength,
          vis = settings.fnRecordsDisplay(),
          all = len === -1;
      return str.replace(/_START_/g, formatter.call(settings, start)).replace(/_END_/g, formatter.call(settings, settings.fnDisplayEnd())).replace(/_MAX_/g, formatter.call(settings, settings.fnRecordsTotal())).replace(/_TOTAL_/g, formatter.call(settings, vis)).replace(/_PAGE_/g, formatter.call(settings, all ? 1 : Math.ceil(start / len))).replace(/_PAGES_/g, formatter.call(settings, all ? 1 : Math.ceil(vis / len)));
    }
    /**
     * Draw the table for the first time, adding all required features
     *  @param {object} settings dataTables settings object
     *  @memberof DataTable#oApi
     */


    function _fnInitialise(settings) {
      var i,
          iLen,
          iAjaxStart = settings.iInitDisplayStart;
      var columns = settings.aoColumns,
          column;
      var features = settings.oFeatures;
      var deferLoading = settings.bDeferLoading; // value modified by the draw

      /* Ensure that the table data is fully initialised */

      if (!settings.bInitialised) {
        setTimeout(function () {
          _fnInitialise(settings);
        }, 200);
        return;
      }
      /* Show the display HTML options */


      _fnAddOptionsHtml(settings);
      /* Build and draw the header / footer for the table */


      _fnBuildHead(settings);

      _fnDrawHead(settings, settings.aoHeader);

      _fnDrawHead(settings, settings.aoFooter);
      /* Okay to show that something is going on now */


      _fnProcessingDisplay(settings, true);
      /* Calculate sizes for columns */


      if (features.bAutoWidth) {
        _fnCalculateColumnWidths(settings);
      }

      for (i = 0, iLen = columns.length; i < iLen; i++) {
        column = columns[i];

        if (column.sWidth) {
          column.nTh.style.width = _fnStringToCss(column.sWidth);
        }
      }

      _fnCallbackFire(settings, null, 'preInit', [settings]); // If there is default sorting required - let's do it. The sort function
      // will do the drawing for us. Otherwise we draw the table regardless of the
      // Ajax source - this allows the table to look initialised for Ajax sourcing
      // data (show 'loading' message possibly)


      _fnReDraw(settings); // Server-side processing init complete is done by _fnAjaxUpdateDraw


      var dataSrc = _fnDataSource(settings);

      if (dataSrc != 'ssp' || deferLoading) {
        // if there is an ajax source load the data
        if (dataSrc == 'ajax') {
          _fnBuildAjax(settings, [], function (json) {
            var aData = _fnAjaxDataSrc(settings, json); // Got the data - add it to the table


            for (i = 0; i < aData.length; i++) {
              _fnAddData(settings, aData[i]);
            } // Reset the init display for cookie saving. We've already done
            // a filter, and therefore cleared it before. So we need to make
            // it appear 'fresh'


            settings.iInitDisplayStart = iAjaxStart;

            _fnReDraw(settings);

            _fnProcessingDisplay(settings, false);

            _fnInitComplete(settings, json);
          }, settings);
        } else {
          _fnProcessingDisplay(settings, false);

          _fnInitComplete(settings);
        }
      }
    }
    /**
     * Draw the table for the first time, adding all required features
     *  @param {object} oSettings dataTables settings object
     *  @param {object} [json] JSON from the server that completed the table, if using Ajax source
     *    with client-side processing (optional)
     *  @memberof DataTable#oApi
     */


    function _fnInitComplete(settings, json) {
      settings._bInitComplete = true; // When data was added after the initialisation (data or Ajax) we need to
      // calculate the column sizing

      if (json || settings.oInit.aaData) {
        _fnAdjustColumnSizing(settings);
      }

      _fnCallbackFire(settings, null, 'plugin-init', [settings, json]);

      _fnCallbackFire(settings, 'aoInitComplete', 'init', [settings, json]);
    }

    function _fnLengthChange(settings, val) {
      var len = parseInt(val, 10);
      settings._iDisplayLength = len;

      _fnLengthOverflow(settings); // Fire length change event


      _fnCallbackFire(settings, null, 'length', [settings, len]);
    }
    /**
     * Generate the node required for user display length changing
     *  @param {object} settings dataTables settings object
     *  @returns {node} Display length feature node
     *  @memberof DataTable#oApi
     */


    function _fnFeatureHtmlLength(settings) {
      var classes = settings.oClasses,
          tableId = settings.sTableId,
          menu = settings.aLengthMenu,
          d2 = $$$1.isArray(menu[0]),
          lengths = d2 ? menu[0] : menu,
          language = d2 ? menu[1] : menu;
      var select = $$$1('<select/>', {
        'name': tableId + '_length',
        'aria-controls': tableId,
        'class': classes.sLengthSelect
      });

      for (var i = 0, ien = lengths.length; i < ien; i++) {
        select[0][i] = new Option(typeof language[i] === 'number' ? settings.fnFormatNumber(language[i]) : language[i], lengths[i]);
      }

      var div = $$$1('<div><label/></div>').addClass(classes.sLength);

      if (!settings.aanFeatures.l) {
        div[0].id = tableId + '_length';
      }

      div.children().append(settings.oLanguage.sLengthMenu.replace('_MENU_', select[0].outerHTML)); // Can't use `select` variable as user might provide their own and the
      // reference is broken by the use of outerHTML

      $$$1('select', div).val(settings._iDisplayLength).on('change.DT', function (e) {
        _fnLengthChange(settings, $$$1(this).val());

        _fnDraw(settings);
      }); // Update node value whenever anything changes the table's length

      $$$1(settings.nTable).on('length.dt.DT', function (e, s, len) {
        if (settings === s) {
          $$$1('select', div).val(len);
        }
      });
      return div[0];
    }
    /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
     * Note that most of the paging logic is done in
     * DataTable.ext.pager
     */

    /**
     * Generate the node required for default pagination
     *  @param {object} oSettings dataTables settings object
     *  @returns {node} Pagination feature node
     *  @memberof DataTable#oApi
     */


    function _fnFeatureHtmlPaginate(settings) {
      var type = settings.sPaginationType,
          plugin = DataTable.ext.pager[type],
          modern = typeof plugin === 'function',
          redraw = function redraw(settings) {
        _fnDraw(settings);
      },
          node = $$$1('<div/>').addClass(settings.oClasses.sPaging + type)[0],
          features = settings.aanFeatures;

      if (!modern) {
        plugin.fnInit(settings, node, redraw);
      }
      /* Add a draw callback for the pagination on first instance, to update the paging display */


      if (!features.p) {
        node.id = settings.sTableId + '_paginate';
        settings.aoDrawCallback.push({
          "fn": function fn(settings) {
            if (modern) {
              var start = settings._iDisplayStart,
                  len = settings._iDisplayLength,
                  visRecords = settings.fnRecordsDisplay(),
                  all = len === -1,
                  page = all ? 0 : Math.ceil(start / len),
                  pages = all ? 1 : Math.ceil(visRecords / len),
                  buttons = plugin(page, pages),
                  i,
                  ien;

              for (i = 0, ien = features.p.length; i < ien; i++) {
                _fnRenderer(settings, 'pageButton')(settings, features.p[i], i, buttons, page, pages);
              }
            } else {
              plugin.fnUpdate(settings, redraw);
            }
          },
          "sName": "pagination"
        });
      }

      return node;
    }
    /**
     * Alter the display settings to change the page
     *  @param {object} settings DataTables settings object
     *  @param {string|int} action Paging action to take: "first", "previous",
     *    "next" or "last" or page number to jump to (integer)
     *  @param [bool] redraw Automatically draw the update or not
     *  @returns {bool} true page has changed, false - no change
     *  @memberof DataTable#oApi
     */


    function _fnPageChange(settings, action, redraw) {
      var start = settings._iDisplayStart,
          len = settings._iDisplayLength,
          records = settings.fnRecordsDisplay();

      if (records === 0 || len === -1) {
        start = 0;
      } else if (typeof action === "number") {
        start = action * len;

        if (start > records) {
          start = 0;
        }
      } else if (action == "first") {
        start = 0;
      } else if (action == "previous") {
        start = len >= 0 ? start - len : 0;

        if (start < 0) {
          start = 0;
        }
      } else if (action == "next") {
        if (start + len < records) {
          start += len;
        }
      } else if (action == "last") {
        start = Math.floor((records - 1) / len) * len;
      } else {
        _fnLog(settings, 0, "Unknown paging action: " + action, 5);
      }

      var changed = settings._iDisplayStart !== start;
      settings._iDisplayStart = start;

      if (changed) {
        _fnCallbackFire(settings, null, 'page', [settings]);

        if (redraw) {
          _fnDraw(settings);
        }
      }

      return changed;
    }
    /**
     * Generate the node required for the processing node
     *  @param {object} settings dataTables settings object
     *  @returns {node} Processing element
     *  @memberof DataTable#oApi
     */


    function _fnFeatureHtmlProcessing(settings) {
      return $$$1('<div/>', {
        'id': !settings.aanFeatures.r ? settings.sTableId + '_processing' : null,
        'class': settings.oClasses.sProcessing
      }).html(settings.oLanguage.sProcessing).insertBefore(settings.nTable)[0];
    }
    /**
     * Display or hide the processing indicator
     *  @param {object} settings dataTables settings object
     *  @param {bool} show Show the processing indicator (true) or not (false)
     *  @memberof DataTable#oApi
     */


    function _fnProcessingDisplay(settings, show) {
      if (settings.oFeatures.bProcessing) {
        $$$1(settings.aanFeatures.r).css('display', show ? 'block' : 'none');
      }

      _fnCallbackFire(settings, null, 'processing', [settings, show]);
    }
    /**
     * Add any control elements for the table - specifically scrolling
     *  @param {object} settings dataTables settings object
     *  @returns {node} Node to add to the DOM
     *  @memberof DataTable#oApi
     */


    function _fnFeatureHtmlTable(settings) {
      var table = $$$1(settings.nTable); // Add the ARIA grid role to the table

      table.attr('role', 'grid'); // Scrolling from here on in

      var scroll = settings.oScroll;

      if (scroll.sX === '' && scroll.sY === '') {
        return settings.nTable;
      }

      var scrollX = scroll.sX;
      var scrollY = scroll.sY;
      var classes = settings.oClasses;
      var caption = table.children('caption');
      var captionSide = caption.length ? caption[0]._captionSide : null;
      var headerClone = $$$1(table[0].cloneNode(false));
      var footerClone = $$$1(table[0].cloneNode(false));
      var footer = table.children('tfoot');
      var _div = '<div/>';

      var size = function size(s) {
        return !s ? null : _fnStringToCss(s);
      };

      if (!footer.length) {
        footer = null;
      }
      /*
       * The HTML structure that we want to generate in this function is:
       *  div - scroller
       *    div - scroll head
       *      div - scroll head inner
       *        table - scroll head table
       *          thead - thead
       *    div - scroll body
       *      table - table (master table)
       *        thead - thead clone for sizing
       *        tbody - tbody
       *    div - scroll foot
       *      div - scroll foot inner
       *        table - scroll foot table
       *          tfoot - tfoot
       */


      var scroller = $$$1(_div, {
        'class': classes.sScrollWrapper
      }).append($$$1(_div, {
        'class': classes.sScrollHead
      }).css({
        overflow: 'hidden',
        position: 'relative',
        border: 0,
        width: scrollX ? size(scrollX) : '100%'
      }).append($$$1(_div, {
        'class': classes.sScrollHeadInner
      }).css({
        'box-sizing': 'content-box',
        width: scroll.sXInner || '100%'
      }).append(headerClone.removeAttr('id').css('margin-left', 0).append(captionSide === 'top' ? caption : null).append(table.children('thead'))))).append($$$1(_div, {
        'class': classes.sScrollBody
      }).css({
        position: 'relative',
        overflow: 'auto',
        width: size(scrollX)
      }).append(table));

      if (footer) {
        scroller.append($$$1(_div, {
          'class': classes.sScrollFoot
        }).css({
          overflow: 'hidden',
          border: 0,
          width: scrollX ? size(scrollX) : '100%'
        }).append($$$1(_div, {
          'class': classes.sScrollFootInner
        }).append(footerClone.removeAttr('id').css('margin-left', 0).append(captionSide === 'bottom' ? caption : null).append(table.children('tfoot')))));
      }

      var children = scroller.children();
      var scrollHead = children[0];
      var scrollBody = children[1];
      var scrollFoot = footer ? children[2] : null; // When the body is scrolled, then we also want to scroll the headers

      if (scrollX) {
        $$$1(scrollBody).on('scroll.DT', function (e) {
          var scrollLeft = this.scrollLeft;
          scrollHead.scrollLeft = scrollLeft;

          if (footer) {
            scrollFoot.scrollLeft = scrollLeft;
          }
        });
      }

      $$$1(scrollBody).css(scrollY && scroll.bCollapse ? 'max-height' : 'height', scrollY);
      settings.nScrollHead = scrollHead;
      settings.nScrollBody = scrollBody;
      settings.nScrollFoot = scrollFoot; // On redraw - align columns

      settings.aoDrawCallback.push({
        "fn": _fnScrollDraw,
        "sName": "scrolling"
      });
      return scroller[0];
    }
    /**
     * Update the header, footer and body tables for resizing - i.e. column
     * alignment.
     *
     * Welcome to the most horrible function DataTables. The process that this
     * function follows is basically:
     *   1. Re-create the table inside the scrolling div
     *   2. Take live measurements from the DOM
     *   3. Apply the measurements to align the columns
     *   4. Clean up
     *
     *  @param {object} settings dataTables settings object
     *  @memberof DataTable#oApi
     */


    function _fnScrollDraw(settings) {
      // Given that this is such a monster function, a lot of variables are use
      // to try and keep the minimised size as small as possible
      var scroll = settings.oScroll,
          scrollX = scroll.sX,
          scrollXInner = scroll.sXInner,
          scrollY = scroll.sY,
          barWidth = scroll.iBarWidth,
          divHeader = $$$1(settings.nScrollHead),
          divHeaderStyle = divHeader[0].style,
          divHeaderInner = divHeader.children('div'),
          divHeaderInnerStyle = divHeaderInner[0].style,
          divHeaderTable = divHeaderInner.children('table'),
          divBodyEl = settings.nScrollBody,
          divBody = $$$1(divBodyEl),
          divBodyStyle = divBodyEl.style,
          divFooter = $$$1(settings.nScrollFoot),
          divFooterInner = divFooter.children('div'),
          divFooterTable = divFooterInner.children('table'),
          header = $$$1(settings.nTHead),
          table = $$$1(settings.nTable),
          tableEl = table[0],
          tableStyle = tableEl.style,
          footer = settings.nTFoot ? $$$1(settings.nTFoot) : null,
          browser = settings.oBrowser,
          ie67 = browser.bScrollOversize,
          dtHeaderCells = _pluck(settings.aoColumns, 'nTh'),
          headerTrgEls,
          footerTrgEls,
          headerSrcEls,
          footerSrcEls,
          headerCopy,
          footerCopy,
          headerWidths = [],
          footerWidths = [],
          headerContent = [],
          footerContent = [],
          idx,
          correction,
          sanityWidth,
          zeroOut = function zeroOut(nSizer) {
        var style = nSizer.style;
        style.paddingTop = "0";
        style.paddingBottom = "0";
        style.borderTopWidth = "0";
        style.borderBottomWidth = "0";
        style.height = 0;
      }; // If the scrollbar visibility has changed from the last draw, we need to
      // adjust the column sizes as the table width will have changed to account
      // for the scrollbar


      var scrollBarVis = divBodyEl.scrollHeight > divBodyEl.clientHeight;

      if (settings.scrollBarVis !== scrollBarVis && settings.scrollBarVis !== undefined) {
        settings.scrollBarVis = scrollBarVis;

        _fnAdjustColumnSizing(settings);

        return; // adjust column sizing will call this function again
      } else {
        settings.scrollBarVis = scrollBarVis;
      }
      /*
       * 1. Re-create the table inside the scrolling div
       */
      // Remove the old minimised thead and tfoot elements in the inner table


      table.children('thead, tfoot').remove();

      if (footer) {
        footerCopy = footer.clone().prependTo(table);
        footerTrgEls = footer.find('tr'); // the original tfoot is in its own table and must be sized

        footerSrcEls = footerCopy.find('tr');
      } // Clone the current header and footer elements and then place it into the inner table


      headerCopy = header.clone().prependTo(table);
      headerTrgEls = header.find('tr'); // original header is in its own table

      headerSrcEls = headerCopy.find('tr');
      headerCopy.find('th, td').removeAttr('tabindex');
      /*
       * 2. Take live measurements from the DOM - do not alter the DOM itself!
       */
      // Remove old sizing and apply the calculated column widths
      // Get the unique column headers in the newly created (cloned) header. We want to apply the
      // calculated sizes to this header

      if (!scrollX) {
        divBodyStyle.width = '100%';
        divHeader[0].style.width = '100%';
      }

      $$$1.each(_fnGetUniqueThs(settings, headerCopy), function (i, el) {
        idx = _fnVisibleToColumnIndex(settings, i);
        el.style.width = settings.aoColumns[idx].sWidth;
      });

      if (footer) {
        _fnApplyToChildren(function (n) {
          n.style.width = "";
        }, footerSrcEls);
      } // Size the table as a whole


      sanityWidth = table.outerWidth();

      if (scrollX === "") {
        // No x scrolling
        tableStyle.width = "100%"; // IE7 will make the width of the table when 100% include the scrollbar
        // - which is shouldn't. When there is a scrollbar we need to take this
        // into account.

        if (ie67 && (table.find('tbody').height() > divBodyEl.offsetHeight || divBody.css('overflow-y') == "scroll")) {
          tableStyle.width = _fnStringToCss(table.outerWidth() - barWidth);
        } // Recalculate the sanity width


        sanityWidth = table.outerWidth();
      } else if (scrollXInner !== "") {
        // legacy x scroll inner has been given - use it
        tableStyle.width = _fnStringToCss(scrollXInner); // Recalculate the sanity width

        sanityWidth = table.outerWidth();
      } // Hidden header should have zero height, so remove padding and borders. Then
      // set the width based on the real headers
      // Apply all styles in one pass


      _fnApplyToChildren(zeroOut, headerSrcEls); // Read all widths in next pass


      _fnApplyToChildren(function (nSizer) {
        headerContent.push(nSizer.innerHTML);
        headerWidths.push(_fnStringToCss($$$1(nSizer).css('width')));
      }, headerSrcEls); // Apply all widths in final pass


      _fnApplyToChildren(function (nToSize, i) {
        // Only apply widths to the DataTables detected header cells - this
        // prevents complex headers from having contradictory sizes applied
        if ($$$1.inArray(nToSize, dtHeaderCells) !== -1) {
          nToSize.style.width = headerWidths[i];
        }
      }, headerTrgEls);

      $$$1(headerSrcEls).height(0);
      /* Same again with the footer if we have one */

      if (footer) {
        _fnApplyToChildren(zeroOut, footerSrcEls);

        _fnApplyToChildren(function (nSizer) {
          footerContent.push(nSizer.innerHTML);
          footerWidths.push(_fnStringToCss($$$1(nSizer).css('width')));
        }, footerSrcEls);

        _fnApplyToChildren(function (nToSize, i) {
          nToSize.style.width = footerWidths[i];
        }, footerTrgEls);

        $$$1(footerSrcEls).height(0);
      }
      /*
       * 3. Apply the measurements
       */
      // "Hide" the header and footer that we used for the sizing. We need to keep
      // the content of the cell so that the width applied to the header and body
      // both match, but we want to hide it completely. We want to also fix their
      // width to what they currently are


      _fnApplyToChildren(function (nSizer, i) {
        nSizer.innerHTML = '<div class="dataTables_sizing">' + headerContent[i] + '</div>';
        nSizer.childNodes[0].style.height = "0";
        nSizer.childNodes[0].style.overflow = "hidden";
        nSizer.style.width = headerWidths[i];
      }, headerSrcEls);

      if (footer) {
        _fnApplyToChildren(function (nSizer, i) {
          nSizer.innerHTML = '<div class="dataTables_sizing">' + footerContent[i] + '</div>';
          nSizer.childNodes[0].style.height = "0";
          nSizer.childNodes[0].style.overflow = "hidden";
          nSizer.style.width = footerWidths[i];
        }, footerSrcEls);
      } // Sanity check that the table is of a sensible width. If not then we are going to get
      // misalignment - try to prevent this by not allowing the table to shrink below its min width


      if (table.outerWidth() < sanityWidth) {
        // The min width depends upon if we have a vertical scrollbar visible or not */
        correction = divBodyEl.scrollHeight > divBodyEl.offsetHeight || divBody.css('overflow-y') == "scroll" ? sanityWidth + barWidth : sanityWidth; // IE6/7 are a law unto themselves...

        if (ie67 && (divBodyEl.scrollHeight > divBodyEl.offsetHeight || divBody.css('overflow-y') == "scroll")) {
          tableStyle.width = _fnStringToCss(correction - barWidth);
        } // And give the user a warning that we've stopped the table getting too small


        if (scrollX === "" || scrollXInner !== "") {
          _fnLog(settings, 1, 'Possible column misalignment', 6);
        }
      } else {
        correction = '100%';
      } // Apply to the container elements


      divBodyStyle.width = _fnStringToCss(correction);
      divHeaderStyle.width = _fnStringToCss(correction);

      if (footer) {
        settings.nScrollFoot.style.width = _fnStringToCss(correction);
      }
      /*
       * 4. Clean up
       */


      if (!scrollY) {
        /* IE7< puts a vertical scrollbar in place (when it shouldn't be) due to subtracting
         * the scrollbar height from the visible display, rather than adding it on. We need to
         * set the height in order to sort this. Don't want to do it in any other browsers.
         */
        if (ie67) {
          divBodyStyle.height = _fnStringToCss(tableEl.offsetHeight + barWidth);
        }
      }
      /* Finally set the width's of the header and footer tables */


      var iOuterWidth = table.outerWidth();
      divHeaderTable[0].style.width = _fnStringToCss(iOuterWidth);
      divHeaderInnerStyle.width = _fnStringToCss(iOuterWidth); // Figure out if there are scrollbar present - if so then we need a the header and footer to
      // provide a bit more space to allow "overflow" scrolling (i.e. past the scrollbar)

      var bScrolling = table.height() > divBodyEl.clientHeight || divBody.css('overflow-y') == "scroll";
      var padding = 'padding' + (browser.bScrollbarLeft ? 'Left' : 'Right');
      divHeaderInnerStyle[padding] = bScrolling ? barWidth + "px" : "0px";

      if (footer) {
        divFooterTable[0].style.width = _fnStringToCss(iOuterWidth);
        divFooterInner[0].style.width = _fnStringToCss(iOuterWidth);
        divFooterInner[0].style[padding] = bScrolling ? barWidth + "px" : "0px";
      } // Correct DOM ordering for colgroup - comes before the thead


      table.children('colgroup').insertBefore(table.children('thead'));
      /* Adjust the position of the header in case we loose the y-scrollbar */

      divBody.scroll(); // If sorting or filtering has occurred, jump the scrolling back to the top
      // only if we aren't holding the position

      if ((settings.bSorted || settings.bFiltered) && !settings._drawHold) {
        divBodyEl.scrollTop = 0;
      }
    }
    /**
     * Apply a given function to the display child nodes of an element array (typically
     * TD children of TR rows
     *  @param {function} fn Method to apply to the objects
     *  @param array {nodes} an1 List of elements to look through for display children
     *  @param array {nodes} an2 Another list (identical structure to the first) - optional
     *  @memberof DataTable#oApi
     */


    function _fnApplyToChildren(fn, an1, an2) {
      var index = 0,
          i = 0,
          iLen = an1.length;
      var nNode1, nNode2;

      while (i < iLen) {
        nNode1 = an1[i].firstChild;
        nNode2 = an2 ? an2[i].firstChild : null;

        while (nNode1) {
          if (nNode1.nodeType === 1) {
            if (an2) {
              fn(nNode1, nNode2, index);
            } else {
              fn(nNode1, index);
            }

            index++;
          }

          nNode1 = nNode1.nextSibling;
          nNode2 = an2 ? nNode2.nextSibling : null;
        }

        i++;
      }
    }

    var __re_html_remove = /<.*?>/g;
    /**
     * Calculate the width of columns for the table
     *  @param {object} oSettings dataTables settings object
     *  @memberof DataTable#oApi
     */

    function _fnCalculateColumnWidths(oSettings) {
      var table = oSettings.nTable,
          columns = oSettings.aoColumns,
          scroll = oSettings.oScroll,
          scrollY = scroll.sY,
          scrollX = scroll.sX,
          scrollXInner = scroll.sXInner,
          columnCount = columns.length,
          visibleColumns = _fnGetColumns(oSettings, 'bVisible'),
          headerCells = $$$1('th', oSettings.nTHead),
          tableWidthAttr = table.getAttribute('width'),
          // from DOM element
      tableContainer = table.parentNode,
          userInputs = false,
          i,
          column,
          columnIdx,
          browser = oSettings.oBrowser,
          ie67 = browser.bScrollOversize;

      var styleWidth = table.style.width;

      if (styleWidth && styleWidth.indexOf('%') !== -1) {
        tableWidthAttr = styleWidth;
      }
      /* Convert any user input sizes into pixel sizes */


      for (i = 0; i < visibleColumns.length; i++) {
        column = columns[visibleColumns[i]];

        if (column.sWidth !== null) {
          column.sWidth = _fnConvertToWidth(column.sWidthOrig, tableContainer);
          userInputs = true;
        }
      }
      /* If the number of columns in the DOM equals the number that we have to
       * process in DataTables, then we can use the offsets that are created by
       * the web- browser. No custom sizes can be set in order for this to happen,
       * nor scrolling used
       */


      if (ie67 || !userInputs && !scrollX && !scrollY && columnCount == _fnVisbleColumns(oSettings) && columnCount == headerCells.length) {
        for (i = 0; i < columnCount; i++) {
          var colIdx = _fnVisibleToColumnIndex(oSettings, i);

          if (colIdx !== null) {
            columns[colIdx].sWidth = _fnStringToCss(headerCells.eq(i).width());
          }
        }
      } else {
        // Otherwise construct a single row, worst case, table with the widest
        // node in the data, assign any user defined widths, then insert it into
        // the DOM and allow the browser to do all the hard work of calculating
        // table widths
        var tmpTable = $$$1(table).clone() // don't use cloneNode - IE8 will remove events on the main table
        .css('visibility', 'hidden').removeAttr('id'); // Clean up the table body

        tmpTable.find('tbody tr').remove();
        var tr = $$$1('<tr/>').appendTo(tmpTable.find('tbody')); // Clone the table header and footer - we can't use the header / footer
        // from the cloned table, since if scrolling is active, the table's
        // real header and footer are contained in different table tags

        tmpTable.find('thead, tfoot').remove();
        tmpTable.append($$$1(oSettings.nTHead).clone()).append($$$1(oSettings.nTFoot).clone()); // Remove any assigned widths from the footer (from scrolling)

        tmpTable.find('tfoot th, tfoot td').css('width', ''); // Apply custom sizing to the cloned header

        headerCells = _fnGetUniqueThs(oSettings, tmpTable.find('thead')[0]);

        for (i = 0; i < visibleColumns.length; i++) {
          column = columns[visibleColumns[i]];
          headerCells[i].style.width = column.sWidthOrig !== null && column.sWidthOrig !== '' ? _fnStringToCss(column.sWidthOrig) : ''; // For scrollX we need to force the column width otherwise the
          // browser will collapse it. If this width is smaller than the
          // width the column requires, then it will have no effect

          if (column.sWidthOrig && scrollX) {
            $$$1(headerCells[i]).append($$$1('<div/>').css({
              width: column.sWidthOrig,
              margin: 0,
              padding: 0,
              border: 0,
              height: 1
            }));
          }
        } // Find the widest cell for each column and put it into the table


        if (oSettings.aoData.length) {
          for (i = 0; i < visibleColumns.length; i++) {
            columnIdx = visibleColumns[i];
            column = columns[columnIdx];
            $$$1(_fnGetWidestNode(oSettings, columnIdx)).clone(false).append(column.sContentPadding).appendTo(tr);
          }
        } // Tidy the temporary table - remove name attributes so there aren't
        // duplicated in the dom (radio elements for example)


        $$$1('[name]', tmpTable).removeAttr('name'); // Table has been built, attach to the document so we can work with it.
        // A holding element is used, positioned at the top of the container
        // with minimal height, so it has no effect on if the container scrolls
        // or not. Otherwise it might trigger scrolling when it actually isn't
        // needed

        var holder = $$$1('<div/>').css(scrollX || scrollY ? {
          position: 'absolute',
          top: 0,
          left: 0,
          height: 1,
          right: 0,
          overflow: 'hidden'
        } : {}).append(tmpTable).appendTo(tableContainer); // When scrolling (X or Y) we want to set the width of the table as 
        // appropriate. However, when not scrolling leave the table width as it
        // is. This results in slightly different, but I think correct behaviour

        if (scrollX && scrollXInner) {
          tmpTable.width(scrollXInner);
        } else if (scrollX) {
          tmpTable.css('width', 'auto');
          tmpTable.removeAttr('width'); // If there is no width attribute or style, then allow the table to
          // collapse

          if (tmpTable.width() < tableContainer.clientWidth && tableWidthAttr) {
            tmpTable.width(tableContainer.clientWidth);
          }
        } else if (scrollY) {
          tmpTable.width(tableContainer.clientWidth);
        } else if (tableWidthAttr) {
          tmpTable.width(tableWidthAttr);
        } // Get the width of each column in the constructed table - we need to
        // know the inner width (so it can be assigned to the other table's
        // cells) and the outer width so we can calculate the full width of the
        // table. This is safe since DataTables requires a unique cell for each
        // column, but if ever a header can span multiple columns, this will
        // need to be modified.


        var total = 0;

        for (i = 0; i < visibleColumns.length; i++) {
          var cell = $$$1(headerCells[i]);
          var border = cell.outerWidth() - cell.width(); // Use getBounding... where possible (not IE8-) because it can give
          // sub-pixel accuracy, which we then want to round up!

          var bounding = browser.bBounding ? Math.ceil(headerCells[i].getBoundingClientRect().width) : cell.outerWidth(); // Total is tracked to remove any sub-pixel errors as the outerWidth
          // of the table might not equal the total given here (IE!).

          total += bounding; // Width for each column to use

          columns[visibleColumns[i]].sWidth = _fnStringToCss(bounding - border);
        }

        table.style.width = _fnStringToCss(total); // Finished with the table - ditch it

        holder.remove();
      } // If there is a width attr, we want to attach an event listener which
      // allows the table sizing to automatically adjust when the window is
      // resized. Use the width attr rather than CSS, since we can't know if the
      // CSS is a relative value or absolute - DOM read is always px.


      if (tableWidthAttr) {
        table.style.width = _fnStringToCss(tableWidthAttr);
      }

      if ((tableWidthAttr || scrollX) && !oSettings._reszEvt) {
        var bindResize = function bindResize() {
          $$$1(window).on('resize.DT-' + oSettings.sInstance, _fnThrottle(function () {
            _fnAdjustColumnSizing(oSettings);
          }));
        }; // IE6/7 will crash if we bind a resize event handler on page load.
        // To be removed in 1.11 which drops IE6/7 support


        if (ie67) {
          setTimeout(bindResize, 1000);
        } else {
          bindResize();
        }

        oSettings._reszEvt = true;
      }
    }
    /**
     * Throttle the calls to a function. Arguments and context are maintained for
     * the throttled function
     *  @param {function} fn Function to be called
     *  @param {int} [freq=200] call frequency in mS
     *  @returns {function} wrapped function
     *  @memberof DataTable#oApi
     */


    var _fnThrottle = DataTable.util.throttle;
    /**
     * Convert a CSS unit width to pixels (e.g. 2em)
     *  @param {string} width width to be converted
     *  @param {node} parent parent to get the with for (required for relative widths) - optional
     *  @returns {int} width in pixels
     *  @memberof DataTable#oApi
     */

    function _fnConvertToWidth(width, parent) {
      if (!width) {
        return 0;
      }

      var n = $$$1('<div/>').css('width', _fnStringToCss(width)).appendTo(parent || document.body);
      var val = n[0].offsetWidth;
      n.remove();
      return val;
    }
    /**
     * Get the widest node
     *  @param {object} settings dataTables settings object
     *  @param {int} colIdx column of interest
     *  @returns {node} widest table node
     *  @memberof DataTable#oApi
     */


    function _fnGetWidestNode(settings, colIdx) {
      var idx = _fnGetMaxLenString(settings, colIdx);

      if (idx < 0) {
        return null;
      }

      var data = settings.aoData[idx];
      return !data.nTr ? // Might not have been created when deferred rendering
      $$$1('<td/>').html(_fnGetCellData(settings, idx, colIdx, 'display'))[0] : data.anCells[colIdx];
    }
    /**
     * Get the maximum strlen for each data column
     *  @param {object} settings dataTables settings object
     *  @param {int} colIdx column of interest
     *  @returns {string} max string length for each column
     *  @memberof DataTable#oApi
     */


    function _fnGetMaxLenString(settings, colIdx) {
      var s,
          max = -1,
          maxIdx = -1;

      for (var i = 0, ien = settings.aoData.length; i < ien; i++) {
        s = _fnGetCellData(settings, i, colIdx, 'display') + '';
        s = s.replace(__re_html_remove, '');
        s = s.replace(/&nbsp;/g, ' ');

        if (s.length > max) {
          max = s.length;
          maxIdx = i;
        }
      }

      return maxIdx;
    }
    /**
     * Append a CSS unit (only if required) to a string
     *  @param {string} value to css-ify
     *  @returns {string} value with css unit
     *  @memberof DataTable#oApi
     */


    function _fnStringToCss(s) {
      if (s === null) {
        return '0px';
      }

      if (typeof s == 'number') {
        return s < 0 ? '0px' : s + 'px';
      } // Check it has a unit character already


      return s.match(/\d$/) ? s + 'px' : s;
    }

    function _fnSortFlatten(settings) {
      var i,
          k,
          kLen,
          aSort = [],
          aoColumns = settings.aoColumns,
          aDataSort,
          iCol,
          sType,
          srcCol,
          fixed = settings.aaSortingFixed,
          fixedObj = $$$1.isPlainObject(fixed),
          nestedSort = [],
          add = function add(a) {
        if (a.length && !$$$1.isArray(a[0])) {
          // 1D array
          nestedSort.push(a);
        } else {
          // 2D array
          $$$1.merge(nestedSort, a);
        }
      }; // Build the sort array, with pre-fix and post-fix options if they have been
      // specified


      if ($$$1.isArray(fixed)) {
        add(fixed);
      }

      if (fixedObj && fixed.pre) {
        add(fixed.pre);
      }

      add(settings.aaSorting);

      if (fixedObj && fixed.post) {
        add(fixed.post);
      }

      for (i = 0; i < nestedSort.length; i++) {
        srcCol = nestedSort[i][0];
        aDataSort = aoColumns[srcCol].aDataSort;

        for (k = 0, kLen = aDataSort.length; k < kLen; k++) {
          iCol = aDataSort[k];
          sType = aoColumns[iCol].sType || 'string';

          if (nestedSort[i]._idx === undefined) {
            nestedSort[i]._idx = $$$1.inArray(nestedSort[i][1], aoColumns[iCol].asSorting);
          }

          aSort.push({
            src: srcCol,
            col: iCol,
            dir: nestedSort[i][1],
            index: nestedSort[i]._idx,
            type: sType,
            formatter: DataTable.ext.type.order[sType + "-pre"]
          });
        }
      }

      return aSort;
    }
    /**
     * Change the order of the table
     *  @param {object} oSettings dataTables settings object
     *  @memberof DataTable#oApi
     *  @todo This really needs split up!
     */


    function _fnSort(oSettings) {
      var i,
          ien,
          iLen,
          aiOrig = [],
          oExtSort = DataTable.ext.type.order,
          aoData = oSettings.aoData,
          aoColumns = oSettings.aoColumns,
          formatters = 0,
          sortCol,
          displayMaster = oSettings.aiDisplayMaster,
          aSort; // Resolve any column types that are unknown due to addition or invalidation
      // @todo Can this be moved into a 'data-ready' handler which is called when
      //   data is going to be used in the table?

      _fnColumnTypes(oSettings);

      aSort = _fnSortFlatten(oSettings);

      for (i = 0, ien = aSort.length; i < ien; i++) {
        sortCol = aSort[i]; // Track if we can use the fast sort algorithm

        if (sortCol.formatter) {
          formatters++;
        } // Load the data needed for the sort, for each cell


        _fnSortData(oSettings, sortCol.col);
      }
      /* No sorting required if server-side or no sorting array */


      if (_fnDataSource(oSettings) != 'ssp' && aSort.length !== 0) {
        // Create a value - key array of the current row positions such that we can use their
        // current position during the sort, if values match, in order to perform stable sorting
        for (i = 0, iLen = displayMaster.length; i < iLen; i++) {
          aiOrig[displayMaster[i]] = i;
        }
        /* Do the sort - here we want multi-column sorting based on a given data source (column)
         * and sorting function (from oSort) in a certain direction. It's reasonably complex to
         * follow on it's own, but this is what we want (example two column sorting):
         *  fnLocalSorting = function(a,b){
         *    var iTest;
         *    iTest = oSort['string-asc']('data11', 'data12');
         *      if (iTest !== 0)
         *        return iTest;
         *    iTest = oSort['numeric-desc']('data21', 'data22');
         *    if (iTest !== 0)
         *      return iTest;
         *    return oSort['numeric-asc']( aiOrig[a], aiOrig[b] );
         *  }
         * Basically we have a test for each sorting column, if the data in that column is equal,
         * test the next column. If all columns match, then we use a numeric sort on the row
         * positions in the original data array to provide a stable sort.
         *
         * Note - I know it seems excessive to have two sorting methods, but the first is around
         * 15% faster, so the second is only maintained for backwards compatibility with sorting
         * methods which do not have a pre-sort formatting function.
         */


        if (formatters === aSort.length) {
          // All sort types have formatting functions
          displayMaster.sort(function (a, b) {
            var x,
                y,
                k,
                test,
                sort,
                len = aSort.length,
                dataA = aoData[a]._aSortData,
                dataB = aoData[b]._aSortData;

            for (k = 0; k < len; k++) {
              sort = aSort[k];
              x = dataA[sort.col];
              y = dataB[sort.col];
              test = x < y ? -1 : x > y ? 1 : 0;

              if (test !== 0) {
                return sort.dir === 'asc' ? test : -test;
              }
            }

            x = aiOrig[a];
            y = aiOrig[b];
            return x < y ? -1 : x > y ? 1 : 0;
          });
        } else {
          // Depreciated - remove in 1.11 (providing a plug-in option)
          // Not all sort types have formatting methods, so we have to call their sorting
          // methods.
          displayMaster.sort(function (a, b) {
            var x,
                y,
                k,
                test,
                sort,
                fn,
                len = aSort.length,
                dataA = aoData[a]._aSortData,
                dataB = aoData[b]._aSortData;

            for (k = 0; k < len; k++) {
              sort = aSort[k];
              x = dataA[sort.col];
              y = dataB[sort.col];
              fn = oExtSort[sort.type + "-" + sort.dir] || oExtSort["string-" + sort.dir];
              test = fn(x, y);

              if (test !== 0) {
                return test;
              }
            }

            x = aiOrig[a];
            y = aiOrig[b];
            return x < y ? -1 : x > y ? 1 : 0;
          });
        }
      }
      /* Tell the draw function that we have sorted the data */


      oSettings.bSorted = true;
    }

    function _fnSortAria(settings) {
      var label;
      var nextSort;
      var columns = settings.aoColumns;

      var aSort = _fnSortFlatten(settings);

      var oAria = settings.oLanguage.oAria; // ARIA attributes - need to loop all columns, to update all (removing old
      // attributes as needed)

      for (var i = 0, iLen = columns.length; i < iLen; i++) {
        var col = columns[i];
        var asSorting = col.asSorting;
        var sTitle = col.sTitle.replace(/<.*?>/g, "");
        var th = col.nTh; // IE7 is throwing an error when setting these properties with jQuery's
        // attr() and removeAttr() methods...

        th.removeAttribute('aria-sort');
        /* In ARIA only the first sorting column can be marked as sorting - no multi-sort option */

        if (col.bSortable) {
          if (aSort.length > 0 && aSort[0].col == i) {
            th.setAttribute('aria-sort', aSort[0].dir == "asc" ? "ascending" : "descending");
            nextSort = asSorting[aSort[0].index + 1] || asSorting[0];
          } else {
            nextSort = asSorting[0];
          }

          label = sTitle + (nextSort === "asc" ? oAria.sSortAscending : oAria.sSortDescending);
        } else {
          label = sTitle;
        }

        th.setAttribute('aria-label', label);
      }
    }
    /**
     * Function to run on user sort request
     *  @param {object} settings dataTables settings object
     *  @param {node} attachTo node to attach the handler to
     *  @param {int} colIdx column sorting index
     *  @param {boolean} [append=false] Append the requested sort to the existing
     *    sort if true (i.e. multi-column sort)
     *  @param {function} [callback] callback function
     *  @memberof DataTable#oApi
     */


    function _fnSortListener(settings, colIdx, append, callback) {
      var col = settings.aoColumns[colIdx];
      var sorting = settings.aaSorting;
      var asSorting = col.asSorting;
      var nextSortIdx;

      var next = function next(a, overflow) {
        var idx = a._idx;

        if (idx === undefined) {
          idx = $$$1.inArray(a[1], asSorting);
        }

        return idx + 1 < asSorting.length ? idx + 1 : overflow ? null : 0;
      }; // Convert to 2D array if needed


      if (typeof sorting[0] === 'number') {
        sorting = settings.aaSorting = [sorting];
      } // If appending the sort then we are multi-column sorting


      if (append && settings.oFeatures.bSortMulti) {
        // Are we already doing some kind of sort on this column?
        var sortIdx = $$$1.inArray(colIdx, _pluck(sorting, '0'));

        if (sortIdx !== -1) {
          // Yes, modify the sort
          nextSortIdx = next(sorting[sortIdx], true);

          if (nextSortIdx === null && sorting.length === 1) {
            nextSortIdx = 0; // can't remove sorting completely
          }

          if (nextSortIdx === null) {
            sorting.splice(sortIdx, 1);
          } else {
            sorting[sortIdx][1] = asSorting[nextSortIdx];
            sorting[sortIdx]._idx = nextSortIdx;
          }
        } else {
          // No sort on this column yet
          sorting.push([colIdx, asSorting[0], 0]);
          sorting[sorting.length - 1]._idx = 0;
        }
      } else if (sorting.length && sorting[0][0] == colIdx) {
        // Single column - already sorting on this column, modify the sort
        nextSortIdx = next(sorting[0]);
        sorting.length = 1;
        sorting[0][1] = asSorting[nextSortIdx];
        sorting[0]._idx = nextSortIdx;
      } else {
        // Single column - sort only on this column
        sorting.length = 0;
        sorting.push([colIdx, asSorting[0]]);
        sorting[0]._idx = 0;
      } // Run the sort by calling a full redraw


      _fnReDraw(settings); // callback used for async user interaction


      if (typeof callback == 'function') {
        callback(settings);
      }
    }
    /**
     * Attach a sort handler (click) to a node
     *  @param {object} settings dataTables settings object
     *  @param {node} attachTo node to attach the handler to
     *  @param {int} colIdx column sorting index
     *  @param {function} [callback] callback function
     *  @memberof DataTable#oApi
     */


    function _fnSortAttachListener(settings, attachTo, colIdx, callback) {
      var col = settings.aoColumns[colIdx];

      _fnBindAction(attachTo, {}, function (e) {
        /* If the column is not sortable - don't to anything */
        if (col.bSortable === false) {
          return;
        } // If processing is enabled use a timeout to allow the processing
        // display to be shown - otherwise to it synchronously


        if (settings.oFeatures.bProcessing) {
          _fnProcessingDisplay(settings, true);

          setTimeout(function () {
            _fnSortListener(settings, colIdx, e.shiftKey, callback); // In server-side processing, the draw callback will remove the
            // processing display


            if (_fnDataSource(settings) !== 'ssp') {
              _fnProcessingDisplay(settings, false);
            }
          }, 0);
        } else {
          _fnSortListener(settings, colIdx, e.shiftKey, callback);
        }
      });
    }
    /**
     * Set the sorting classes on table's body, Note: it is safe to call this function
     * when bSort and bSortClasses are false
     *  @param {object} oSettings dataTables settings object
     *  @memberof DataTable#oApi
     */


    function _fnSortingClasses(settings) {
      var oldSort = settings.aLastSort;
      var sortClass = settings.oClasses.sSortColumn;

      var sort = _fnSortFlatten(settings);

      var features = settings.oFeatures;
      var i, ien, colIdx;

      if (features.bSort && features.bSortClasses) {
        // Remove old sorting classes
        for (i = 0, ien = oldSort.length; i < ien; i++) {
          colIdx = oldSort[i].src; // Remove column sorting

          $$$1(_pluck(settings.aoData, 'anCells', colIdx)).removeClass(sortClass + (i < 2 ? i + 1 : 3));
        } // Add new column sorting


        for (i = 0, ien = sort.length; i < ien; i++) {
          colIdx = sort[i].src;
          $$$1(_pluck(settings.aoData, 'anCells', colIdx)).addClass(sortClass + (i < 2 ? i + 1 : 3));
        }
      }

      settings.aLastSort = sort;
    } // Get the data to sort a column, be it from cache, fresh (populating the
    // cache), or from a sort formatter


    function _fnSortData(settings, idx) {
      // Custom sorting function - provided by the sort data type
      var column = settings.aoColumns[idx];
      var customSort = DataTable.ext.order[column.sSortDataType];
      var customData;

      if (customSort) {
        customData = customSort.call(settings.oInstance, settings, idx, _fnColumnIndexToVisible(settings, idx));
      } // Use / populate cache


      var row, cellData;
      var formatter = DataTable.ext.type.order[column.sType + "-pre"];

      for (var i = 0, ien = settings.aoData.length; i < ien; i++) {
        row = settings.aoData[i];

        if (!row._aSortData) {
          row._aSortData = [];
        }

        if (!row._aSortData[idx] || customSort) {
          cellData = customSort ? customData[i] : // If there was a custom sort function, use data from there
          _fnGetCellData(settings, i, idx, 'sort');
          row._aSortData[idx] = formatter ? formatter(cellData) : cellData;
        }
      }
    }
    /**
     * Save the state of a table
     *  @param {object} oSettings dataTables settings object
     *  @memberof DataTable#oApi
     */


    function _fnSaveState(settings) {
      if (!settings.oFeatures.bStateSave || settings.bDestroying) {
        return;
      }
      /* Store the interesting variables */


      var state = {
        time: +new Date(),
        start: settings._iDisplayStart,
        length: settings._iDisplayLength,
        order: $$$1.extend(true, [], settings.aaSorting),
        search: _fnSearchToCamel(settings.oPreviousSearch),
        columns: $$$1.map(settings.aoColumns, function (col, i) {
          return {
            visible: col.bVisible,
            search: _fnSearchToCamel(settings.aoPreSearchCols[i])
          };
        })
      };

      _fnCallbackFire(settings, "aoStateSaveParams", 'stateSaveParams', [settings, state]);

      settings.oSavedState = state;
      settings.fnStateSaveCallback.call(settings.oInstance, settings, state);
    }
    /**
     * Attempt to load a saved table state
     *  @param {object} oSettings dataTables settings object
     *  @param {object} oInit DataTables init object so we can override settings
     *  @param {function} callback Callback to execute when the state has been loaded
     *  @memberof DataTable#oApi
     */


    function _fnLoadState(settings, oInit, callback) {
      var i, ien;
      var columns = settings.aoColumns;

      var loaded = function loaded(s) {
        if (!s || !s.time) {
          callback();
          return;
        } // Allow custom and plug-in manipulation functions to alter the saved data set and
        // cancelling of loading by returning false


        var abStateLoad = _fnCallbackFire(settings, 'aoStateLoadParams', 'stateLoadParams', [settings, s]);

        if ($$$1.inArray(false, abStateLoad) !== -1) {
          callback();
          return;
        } // Reject old data


        var duration = settings.iStateDuration;

        if (duration > 0 && s.time < +new Date() - duration * 1000) {
          callback();
          return;
        } // Number of columns have changed - all bets are off, no restore of settings


        if (s.columns && columns.length !== s.columns.length) {
          callback();
          return;
        } // Store the saved state so it might be accessed at any time


        settings.oLoadedState = $$$1.extend(true, {}, s); // Restore key features - todo - for 1.11 this needs to be done by
        // subscribed events

        if (s.start !== undefined) {
          settings._iDisplayStart = s.start;
          settings.iInitDisplayStart = s.start;
        }

        if (s.length !== undefined) {
          settings._iDisplayLength = s.length;
        } // Order


        if (s.order !== undefined) {
          settings.aaSorting = [];
          $$$1.each(s.order, function (i, col) {
            settings.aaSorting.push(col[0] >= columns.length ? [0, col[1]] : col);
          });
        } // Search


        if (s.search !== undefined) {
          $$$1.extend(settings.oPreviousSearch, _fnSearchToHung(s.search));
        } // Columns
        //


        if (s.columns) {
          for (i = 0, ien = s.columns.length; i < ien; i++) {
            var col = s.columns[i]; // Visibility

            if (col.visible !== undefined) {
              columns[i].bVisible = col.visible;
            } // Search


            if (col.search !== undefined) {
              $$$1.extend(settings.aoPreSearchCols[i], _fnSearchToHung(col.search));
            }
          }
        }

        _fnCallbackFire(settings, 'aoStateLoaded', 'stateLoaded', [settings, s]);

        callback();
      };

      if (!settings.oFeatures.bStateSave) {
        callback();
        return;
      }

      var state = settings.fnStateLoadCallback.call(settings.oInstance, settings, loaded);

      if (state !== undefined) {
        loaded(state);
      } // otherwise, wait for the loaded callback to be executed

    }
    /**
     * Return the settings object for a particular table
     *  @param {node} table table we are using as a dataTable
     *  @returns {object} Settings object - or null if not found
     *  @memberof DataTable#oApi
     */


    function _fnSettingsFromNode(table) {
      var settings = DataTable.settings;
      var idx = $$$1.inArray(table, _pluck(settings, 'nTable'));
      return idx !== -1 ? settings[idx] : null;
    }
    /**
     * Log an error message
     *  @param {object} settings dataTables settings object
     *  @param {int} level log error messages, or display them to the user
     *  @param {string} msg error message
     *  @param {int} tn Technical note id to get more information about the error.
     *  @memberof DataTable#oApi
     */


    function _fnLog(settings, level, msg, tn) {
      msg = 'DataTables warning: ' + (settings ? 'table id=' + settings.sTableId + ' - ' : '') + msg;

      if (tn) {
        msg += '. For more information about this error, please see ' + 'http://datatables.net/tn/' + tn;
      }

      if (!level) {
        // Backwards compatibility pre 1.10
        var ext = DataTable.ext;
        var type = ext.sErrMode || ext.errMode;

        if (settings) {
          _fnCallbackFire(settings, null, 'error', [settings, tn, msg]);
        }

        if (type == 'alert') {
          alert(msg);
        } else if (type == 'throw') {
          throw new Error(msg);
        } else if (typeof type == 'function') {
          type(settings, tn, msg);
        }
      } else if (window.console && console.log) {
        console.log(msg);
      }
    }
    /**
     * See if a property is defined on one object, if so assign it to the other object
     *  @param {object} ret target object
     *  @param {object} src source object
     *  @param {string} name property
     *  @param {string} [mappedName] name to map too - optional, name used if not given
     *  @memberof DataTable#oApi
     */


    function _fnMap(ret, src, name, mappedName) {
      if ($$$1.isArray(name)) {
        $$$1.each(name, function (i, val) {
          if ($$$1.isArray(val)) {
            _fnMap(ret, src, val[0], val[1]);
          } else {
            _fnMap(ret, src, val);
          }
        });
        return;
      }

      if (mappedName === undefined) {
        mappedName = name;
      }

      if (src[name] !== undefined) {
        ret[mappedName] = src[name];
      }
    }
    /**
     * Extend objects - very similar to jQuery.extend, but deep copy objects, and
     * shallow copy arrays. The reason we need to do this, is that we don't want to
     * deep copy array init values (such as aaSorting) since the dev wouldn't be
     * able to override them, but we do want to deep copy arrays.
     *  @param {object} out Object to extend
     *  @param {object} extender Object from which the properties will be applied to
     *      out
     *  @param {boolean} breakRefs If true, then arrays will be sliced to take an
     *      independent copy with the exception of the `data` or `aaData` parameters
     *      if they are present. This is so you can pass in a collection to
     *      DataTables and have that used as your data source without breaking the
     *      references
     *  @returns {object} out Reference, just for convenience - out === the return.
     *  @memberof DataTable#oApi
     *  @todo This doesn't take account of arrays inside the deep copied objects.
     */


    function _fnExtend(out, extender, breakRefs) {
      var val;

      for (var prop in extender) {
        if (extender.hasOwnProperty(prop)) {
          val = extender[prop];

          if ($$$1.isPlainObject(val)) {
            if (!$$$1.isPlainObject(out[prop])) {
              out[prop] = {};
            }

            $$$1.extend(true, out[prop], val);
          } else if (breakRefs && prop !== 'data' && prop !== 'aaData' && $$$1.isArray(val)) {
            out[prop] = val.slice();
          } else {
            out[prop] = val;
          }
        }
      }

      return out;
    }
    /**
     * Bind an event handers to allow a click or return key to activate the callback.
     * This is good for accessibility since a return on the keyboard will have the
     * same effect as a click, if the element has focus.
     *  @param {element} n Element to bind the action to
     *  @param {object} oData Data object to pass to the triggered function
     *  @param {function} fn Callback function for when the event is triggered
     *  @memberof DataTable#oApi
     */


    function _fnBindAction(n, oData, fn) {
      $$$1(n).on('click.DT', oData, function (e) {
        $$$1(n).blur(); // Remove focus outline for mouse users

        fn(e);
      }).on('keypress.DT', oData, function (e) {
        if (e.which === 13) {
          e.preventDefault();
          fn(e);
        }
      }).on('selectstart.DT', function () {
        /* Take the brutal approach to cancelling text selection */
        return false;
      });
    }
    /**
     * Register a callback function. Easily allows a callback function to be added to
     * an array store of callback functions that can then all be called together.
     *  @param {object} oSettings dataTables settings object
     *  @param {string} sStore Name of the array storage for the callbacks in oSettings
     *  @param {function} fn Function to be called back
     *  @param {string} sName Identifying name for the callback (i.e. a label)
     *  @memberof DataTable#oApi
     */


    function _fnCallbackReg(oSettings, sStore, fn, sName) {
      if (fn) {
        oSettings[sStore].push({
          "fn": fn,
          "sName": sName
        });
      }
    }
    /**
     * Fire callback functions and trigger events. Note that the loop over the
     * callback array store is done backwards! Further note that you do not want to
     * fire off triggers in time sensitive applications (for example cell creation)
     * as its slow.
     *  @param {object} settings dataTables settings object
     *  @param {string} callbackArr Name of the array storage for the callbacks in
     *      oSettings
     *  @param {string} eventName Name of the jQuery custom event to trigger. If
     *      null no trigger is fired
     *  @param {array} args Array of arguments to pass to the callback function /
     *      trigger
     *  @memberof DataTable#oApi
     */


    function _fnCallbackFire(settings, callbackArr, eventName, args) {
      var ret = [];

      if (callbackArr) {
        ret = $$$1.map(settings[callbackArr].slice().reverse(), function (val, i) {
          return val.fn.apply(settings.oInstance, args);
        });
      }

      if (eventName !== null) {
        var e = $$$1.Event(eventName + '.dt');
        $$$1(settings.nTable).trigger(e, args);
        ret.push(e.result);
      }

      return ret;
    }

    function _fnLengthOverflow(settings) {
      var start = settings._iDisplayStart,
          end = settings.fnDisplayEnd(),
          len = settings._iDisplayLength;
      /* If we have space to show extra rows (backing up from the end point - then do so */

      if (start >= end) {
        start = end - len;
      } // Keep the start record on the current page


      start -= start % len;

      if (len === -1 || start < 0) {
        start = 0;
      }

      settings._iDisplayStart = start;
    }

    function _fnRenderer(settings, type) {
      var renderer = settings.renderer;
      var host = DataTable.ext.renderer[type];

      if ($$$1.isPlainObject(renderer) && renderer[type]) {
        // Specific renderer for this type. If available use it, otherwise use
        // the default.
        return host[renderer[type]] || host._;
      } else if (typeof renderer === 'string') {
        // Common renderer - if there is one available for this type use it,
        // otherwise use the default
        return host[renderer] || host._;
      } // Use the default


      return host._;
    }
    /**
     * Detect the data source being used for the table. Used to simplify the code
     * a little (ajax) and to make it compress a little smaller.
     *
     *  @param {object} settings dataTables settings object
     *  @returns {string} Data source
     *  @memberof DataTable#oApi
     */


    function _fnDataSource(settings) {
      if (settings.oFeatures.bServerSide) {
        return 'ssp';
      } else if (settings.ajax || settings.sAjaxSource) {
        return 'ajax';
      }

      return 'dom';
    }
    /**
     * Computed structure of the DataTables API, defined by the options passed to
     * `DataTable.Api.register()` when building the API.
     *
     * The structure is built in order to speed creation and extension of the Api
     * objects since the extensions are effectively pre-parsed.
     *
     * The array is an array of objects with the following structure, where this
     * base array represents the Api prototype base:
     *
     *     [
     *       {
     *         name:      'data'                -- string   - Property name
     *         val:       function () {},       -- function - Api method (or undefined if just an object
     *         methodExt: [ ... ],              -- array    - Array of Api object definitions to extend the method result
     *         propExt:   [ ... ]               -- array    - Array of Api object definitions to extend the property
     *       },
     *       {
     *         name:     'row'
     *         val:       {},
     *         methodExt: [ ... ],
     *         propExt:   [
     *           {
     *             name:      'data'
     *             val:       function () {},
     *             methodExt: [ ... ],
     *             propExt:   [ ... ]
     *           },
     *           ...
     *         ]
     *       }
     *     ]
     *
     * @type {Array}
     * @ignore
     */


    var __apiStruct = [];
    /**
     * `Array.prototype` reference.
     *
     * @type object
     * @ignore
     */

    var __arrayProto = Array.prototype;
    /**
     * Abstraction for `context` parameter of the `Api` constructor to allow it to
     * take several different forms for ease of use.
     *
     * Each of the input parameter types will be converted to a DataTables settings
     * object where possible.
     *
     * @param  {string|node|jQuery|object} mixed DataTable identifier. Can be one
     *   of:
     *
     *   * `string` - jQuery selector. Any DataTables' matching the given selector
     *     with be found and used.
     *   * `node` - `TABLE` node which has already been formed into a DataTable.
     *   * `jQuery` - A jQuery object of `TABLE` nodes.
     *   * `object` - DataTables settings object
     *   * `DataTables.Api` - API instance
     * @return {array|null} Matching DataTables settings objects. `null` or
     *   `undefined` is returned if no matching DataTable is found.
     * @ignore
     */

    var _toSettings = function _toSettings(mixed) {
      var idx, jq;
      var settings = DataTable.settings;
      var tables = $$$1.map(settings, function (el, i) {
        return el.nTable;
      });

      if (!mixed) {
        return [];
      } else if (mixed.nTable && mixed.oApi) {
        // DataTables settings object
        return [mixed];
      } else if (mixed.nodeName && mixed.nodeName.toLowerCase() === 'table') {
        // Table node
        idx = $$$1.inArray(mixed, tables);
        return idx !== -1 ? [settings[idx]] : null;
      } else if (mixed && typeof mixed.settings === 'function') {
        return mixed.settings().toArray();
      } else if (typeof mixed === 'string') {
        // jQuery selector
        jq = $$$1(mixed);
      } else if (mixed instanceof $$$1) {
        // jQuery object (also DataTables instance)
        jq = mixed;
      }

      if (jq) {
        return jq.map(function (i) {
          idx = $$$1.inArray(this, tables);
          return idx !== -1 ? settings[idx] : null;
        }).toArray();
      }
    };
    /**
     * DataTables API class - used to control and interface with  one or more
     * DataTables enhanced tables.
     *
     * The API class is heavily based on jQuery, presenting a chainable interface
     * that you can use to interact with tables. Each instance of the API class has
     * a "context" - i.e. the tables that it will operate on. This could be a single
     * table, all tables on a page or a sub-set thereof.
     *
     * Additionally the API is designed to allow you to easily work with the data in
     * the tables, retrieving and manipulating it as required. This is done by
     * presenting the API class as an array like interface. The contents of the
     * array depend upon the actions requested by each method (for example
     * `rows().nodes()` will return an array of nodes, while `rows().data()` will
     * return an array of objects or arrays depending upon your table's
     * configuration). The API object has a number of array like methods (`push`,
     * `pop`, `reverse` etc) as well as additional helper methods (`each`, `pluck`,
     * `unique` etc) to assist your working with the data held in a table.
     *
     * Most methods (those which return an Api instance) are chainable, which means
     * the return from a method call also has all of the methods available that the
     * top level object had. For example, these two calls are equivalent:
     *
     *     // Not chained
     *     api.row.add( {...} );
     *     api.draw();
     *
     *     // Chained
     *     api.row.add( {...} ).draw();
     *
     * @class DataTable.Api
     * @param {array|object|string|jQuery} context DataTable identifier. This is
     *   used to define which DataTables enhanced tables this API will operate on.
     *   Can be one of:
     *
     *   * `string` - jQuery selector. Any DataTables' matching the given selector
     *     with be found and used.
     *   * `node` - `TABLE` node which has already been formed into a DataTable.
     *   * `jQuery` - A jQuery object of `TABLE` nodes.
     *   * `object` - DataTables settings object
     * @param {array} [data] Data to initialise the Api instance with.
     *
     * @example
     *   // Direct initialisation during DataTables construction
     *   var api = $('#example').DataTable();
     *
     * @example
     *   // Initialisation using a DataTables jQuery object
     *   var api = $('#example').dataTable().api();
     *
     * @example
     *   // Initialisation as a constructor
     *   var api = new $.fn.DataTable.Api( 'table.dataTable' );
     */


    _Api2 = function _Api(context, data) {
      if (!(this instanceof _Api2)) {
        return new _Api2(context, data);
      }

      var settings = [];

      var ctxSettings = function ctxSettings(o) {
        var a = _toSettings(o);

        if (a) {
          settings = settings.concat(a);
        }
      };

      if ($$$1.isArray(context)) {
        for (var i = 0, ien = context.length; i < ien; i++) {
          ctxSettings(context[i]);
        }
      } else {
        ctxSettings(context);
      } // Remove duplicates


      this.context = _unique(settings); // Initial data

      if (data) {
        $$$1.merge(this, data);
      } // selector


      this.selector = {
        rows: null,
        cols: null,
        opts: null
      };

      _Api2.extend(this, this, __apiStruct);
    };

    DataTable.Api = _Api2; // Don't destroy the existing prototype, just extend it. Required for jQuery 2's
    // isPlainObject.

    $$$1.extend(_Api2.prototype, {
      any: function any() {
        return this.count() !== 0;
      },
      concat: __arrayProto.concat,
      context: [],
      // array of table settings objects
      count: function count() {
        return this.flatten().length;
      },
      each: function each(fn) {
        for (var i = 0, ien = this.length; i < ien; i++) {
          fn.call(this, this[i], i, this);
        }

        return this;
      },
      eq: function eq(idx) {
        var ctx = this.context;
        return ctx.length > idx ? new _Api2(ctx[idx], this[idx]) : null;
      },
      filter: function filter(fn) {
        var a = [];

        if (__arrayProto.filter) {
          a = __arrayProto.filter.call(this, fn, this);
        } else {
          // Compatibility for browsers without EMCA-252-5 (JS 1.6)
          for (var i = 0, ien = this.length; i < ien; i++) {
            if (fn.call(this, this[i], i, this)) {
              a.push(this[i]);
            }
          }
        }

        return new _Api2(this.context, a);
      },
      flatten: function flatten() {
        var a = [];
        return new _Api2(this.context, a.concat.apply(a, this.toArray()));
      },
      join: __arrayProto.join,
      indexOf: __arrayProto.indexOf || function (obj, start) {
        for (var i = start || 0, ien = this.length; i < ien; i++) {
          if (this[i] === obj) {
            return i;
          }
        }

        return -1;
      },
      iterator: function iterator(flatten, type, fn, alwaysNew) {
        var a = [],
            ret,
            i,
            ien,
            j,
            jen,
            context = this.context,
            rows,
            items,
            item,
            selector = this.selector; // Argument shifting

        if (typeof flatten === 'string') {
          alwaysNew = fn;
          fn = type;
          type = flatten;
          flatten = false;
        }

        for (i = 0, ien = context.length; i < ien; i++) {
          var apiInst = new _Api2(context[i]);

          if (type === 'table') {
            ret = fn.call(apiInst, context[i], i);

            if (ret !== undefined) {
              a.push(ret);
            }
          } else if (type === 'columns' || type === 'rows') {
            // this has same length as context - one entry for each table
            ret = fn.call(apiInst, context[i], this[i], i);

            if (ret !== undefined) {
              a.push(ret);
            }
          } else if (type === 'column' || type === 'column-rows' || type === 'row' || type === 'cell') {
            // columns and rows share the same structure.
            // 'this' is an array of column indexes for each context
            items = this[i];

            if (type === 'column-rows') {
              rows = _selector_row_indexes(context[i], selector.opts);
            }

            for (j = 0, jen = items.length; j < jen; j++) {
              item = items[j];

              if (type === 'cell') {
                ret = fn.call(apiInst, context[i], item.row, item.column, i, j);
              } else {
                ret = fn.call(apiInst, context[i], item, i, j, rows);
              }

              if (ret !== undefined) {
                a.push(ret);
              }
            }
          }
        }

        if (a.length || alwaysNew) {
          var api = new _Api2(context, flatten ? a.concat.apply([], a) : a);
          var apiSelector = api.selector;
          apiSelector.rows = selector.rows;
          apiSelector.cols = selector.cols;
          apiSelector.opts = selector.opts;
          return api;
        }

        return this;
      },
      lastIndexOf: __arrayProto.lastIndexOf || function (obj, start) {
        // Bit cheeky...
        return this.indexOf.apply(this.toArray.reverse(), arguments);
      },
      length: 0,
      map: function map(fn) {
        var a = [];

        if (__arrayProto.map) {
          a = __arrayProto.map.call(this, fn, this);
        } else {
          // Compatibility for browsers without EMCA-252-5 (JS 1.6)
          for (var i = 0, ien = this.length; i < ien; i++) {
            a.push(fn.call(this, this[i], i));
          }
        }

        return new _Api2(this.context, a);
      },
      pluck: function pluck(prop) {
        return this.map(function (el) {
          return el[prop];
        });
      },
      pop: __arrayProto.pop,
      push: __arrayProto.push,
      // Does not return an API instance
      reduce: __arrayProto.reduce || function (fn, init) {
        return _fnReduce(this, fn, init, 0, this.length, 1);
      },
      reduceRight: __arrayProto.reduceRight || function (fn, init) {
        return _fnReduce(this, fn, init, this.length - 1, -1, -1);
      },
      reverse: __arrayProto.reverse,
      // Object with rows, columns and opts
      selector: null,
      shift: __arrayProto.shift,
      slice: function slice() {
        return new _Api2(this.context, this);
      },
      sort: __arrayProto.sort,
      // ? name - order?
      splice: __arrayProto.splice,
      toArray: function toArray() {
        return __arrayProto.slice.call(this);
      },
      to$: function to$() {
        return $$$1(this);
      },
      toJQuery: function toJQuery() {
        return $$$1(this);
      },
      unique: function unique() {
        return new _Api2(this.context, _unique(this));
      },
      unshift: __arrayProto.unshift
    });

    _Api2.extend = function (scope, obj, ext) {
      // Only extend API instances and static properties of the API
      if (!ext.length || !obj || !(obj instanceof _Api2) && !obj.__dt_wrapper) {
        return;
      }

      var i,
          ien,
          struct,
          methodScoping = function methodScoping(scope, fn, struc) {
        return function () {
          var ret = fn.apply(scope, arguments); // Method extension

          _Api2.extend(ret, ret, struc.methodExt);

          return ret;
        };
      };

      for (i = 0, ien = ext.length; i < ien; i++) {
        struct = ext[i]; // Value

        obj[struct.name] = typeof struct.val === 'function' ? methodScoping(scope, struct.val, struct) : $$$1.isPlainObject(struct.val) ? {} : struct.val;
        obj[struct.name].__dt_wrapper = true; // Property extension

        _Api2.extend(scope, obj[struct.name], struct.propExt);
      }
    }; // @todo - Is there need for an augment function?
    // _Api.augment = function ( inst, name )
    // {
    // 	// Find src object in the structure from the name
    // 	var parts = name.split('.');
    // 	_Api.extend( inst, obj );
    // };
    //     [
    //       {
    //         name:      'data'                -- string   - Property name
    //         val:       function () {},       -- function - Api method (or undefined if just an object
    //         methodExt: [ ... ],              -- array    - Array of Api object definitions to extend the method result
    //         propExt:   [ ... ]               -- array    - Array of Api object definitions to extend the property
    //       },
    //       {
    //         name:     'row'
    //         val:       {},
    //         methodExt: [ ... ],
    //         propExt:   [
    //           {
    //             name:      'data'
    //             val:       function () {},
    //             methodExt: [ ... ],
    //             propExt:   [ ... ]
    //           },
    //           ...
    //         ]
    //       }
    //     ]


    _Api2.register = _api_register = function _api_register(name, val) {
      if ($$$1.isArray(name)) {
        for (var j = 0, jen = name.length; j < jen; j++) {
          _Api2.register(name[j], val);
        }

        return;
      }

      var i,
          ien,
          heir = name.split('.'),
          struct = __apiStruct,
          key,
          method;

      var find = function find(src, name) {
        for (var i = 0, ien = src.length; i < ien; i++) {
          if (src[i].name === name) {
            return src[i];
          }
        }

        return null;
      };

      for (i = 0, ien = heir.length; i < ien; i++) {
        method = heir[i].indexOf('()') !== -1;
        key = method ? heir[i].replace('()', '') : heir[i];
        var src = find(struct, key);

        if (!src) {
          src = {
            name: key,
            val: {},
            methodExt: [],
            propExt: []
          };
          struct.push(src);
        }

        if (i === ien - 1) {
          src.val = val;
        } else {
          struct = method ? src.methodExt : src.propExt;
        }
      }
    };

    _Api2.registerPlural = _api_registerPlural = function _api_registerPlural(pluralName, singularName, val) {
      _Api2.register(pluralName, val);

      _Api2.register(singularName, function () {
        var ret = val.apply(this, arguments);

        if (ret === this) {
          // Returned item is the API instance that was passed in, return it
          return this;
        } else if (ret instanceof _Api2) {
          // New API instance returned, want the value from the first item
          // in the returned array for the singular result.
          return ret.length ? $$$1.isArray(ret[0]) ? new _Api2(ret.context, ret[0]) : // Array results are 'enhanced'
          ret[0] : undefined;
        } // Non-API return - just fire it back


        return ret;
      });
    };
    /**
     * Selector for HTML tables. Apply the given selector to the give array of
     * DataTables settings objects.
     *
     * @param {string|integer} [selector] jQuery selector string or integer
     * @param  {array} Array of DataTables settings objects to be filtered
     * @return {array}
     * @ignore
     */


    var __table_selector = function __table_selector(selector, a) {
      // Integer is used to pick out a table by index
      if (typeof selector === 'number') {
        return [a[selector]];
      } // Perform a jQuery selector on the table nodes


      var nodes = $$$1.map(a, function (el, i) {
        return el.nTable;
      });
      return $$$1(nodes).filter(selector).map(function (i) {
        // Need to translate back from the table node to the settings
        var idx = $$$1.inArray(this, nodes);
        return a[idx];
      }).toArray();
    };
    /**
     * Context selector for the API's context (i.e. the tables the API instance
     * refers to.
     *
     * @name    DataTable.Api#tables
     * @param {string|integer} [selector] Selector to pick which tables the iterator
     *   should operate on. If not given, all tables in the current context are
     *   used. This can be given as a jQuery selector (for example `':gt(0)'`) to
     *   select multiple tables or as an integer to select a single table.
     * @returns {DataTable.Api} Returns a new API instance if a selector is given.
     */


    _api_register('tables()', function (selector) {
      // A new instance is created if there was a selector specified
      return selector ? new _Api2(__table_selector(selector, this.context)) : this;
    });

    _api_register('table()', function (selector) {
      var tables = this.tables(selector);
      var ctx = tables.context; // Truncate to the first matched table

      return ctx.length ? new _Api2(ctx[0]) : tables;
    });

    _api_registerPlural('tables().nodes()', 'table().node()', function () {
      return this.iterator('table', function (ctx) {
        return ctx.nTable;
      }, 1);
    });

    _api_registerPlural('tables().body()', 'table().body()', function () {
      return this.iterator('table', function (ctx) {
        return ctx.nTBody;
      }, 1);
    });

    _api_registerPlural('tables().header()', 'table().header()', function () {
      return this.iterator('table', function (ctx) {
        return ctx.nTHead;
      }, 1);
    });

    _api_registerPlural('tables().footer()', 'table().footer()', function () {
      return this.iterator('table', function (ctx) {
        return ctx.nTFoot;
      }, 1);
    });

    _api_registerPlural('tables().containers()', 'table().container()', function () {
      return this.iterator('table', function (ctx) {
        return ctx.nTableWrapper;
      }, 1);
    });
    /**
     * Redraw the tables in the current context.
     */


    _api_register('draw()', function (paging) {
      return this.iterator('table', function (settings) {
        if (paging === 'page') {
          _fnDraw(settings);
        } else {
          if (typeof paging === 'string') {
            paging = paging === 'full-hold' ? false : true;
          }

          _fnReDraw(settings, paging === false);
        }
      });
    });
    /**
     * Get the current page index.
     *
     * @return {integer} Current page index (zero based)
     */

    /**
    * Set the current page.
    *
    * Note that if you attempt to show a page which does not exist, DataTables will
    * not throw an error, but rather reset the paging.
    *
    * @param {integer|string} action The paging action to take. This can be one of:
    *  * `integer` - The page index to jump to
    *  * `string` - An action to take:
    *    * `first` - Jump to first page.
    *    * `next` - Jump to the next page
    *    * `previous` - Jump to previous page
    *    * `last` - Jump to the last page.
    * @returns {DataTables.Api} this
    */


    _api_register('page()', function (action) {
      if (action === undefined) {
        return this.page.info().page; // not an expensive call
      } // else, have an action to take on all tables


      return this.iterator('table', function (settings) {
        _fnPageChange(settings, action);
      });
    });
    /**
     * Paging information for the first table in the current context.
     *
     * If you require paging information for another table, use the `table()` method
     * with a suitable selector.
     *
     * @return {object} Object with the following properties set:
     *  * `page` - Current page index (zero based - i.e. the first page is `0`)
     *  * `pages` - Total number of pages
     *  * `start` - Display index for the first record shown on the current page
     *  * `end` - Display index for the last record shown on the current page
     *  * `length` - Display length (number of records). Note that generally `start
     *    + length = end`, but this is not always true, for example if there are
     *    only 2 records to show on the final page, with a length of 10.
     *  * `recordsTotal` - Full data set length
     *  * `recordsDisplay` - Data set length once the current filtering criterion
     *    are applied.
     */


    _api_register('page.info()', function (action) {
      if (this.context.length === 0) {
        return undefined;
      }

      var settings = this.context[0],
          start = settings._iDisplayStart,
          len = settings.oFeatures.bPaginate ? settings._iDisplayLength : -1,
          visRecords = settings.fnRecordsDisplay(),
          all = len === -1;
      return {
        "page": all ? 0 : Math.floor(start / len),
        "pages": all ? 1 : Math.ceil(visRecords / len),
        "start": start,
        "end": settings.fnDisplayEnd(),
        "length": len,
        "recordsTotal": settings.fnRecordsTotal(),
        "recordsDisplay": visRecords,
        "serverSide": _fnDataSource(settings) === 'ssp'
      };
    });
    /**
     * Get the current page length.
     *
     * @return {integer} Current page length. Note `-1` indicates that all records
     *   are to be shown.
     */

    /**
    * Set the current page length.
    *
    * @param {integer} Page length to set. Use `-1` to show all records.
    * @returns {DataTables.Api} this
    */


    _api_register('page.len()', function (len) {
      // Note that we can't call this function 'length()' because `length`
      // is a Javascript property of functions which defines how many arguments
      // the function expects.
      if (len === undefined) {
        return this.context.length !== 0 ? this.context[0]._iDisplayLength : undefined;
      } // else, set the page length


      return this.iterator('table', function (settings) {
        _fnLengthChange(settings, len);
      });
    });

    var __reload = function __reload(settings, holdPosition, callback) {
      // Use the draw event to trigger a callback
      if (callback) {
        var api = new _Api2(settings);
        api.one('draw', function () {
          callback(api.ajax.json());
        });
      }

      if (_fnDataSource(settings) == 'ssp') {
        _fnReDraw(settings, holdPosition);
      } else {
        _fnProcessingDisplay(settings, true); // Cancel an existing request


        var xhr = settings.jqXHR;

        if (xhr && xhr.readyState !== 4) {
          xhr.abort();
        } // Trigger xhr


        _fnBuildAjax(settings, [], function (json) {
          _fnClearTable(settings);

          var data = _fnAjaxDataSrc(settings, json);

          for (var i = 0, ien = data.length; i < ien; i++) {
            _fnAddData(settings, data[i]);
          }

          _fnReDraw(settings, holdPosition);

          _fnProcessingDisplay(settings, false);
        });
      }
    };
    /**
     * Get the JSON response from the last Ajax request that DataTables made to the
     * server. Note that this returns the JSON from the first table in the current
     * context.
     *
     * @return {object} JSON received from the server.
     */


    _api_register('ajax.json()', function () {
      var ctx = this.context;

      if (ctx.length > 0) {
        return ctx[0].json;
      } // else return undefined;

    });
    /**
     * Get the data submitted in the last Ajax request
     */


    _api_register('ajax.params()', function () {
      var ctx = this.context;

      if (ctx.length > 0) {
        return ctx[0].oAjaxData;
      } // else return undefined;

    });
    /**
     * Reload tables from the Ajax data source. Note that this function will
     * automatically re-draw the table when the remote data has been loaded.
     *
     * @param {boolean} [reset=true] Reset (default) or hold the current paging
     *   position. A full re-sort and re-filter is performed when this method is
     *   called, which is why the pagination reset is the default action.
     * @returns {DataTables.Api} this
     */


    _api_register('ajax.reload()', function (callback, resetPaging) {
      return this.iterator('table', function (settings) {
        __reload(settings, resetPaging === false, callback);
      });
    });
    /**
     * Get the current Ajax URL. Note that this returns the URL from the first
     * table in the current context.
     *
     * @return {string} Current Ajax source URL
     */

    /**
    * Set the Ajax URL. Note that this will set the URL for all tables in the
    * current context.
    *
    * @param {string} url URL to set.
    * @returns {DataTables.Api} this
    */


    _api_register('ajax.url()', function (url) {
      var ctx = this.context;

      if (url === undefined) {
        // get
        if (ctx.length === 0) {
          return undefined;
        }

        ctx = ctx[0];
        return ctx.ajax ? $$$1.isPlainObject(ctx.ajax) ? ctx.ajax.url : ctx.ajax : ctx.sAjaxSource;
      } // set


      return this.iterator('table', function (settings) {
        if ($$$1.isPlainObject(settings.ajax)) {
          settings.ajax.url = url;
        } else {
          settings.ajax = url;
        } // No need to consider sAjaxSource here since DataTables gives priority
        // to `ajax` over `sAjaxSource`. So setting `ajax` here, renders any
        // value of `sAjaxSource` redundant.

      });
    });
    /**
     * Load data from the newly set Ajax URL. Note that this method is only
     * available when `ajax.url()` is used to set a URL. Additionally, this method
     * has the same effect as calling `ajax.reload()` but is provided for
     * convenience when setting a new URL. Like `ajax.reload()` it will
     * automatically redraw the table once the remote data has been loaded.
     *
     * @returns {DataTables.Api} this
     */


    _api_register('ajax.url().load()', function (callback, resetPaging) {
      // Same as a reload, but makes sense to present it for easy access after a
      // url change
      return this.iterator('table', function (ctx) {
        __reload(ctx, resetPaging === false, callback);
      });
    });

    var _selector_run = function _selector_run(type, selector, selectFn, settings, opts) {
      var out = [],
          res,
          a,
          i,
          ien,
          j,
          jen,
          selectorType = typeof selector; // Can't just check for isArray here, as an API or jQuery instance might be
      // given with their array like look

      if (!selector || selectorType === 'string' || selectorType === 'function' || selector.length === undefined) {
        selector = [selector];
      }

      for (i = 0, ien = selector.length; i < ien; i++) {
        // Only split on simple strings - complex expressions will be jQuery selectors
        a = selector[i] && selector[i].split && !selector[i].match(/[\[\(:]/) ? selector[i].split(',') : [selector[i]];

        for (j = 0, jen = a.length; j < jen; j++) {
          res = selectFn(typeof a[j] === 'string' ? $$$1.trim(a[j]) : a[j]);

          if (res && res.length) {
            out = out.concat(res);
          }
        }
      } // selector extensions


      var ext = _ext.selector[type];

      if (ext.length) {
        for (i = 0, ien = ext.length; i < ien; i++) {
          out = ext[i](settings, opts, out);
        }
      }

      return _unique(out);
    };

    var _selector_opts = function _selector_opts(opts) {
      if (!opts) {
        opts = {};
      } // Backwards compatibility for 1.9- which used the terminology filter rather
      // than search


      if (opts.filter && opts.search === undefined) {
        opts.search = opts.filter;
      }

      return $$$1.extend({
        search: 'none',
        order: 'current',
        page: 'all'
      }, opts);
    };

    var _selector_first = function _selector_first(inst) {
      // Reduce the API instance to the first item found
      for (var i = 0, ien = inst.length; i < ien; i++) {
        if (inst[i].length > 0) {
          // Assign the first element to the first item in the instance
          // and truncate the instance and context
          inst[0] = inst[i];
          inst[0].length = 1;
          inst.length = 1;
          inst.context = [inst.context[i]];
          return inst;
        }
      } // Not found - return an empty instance


      inst.length = 0;
      return inst;
    };

    var _selector_row_indexes = function _selector_row_indexes(settings, opts) {
      var i,
          ien,
          tmp,
          a = [],
          displayFiltered = settings.aiDisplay,
          displayMaster = settings.aiDisplayMaster;
      var search = opts.search,
          // none, applied, removed
      order = opts.order,
          // applied, current, index (original - compatibility with 1.9)
      page = opts.page; // all, current

      if (_fnDataSource(settings) == 'ssp') {
        // In server-side processing mode, most options are irrelevant since
        // rows not shown don't exist and the index order is the applied order
        // Removed is a special case - for consistency just return an empty
        // array
        return search === 'removed' ? [] : _range(0, displayMaster.length);
      } else if (page == 'current') {
        // Current page implies that order=current and fitler=applied, since it is
        // fairly senseless otherwise, regardless of what order and search actually
        // are
        for (i = settings._iDisplayStart, ien = settings.fnDisplayEnd(); i < ien; i++) {
          a.push(displayFiltered[i]);
        }
      } else if (order == 'current' || order == 'applied') {
        if (search == 'none') {
          a = displayMaster.slice();
        } else if (search == 'applied') {
          a = displayFiltered.slice();
        } else if (search == 'removed') {
          // O(n+m) solution by creating a hash map
          var displayFilteredMap = {};

          for (var i = 0, ien = displayFiltered.length; i < ien; i++) {
            displayFilteredMap[displayFiltered[i]] = null;
          }

          a = $$$1.map(displayMaster, function (el) {
            return !displayFilteredMap.hasOwnProperty(el) ? el : null;
          });
        }
      } else if (order == 'index' || order == 'original') {
        for (i = 0, ien = settings.aoData.length; i < ien; i++) {
          if (search == 'none') {
            a.push(i);
          } else {
            // applied | removed
            tmp = $$$1.inArray(i, displayFiltered);

            if (tmp === -1 && search == 'removed' || tmp >= 0 && search == 'applied') {
              a.push(i);
            }
          }
        }
      }

      return a;
    };
    /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
     * Rows
     *
     * {}          - no selector - use all available rows
     * {integer}   - row aoData index
     * {node}      - TR node
     * {string}    - jQuery selector to apply to the TR elements
     * {array}     - jQuery array of nodes, or simply an array of TR nodes
     *
     */


    var __row_selector = function __row_selector(settings, selector, opts) {
      var rows;

      var run = function run(sel) {
        var selInt = _intVal(sel);
        var aoData = settings.aoData; // Short cut - selector is a number and no options provided (default is
        // all records, so no need to check if the index is in there, since it
        // must be - dev error if the index doesn't exist).

        if (selInt !== null && !opts) {
          return [selInt];
        }

        if (!rows) {
          rows = _selector_row_indexes(settings, opts);
        }

        if (selInt !== null && $$$1.inArray(selInt, rows) !== -1) {
          // Selector - integer
          return [selInt];
        } else if (sel === null || sel === undefined || sel === '') {
          // Selector - none
          return rows;
        } // Selector - function


        if (typeof sel === 'function') {
          return $$$1.map(rows, function (idx) {
            var row = aoData[idx];
            return sel(idx, row._aData, row.nTr) ? idx : null;
          });
        } // Selector - node


        if (sel.nodeName) {
          var rowIdx = sel._DT_RowIndex; // Property added by DT for fast lookup

          var cellIdx = sel._DT_CellIndex;

          if (rowIdx !== undefined) {
            // Make sure that the row is actually still present in the table
            return aoData[rowIdx] && aoData[rowIdx].nTr === sel ? [rowIdx] : [];
          } else if (cellIdx) {
            return aoData[cellIdx.row] && aoData[cellIdx.row].nTr === sel ? [cellIdx.row] : [];
          } else {
            var host = $$$1(sel).closest('*[data-dt-row]');
            return host.length ? [host.data('dt-row')] : [];
          }
        } // ID selector. Want to always be able to select rows by id, regardless
        // of if the tr element has been created or not, so can't rely upon
        // jQuery here - hence a custom implementation. This does not match
        // Sizzle's fast selector or HTML4 - in HTML5 the ID can be anything,
        // but to select it using a CSS selector engine (like Sizzle or
        // querySelect) it would need to need to be escaped for some characters.
        // DataTables simplifies this for row selectors since you can select
        // only a row. A # indicates an id any anything that follows is the id -
        // unescaped.


        if (typeof sel === 'string' && sel.charAt(0) === '#') {
          // get row index from id
          var rowObj = settings.aIds[sel.replace(/^#/, '')];

          if (rowObj !== undefined) {
            return [rowObj.idx];
          } // need to fall through to jQuery in case there is DOM id that
          // matches

        } // Get nodes in the order from the `rows` array with null values removed


        var nodes = _removeEmpty(_pluck_order(settings.aoData, rows, 'nTr')); // Selector - jQuery selector string, array of nodes or jQuery object/
        // As jQuery's .filter() allows jQuery objects to be passed in filter,
        // it also allows arrays, so this will cope with all three options


        return $$$1(nodes).filter(sel).map(function () {
          return this._DT_RowIndex;
        }).toArray();
      };

      return _selector_run('row', selector, run, settings, opts);
    };

    _api_register('rows()', function (selector, opts) {
      // argument shifting
      if (selector === undefined) {
        selector = '';
      } else if ($$$1.isPlainObject(selector)) {
        opts = selector;
        selector = '';
      }

      opts = _selector_opts(opts);
      var inst = this.iterator('table', function (settings) {
        return __row_selector(settings, selector, opts);
      }, 1); // Want argument shifting here and in __row_selector?

      inst.selector.rows = selector;
      inst.selector.opts = opts;
      return inst;
    });

    _api_register('rows().nodes()', function () {
      return this.iterator('row', function (settings, row) {
        return settings.aoData[row].nTr || undefined;
      }, 1);
    });

    _api_register('rows().data()', function () {
      return this.iterator(true, 'rows', function (settings, rows) {
        return _pluck_order(settings.aoData, rows, '_aData');
      }, 1);
    });

    _api_registerPlural('rows().cache()', 'row().cache()', function (type) {
      return this.iterator('row', function (settings, row) {
        var r = settings.aoData[row];
        return type === 'search' ? r._aFilterData : r._aSortData;
      }, 1);
    });

    _api_registerPlural('rows().invalidate()', 'row().invalidate()', function (src) {
      return this.iterator('row', function (settings, row) {
        _fnInvalidate(settings, row, src);
      });
    });

    _api_registerPlural('rows().indexes()', 'row().index()', function () {
      return this.iterator('row', function (settings, row) {
        return row;
      }, 1);
    });

    _api_registerPlural('rows().ids()', 'row().id()', function (hash) {
      var a = [];
      var context = this.context; // `iterator` will drop undefined values, but in this case we want them

      for (var i = 0, ien = context.length; i < ien; i++) {
        for (var j = 0, jen = this[i].length; j < jen; j++) {
          var id = context[i].rowIdFn(context[i].aoData[this[i][j]]._aData);
          a.push((hash === true ? '#' : '') + id);
        }
      }

      return new _Api2(context, a);
    });

    _api_registerPlural('rows().remove()', 'row().remove()', function () {
      var that = this;
      this.iterator('row', function (settings, row, thatIdx) {
        var data = settings.aoData;
        var rowData = data[row];
        var i, ien, j, jen;
        var loopRow, loopCells;
        data.splice(row, 1); // Update the cached indexes

        for (i = 0, ien = data.length; i < ien; i++) {
          loopRow = data[i];
          loopCells = loopRow.anCells; // Rows

          if (loopRow.nTr !== null) {
            loopRow.nTr._DT_RowIndex = i;
          } // Cells


          if (loopCells !== null) {
            for (j = 0, jen = loopCells.length; j < jen; j++) {
              loopCells[j]._DT_CellIndex.row = i;
            }
          }
        } // Delete from the display arrays


        _fnDeleteIndex(settings.aiDisplayMaster, row);

        _fnDeleteIndex(settings.aiDisplay, row);

        _fnDeleteIndex(that[thatIdx], row, false); // maintain local indexes
        // For server-side processing tables - subtract the deleted row from the count


        if (settings._iRecordsDisplay > 0) {
          settings._iRecordsDisplay--;
        } // Check for an 'overflow' they case for displaying the table


        _fnLengthOverflow(settings); // Remove the row's ID reference if there is one


        var id = settings.rowIdFn(rowData._aData);

        if (id !== undefined) {
          delete settings.aIds[id];
        }
      });
      this.iterator('table', function (settings) {
        for (var i = 0, ien = settings.aoData.length; i < ien; i++) {
          settings.aoData[i].idx = i;
        }
      });
      return this;
    });

    _api_register('rows.add()', function (rows) {
      var newRows = this.iterator('table', function (settings) {
        var row, i, ien;
        var out = [];

        for (i = 0, ien = rows.length; i < ien; i++) {
          row = rows[i];

          if (row.nodeName && row.nodeName.toUpperCase() === 'TR') {
            out.push(_fnAddTr(settings, row)[0]);
          } else {
            out.push(_fnAddData(settings, row));
          }
        }

        return out;
      }, 1); // Return an Api.rows() extended instance, so rows().nodes() etc can be used

      var modRows = this.rows(-1);
      modRows.pop();
      $$$1.merge(modRows, newRows);
      return modRows;
    });
    /**
     *
     */


    _api_register('row()', function (selector, opts) {
      return _selector_first(this.rows(selector, opts));
    });

    _api_register('row().data()', function (data) {
      var ctx = this.context;

      if (data === undefined) {
        // Get
        return ctx.length && this.length ? ctx[0].aoData[this[0]]._aData : undefined;
      } // Set


      var row = ctx[0].aoData[this[0]];
      row._aData = data; // If the DOM has an id, and the data source is an array

      if ($$$1.isArray(data) && row.nTr.id) {
        _fnSetObjectDataFn(ctx[0].rowId)(data, row.nTr.id);
      } // Automatically invalidate


      _fnInvalidate(ctx[0], this[0], 'data');

      return this;
    });

    _api_register('row().node()', function () {
      var ctx = this.context;
      return ctx.length && this.length ? ctx[0].aoData[this[0]].nTr || null : null;
    });

    _api_register('row.add()', function (row) {
      // Allow a jQuery object to be passed in - only a single row is added from
      // it though - the first element in the set
      if (row instanceof $$$1 && row.length) {
        row = row[0];
      }

      var rows = this.iterator('table', function (settings) {
        if (row.nodeName && row.nodeName.toUpperCase() === 'TR') {
          return _fnAddTr(settings, row)[0];
        }

        return _fnAddData(settings, row);
      }); // Return an Api.rows() extended instance, with the newly added row selected

      return this.row(rows[0]);
    });

    var __details_add = function __details_add(ctx, row, data, klass) {
      // Convert to array of TR elements
      var rows = [];

      var addRow = function addRow(r, k) {
        // Recursion to allow for arrays of jQuery objects
        if ($$$1.isArray(r) || r instanceof $$$1) {
          for (var i = 0, ien = r.length; i < ien; i++) {
            addRow(r[i], k);
          }

          return;
        } // If we get a TR element, then just add it directly - up to the dev
        // to add the correct number of columns etc


        if (r.nodeName && r.nodeName.toLowerCase() === 'tr') {
          rows.push(r);
        } else {
          // Otherwise create a row with a wrapper
          var created = $$$1('<tr><td/></tr>').addClass(k);
          $$$1('td', created).addClass(k).html(r)[0].colSpan = _fnVisbleColumns(ctx);
          rows.push(created[0]);
        }
      };

      addRow(data, klass);

      if (row._details) {
        row._details.detach();
      }

      row._details = $$$1(rows); // If the children were already shown, that state should be retained

      if (row._detailsShow) {
        row._details.insertAfter(row.nTr);
      }
    };

    var __details_remove = function __details_remove(api, idx) {
      var ctx = api.context;

      if (ctx.length) {
        var row = ctx[0].aoData[idx !== undefined ? idx : api[0]];

        if (row && row._details) {
          row._details.remove();

          row._detailsShow = undefined;
          row._details = undefined;
        }
      }
    };

    var __details_display = function __details_display(api, show) {
      var ctx = api.context;

      if (ctx.length && api.length) {
        var row = ctx[0].aoData[api[0]];

        if (row._details) {
          row._detailsShow = show;

          if (show) {
            row._details.insertAfter(row.nTr);
          } else {
            row._details.detach();
          }

          __details_events(ctx[0]);
        }
      }
    };

    var __details_events = function __details_events(settings) {
      var api = new _Api2(settings);
      var namespace = '.dt.DT_details';
      var drawEvent = 'draw' + namespace;
      var colvisEvent = 'column-visibility' + namespace;
      var destroyEvent = 'destroy' + namespace;
      var data = settings.aoData;
      api.off(drawEvent + ' ' + colvisEvent + ' ' + destroyEvent);

      if (_pluck(data, '_details').length > 0) {
        // On each draw, insert the required elements into the document
        api.on(drawEvent, function (e, ctx) {
          if (settings !== ctx) {
            return;
          }

          api.rows({
            page: 'current'
          }).eq(0).each(function (idx) {
            // Internal data grab
            var row = data[idx];

            if (row._detailsShow) {
              row._details.insertAfter(row.nTr);
            }
          });
        }); // Column visibility change - update the colspan

        api.on(colvisEvent, function (e, ctx, idx, vis) {
          if (settings !== ctx) {
            return;
          } // Update the colspan for the details rows (note, only if it already has
          // a colspan)


          var row,
              visible = _fnVisbleColumns(ctx);

          for (var i = 0, ien = data.length; i < ien; i++) {
            row = data[i];

            if (row._details) {
              row._details.children('td[colspan]').attr('colspan', visible);
            }
          }
        }); // Table destroyed - nuke any child rows

        api.on(destroyEvent, function (e, ctx) {
          if (settings !== ctx) {
            return;
          }

          for (var i = 0, ien = data.length; i < ien; i++) {
            if (data[i]._details) {
              __details_remove(api, i);
            }
          }
        });
      }
    }; // Strings for the method names to help minification


    var _emp = '';

    var _child_obj = _emp + 'row().child';

    var _child_mth = _child_obj + '()'; // data can be:
    //  tr
    //  string
    //  jQuery or array of any of the above


    _api_register(_child_mth, function (data, klass) {
      var ctx = this.context;

      if (data === undefined) {
        // get
        return ctx.length && this.length ? ctx[0].aoData[this[0]]._details : undefined;
      } else if (data === true) {
        // show
        this.child.show();
      } else if (data === false) {
        // remove
        __details_remove(this);
      } else if (ctx.length && this.length) {
        // set
        __details_add(ctx[0], ctx[0].aoData[this[0]], data, klass);
      }

      return this;
    });

    _api_register([_child_obj + '.show()', _child_mth + '.show()' // only when `child()` was called with parameters (without
    ], function (show) {
      // it returns an object and this method is not executed)
      __details_display(this, true);

      return this;
    });

    _api_register([_child_obj + '.hide()', _child_mth + '.hide()' // only when `child()` was called with parameters (without
    ], function () {
      // it returns an object and this method is not executed)
      __details_display(this, false);

      return this;
    });

    _api_register([_child_obj + '.remove()', _child_mth + '.remove()' // only when `child()` was called with parameters (without
    ], function () {
      // it returns an object and this method is not executed)
      __details_remove(this);

      return this;
    });

    _api_register(_child_obj + '.isShown()', function () {
      var ctx = this.context;

      if (ctx.length && this.length) {
        // _detailsShown as false or undefined will fall through to return false
        return ctx[0].aoData[this[0]]._detailsShow || false;
      }

      return false;
    });
    /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
     * Columns
     *
     * {integer}           - column index (>=0 count from left, <0 count from right)
     * "{integer}:visIdx"  - visible column index (i.e. translate to column index)  (>=0 count from left, <0 count from right)
     * "{integer}:visible" - alias for {integer}:visIdx  (>=0 count from left, <0 count from right)
     * "{string}:name"     - column name
     * "{string}"          - jQuery selector on column header nodes
     *
     */
    // can be an array of these items, comma separated list, or an array of comma
    // separated lists


    var __re_column_selector = /^([^:]+):(name|visIdx|visible)$/; // r1 and r2 are redundant - but it means that the parameters match for the
    // iterator callback in columns().data()

    var __columnData = function __columnData(settings, column, r1, r2, rows) {
      var a = [];

      for (var row = 0, ien = rows.length; row < ien; row++) {
        a.push(_fnGetCellData(settings, rows[row], column));
      }

      return a;
    };

    var __column_selector = function __column_selector(settings, selector, opts) {
      var columns = settings.aoColumns,
          names = _pluck(columns, 'sName'),
          nodes = _pluck(columns, 'nTh');

      var run = function run(s) {
        var selInt = _intVal(s); // Selector - all


        if (s === '') {
          return _range(columns.length);
        } // Selector - index


        if (selInt !== null) {
          return [selInt >= 0 ? selInt : // Count from left
          columns.length + selInt // Count from right (+ because its a negative value)
          ];
        } // Selector = function


        if (typeof s === 'function') {
          var rows = _selector_row_indexes(settings, opts);

          return $$$1.map(columns, function (col, idx) {
            return s(idx, __columnData(settings, idx, 0, 0, rows), nodes[idx]) ? idx : null;
          });
        } // jQuery or string selector


        var match = typeof s === 'string' ? s.match(__re_column_selector) : '';

        if (match) {
          switch (match[2]) {
            case 'visIdx':
            case 'visible':
              var idx = parseInt(match[1], 10); // Visible index given, convert to column index

              if (idx < 0) {
                // Counting from the right
                var visColumns = $$$1.map(columns, function (col, i) {
                  return col.bVisible ? i : null;
                });
                return [visColumns[visColumns.length + idx]];
              } // Counting from the left


              return [_fnVisibleToColumnIndex(settings, idx)];

            case 'name':
              // match by name. `names` is column index complete and in order
              return $$$1.map(names, function (name, i) {
                return name === match[1] ? i : null;
              });

            default:
              return [];
          }
        } // Cell in the table body


        if (s.nodeName && s._DT_CellIndex) {
          return [s._DT_CellIndex.column];
        } // jQuery selector on the TH elements for the columns


        var jqResult = $$$1(nodes).filter(s).map(function () {
          return $$$1.inArray(this, nodes); // `nodes` is column index complete and in order
        }).toArray();

        if (jqResult.length || !s.nodeName) {
          return jqResult;
        } // Otherwise a node which might have a `dt-column` data attribute, or be
        // a child or such an element


        var host = $$$1(s).closest('*[data-dt-column]');
        return host.length ? [host.data('dt-column')] : [];
      };

      return _selector_run('column', selector, run, settings, opts);
    };

    var __setColumnVis = function __setColumnVis(settings, column, vis) {
      var cols = settings.aoColumns,
          col = cols[column],
          data = settings.aoData,
          cells,
          i,
          ien,
          tr; // Get

      if (vis === undefined) {
        return col.bVisible;
      } // Set
      // No change


      if (col.bVisible === vis) {
        return;
      }

      if (vis) {
        // Insert column
        // Need to decide if we should use appendChild or insertBefore
        var insertBefore = $$$1.inArray(true, _pluck(cols, 'bVisible'), column + 1);

        for (i = 0, ien = data.length; i < ien; i++) {
          tr = data[i].nTr;
          cells = data[i].anCells;

          if (tr) {
            // insertBefore can act like appendChild if 2nd arg is null
            tr.insertBefore(cells[column], cells[insertBefore] || null);
          }
        }
      } else {
        // Remove column
        $$$1(_pluck(settings.aoData, 'anCells', column)).detach();
      } // Common actions


      col.bVisible = vis;

      _fnDrawHead(settings, settings.aoHeader);

      _fnDrawHead(settings, settings.aoFooter); // Update colspan for no records display. Child rows and extensions will use their own
      // listeners to do this - only need to update the empty table item here


      if (!settings.aiDisplay.length) {
        $$$1(settings.nTBody).find('td[colspan]').attr('colspan', _fnVisbleColumns(settings));
      }

      _fnSaveState(settings);
    };

    _api_register('columns()', function (selector, opts) {
      // argument shifting
      if (selector === undefined) {
        selector = '';
      } else if ($$$1.isPlainObject(selector)) {
        opts = selector;
        selector = '';
      }

      opts = _selector_opts(opts);
      var inst = this.iterator('table', function (settings) {
        return __column_selector(settings, selector, opts);
      }, 1); // Want argument shifting here and in _row_selector?

      inst.selector.cols = selector;
      inst.selector.opts = opts;
      return inst;
    });

    _api_registerPlural('columns().header()', 'column().header()', function (selector, opts) {
      return this.iterator('column', function (settings, column) {
        return settings.aoColumns[column].nTh;
      }, 1);
    });

    _api_registerPlural('columns().footer()', 'column().footer()', function (selector, opts) {
      return this.iterator('column', function (settings, column) {
        return settings.aoColumns[column].nTf;
      }, 1);
    });

    _api_registerPlural('columns().data()', 'column().data()', function () {
      return this.iterator('column-rows', __columnData, 1);
    });

    _api_registerPlural('columns().dataSrc()', 'column().dataSrc()', function () {
      return this.iterator('column', function (settings, column) {
        return settings.aoColumns[column].mData;
      }, 1);
    });

    _api_registerPlural('columns().cache()', 'column().cache()', function (type) {
      return this.iterator('column-rows', function (settings, column, i, j, rows) {
        return _pluck_order(settings.aoData, rows, type === 'search' ? '_aFilterData' : '_aSortData', column);
      }, 1);
    });

    _api_registerPlural('columns().nodes()', 'column().nodes()', function () {
      return this.iterator('column-rows', function (settings, column, i, j, rows) {
        return _pluck_order(settings.aoData, rows, 'anCells', column);
      }, 1);
    });

    _api_registerPlural('columns().visible()', 'column().visible()', function (vis, calc) {
      var ret = this.iterator('column', function (settings, column) {
        if (vis === undefined) {
          return settings.aoColumns[column].bVisible;
        } // else


        __setColumnVis(settings, column, vis);
      }); // Group the column visibility changes

      if (vis !== undefined) {
        // Second loop once the first is done for events
        this.iterator('column', function (settings, column) {
          _fnCallbackFire(settings, null, 'column-visibility', [settings, column, vis, calc]);
        });

        if (calc === undefined || calc) {
          this.columns.adjust();
        }
      }

      return ret;
    });

    _api_registerPlural('columns().indexes()', 'column().index()', function (type) {
      return this.iterator('column', function (settings, column) {
        return type === 'visible' ? _fnColumnIndexToVisible(settings, column) : column;
      }, 1);
    });

    _api_register('columns.adjust()', function () {
      return this.iterator('table', function (settings) {
        _fnAdjustColumnSizing(settings);
      }, 1);
    });

    _api_register('column.index()', function (type, idx) {
      if (this.context.length !== 0) {
        var ctx = this.context[0];

        if (type === 'fromVisible' || type === 'toData') {
          return _fnVisibleToColumnIndex(ctx, idx);
        } else if (type === 'fromData' || type === 'toVisible') {
          return _fnColumnIndexToVisible(ctx, idx);
        }
      }
    });

    _api_register('column()', function (selector, opts) {
      return _selector_first(this.columns(selector, opts));
    });

    var __cell_selector = function __cell_selector(settings, selector, opts) {
      var data = settings.aoData;

      var rows = _selector_row_indexes(settings, opts);

      var cells = _removeEmpty(_pluck_order(data, rows, 'anCells'));

      var allCells = $$$1([].concat.apply([], cells));
      var row;
      var columns = settings.aoColumns.length;
      var a, i, ien, j, o, host;

      var run = function run(s) {
        var fnSelector = typeof s === 'function';

        if (s === null || s === undefined || fnSelector) {
          // All cells and function selectors
          a = [];

          for (i = 0, ien = rows.length; i < ien; i++) {
            row = rows[i];

            for (j = 0; j < columns; j++) {
              o = {
                row: row,
                column: j
              };

              if (fnSelector) {
                // Selector - function
                host = data[row];

                if (s(o, _fnGetCellData(settings, row, j), host.anCells ? host.anCells[j] : null)) {
                  a.push(o);
                }
              } else {
                // Selector - all
                a.push(o);
              }
            }
          }

          return a;
        } // Selector - index


        if ($$$1.isPlainObject(s)) {
          // Valid cell index and its in the array of selectable rows
          return s.column !== undefined && s.row !== undefined && $$$1.inArray(s.row, rows) !== -1 ? [s] : [];
        } // Selector - jQuery filtered cells


        var jqResult = allCells.filter(s).map(function (i, el) {
          return {
            // use a new object, in case someone changes the values
            row: el._DT_CellIndex.row,
            column: el._DT_CellIndex.column
          };
        }).toArray();

        if (jqResult.length || !s.nodeName) {
          return jqResult;
        } // Otherwise the selector is a node, and there is one last option - the
        // element might be a child of an element which has dt-row and dt-column
        // data attributes


        host = $$$1(s).closest('*[data-dt-row]');
        return host.length ? [{
          row: host.data('dt-row'),
          column: host.data('dt-column')
        }] : [];
      };

      return _selector_run('cell', selector, run, settings, opts);
    };

    _api_register('cells()', function (rowSelector, columnSelector, opts) {
      // Argument shifting
      if ($$$1.isPlainObject(rowSelector)) {
        // Indexes
        if (rowSelector.row === undefined) {
          // Selector options in first parameter
          opts = rowSelector;
          rowSelector = null;
        } else {
          // Cell index objects in first parameter
          opts = columnSelector;
          columnSelector = null;
        }
      }

      if ($$$1.isPlainObject(columnSelector)) {
        opts = columnSelector;
        columnSelector = null;
      } // Cell selector


      if (columnSelector === null || columnSelector === undefined) {
        return this.iterator('table', function (settings) {
          return __cell_selector(settings, rowSelector, _selector_opts(opts));
        });
      } // Row + column selector


      var columns = this.columns(columnSelector);
      var rows = this.rows(rowSelector);
      var a, i, ien, j, jen;
      this.iterator('table', function (settings, idx) {
        a = [];

        for (i = 0, ien = rows[idx].length; i < ien; i++) {
          for (j = 0, jen = columns[idx].length; j < jen; j++) {
            a.push({
              row: rows[idx][i],
              column: columns[idx][j]
            });
          }
        }
      }, 1); // Now pass through the cell selector for options

      var cells = this.cells(a, opts);
      $$$1.extend(cells.selector, {
        cols: columnSelector,
        rows: rowSelector,
        opts: opts
      });
      return cells;
    });

    _api_registerPlural('cells().nodes()', 'cell().node()', function () {
      return this.iterator('cell', function (settings, row, column) {
        var data = settings.aoData[row];
        return data && data.anCells ? data.anCells[column] : undefined;
      }, 1);
    });

    _api_register('cells().data()', function () {
      return this.iterator('cell', function (settings, row, column) {
        return _fnGetCellData(settings, row, column);
      }, 1);
    });

    _api_registerPlural('cells().cache()', 'cell().cache()', function (type) {
      type = type === 'search' ? '_aFilterData' : '_aSortData';
      return this.iterator('cell', function (settings, row, column) {
        return settings.aoData[row][type][column];
      }, 1);
    });

    _api_registerPlural('cells().render()', 'cell().render()', function (type) {
      return this.iterator('cell', function (settings, row, column) {
        return _fnGetCellData(settings, row, column, type);
      }, 1);
    });

    _api_registerPlural('cells().indexes()', 'cell().index()', function () {
      return this.iterator('cell', function (settings, row, column) {
        return {
          row: row,
          column: column,
          columnVisible: _fnColumnIndexToVisible(settings, column)
        };
      }, 1);
    });

    _api_registerPlural('cells().invalidate()', 'cell().invalidate()', function (src) {
      return this.iterator('cell', function (settings, row, column) {
        _fnInvalidate(settings, row, src, column);
      });
    });

    _api_register('cell()', function (rowSelector, columnSelector, opts) {
      return _selector_first(this.cells(rowSelector, columnSelector, opts));
    });

    _api_register('cell().data()', function (data) {
      var ctx = this.context;
      var cell = this[0];

      if (data === undefined) {
        // Get
        return ctx.length && cell.length ? _fnGetCellData(ctx[0], cell[0].row, cell[0].column) : undefined;
      } // Set


      _fnSetCellData(ctx[0], cell[0].row, cell[0].column, data);

      _fnInvalidate(ctx[0], cell[0].row, 'data', cell[0].column);

      return this;
    });
    /**
     * Get current ordering (sorting) that has been applied to the table.
     *
     * @returns {array} 2D array containing the sorting information for the first
     *   table in the current context. Each element in the parent array represents
     *   a column being sorted upon (i.e. multi-sorting with two columns would have
     *   2 inner arrays). The inner arrays may have 2 or 3 elements. The first is
     *   the column index that the sorting condition applies to, the second is the
     *   direction of the sort (`desc` or `asc`) and, optionally, the third is the
     *   index of the sorting order from the `column.sorting` initialisation array.
     */

    /**
    * Set the ordering for the table.
    *
    * @param {integer} order Column index to sort upon.
    * @param {string} direction Direction of the sort to be applied (`asc` or `desc`)
    * @returns {DataTables.Api} this
    */

    /**
    * Set the ordering for the table.
    *
    * @param {array} order 1D array of sorting information to be applied.
    * @param {array} [...] Optional additional sorting conditions
    * @returns {DataTables.Api} this
    */

    /**
    * Set the ordering for the table.
    *
    * @param {array} order 2D array of sorting information to be applied.
    * @returns {DataTables.Api} this
    */


    _api_register('order()', function (order, dir) {
      var ctx = this.context;

      if (order === undefined) {
        // get
        return ctx.length !== 0 ? ctx[0].aaSorting : undefined;
      } // set


      if (typeof order === 'number') {
        // Simple column / direction passed in
        order = [[order, dir]];
      } else if (order.length && !$$$1.isArray(order[0])) {
        // Arguments passed in (list of 1D arrays)
        order = Array.prototype.slice.call(arguments);
      } // otherwise a 2D array was passed in


      return this.iterator('table', function (settings) {
        settings.aaSorting = order.slice();
      });
    });
    /**
     * Attach a sort listener to an element for a given column
     *
     * @param {node|jQuery|string} node Identifier for the element(s) to attach the
     *   listener to. This can take the form of a single DOM node, a jQuery
     *   collection of nodes or a jQuery selector which will identify the node(s).
     * @param {integer} column the column that a click on this node will sort on
     * @param {function} [callback] callback function when sort is run
     * @returns {DataTables.Api} this
     */


    _api_register('order.listener()', function (node, column, callback) {
      return this.iterator('table', function (settings) {
        _fnSortAttachListener(settings, node, column, callback);
      });
    });

    _api_register('order.fixed()', function (set) {
      if (!set) {
        var ctx = this.context;
        var fixed = ctx.length ? ctx[0].aaSortingFixed : undefined;
        return $$$1.isArray(fixed) ? {
          pre: fixed
        } : fixed;
      }

      return this.iterator('table', function (settings) {
        settings.aaSortingFixed = $$$1.extend(true, {}, set);
      });
    }); // Order by the selected column(s)


    _api_register(['columns().order()', 'column().order()'], function (dir) {
      var that = this;
      return this.iterator('table', function (settings, i) {
        var sort = [];
        $$$1.each(that[i], function (j, col) {
          sort.push([col, dir]);
        });
        settings.aaSorting = sort;
      });
    });

    _api_register('search()', function (input, regex, smart, caseInsen) {
      var ctx = this.context;

      if (input === undefined) {
        // get
        return ctx.length !== 0 ? ctx[0].oPreviousSearch.sSearch : undefined;
      } // set


      return this.iterator('table', function (settings) {
        if (!settings.oFeatures.bFilter) {
          return;
        }

        _fnFilterComplete(settings, $$$1.extend({}, settings.oPreviousSearch, {
          "sSearch": input + "",
          "bRegex": regex === null ? false : regex,
          "bSmart": smart === null ? true : smart,
          "bCaseInsensitive": caseInsen === null ? true : caseInsen
        }), 1);
      });
    });

    _api_registerPlural('columns().search()', 'column().search()', function (input, regex, smart, caseInsen) {
      return this.iterator('column', function (settings, column) {
        var preSearch = settings.aoPreSearchCols;

        if (input === undefined) {
          // get
          return preSearch[column].sSearch;
        } // set


        if (!settings.oFeatures.bFilter) {
          return;
        }

        $$$1.extend(preSearch[column], {
          "sSearch": input + "",
          "bRegex": regex === null ? false : regex,
          "bSmart": smart === null ? true : smart,
          "bCaseInsensitive": caseInsen === null ? true : caseInsen
        });

        _fnFilterComplete(settings, settings.oPreviousSearch, 1);
      });
    });
    /*
     * State API methods
     */


    _api_register('state()', function () {
      return this.context.length ? this.context[0].oSavedState : null;
    });

    _api_register('state.clear()', function () {
      return this.iterator('table', function (settings) {
        // Save an empty object
        settings.fnStateSaveCallback.call(settings.oInstance, settings, {});
      });
    });

    _api_register('state.loaded()', function () {
      return this.context.length ? this.context[0].oLoadedState : null;
    });

    _api_register('state.save()', function () {
      return this.iterator('table', function (settings) {
        _fnSaveState(settings);
      });
    });
    /**
     * Provide a common method for plug-ins to check the version of DataTables being
     * used, in order to ensure compatibility.
     *
     *  @param {string} version Version string to check for, in the format "X.Y.Z".
     *    Note that the formats "X" and "X.Y" are also acceptable.
     *  @returns {boolean} true if this version of DataTables is greater or equal to
     *    the required version, or false if this version of DataTales is not
     *    suitable
     *  @static
     *  @dtopt API-Static
     *
     *  @example
     *    alert( $.fn.dataTable.versionCheck( '1.9.0' ) );
     */


    DataTable.versionCheck = DataTable.fnVersionCheck = function (version) {
      var aThis = DataTable.version.split('.');
      var aThat = version.split('.');
      var iThis, iThat;

      for (var i = 0, iLen = aThat.length; i < iLen; i++) {
        iThis = parseInt(aThis[i], 10) || 0;
        iThat = parseInt(aThat[i], 10) || 0; // Parts are the same, keep comparing

        if (iThis === iThat) {
          continue;
        } // Parts are different, return immediately


        return iThis > iThat;
      }

      return true;
    };
    /**
     * Check if a `<table>` node is a DataTable table already or not.
     *
     *  @param {node|jquery|string} table Table node, jQuery object or jQuery
     *      selector for the table to test. Note that if more than more than one
     *      table is passed on, only the first will be checked
     *  @returns {boolean} true the table given is a DataTable, or false otherwise
     *  @static
     *  @dtopt API-Static
     *
     *  @example
     *    if ( ! $.fn.DataTable.isDataTable( '#example' ) ) {
     *      $('#example').dataTable();
     *    }
     */


    DataTable.isDataTable = DataTable.fnIsDataTable = function (table) {
      var t = $$$1(table).get(0);
      var is = false;

      if (table instanceof DataTable.Api) {
        return true;
      }

      $$$1.each(DataTable.settings, function (i, o) {
        var head = o.nScrollHead ? $$$1('table', o.nScrollHead)[0] : null;
        var foot = o.nScrollFoot ? $$$1('table', o.nScrollFoot)[0] : null;

        if (o.nTable === t || head === t || foot === t) {
          is = true;
        }
      });
      return is;
    };
    /**
     * Get all DataTable tables that have been initialised - optionally you can
     * select to get only currently visible tables.
     *
     *  @param {boolean} [visible=false] Flag to indicate if you want all (default)
     *    or visible tables only.
     *  @returns {array} Array of `table` nodes (not DataTable instances) which are
     *    DataTables
     *  @static
     *  @dtopt API-Static
     *
     *  @example
     *    $.each( $.fn.dataTable.tables(true), function () {
     *      $(table).DataTable().columns.adjust();
     *    } );
     */


    DataTable.tables = DataTable.fnTables = function (visible) {
      var api = false;

      if ($$$1.isPlainObject(visible)) {
        api = visible.api;
        visible = visible.visible;
      }

      var a = $$$1.map(DataTable.settings, function (o) {
        if (!visible || visible && $$$1(o.nTable).is(':visible')) {
          return o.nTable;
        }
      });
      return api ? new _Api2(a) : a;
    };
    /**
     * Convert from camel case parameters to Hungarian notation. This is made public
     * for the extensions to provide the same ability as DataTables core to accept
     * either the 1.9 style Hungarian notation, or the 1.10+ style camelCase
     * parameters.
     *
     *  @param {object} src The model object which holds all parameters that can be
     *    mapped.
     *  @param {object} user The object to convert from camel case to Hungarian.
     *  @param {boolean} force When set to `true`, properties which already have a
     *    Hungarian value in the `user` object will be overwritten. Otherwise they
     *    won't be.
     */


    DataTable.camelToHungarian = _fnCamelToHungarian;
    /**
     *
     */

    _api_register('$()', function (selector, opts) {
      var rows = this.rows(opts).nodes(),
          // Get all rows
      jqRows = $$$1(rows);
      return $$$1([].concat(jqRows.filter(selector).toArray(), jqRows.find(selector).toArray()));
    }); // jQuery functions to operate on the tables


    $$$1.each(['on', 'one', 'off'], function (i, key) {
      _api_register(key + '()', function ()
      /* event, handler */
      {
        var args = Array.prototype.slice.call(arguments); // Add the `dt` namespace automatically if it isn't already present

        args[0] = $$$1.map(args[0].split(/\s/), function (e) {
          return !e.match(/\.dt\b/) ? e + '.dt' : e;
        }).join(' ');
        var inst = $$$1(this.tables().nodes());
        inst[key].apply(inst, args);
        return this;
      });
    });

    _api_register('clear()', function () {
      return this.iterator('table', function (settings) {
        _fnClearTable(settings);
      });
    });

    _api_register('settings()', function () {
      return new _Api2(this.context, this.context);
    });

    _api_register('init()', function () {
      var ctx = this.context;
      return ctx.length ? ctx[0].oInit : null;
    });

    _api_register('data()', function () {
      return this.iterator('table', function (settings) {
        return _pluck(settings.aoData, '_aData');
      }).flatten();
    });

    _api_register('destroy()', function (remove) {
      remove = remove || false;
      return this.iterator('table', function (settings) {
        var orig = settings.nTableWrapper.parentNode;
        var classes = settings.oClasses;
        var table = settings.nTable;
        var tbody = settings.nTBody;
        var thead = settings.nTHead;
        var tfoot = settings.nTFoot;
        var jqTable = $$$1(table);
        var jqTbody = $$$1(tbody);
        var jqWrapper = $$$1(settings.nTableWrapper);
        var rows = $$$1.map(settings.aoData, function (r) {
          return r.nTr;
        });
        var ien; // Flag to note that the table is currently being destroyed - no action
        // should be taken

        settings.bDestroying = true; // Fire off the destroy callbacks for plug-ins etc

        _fnCallbackFire(settings, "aoDestroyCallback", "destroy", [settings]); // If not being removed from the document, make all columns visible


        if (!remove) {
          new _Api2(settings).columns().visible(true);
        } // Blitz all `DT` namespaced events (these are internal events, the
        // lowercase, `dt` events are user subscribed and they are responsible
        // for removing them


        jqWrapper.off('.DT').find(':not(tbody *)').off('.DT');
        $$$1(window).off('.DT-' + settings.sInstance); // When scrolling we had to break the table up - restore it

        if (table != thead.parentNode) {
          jqTable.children('thead').detach();
          jqTable.append(thead);
        }

        if (tfoot && table != tfoot.parentNode) {
          jqTable.children('tfoot').detach();
          jqTable.append(tfoot);
        }

        settings.aaSorting = [];
        settings.aaSortingFixed = [];

        _fnSortingClasses(settings);

        $$$1(rows).removeClass(settings.asStripeClasses.join(' '));
        $$$1('th, td', thead).removeClass(classes.sSortable + ' ' + classes.sSortableAsc + ' ' + classes.sSortableDesc + ' ' + classes.sSortableNone); // Add the TR elements back into the table in their original order

        jqTbody.children().detach();
        jqTbody.append(rows); // Remove the DataTables generated nodes, events and classes

        var removedMethod = remove ? 'remove' : 'detach';
        jqTable[removedMethod]();
        jqWrapper[removedMethod](); // If we need to reattach the table to the document

        if (!remove && orig) {
          // insertBefore acts like appendChild if !arg[1]
          orig.insertBefore(table, settings.nTableReinsertBefore); // Restore the width of the original table - was read from the style property,
          // so we can restore directly to that

          jqTable.css('width', settings.sDestroyWidth).removeClass(classes.sTable); // If the were originally stripe classes - then we add them back here.
          // Note this is not fool proof (for example if not all rows had stripe
          // classes - but it's a good effort without getting carried away

          ien = settings.asDestroyStripes.length;

          if (ien) {
            jqTbody.children().each(function (i) {
              $$$1(this).addClass(settings.asDestroyStripes[i % ien]);
            });
          }
        }
        /* Remove the settings object from the settings array */


        var idx = $$$1.inArray(settings, DataTable.settings);

        if (idx !== -1) {
          DataTable.settings.splice(idx, 1);
        }
      });
    }); // Add the `every()` method for rows, columns and cells in a compact form


    $$$1.each(['column', 'row', 'cell'], function (i, type) {
      _api_register(type + 's().every()', function (fn) {
        var opts = this.selector.opts;
        var api = this;
        return this.iterator(type, function (settings, arg1, arg2, arg3, arg4) {
          // Rows and columns:
          //  arg1 - index
          //  arg2 - table counter
          //  arg3 - loop counter
          //  arg4 - undefined
          // Cells:
          //  arg1 - row index
          //  arg2 - column index
          //  arg3 - table counter
          //  arg4 - loop counter
          fn.call(api[type](arg1, type === 'cell' ? arg2 : opts, type === 'cell' ? opts : undefined), arg1, arg2, arg3, arg4);
        });
      });
    }); // i18n method for extensions to be able to use the language object from the
    // DataTable

    _api_register('i18n()', function (token, def, plural) {
      var ctx = this.context[0];

      var resolved = _fnGetObjectDataFn(token)(ctx.oLanguage);

      if (resolved === undefined) {
        resolved = def;
      }

      if (plural !== undefined && $$$1.isPlainObject(resolved)) {
        resolved = resolved[plural] !== undefined ? resolved[plural] : resolved._;
      }

      return resolved.replace('%d', plural); // nb: plural might be undefined,
    });
    /**
     * Version string for plug-ins to check compatibility. Allowed format is
     * `a.b.c-d` where: a:int, b:int, c:int, d:string(dev|beta|alpha). `d` is used
     * only for non-release builds. See http://semver.org/ for more information.
     *  @member
     *  @type string
     *  @default Version number
     */


    DataTable.version = "1.10.18";
    /**
     * Private data store, containing all of the settings objects that are
     * created for the tables on a given page.
     *
     * Note that the `DataTable.settings` object is aliased to
     * `jQuery.fn.dataTableExt` through which it may be accessed and
     * manipulated, or `jQuery.fn.dataTable.settings`.
     *  @member
     *  @type array
     *  @default []
     *  @private
     */

    DataTable.settings = [];
    /**
     * Object models container, for the various models that DataTables has
     * available to it. These models define the objects that are used to hold
     * the active state and configuration of the table.
     *  @namespace
     */

    DataTable.models = {};
    /**
     * Template object for the way in which DataTables holds information about
     * search information for the global filter and individual column filters.
     *  @namespace
     */

    DataTable.models.oSearch = {
      /**
       * Flag to indicate if the filtering should be case insensitive or not
       *  @type boolean
       *  @default true
       */
      "bCaseInsensitive": true,

      /**
       * Applied search term
       *  @type string
       *  @default <i>Empty string</i>
       */
      "sSearch": "",

      /**
       * Flag to indicate if the search term should be interpreted as a
       * regular expression (true) or not (false) and therefore and special
       * regex characters escaped.
       *  @type boolean
       *  @default false
       */
      "bRegex": false,

      /**
       * Flag to indicate if DataTables is to use its smart filtering or not.
       *  @type boolean
       *  @default true
       */
      "bSmart": true
    };
    /**
     * Template object for the way in which DataTables holds information about
     * each individual row. This is the object format used for the settings
     * aoData array.
     *  @namespace
     */

    DataTable.models.oRow = {
      /**
       * TR element for the row
       *  @type node
       *  @default null
       */
      "nTr": null,

      /**
       * Array of TD elements for each row. This is null until the row has been
       * created.
       *  @type array nodes
       *  @default []
       */
      "anCells": null,

      /**
       * Data object from the original data source for the row. This is either
       * an array if using the traditional form of DataTables, or an object if
       * using mData options. The exact type will depend on the passed in
       * data from the data source, or will be an array if using DOM a data
       * source.
       *  @type array|object
       *  @default []
       */
      "_aData": [],

      /**
       * Sorting data cache - this array is ostensibly the same length as the
       * number of columns (although each index is generated only as it is
       * needed), and holds the data that is used for sorting each column in the
       * row. We do this cache generation at the start of the sort in order that
       * the formatting of the sort data need be done only once for each cell
       * per sort. This array should not be read from or written to by anything
       * other than the master sorting methods.
       *  @type array
       *  @default null
       *  @private
       */
      "_aSortData": null,

      /**
       * Per cell filtering data cache. As per the sort data cache, used to
       * increase the performance of the filtering in DataTables
       *  @type array
       *  @default null
       *  @private
       */
      "_aFilterData": null,

      /**
       * Filtering data cache. This is the same as the cell filtering cache, but
       * in this case a string rather than an array. This is easily computed with
       * a join on `_aFilterData`, but is provided as a cache so the join isn't
       * needed on every search (memory traded for performance)
       *  @type array
       *  @default null
       *  @private
       */
      "_sFilterRow": null,

      /**
       * Cache of the class name that DataTables has applied to the row, so we
       * can quickly look at this variable rather than needing to do a DOM check
       * on className for the nTr property.
       *  @type string
       *  @default <i>Empty string</i>
       *  @private
       */
      "_sRowStripe": "",

      /**
       * Denote if the original data source was from the DOM, or the data source
       * object. This is used for invalidating data, so DataTables can
       * automatically read data from the original source, unless uninstructed
       * otherwise.
       *  @type string
       *  @default null
       *  @private
       */
      "src": null,

      /**
       * Index in the aoData array. This saves an indexOf lookup when we have the
       * object, but want to know the index
       *  @type integer
       *  @default -1
       *  @private
       */
      "idx": -1
    };
    /**
     * Template object for the column information object in DataTables. This object
     * is held in the settings aoColumns array and contains all the information that
     * DataTables needs about each individual column.
     *
     * Note that this object is related to {@link DataTable.defaults.column}
     * but this one is the internal data store for DataTables's cache of columns.
     * It should NOT be manipulated outside of DataTables. Any configuration should
     * be done through the initialisation options.
     *  @namespace
     */

    DataTable.models.oColumn = {
      /**
       * Column index. This could be worked out on-the-fly with $.inArray, but it
       * is faster to just hold it as a variable
       *  @type integer
       *  @default null
       */
      "idx": null,

      /**
       * A list of the columns that sorting should occur on when this column
       * is sorted. That this property is an array allows multi-column sorting
       * to be defined for a column (for example first name / last name columns
       * would benefit from this). The values are integers pointing to the
       * columns to be sorted on (typically it will be a single integer pointing
       * at itself, but that doesn't need to be the case).
       *  @type array
       */
      "aDataSort": null,

      /**
       * Define the sorting directions that are applied to the column, in sequence
       * as the column is repeatedly sorted upon - i.e. the first value is used
       * as the sorting direction when the column if first sorted (clicked on).
       * Sort it again (click again) and it will move on to the next index.
       * Repeat until loop.
       *  @type array
       */
      "asSorting": null,

      /**
       * Flag to indicate if the column is searchable, and thus should be included
       * in the filtering or not.
       *  @type boolean
       */
      "bSearchable": null,

      /**
       * Flag to indicate if the column is sortable or not.
       *  @type boolean
       */
      "bSortable": null,

      /**
       * Flag to indicate if the column is currently visible in the table or not
       *  @type boolean
       */
      "bVisible": null,

      /**
       * Store for manual type assignment using the `column.type` option. This
       * is held in store so we can manipulate the column's `sType` property.
       *  @type string
       *  @default null
       *  @private
       */
      "_sManualType": null,

      /**
       * Flag to indicate if HTML5 data attributes should be used as the data
       * source for filtering or sorting. True is either are.
       *  @type boolean
       *  @default false
       *  @private
       */
      "_bAttrSrc": false,

      /**
       * Developer definable function that is called whenever a cell is created (Ajax source,
       * etc) or processed for input (DOM source). This can be used as a compliment to mRender
       * allowing you to modify the DOM element (add background colour for example) when the
       * element is available.
       *  @type function
       *  @param {element} nTd The TD node that has been created
       *  @param {*} sData The Data for the cell
       *  @param {array|object} oData The data for the whole row
       *  @param {int} iRow The row index for the aoData data store
       *  @default null
       */
      "fnCreatedCell": null,

      /**
       * Function to get data from a cell in a column. You should <b>never</b>
       * access data directly through _aData internally in DataTables - always use
       * the method attached to this property. It allows mData to function as
       * required. This function is automatically assigned by the column
       * initialisation method
       *  @type function
       *  @param {array|object} oData The data array/object for the array
       *    (i.e. aoData[]._aData)
       *  @param {string} sSpecific The specific data type you want to get -
       *    'display', 'type' 'filter' 'sort'
       *  @returns {*} The data for the cell from the given row's data
       *  @default null
       */
      "fnGetData": null,

      /**
       * Function to set data for a cell in the column. You should <b>never</b>
       * set the data directly to _aData internally in DataTables - always use
       * this method. It allows mData to function as required. This function
       * is automatically assigned by the column initialisation method
       *  @type function
       *  @param {array|object} oData The data array/object for the array
       *    (i.e. aoData[]._aData)
       *  @param {*} sValue Value to set
       *  @default null
       */
      "fnSetData": null,

      /**
       * Property to read the value for the cells in the column from the data
       * source array / object. If null, then the default content is used, if a
       * function is given then the return from the function is used.
       *  @type function|int|string|null
       *  @default null
       */
      "mData": null,

      /**
       * Partner property to mData which is used (only when defined) to get
       * the data - i.e. it is basically the same as mData, but without the
       * 'set' option, and also the data fed to it is the result from mData.
       * This is the rendering method to match the data method of mData.
       *  @type function|int|string|null
       *  @default null
       */
      "mRender": null,

      /**
       * Unique header TH/TD element for this column - this is what the sorting
       * listener is attached to (if sorting is enabled.)
       *  @type node
       *  @default null
       */
      "nTh": null,

      /**
       * Unique footer TH/TD element for this column (if there is one). Not used
       * in DataTables as such, but can be used for plug-ins to reference the
       * footer for each column.
       *  @type node
       *  @default null
       */
      "nTf": null,

      /**
       * The class to apply to all TD elements in the table's TBODY for the column
       *  @type string
       *  @default null
       */
      "sClass": null,

      /**
       * When DataTables calculates the column widths to assign to each column,
       * it finds the longest string in each column and then constructs a
       * temporary table and reads the widths from that. The problem with this
       * is that "mmm" is much wider then "iiii", but the latter is a longer
       * string - thus the calculation can go wrong (doing it properly and putting
       * it into an DOM object and measuring that is horribly(!) slow). Thus as
       * a "work around" we provide this option. It will append its value to the
       * text that is found to be the longest string for the column - i.e. padding.
       *  @type string
       */
      "sContentPadding": null,

      /**
       * Allows a default value to be given for a column's data, and will be used
       * whenever a null data source is encountered (this can be because mData
       * is set to null, or because the data source itself is null).
       *  @type string
       *  @default null
       */
      "sDefaultContent": null,

      /**
       * Name for the column, allowing reference to the column by name as well as
       * by index (needs a lookup to work by name).
       *  @type string
       */
      "sName": null,

      /**
       * Custom sorting data type - defines which of the available plug-ins in
       * afnSortData the custom sorting will use - if any is defined.
       *  @type string
       *  @default std
       */
      "sSortDataType": 'std',

      /**
       * Class to be applied to the header element when sorting on this column
       *  @type string
       *  @default null
       */
      "sSortingClass": null,

      /**
       * Class to be applied to the header element when sorting on this column -
       * when jQuery UI theming is used.
       *  @type string
       *  @default null
       */
      "sSortingClassJUI": null,

      /**
       * Title of the column - what is seen in the TH element (nTh).
       *  @type string
       */
      "sTitle": null,

      /**
       * Column sorting and filtering type
       *  @type string
       *  @default null
       */
      "sType": null,

      /**
       * Width of the column
       *  @type string
       *  @default null
       */
      "sWidth": null,

      /**
       * Width of the column when it was first "encountered"
       *  @type string
       *  @default null
       */
      "sWidthOrig": null
    };
    /*
     * Developer note: The properties of the object below are given in Hungarian
     * notation, that was used as the interface for DataTables prior to v1.10, however
     * from v1.10 onwards the primary interface is camel case. In order to avoid
     * breaking backwards compatibility utterly with this change, the Hungarian
     * version is still, internally the primary interface, but is is not documented
     * - hence the @name tags in each doc comment. This allows a Javascript function
     * to create a map from Hungarian notation to camel case (going the other direction
     * would require each property to be listed, which would at around 3K to the size
     * of DataTables, while this method is about a 0.5K hit.
     *
     * Ultimately this does pave the way for Hungarian notation to be dropped
     * completely, but that is a massive amount of work and will break current
     * installs (therefore is on-hold until v2).
     */

    /**
     * Initialisation options that can be given to DataTables at initialisation
     * time.
     *  @namespace
     */

    DataTable.defaults = {
      /**
       * An array of data to use for the table, passed in at initialisation which
       * will be used in preference to any data which is already in the DOM. This is
       * particularly useful for constructing tables purely in Javascript, for
       * example with a custom Ajax call.
       *  @type array
       *  @default null
       *
       *  @dtopt Option
       *  @name DataTable.defaults.data
       *
       *  @example
       *    // Using a 2D array data source
       *    $(document).ready( function () {
       *      $('#example').dataTable( {
       *        "data": [
       *          ['Trident', 'Internet Explorer 4.0', 'Win 95+', 4, 'X'],
       *          ['Trident', 'Internet Explorer 5.0', 'Win 95+', 5, 'C'],
       *        ],
       *        "columns": [
       *          { "title": "Engine" },
       *          { "title": "Browser" },
       *          { "title": "Platform" },
       *          { "title": "Version" },
       *          { "title": "Grade" }
       *        ]
       *      } );
       *    } );
       *
       *  @example
       *    // Using an array of objects as a data source (`data`)
       *    $(document).ready( function () {
       *      $('#example').dataTable( {
       *        "data": [
       *          {
       *            "engine":   "Trident",
       *            "browser":  "Internet Explorer 4.0",
       *            "platform": "Win 95+",
       *            "version":  4,
       *            "grade":    "X"
       *          },
       *          {
       *            "engine":   "Trident",
       *            "browser":  "Internet Explorer 5.0",
       *            "platform": "Win 95+",
       *            "version":  5,
       *            "grade":    "C"
       *          }
       *        ],
       *        "columns": [
       *          { "title": "Engine",   "data": "engine" },
       *          { "title": "Browser",  "data": "browser" },
       *          { "title": "Platform", "data": "platform" },
       *          { "title": "Version",  "data": "version" },
       *          { "title": "Grade",    "data": "grade" }
       *        ]
       *      } );
       *    } );
       */
      "aaData": null,

      /**
       * If ordering is enabled, then DataTables will perform a first pass sort on
       * initialisation. You can define which column(s) the sort is performed
       * upon, and the sorting direction, with this variable. The `sorting` array
       * should contain an array for each column to be sorted initially containing
       * the column's index and a direction string ('asc' or 'desc').
       *  @type array
       *  @default [[0,'asc']]
       *
       *  @dtopt Option
       *  @name DataTable.defaults.order
       *
       *  @example
       *    // Sort by 3rd column first, and then 4th column
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "order": [[2,'asc'], [3,'desc']]
       *      } );
       *    } );
       *
       *    // No initial sorting
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "order": []
       *      } );
       *    } );
       */
      "aaSorting": [[0, 'asc']],

      /**
       * This parameter is basically identical to the `sorting` parameter, but
       * cannot be overridden by user interaction with the table. What this means
       * is that you could have a column (visible or hidden) which the sorting
       * will always be forced on first - any sorting after that (from the user)
       * will then be performed as required. This can be useful for grouping rows
       * together.
       *  @type array
       *  @default null
       *
       *  @dtopt Option
       *  @name DataTable.defaults.orderFixed
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "orderFixed": [[0,'asc']]
       *      } );
       *    } )
       */
      "aaSortingFixed": [],

      /**
       * DataTables can be instructed to load data to display in the table from a
       * Ajax source. This option defines how that Ajax call is made and where to.
       *
       * The `ajax` property has three different modes of operation, depending on
       * how it is defined. These are:
       *
       * * `string` - Set the URL from where the data should be loaded from.
       * * `object` - Define properties for `jQuery.ajax`.
       * * `function` - Custom data get function
       *
       * `string`
       * --------
       *
       * As a string, the `ajax` property simply defines the URL from which
       * DataTables will load data.
       *
       * `object`
       * --------
       *
       * As an object, the parameters in the object are passed to
       * [jQuery.ajax](http://api.jquery.com/jQuery.ajax/) allowing fine control
       * of the Ajax request. DataTables has a number of default parameters which
       * you can override using this option. Please refer to the jQuery
       * documentation for a full description of the options available, although
       * the following parameters provide additional options in DataTables or
       * require special consideration:
       *
       * * `data` - As with jQuery, `data` can be provided as an object, but it
       *   can also be used as a function to manipulate the data DataTables sends
       *   to the server. The function takes a single parameter, an object of
       *   parameters with the values that DataTables has readied for sending. An
       *   object may be returned which will be merged into the DataTables
       *   defaults, or you can add the items to the object that was passed in and
       *   not return anything from the function. This supersedes `fnServerParams`
       *   from DataTables 1.9-.
       *
       * * `dataSrc` - By default DataTables will look for the property `data` (or
       *   `aaData` for compatibility with DataTables 1.9-) when obtaining data
       *   from an Ajax source or for server-side processing - this parameter
       *   allows that property to be changed. You can use Javascript dotted
       *   object notation to get a data source for multiple levels of nesting, or
       *   it my be used as a function. As a function it takes a single parameter,
       *   the JSON returned from the server, which can be manipulated as
       *   required, with the returned value being that used by DataTables as the
       *   data source for the table. This supersedes `sAjaxDataProp` from
       *   DataTables 1.9-.
       *
       * * `success` - Should not be overridden it is used internally in
       *   DataTables. To manipulate / transform the data returned by the server
       *   use `ajax.dataSrc`, or use `ajax` as a function (see below).
       *
       * `function`
       * ----------
       *
       * As a function, making the Ajax call is left up to yourself allowing
       * complete control of the Ajax request. Indeed, if desired, a method other
       * than Ajax could be used to obtain the required data, such as Web storage
       * or an AIR database.
       *
       * The function is given four parameters and no return is required. The
       * parameters are:
       *
       * 1. _object_ - Data to send to the server
       * 2. _function_ - Callback function that must be executed when the required
       *    data has been obtained. That data should be passed into the callback
       *    as the only parameter
       * 3. _object_ - DataTables settings object for the table
       *
       * Note that this supersedes `fnServerData` from DataTables 1.9-.
       *
       *  @type string|object|function
       *  @default null
       *
       *  @dtopt Option
       *  @name DataTable.defaults.ajax
       *  @since 1.10.0
       *
       * @example
       *   // Get JSON data from a file via Ajax.
       *   // Note DataTables expects data in the form `{ data: [ ...data... ] }` by default).
       *   $('#example').dataTable( {
       *     "ajax": "data.json"
       *   } );
       *
       * @example
       *   // Get JSON data from a file via Ajax, using `dataSrc` to change
       *   // `data` to `tableData` (i.e. `{ tableData: [ ...data... ] }`)
       *   $('#example').dataTable( {
       *     "ajax": {
       *       "url": "data.json",
       *       "dataSrc": "tableData"
       *     }
       *   } );
       *
       * @example
       *   // Get JSON data from a file via Ajax, using `dataSrc` to read data
       *   // from a plain array rather than an array in an object
       *   $('#example').dataTable( {
       *     "ajax": {
       *       "url": "data.json",
       *       "dataSrc": ""
       *     }
       *   } );
       *
       * @example
       *   // Manipulate the data returned from the server - add a link to data
       *   // (note this can, should, be done using `render` for the column - this
       *   // is just a simple example of how the data can be manipulated).
       *   $('#example').dataTable( {
       *     "ajax": {
       *       "url": "data.json",
       *       "dataSrc": function ( json ) {
       *         for ( var i=0, ien=json.length ; i<ien ; i++ ) {
       *           json[i][0] = '<a href="/message/'+json[i][0]+'>View message</a>';
       *         }
       *         return json;
       *       }
       *     }
       *   } );
       *
       * @example
       *   // Add data to the request
       *   $('#example').dataTable( {
       *     "ajax": {
       *       "url": "data.json",
       *       "data": function ( d ) {
       *         return {
       *           "extra_search": $('#extra').val()
       *         };
       *       }
       *     }
       *   } );
       *
       * @example
       *   // Send request as POST
       *   $('#example').dataTable( {
       *     "ajax": {
       *       "url": "data.json",
       *       "type": "POST"
       *     }
       *   } );
       *
       * @example
       *   // Get the data from localStorage (could interface with a form for
       *   // adding, editing and removing rows).
       *   $('#example').dataTable( {
       *     "ajax": function (data, callback, settings) {
       *       callback(
       *         JSON.parse( localStorage.getItem('dataTablesData') )
       *       );
       *     }
       *   } );
       */
      "ajax": null,

      /**
       * This parameter allows you to readily specify the entries in the length drop
       * down menu that DataTables shows when pagination is enabled. It can be
       * either a 1D array of options which will be used for both the displayed
       * option and the value, or a 2D array which will use the array in the first
       * position as the value, and the array in the second position as the
       * displayed options (useful for language strings such as 'All').
       *
       * Note that the `pageLength` property will be automatically set to the
       * first value given in this array, unless `pageLength` is also provided.
       *  @type array
       *  @default [ 10, 25, 50, 100 ]
       *
       *  @dtopt Option
       *  @name DataTable.defaults.lengthMenu
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]]
       *      } );
       *    } );
       */
      "aLengthMenu": [10, 25, 50, 100],

      /**
       * The `columns` option in the initialisation parameter allows you to define
       * details about the way individual columns behave. For a full list of
       * column options that can be set, please see
       * {@link DataTable.defaults.column}. Note that if you use `columns` to
       * define your columns, you must have an entry in the array for every single
       * column that you have in your table (these can be null if you don't which
       * to specify any options).
       *  @member
       *
       *  @name DataTable.defaults.column
       */
      "aoColumns": null,

      /**
       * Very similar to `columns`, `columnDefs` allows you to target a specific
       * column, multiple columns, or all columns, using the `targets` property of
       * each object in the array. This allows great flexibility when creating
       * tables, as the `columnDefs` arrays can be of any length, targeting the
       * columns you specifically want. `columnDefs` may use any of the column
       * options available: {@link DataTable.defaults.column}, but it _must_
       * have `targets` defined in each object in the array. Values in the `targets`
       * array may be:
       *   <ul>
       *     <li>a string - class name will be matched on the TH for the column</li>
       *     <li>0 or a positive integer - column index counting from the left</li>
       *     <li>a negative integer - column index counting from the right</li>
       *     <li>the string "_all" - all columns (i.e. assign a default)</li>
       *   </ul>
       *  @member
       *
       *  @name DataTable.defaults.columnDefs
       */
      "aoColumnDefs": null,

      /**
       * Basically the same as `search`, this parameter defines the individual column
       * filtering state at initialisation time. The array must be of the same size
       * as the number of columns, and each element be an object with the parameters
       * `search` and `escapeRegex` (the latter is optional). 'null' is also
       * accepted and the default will be used.
       *  @type array
       *  @default []
       *
       *  @dtopt Option
       *  @name DataTable.defaults.searchCols
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "searchCols": [
       *          null,
       *          { "search": "My filter" },
       *          null,
       *          { "search": "^[0-9]", "escapeRegex": false }
       *        ]
       *      } );
       *    } )
       */
      "aoSearchCols": [],

      /**
       * An array of CSS classes that should be applied to displayed rows. This
       * array may be of any length, and DataTables will apply each class
       * sequentially, looping when required.
       *  @type array
       *  @default null <i>Will take the values determined by the `oClasses.stripe*`
       *    options</i>
       *
       *  @dtopt Option
       *  @name DataTable.defaults.stripeClasses
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "stripeClasses": [ 'strip1', 'strip2', 'strip3' ]
       *      } );
       *    } )
       */
      "asStripeClasses": null,

      /**
       * Enable or disable automatic column width calculation. This can be disabled
       * as an optimisation (it takes some time to calculate the widths) if the
       * tables widths are passed in using `columns`.
       *  @type boolean
       *  @default true
       *
       *  @dtopt Features
       *  @name DataTable.defaults.autoWidth
       *
       *  @example
       *    $(document).ready( function () {
       *      $('#example').dataTable( {
       *        "autoWidth": false
       *      } );
       *    } );
       */
      "bAutoWidth": true,

      /**
       * Deferred rendering can provide DataTables with a huge speed boost when you
       * are using an Ajax or JS data source for the table. This option, when set to
       * true, will cause DataTables to defer the creation of the table elements for
       * each row until they are needed for a draw - saving a significant amount of
       * time.
       *  @type boolean
       *  @default false
       *
       *  @dtopt Features
       *  @name DataTable.defaults.deferRender
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "ajax": "sources/arrays.txt",
       *        "deferRender": true
       *      } );
       *    } );
       */
      "bDeferRender": false,

      /**
       * Replace a DataTable which matches the given selector and replace it with
       * one which has the properties of the new initialisation object passed. If no
       * table matches the selector, then the new DataTable will be constructed as
       * per normal.
       *  @type boolean
       *  @default false
       *
       *  @dtopt Options
       *  @name DataTable.defaults.destroy
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "srollY": "200px",
       *        "paginate": false
       *      } );
       *
       *      // Some time later....
       *      $('#example').dataTable( {
       *        "filter": false,
       *        "destroy": true
       *      } );
       *    } );
       */
      "bDestroy": false,

      /**
       * Enable or disable filtering of data. Filtering in DataTables is "smart" in
       * that it allows the end user to input multiple words (space separated) and
       * will match a row containing those words, even if not in the order that was
       * specified (this allow matching across multiple columns). Note that if you
       * wish to use filtering in DataTables this must remain 'true' - to remove the
       * default filtering input box and retain filtering abilities, please use
       * {@link DataTable.defaults.dom}.
       *  @type boolean
       *  @default true
       *
       *  @dtopt Features
       *  @name DataTable.defaults.searching
       *
       *  @example
       *    $(document).ready( function () {
       *      $('#example').dataTable( {
       *        "searching": false
       *      } );
       *    } );
       */
      "bFilter": true,

      /**
       * Enable or disable the table information display. This shows information
       * about the data that is currently visible on the page, including information
       * about filtered data if that action is being performed.
       *  @type boolean
       *  @default true
       *
       *  @dtopt Features
       *  @name DataTable.defaults.info
       *
       *  @example
       *    $(document).ready( function () {
       *      $('#example').dataTable( {
       *        "info": false
       *      } );
       *    } );
       */
      "bInfo": true,

      /**
       * Allows the end user to select the size of a formatted page from a select
       * menu (sizes are 10, 25, 50 and 100). Requires pagination (`paginate`).
       *  @type boolean
       *  @default true
       *
       *  @dtopt Features
       *  @name DataTable.defaults.lengthChange
       *
       *  @example
       *    $(document).ready( function () {
       *      $('#example').dataTable( {
       *        "lengthChange": false
       *      } );
       *    } );
       */
      "bLengthChange": true,

      /**
       * Enable or disable pagination.
       *  @type boolean
       *  @default true
       *
       *  @dtopt Features
       *  @name DataTable.defaults.paging
       *
       *  @example
       *    $(document).ready( function () {
       *      $('#example').dataTable( {
       *        "paging": false
       *      } );
       *    } );
       */
      "bPaginate": true,

      /**
       * Enable or disable the display of a 'processing' indicator when the table is
       * being processed (e.g. a sort). This is particularly useful for tables with
       * large amounts of data where it can take a noticeable amount of time to sort
       * the entries.
       *  @type boolean
       *  @default false
       *
       *  @dtopt Features
       *  @name DataTable.defaults.processing
       *
       *  @example
       *    $(document).ready( function () {
       *      $('#example').dataTable( {
       *        "processing": true
       *      } );
       *    } );
       */
      "bProcessing": false,

      /**
       * Retrieve the DataTables object for the given selector. Note that if the
       * table has already been initialised, this parameter will cause DataTables
       * to simply return the object that has already been set up - it will not take
       * account of any changes you might have made to the initialisation object
       * passed to DataTables (setting this parameter to true is an acknowledgement
       * that you understand this). `destroy` can be used to reinitialise a table if
       * you need.
       *  @type boolean
       *  @default false
       *
       *  @dtopt Options
       *  @name DataTable.defaults.retrieve
       *
       *  @example
       *    $(document).ready( function() {
       *      initTable();
       *      tableActions();
       *    } );
       *
       *    function initTable ()
       *    {
       *      return $('#example').dataTable( {
       *        "scrollY": "200px",
       *        "paginate": false,
       *        "retrieve": true
       *      } );
       *    }
       *
       *    function tableActions ()
       *    {
       *      var table = initTable();
       *      // perform API operations with oTable
       *    }
       */
      "bRetrieve": false,

      /**
       * When vertical (y) scrolling is enabled, DataTables will force the height of
       * the table's viewport to the given height at all times (useful for layout).
       * However, this can look odd when filtering data down to a small data set,
       * and the footer is left "floating" further down. This parameter (when
       * enabled) will cause DataTables to collapse the table's viewport down when
       * the result set will fit within the given Y height.
       *  @type boolean
       *  @default false
       *
       *  @dtopt Options
       *  @name DataTable.defaults.scrollCollapse
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "scrollY": "200",
       *        "scrollCollapse": true
       *      } );
       *    } );
       */
      "bScrollCollapse": false,

      /**
       * Configure DataTables to use server-side processing. Note that the
       * `ajax` parameter must also be given in order to give DataTables a
       * source to obtain the required data for each draw.
       *  @type boolean
       *  @default false
       *
       *  @dtopt Features
       *  @dtopt Server-side
       *  @name DataTable.defaults.serverSide
       *
       *  @example
       *    $(document).ready( function () {
       *      $('#example').dataTable( {
       *        "serverSide": true,
       *        "ajax": "xhr.php"
       *      } );
       *    } );
       */
      "bServerSide": false,

      /**
       * Enable or disable sorting of columns. Sorting of individual columns can be
       * disabled by the `sortable` option for each column.
       *  @type boolean
       *  @default true
       *
       *  @dtopt Features
       *  @name DataTable.defaults.ordering
       *
       *  @example
       *    $(document).ready( function () {
       *      $('#example').dataTable( {
       *        "ordering": false
       *      } );
       *    } );
       */
      "bSort": true,

      /**
       * Enable or display DataTables' ability to sort multiple columns at the
       * same time (activated by shift-click by the user).
       *  @type boolean
       *  @default true
       *
       *  @dtopt Options
       *  @name DataTable.defaults.orderMulti
       *
       *  @example
       *    // Disable multiple column sorting ability
       *    $(document).ready( function () {
       *      $('#example').dataTable( {
       *        "orderMulti": false
       *      } );
       *    } );
       */
      "bSortMulti": true,

      /**
       * Allows control over whether DataTables should use the top (true) unique
       * cell that is found for a single column, or the bottom (false - default).
       * This is useful when using complex headers.
       *  @type boolean
       *  @default false
       *
       *  @dtopt Options
       *  @name DataTable.defaults.orderCellsTop
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "orderCellsTop": true
       *      } );
       *    } );
       */
      "bSortCellsTop": false,

      /**
       * Enable or disable the addition of the classes `sorting\_1`, `sorting\_2` and
       * `sorting\_3` to the columns which are currently being sorted on. This is
       * presented as a feature switch as it can increase processing time (while
       * classes are removed and added) so for large data sets you might want to
       * turn this off.
       *  @type boolean
       *  @default true
       *
       *  @dtopt Features
       *  @name DataTable.defaults.orderClasses
       *
       *  @example
       *    $(document).ready( function () {
       *      $('#example').dataTable( {
       *        "orderClasses": false
       *      } );
       *    } );
       */
      "bSortClasses": true,

      /**
       * Enable or disable state saving. When enabled HTML5 `localStorage` will be
       * used to save table display information such as pagination information,
       * display length, filtering and sorting. As such when the end user reloads
       * the page the display display will match what thy had previously set up.
       *
       * Due to the use of `localStorage` the default state saving is not supported
       * in IE6 or 7. If state saving is required in those browsers, use
       * `stateSaveCallback` to provide a storage solution such as cookies.
       *  @type boolean
       *  @default false
       *
       *  @dtopt Features
       *  @name DataTable.defaults.stateSave
       *
       *  @example
       *    $(document).ready( function () {
       *      $('#example').dataTable( {
       *        "stateSave": true
       *      } );
       *    } );
       */
      "bStateSave": false,

      /**
       * This function is called when a TR element is created (and all TD child
       * elements have been inserted), or registered if using a DOM source, allowing
       * manipulation of the TR element (adding classes etc).
       *  @type function
       *  @param {node} row "TR" element for the current row
       *  @param {array} data Raw data array for this row
       *  @param {int} dataIndex The index of this row in the internal aoData array
       *
       *  @dtopt Callbacks
       *  @name DataTable.defaults.createdRow
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "createdRow": function( row, data, dataIndex ) {
       *          // Bold the grade for all 'A' grade browsers
       *          if ( data[4] == "A" )
       *          {
       *            $('td:eq(4)', row).html( '<b>A</b>' );
       *          }
       *        }
       *      } );
       *    } );
       */
      "fnCreatedRow": null,

      /**
       * This function is called on every 'draw' event, and allows you to
       * dynamically modify any aspect you want about the created DOM.
       *  @type function
       *  @param {object} settings DataTables settings object
       *
       *  @dtopt Callbacks
       *  @name DataTable.defaults.drawCallback
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "drawCallback": function( settings ) {
       *          alert( 'DataTables has redrawn the table' );
       *        }
       *      } );
       *    } );
       */
      "fnDrawCallback": null,

      /**
       * Identical to fnHeaderCallback() but for the table footer this function
       * allows you to modify the table footer on every 'draw' event.
       *  @type function
       *  @param {node} foot "TR" element for the footer
       *  @param {array} data Full table data (as derived from the original HTML)
       *  @param {int} start Index for the current display starting point in the
       *    display array
       *  @param {int} end Index for the current display ending point in the
       *    display array
       *  @param {array int} display Index array to translate the visual position
       *    to the full data array
       *
       *  @dtopt Callbacks
       *  @name DataTable.defaults.footerCallback
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "footerCallback": function( tfoot, data, start, end, display ) {
       *          tfoot.getElementsByTagName('th')[0].innerHTML = "Starting index is "+start;
       *        }
       *      } );
       *    } )
       */
      "fnFooterCallback": null,

      /**
       * When rendering large numbers in the information element for the table
       * (i.e. "Showing 1 to 10 of 57 entries") DataTables will render large numbers
       * to have a comma separator for the 'thousands' units (e.g. 1 million is
       * rendered as "1,000,000") to help readability for the end user. This
       * function will override the default method DataTables uses.
       *  @type function
       *  @member
       *  @param {int} toFormat number to be formatted
       *  @returns {string} formatted string for DataTables to show the number
       *
       *  @dtopt Callbacks
       *  @name DataTable.defaults.formatNumber
       *
       *  @example
       *    // Format a number using a single quote for the separator (note that
       *    // this can also be done with the language.thousands option)
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "formatNumber": function ( toFormat ) {
       *          return toFormat.toString().replace(
       *            /\B(?=(\d{3})+(?!\d))/g, "'"
       *          );
       *        };
       *      } );
       *    } );
       */
      "fnFormatNumber": function fnFormatNumber(toFormat) {
        return toFormat.toString().replace(/\B(?=(\d{3})+(?!\d))/g, this.oLanguage.sThousands);
      },

      /**
       * This function is called on every 'draw' event, and allows you to
       * dynamically modify the header row. This can be used to calculate and
       * display useful information about the table.
       *  @type function
       *  @param {node} head "TR" element for the header
       *  @param {array} data Full table data (as derived from the original HTML)
       *  @param {int} start Index for the current display starting point in the
       *    display array
       *  @param {int} end Index for the current display ending point in the
       *    display array
       *  @param {array int} display Index array to translate the visual position
       *    to the full data array
       *
       *  @dtopt Callbacks
       *  @name DataTable.defaults.headerCallback
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "fheaderCallback": function( head, data, start, end, display ) {
       *          head.getElementsByTagName('th')[0].innerHTML = "Displaying "+(end-start)+" records";
       *        }
       *      } );
       *    } )
       */
      "fnHeaderCallback": null,

      /**
       * The information element can be used to convey information about the current
       * state of the table. Although the internationalisation options presented by
       * DataTables are quite capable of dealing with most customisations, there may
       * be times where you wish to customise the string further. This callback
       * allows you to do exactly that.
       *  @type function
       *  @param {object} oSettings DataTables settings object
       *  @param {int} start Starting position in data for the draw
       *  @param {int} end End position in data for the draw
       *  @param {int} max Total number of rows in the table (regardless of
       *    filtering)
       *  @param {int} total Total number of rows in the data set, after filtering
       *  @param {string} pre The string that DataTables has formatted using it's
       *    own rules
       *  @returns {string} The string to be displayed in the information element.
       *
       *  @dtopt Callbacks
       *  @name DataTable.defaults.infoCallback
       *
       *  @example
       *    $('#example').dataTable( {
       *      "infoCallback": function( settings, start, end, max, total, pre ) {
       *        return start +" to "+ end;
       *      }
       *    } );
       */
      "fnInfoCallback": null,

      /**
       * Called when the table has been initialised. Normally DataTables will
       * initialise sequentially and there will be no need for this function,
       * however, this does not hold true when using external language information
       * since that is obtained using an async XHR call.
       *  @type function
       *  @param {object} settings DataTables settings object
       *  @param {object} json The JSON object request from the server - only
       *    present if client-side Ajax sourced data is used
       *
       *  @dtopt Callbacks
       *  @name DataTable.defaults.initComplete
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "initComplete": function(settings, json) {
       *          alert( 'DataTables has finished its initialisation.' );
       *        }
       *      } );
       *    } )
       */
      "fnInitComplete": null,

      /**
       * Called at the very start of each table draw and can be used to cancel the
       * draw by returning false, any other return (including undefined) results in
       * the full draw occurring).
       *  @type function
       *  @param {object} settings DataTables settings object
       *  @returns {boolean} False will cancel the draw, anything else (including no
       *    return) will allow it to complete.
       *
       *  @dtopt Callbacks
       *  @name DataTable.defaults.preDrawCallback
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "preDrawCallback": function( settings ) {
       *          if ( $('#test').val() == 1 ) {
       *            return false;
       *          }
       *        }
       *      } );
       *    } );
       */
      "fnPreDrawCallback": null,

      /**
       * This function allows you to 'post process' each row after it have been
       * generated for each table draw, but before it is rendered on screen. This
       * function might be used for setting the row class name etc.
       *  @type function
       *  @param {node} row "TR" element for the current row
       *  @param {array} data Raw data array for this row
       *  @param {int} displayIndex The display index for the current table draw
       *  @param {int} displayIndexFull The index of the data in the full list of
       *    rows (after filtering)
       *
       *  @dtopt Callbacks
       *  @name DataTable.defaults.rowCallback
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "rowCallback": function( row, data, displayIndex, displayIndexFull ) {
       *          // Bold the grade for all 'A' grade browsers
       *          if ( data[4] == "A" ) {
       *            $('td:eq(4)', row).html( '<b>A</b>' );
       *          }
       *        }
       *      } );
       *    } );
       */
      "fnRowCallback": null,

      /**
       * __Deprecated__ The functionality provided by this parameter has now been
       * superseded by that provided through `ajax`, which should be used instead.
       *
       * This parameter allows you to override the default function which obtains
       * the data from the server so something more suitable for your application.
       * For example you could use POST data, or pull information from a Gears or
       * AIR database.
       *  @type function
       *  @member
       *  @param {string} source HTTP source to obtain the data from (`ajax`)
       *  @param {array} data A key/value pair object containing the data to send
       *    to the server
       *  @param {function} callback to be called on completion of the data get
       *    process that will draw the data on the page.
       *  @param {object} settings DataTables settings object
       *
       *  @dtopt Callbacks
       *  @dtopt Server-side
       *  @name DataTable.defaults.serverData
       *
       *  @deprecated 1.10. Please use `ajax` for this functionality now.
       */
      "fnServerData": null,

      /**
       * __Deprecated__ The functionality provided by this parameter has now been
       * superseded by that provided through `ajax`, which should be used instead.
       *
       *  It is often useful to send extra data to the server when making an Ajax
       * request - for example custom filtering information, and this callback
       * function makes it trivial to send extra information to the server. The
       * passed in parameter is the data set that has been constructed by
       * DataTables, and you can add to this or modify it as you require.
       *  @type function
       *  @param {array} data Data array (array of objects which are name/value
       *    pairs) that has been constructed by DataTables and will be sent to the
       *    server. In the case of Ajax sourced data with server-side processing
       *    this will be an empty array, for server-side processing there will be a
       *    significant number of parameters!
       *  @returns {undefined} Ensure that you modify the data array passed in,
       *    as this is passed by reference.
       *
       *  @dtopt Callbacks
       *  @dtopt Server-side
       *  @name DataTable.defaults.serverParams
       *
       *  @deprecated 1.10. Please use `ajax` for this functionality now.
       */
      "fnServerParams": null,

      /**
       * Load the table state. With this function you can define from where, and how, the
       * state of a table is loaded. By default DataTables will load from `localStorage`
       * but you might wish to use a server-side database or cookies.
       *  @type function
       *  @member
       *  @param {object} settings DataTables settings object
       *  @param {object} callback Callback that can be executed when done. It
       *    should be passed the loaded state object.
       *  @return {object} The DataTables state object to be loaded
       *
       *  @dtopt Callbacks
       *  @name DataTable.defaults.stateLoadCallback
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "stateSave": true,
       *        "stateLoadCallback": function (settings, callback) {
       *          $.ajax( {
       *            "url": "/state_load",
       *            "dataType": "json",
       *            "success": function (json) {
       *              callback( json );
       *            }
       *          } );
       *        }
       *      } );
       *    } );
       */
      "fnStateLoadCallback": function fnStateLoadCallback(settings) {
        try {
          return JSON.parse((settings.iStateDuration === -1 ? sessionStorage : localStorage).getItem('DataTables_' + settings.sInstance + '_' + location.pathname));
        } catch (e) {}
      },

      /**
       * Callback which allows modification of the saved state prior to loading that state.
       * This callback is called when the table is loading state from the stored data, but
       * prior to the settings object being modified by the saved state. Note that for
       * plug-in authors, you should use the `stateLoadParams` event to load parameters for
       * a plug-in.
       *  @type function
       *  @param {object} settings DataTables settings object
       *  @param {object} data The state object that is to be loaded
       *
       *  @dtopt Callbacks
       *  @name DataTable.defaults.stateLoadParams
       *
       *  @example
       *    // Remove a saved filter, so filtering is never loaded
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "stateSave": true,
       *        "stateLoadParams": function (settings, data) {
       *          data.oSearch.sSearch = "";
       *        }
       *      } );
       *    } );
       *
       *  @example
       *    // Disallow state loading by returning false
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "stateSave": true,
       *        "stateLoadParams": function (settings, data) {
       *          return false;
       *        }
       *      } );
       *    } );
       */
      "fnStateLoadParams": null,

      /**
       * Callback that is called when the state has been loaded from the state saving method
       * and the DataTables settings object has been modified as a result of the loaded state.
       *  @type function
       *  @param {object} settings DataTables settings object
       *  @param {object} data The state object that was loaded
       *
       *  @dtopt Callbacks
       *  @name DataTable.defaults.stateLoaded
       *
       *  @example
       *    // Show an alert with the filtering value that was saved
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "stateSave": true,
       *        "stateLoaded": function (settings, data) {
       *          alert( 'Saved filter was: '+data.oSearch.sSearch );
       *        }
       *      } );
       *    } );
       */
      "fnStateLoaded": null,

      /**
       * Save the table state. This function allows you to define where and how the state
       * information for the table is stored By default DataTables will use `localStorage`
       * but you might wish to use a server-side database or cookies.
       *  @type function
       *  @member
       *  @param {object} settings DataTables settings object
       *  @param {object} data The state object to be saved
       *
       *  @dtopt Callbacks
       *  @name DataTable.defaults.stateSaveCallback
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "stateSave": true,
       *        "stateSaveCallback": function (settings, data) {
       *          // Send an Ajax request to the server with the state object
       *          $.ajax( {
       *            "url": "/state_save",
       *            "data": data,
       *            "dataType": "json",
       *            "method": "POST"
       *            "success": function () {}
       *          } );
       *        }
       *      } );
       *    } );
       */
      "fnStateSaveCallback": function fnStateSaveCallback(settings, data) {
        try {
          (settings.iStateDuration === -1 ? sessionStorage : localStorage).setItem('DataTables_' + settings.sInstance + '_' + location.pathname, JSON.stringify(data));
        } catch (e) {}
      },

      /**
       * Callback which allows modification of the state to be saved. Called when the table
       * has changed state a new state save is required. This method allows modification of
       * the state saving object prior to actually doing the save, including addition or
       * other state properties or modification. Note that for plug-in authors, you should
       * use the `stateSaveParams` event to save parameters for a plug-in.
       *  @type function
       *  @param {object} settings DataTables settings object
       *  @param {object} data The state object to be saved
       *
       *  @dtopt Callbacks
       *  @name DataTable.defaults.stateSaveParams
       *
       *  @example
       *    // Remove a saved filter, so filtering is never saved
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "stateSave": true,
       *        "stateSaveParams": function (settings, data) {
       *          data.oSearch.sSearch = "";
       *        }
       *      } );
       *    } );
       */
      "fnStateSaveParams": null,

      /**
       * Duration for which the saved state information is considered valid. After this period
       * has elapsed the state will be returned to the default.
       * Value is given in seconds.
       *  @type int
       *  @default 7200 <i>(2 hours)</i>
       *
       *  @dtopt Options
       *  @name DataTable.defaults.stateDuration
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "stateDuration": 60*60*24; // 1 day
       *      } );
       *    } )
       */
      "iStateDuration": 7200,

      /**
       * When enabled DataTables will not make a request to the server for the first
       * page draw - rather it will use the data already on the page (no sorting etc
       * will be applied to it), thus saving on an XHR at load time. `deferLoading`
       * is used to indicate that deferred loading is required, but it is also used
       * to tell DataTables how many records there are in the full table (allowing
       * the information element and pagination to be displayed correctly). In the case
       * where a filtering is applied to the table on initial load, this can be
       * indicated by giving the parameter as an array, where the first element is
       * the number of records available after filtering and the second element is the
       * number of records without filtering (allowing the table information element
       * to be shown correctly).
       *  @type int | array
       *  @default null
       *
       *  @dtopt Options
       *  @name DataTable.defaults.deferLoading
       *
       *  @example
       *    // 57 records available in the table, no filtering applied
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "serverSide": true,
       *        "ajax": "scripts/server_processing.php",
       *        "deferLoading": 57
       *      } );
       *    } );
       *
       *  @example
       *    // 57 records after filtering, 100 without filtering (an initial filter applied)
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "serverSide": true,
       *        "ajax": "scripts/server_processing.php",
       *        "deferLoading": [ 57, 100 ],
       *        "search": {
       *          "search": "my_filter"
       *        }
       *      } );
       *    } );
       */
      "iDeferLoading": null,

      /**
       * Number of rows to display on a single page when using pagination. If
       * feature enabled (`lengthChange`) then the end user will be able to override
       * this to a custom setting using a pop-up menu.
       *  @type int
       *  @default 10
       *
       *  @dtopt Options
       *  @name DataTable.defaults.pageLength
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "pageLength": 50
       *      } );
       *    } )
       */
      "iDisplayLength": 10,

      /**
       * Define the starting point for data display when using DataTables with
       * pagination. Note that this parameter is the number of records, rather than
       * the page number, so if you have 10 records per page and want to start on
       * the third page, it should be "20".
       *  @type int
       *  @default 0
       *
       *  @dtopt Options
       *  @name DataTable.defaults.displayStart
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "displayStart": 20
       *      } );
       *    } )
       */
      "iDisplayStart": 0,

      /**
       * By default DataTables allows keyboard navigation of the table (sorting, paging,
       * and filtering) by adding a `tabindex` attribute to the required elements. This
       * allows you to tab through the controls and press the enter key to activate them.
       * The tabindex is default 0, meaning that the tab follows the flow of the document.
       * You can overrule this using this parameter if you wish. Use a value of -1 to
       * disable built-in keyboard navigation.
       *  @type int
       *  @default 0
       *
       *  @dtopt Options
       *  @name DataTable.defaults.tabIndex
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "tabIndex": 1
       *      } );
       *    } );
       */
      "iTabIndex": 0,

      /**
       * Classes that DataTables assigns to the various components and features
       * that it adds to the HTML table. This allows classes to be configured
       * during initialisation in addition to through the static
       * {@link DataTable.ext.oStdClasses} object).
       *  @namespace
       *  @name DataTable.defaults.classes
       */
      "oClasses": {},

      /**
       * All strings that DataTables uses in the user interface that it creates
       * are defined in this object, allowing you to modified them individually or
       * completely replace them all as required.
       *  @namespace
       *  @name DataTable.defaults.language
       */
      "oLanguage": {
        /**
         * Strings that are used for WAI-ARIA labels and controls only (these are not
         * actually visible on the page, but will be read by screenreaders, and thus
         * must be internationalised as well).
         *  @namespace
         *  @name DataTable.defaults.language.aria
         */
        "oAria": {
          /**
           * ARIA label that is added to the table headers when the column may be
           * sorted ascending by activing the column (click or return when focused).
           * Note that the column header is prefixed to this string.
           *  @type string
           *  @default : activate to sort column ascending
           *
           *  @dtopt Language
           *  @name DataTable.defaults.language.aria.sortAscending
           *
           *  @example
           *    $(document).ready( function() {
           *      $('#example').dataTable( {
           *        "language": {
           *          "aria": {
           *            "sortAscending": " - click/return to sort ascending"
           *          }
           *        }
           *      } );
           *    } );
           */
          "sSortAscending": ": activate to sort column ascending",

          /**
           * ARIA label that is added to the table headers when the column may be
           * sorted descending by activing the column (click or return when focused).
           * Note that the column header is prefixed to this string.
           *  @type string
           *  @default : activate to sort column ascending
           *
           *  @dtopt Language
           *  @name DataTable.defaults.language.aria.sortDescending
           *
           *  @example
           *    $(document).ready( function() {
           *      $('#example').dataTable( {
           *        "language": {
           *          "aria": {
           *            "sortDescending": " - click/return to sort descending"
           *          }
           *        }
           *      } );
           *    } );
           */
          "sSortDescending": ": activate to sort column descending"
        },

        /**
         * Pagination string used by DataTables for the built-in pagination
         * control types.
         *  @namespace
         *  @name DataTable.defaults.language.paginate
         */
        "oPaginate": {
          /**
           * Text to use when using the 'full_numbers' type of pagination for the
           * button to take the user to the first page.
           *  @type string
           *  @default First
           *
           *  @dtopt Language
           *  @name DataTable.defaults.language.paginate.first
           *
           *  @example
           *    $(document).ready( function() {
           *      $('#example').dataTable( {
           *        "language": {
           *          "paginate": {
           *            "first": "First page"
           *          }
           *        }
           *      } );
           *    } );
           */
          "sFirst": "First",

          /**
           * Text to use when using the 'full_numbers' type of pagination for the
           * button to take the user to the last page.
           *  @type string
           *  @default Last
           *
           *  @dtopt Language
           *  @name DataTable.defaults.language.paginate.last
           *
           *  @example
           *    $(document).ready( function() {
           *      $('#example').dataTable( {
           *        "language": {
           *          "paginate": {
           *            "last": "Last page"
           *          }
           *        }
           *      } );
           *    } );
           */
          "sLast": "Last",

          /**
           * Text to use for the 'next' pagination button (to take the user to the
           * next page).
           *  @type string
           *  @default Next
           *
           *  @dtopt Language
           *  @name DataTable.defaults.language.paginate.next
           *
           *  @example
           *    $(document).ready( function() {
           *      $('#example').dataTable( {
           *        "language": {
           *          "paginate": {
           *            "next": "Next page"
           *          }
           *        }
           *      } );
           *    } );
           */
          "sNext": "Next",

          /**
           * Text to use for the 'previous' pagination button (to take the user to
           * the previous page).
           *  @type string
           *  @default Previous
           *
           *  @dtopt Language
           *  @name DataTable.defaults.language.paginate.previous
           *
           *  @example
           *    $(document).ready( function() {
           *      $('#example').dataTable( {
           *        "language": {
           *          "paginate": {
           *            "previous": "Previous page"
           *          }
           *        }
           *      } );
           *    } );
           */
          "sPrevious": "Previous"
        },

        /**
         * This string is shown in preference to `zeroRecords` when the table is
         * empty of data (regardless of filtering). Note that this is an optional
         * parameter - if it is not given, the value of `zeroRecords` will be used
         * instead (either the default or given value).
         *  @type string
         *  @default No data available in table
         *
         *  @dtopt Language
         *  @name DataTable.defaults.language.emptyTable
         *
         *  @example
         *    $(document).ready( function() {
         *      $('#example').dataTable( {
         *        "language": {
         *          "emptyTable": "No data available in table"
         *        }
         *      } );
         *    } );
         */
        "sEmptyTable": "No data available in table",

        /**
         * This string gives information to the end user about the information
         * that is current on display on the page. The following tokens can be
         * used in the string and will be dynamically replaced as the table
         * display updates. This tokens can be placed anywhere in the string, or
         * removed as needed by the language requires:
         *
         * * `\_START\_` - Display index of the first record on the current page
         * * `\_END\_` - Display index of the last record on the current page
         * * `\_TOTAL\_` - Number of records in the table after filtering
         * * `\_MAX\_` - Number of records in the table without filtering
         * * `\_PAGE\_` - Current page number
         * * `\_PAGES\_` - Total number of pages of data in the table
         *
         *  @type string
         *  @default Showing _START_ to _END_ of _TOTAL_ entries
         *
         *  @dtopt Language
         *  @name DataTable.defaults.language.info
         *
         *  @example
         *    $(document).ready( function() {
         *      $('#example').dataTable( {
         *        "language": {
         *          "info": "Showing page _PAGE_ of _PAGES_"
         *        }
         *      } );
         *    } );
         */
        "sInfo": "Showing _START_ to _END_ of _TOTAL_ entries",

        /**
         * Display information string for when the table is empty. Typically the
         * format of this string should match `info`.
         *  @type string
         *  @default Showing 0 to 0 of 0 entries
         *
         *  @dtopt Language
         *  @name DataTable.defaults.language.infoEmpty
         *
         *  @example
         *    $(document).ready( function() {
         *      $('#example').dataTable( {
         *        "language": {
         *          "infoEmpty": "No entries to show"
         *        }
         *      } );
         *    } );
         */
        "sInfoEmpty": "Showing 0 to 0 of 0 entries",

        /**
         * When a user filters the information in a table, this string is appended
         * to the information (`info`) to give an idea of how strong the filtering
         * is. The variable _MAX_ is dynamically updated.
         *  @type string
         *  @default (filtered from _MAX_ total entries)
         *
         *  @dtopt Language
         *  @name DataTable.defaults.language.infoFiltered
         *
         *  @example
         *    $(document).ready( function() {
         *      $('#example').dataTable( {
         *        "language": {
         *          "infoFiltered": " - filtering from _MAX_ records"
         *        }
         *      } );
         *    } );
         */
        "sInfoFiltered": "(filtered from _MAX_ total entries)",

        /**
         * If can be useful to append extra information to the info string at times,
         * and this variable does exactly that. This information will be appended to
         * the `info` (`infoEmpty` and `infoFiltered` in whatever combination they are
         * being used) at all times.
         *  @type string
         *  @default <i>Empty string</i>
         *
         *  @dtopt Language
         *  @name DataTable.defaults.language.infoPostFix
         *
         *  @example
         *    $(document).ready( function() {
         *      $('#example').dataTable( {
         *        "language": {
         *          "infoPostFix": "All records shown are derived from real information."
         *        }
         *      } );
         *    } );
         */
        "sInfoPostFix": "",

        /**
         * This decimal place operator is a little different from the other
         * language options since DataTables doesn't output floating point
         * numbers, so it won't ever use this for display of a number. Rather,
         * what this parameter does is modify the sort methods of the table so
         * that numbers which are in a format which has a character other than
         * a period (`.`) as a decimal place will be sorted numerically.
         *
         * Note that numbers with different decimal places cannot be shown in
         * the same table and still be sortable, the table must be consistent.
         * However, multiple different tables on the page can use different
         * decimal place characters.
         *  @type string
         *  @default 
         *
         *  @dtopt Language
         *  @name DataTable.defaults.language.decimal
         *
         *  @example
         *    $(document).ready( function() {
         *      $('#example').dataTable( {
         *        "language": {
         *          "decimal": ","
         *          "thousands": "."
         *        }
         *      } );
         *    } );
         */
        "sDecimal": "",

        /**
         * DataTables has a build in number formatter (`formatNumber`) which is
         * used to format large numbers that are used in the table information.
         * By default a comma is used, but this can be trivially changed to any
         * character you wish with this parameter.
         *  @type string
         *  @default ,
         *
         *  @dtopt Language
         *  @name DataTable.defaults.language.thousands
         *
         *  @example
         *    $(document).ready( function() {
         *      $('#example').dataTable( {
         *        "language": {
         *          "thousands": "'"
         *        }
         *      } );
         *    } );
         */
        "sThousands": ",",

        /**
         * Detail the action that will be taken when the drop down menu for the
         * pagination length option is changed. The '_MENU_' variable is replaced
         * with a default select list of 10, 25, 50 and 100, and can be replaced
         * with a custom select box if required.
         *  @type string
         *  @default Show _MENU_ entries
         *
         *  @dtopt Language
         *  @name DataTable.defaults.language.lengthMenu
         *
         *  @example
         *    // Language change only
         *    $(document).ready( function() {
         *      $('#example').dataTable( {
         *        "language": {
         *          "lengthMenu": "Display _MENU_ records"
         *        }
         *      } );
         *    } );
         *
         *  @example
         *    // Language and options change
         *    $(document).ready( function() {
         *      $('#example').dataTable( {
         *        "language": {
         *          "lengthMenu": 'Display <select>'+
         *            '<option value="10">10</option>'+
         *            '<option value="20">20</option>'+
         *            '<option value="30">30</option>'+
         *            '<option value="40">40</option>'+
         *            '<option value="50">50</option>'+
         *            '<option value="-1">All</option>'+
         *            '</select> records'
         *        }
         *      } );
         *    } );
         */
        "sLengthMenu": "Show _MENU_ entries",

        /**
         * When using Ajax sourced data and during the first draw when DataTables is
         * gathering the data, this message is shown in an empty row in the table to
         * indicate to the end user the the data is being loaded. Note that this
         * parameter is not used when loading data by server-side processing, just
         * Ajax sourced data with client-side processing.
         *  @type string
         *  @default Loading...
         *
         *  @dtopt Language
         *  @name DataTable.defaults.language.loadingRecords
         *
         *  @example
         *    $(document).ready( function() {
         *      $('#example').dataTable( {
         *        "language": {
         *          "loadingRecords": "Please wait - loading..."
         *        }
         *      } );
         *    } );
         */
        "sLoadingRecords": "Loading...",

        /**
         * Text which is displayed when the table is processing a user action
         * (usually a sort command or similar).
         *  @type string
         *  @default Processing...
         *
         *  @dtopt Language
         *  @name DataTable.defaults.language.processing
         *
         *  @example
         *    $(document).ready( function() {
         *      $('#example').dataTable( {
         *        "language": {
         *          "processing": "DataTables is currently busy"
         *        }
         *      } );
         *    } );
         */
        "sProcessing": "Processing...",

        /**
         * Details the actions that will be taken when the user types into the
         * filtering input text box. The variable "_INPUT_", if used in the string,
         * is replaced with the HTML text box for the filtering input allowing
         * control over where it appears in the string. If "_INPUT_" is not given
         * then the input box is appended to the string automatically.
         *  @type string
         *  @default Search:
         *
         *  @dtopt Language
         *  @name DataTable.defaults.language.search
         *
         *  @example
         *    // Input text box will be appended at the end automatically
         *    $(document).ready( function() {
         *      $('#example').dataTable( {
         *        "language": {
         *          "search": "Filter records:"
         *        }
         *      } );
         *    } );
         *
         *  @example
         *    // Specify where the filter should appear
         *    $(document).ready( function() {
         *      $('#example').dataTable( {
         *        "language": {
         *          "search": "Apply filter _INPUT_ to table"
         *        }
         *      } );
         *    } );
         */
        "sSearch": "Search:",

        /**
         * Assign a `placeholder` attribute to the search `input` element
         *  @type string
         *  @default 
         *
         *  @dtopt Language
         *  @name DataTable.defaults.language.searchPlaceholder
         */
        "sSearchPlaceholder": "",

        /**
         * All of the language information can be stored in a file on the
         * server-side, which DataTables will look up if this parameter is passed.
         * It must store the URL of the language file, which is in a JSON format,
         * and the object has the same properties as the oLanguage object in the
         * initialiser object (i.e. the above parameters). Please refer to one of
         * the example language files to see how this works in action.
         *  @type string
         *  @default <i>Empty string - i.e. disabled</i>
         *
         *  @dtopt Language
         *  @name DataTable.defaults.language.url
         *
         *  @example
         *    $(document).ready( function() {
         *      $('#example').dataTable( {
         *        "language": {
         *          "url": "http://www.sprymedia.co.uk/dataTables/lang.txt"
         *        }
         *      } );
         *    } );
         */
        "sUrl": "",

        /**
         * Text shown inside the table records when the is no information to be
         * displayed after filtering. `emptyTable` is shown when there is simply no
         * information in the table at all (regardless of filtering).
         *  @type string
         *  @default No matching records found
         *
         *  @dtopt Language
         *  @name DataTable.defaults.language.zeroRecords
         *
         *  @example
         *    $(document).ready( function() {
         *      $('#example').dataTable( {
         *        "language": {
         *          "zeroRecords": "No records to display"
         *        }
         *      } );
         *    } );
         */
        "sZeroRecords": "No matching records found"
      },

      /**
       * This parameter allows you to have define the global filtering state at
       * initialisation time. As an object the `search` parameter must be
       * defined, but all other parameters are optional. When `regex` is true,
       * the search string will be treated as a regular expression, when false
       * (default) it will be treated as a straight string. When `smart`
       * DataTables will use it's smart filtering methods (to word match at
       * any point in the data), when false this will not be done.
       *  @namespace
       *  @extends DataTable.models.oSearch
       *
       *  @dtopt Options
       *  @name DataTable.defaults.search
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "search": {"search": "Initial search"}
       *      } );
       *    } )
       */
      "oSearch": $$$1.extend({}, DataTable.models.oSearch),

      /**
       * __Deprecated__ The functionality provided by this parameter has now been
       * superseded by that provided through `ajax`, which should be used instead.
       *
       * By default DataTables will look for the property `data` (or `aaData` for
       * compatibility with DataTables 1.9-) when obtaining data from an Ajax
       * source or for server-side processing - this parameter allows that
       * property to be changed. You can use Javascript dotted object notation to
       * get a data source for multiple levels of nesting.
       *  @type string
       *  @default data
       *
       *  @dtopt Options
       *  @dtopt Server-side
       *  @name DataTable.defaults.ajaxDataProp
       *
       *  @deprecated 1.10. Please use `ajax` for this functionality now.
       */
      "sAjaxDataProp": "data",

      /**
       * __Deprecated__ The functionality provided by this parameter has now been
       * superseded by that provided through `ajax`, which should be used instead.
       *
       * You can instruct DataTables to load data from an external
       * source using this parameter (use aData if you want to pass data in you
       * already have). Simply provide a url a JSON object can be obtained from.
       *  @type string
       *  @default null
       *
       *  @dtopt Options
       *  @dtopt Server-side
       *  @name DataTable.defaults.ajaxSource
       *
       *  @deprecated 1.10. Please use `ajax` for this functionality now.
       */
      "sAjaxSource": null,

      /**
       * This initialisation variable allows you to specify exactly where in the
       * DOM you want DataTables to inject the various controls it adds to the page
       * (for example you might want the pagination controls at the top of the
       * table). DIV elements (with or without a custom class) can also be added to
       * aid styling. The follow syntax is used:
       *   <ul>
       *     <li>The following options are allowed:
       *       <ul>
       *         <li>'l' - Length changing</li>
       *         <li>'f' - Filtering input</li>
       *         <li>'t' - The table!</li>
       *         <li>'i' - Information</li>
       *         <li>'p' - Pagination</li>
       *         <li>'r' - pRocessing</li>
       *       </ul>
       *     </li>
       *     <li>The following constants are allowed:
       *       <ul>
       *         <li>'H' - jQueryUI theme "header" classes ('fg-toolbar ui-widget-header ui-corner-tl ui-corner-tr ui-helper-clearfix')</li>
       *         <li>'F' - jQueryUI theme "footer" classes ('fg-toolbar ui-widget-header ui-corner-bl ui-corner-br ui-helper-clearfix')</li>
       *       </ul>
       *     </li>
       *     <li>The following syntax is expected:
       *       <ul>
       *         <li>'&lt;' and '&gt;' - div elements</li>
       *         <li>'&lt;"class" and '&gt;' - div with a class</li>
       *         <li>'&lt;"#id" and '&gt;' - div with an ID</li>
       *       </ul>
       *     </li>
       *     <li>Examples:
       *       <ul>
       *         <li>'&lt;"wrapper"flipt&gt;'</li>
       *         <li>'&lt;lf&lt;t&gt;ip&gt;'</li>
       *       </ul>
       *     </li>
       *   </ul>
       *  @type string
       *  @default lfrtip <i>(when `jQueryUI` is false)</i> <b>or</b>
       *    <"H"lfr>t<"F"ip> <i>(when `jQueryUI` is true)</i>
       *
       *  @dtopt Options
       *  @name DataTable.defaults.dom
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "dom": '&lt;"top"i&gt;rt&lt;"bottom"flp&gt;&lt;"clear"&gt;'
       *      } );
       *    } );
       */
      "sDom": "lfrtip",

      /**
       * Search delay option. This will throttle full table searches that use the
       * DataTables provided search input element (it does not effect calls to
       * `dt-api search()`, providing a delay before the search is made.
       *  @type integer
       *  @default 0
       *
       *  @dtopt Options
       *  @name DataTable.defaults.searchDelay
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "searchDelay": 200
       *      } );
       *    } )
       */
      "searchDelay": null,

      /**
       * DataTables features six different built-in options for the buttons to
       * display for pagination control:
       *
       * * `numbers` - Page number buttons only
       * * `simple` - 'Previous' and 'Next' buttons only
       * * 'simple_numbers` - 'Previous' and 'Next' buttons, plus page numbers
       * * `full` - 'First', 'Previous', 'Next' and 'Last' buttons
       * * `full_numbers` - 'First', 'Previous', 'Next' and 'Last' buttons, plus page numbers
       * * `first_last_numbers` - 'First' and 'Last' buttons, plus page numbers
       *  
       * Further methods can be added using {@link DataTable.ext.oPagination}.
       *  @type string
       *  @default simple_numbers
       *
       *  @dtopt Options
       *  @name DataTable.defaults.pagingType
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "pagingType": "full_numbers"
       *      } );
       *    } )
       */
      "sPaginationType": "simple_numbers",

      /**
       * Enable horizontal scrolling. When a table is too wide to fit into a
       * certain layout, or you have a large number of columns in the table, you
       * can enable x-scrolling to show the table in a viewport, which can be
       * scrolled. This property can be `true` which will allow the table to
       * scroll horizontally when needed, or any CSS unit, or a number (in which
       * case it will be treated as a pixel measurement). Setting as simply `true`
       * is recommended.
       *  @type boolean|string
       *  @default <i>blank string - i.e. disabled</i>
       *
       *  @dtopt Features
       *  @name DataTable.defaults.scrollX
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "scrollX": true,
       *        "scrollCollapse": true
       *      } );
       *    } );
       */
      "sScrollX": "",

      /**
       * This property can be used to force a DataTable to use more width than it
       * might otherwise do when x-scrolling is enabled. For example if you have a
       * table which requires to be well spaced, this parameter is useful for
       * "over-sizing" the table, and thus forcing scrolling. This property can by
       * any CSS unit, or a number (in which case it will be treated as a pixel
       * measurement).
       *  @type string
       *  @default <i>blank string - i.e. disabled</i>
       *
       *  @dtopt Options
       *  @name DataTable.defaults.scrollXInner
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "scrollX": "100%",
       *        "scrollXInner": "110%"
       *      } );
       *    } );
       */
      "sScrollXInner": "",

      /**
       * Enable vertical scrolling. Vertical scrolling will constrain the DataTable
       * to the given height, and enable scrolling for any data which overflows the
       * current viewport. This can be used as an alternative to paging to display
       * a lot of data in a small area (although paging and scrolling can both be
       * enabled at the same time). This property can be any CSS unit, or a number
       * (in which case it will be treated as a pixel measurement).
       *  @type string
       *  @default <i>blank string - i.e. disabled</i>
       *
       *  @dtopt Features
       *  @name DataTable.defaults.scrollY
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "scrollY": "200px",
       *        "paginate": false
       *      } );
       *    } );
       */
      "sScrollY": "",

      /**
       * __Deprecated__ The functionality provided by this parameter has now been
       * superseded by that provided through `ajax`, which should be used instead.
       *
       * Set the HTTP method that is used to make the Ajax call for server-side
       * processing or Ajax sourced data.
       *  @type string
       *  @default GET
       *
       *  @dtopt Options
       *  @dtopt Server-side
       *  @name DataTable.defaults.serverMethod
       *
       *  @deprecated 1.10. Please use `ajax` for this functionality now.
       */
      "sServerMethod": "GET",

      /**
       * DataTables makes use of renderers when displaying HTML elements for
       * a table. These renderers can be added or modified by plug-ins to
       * generate suitable mark-up for a site. For example the Bootstrap
       * integration plug-in for DataTables uses a paging button renderer to
       * display pagination buttons in the mark-up required by Bootstrap.
       *
       * For further information about the renderers available see
       * DataTable.ext.renderer
       *  @type string|object
       *  @default null
       *
       *  @name DataTable.defaults.renderer
       *
       */
      "renderer": null,

      /**
       * Set the data property name that DataTables should use to get a row's id
       * to set as the `id` property in the node.
       *  @type string
       *  @default DT_RowId
       *
       *  @name DataTable.defaults.rowId
       */
      "rowId": "DT_RowId"
    };

    _fnHungarianMap(DataTable.defaults);
    /*
     * Developer note - See note in model.defaults.js about the use of Hungarian
     * notation and camel case.
     */

    /**
     * Column options that can be given to DataTables at initialisation time.
     *  @namespace
     */


    DataTable.defaults.column = {
      /**
       * Define which column(s) an order will occur on for this column. This
       * allows a column's ordering to take multiple columns into account when
       * doing a sort or use the data from a different column. For example first
       * name / last name columns make sense to do a multi-column sort over the
       * two columns.
       *  @type array|int
       *  @default null <i>Takes the value of the column index automatically</i>
       *
       *  @name DataTable.defaults.column.orderData
       *  @dtopt Columns
       *
       *  @example
       *    // Using `columnDefs`
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columnDefs": [
       *          { "orderData": [ 0, 1 ], "targets": [ 0 ] },
       *          { "orderData": [ 1, 0 ], "targets": [ 1 ] },
       *          { "orderData": 2, "targets": [ 2 ] }
       *        ]
       *      } );
       *    } );
       *
       *  @example
       *    // Using `columns`
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columns": [
       *          { "orderData": [ 0, 1 ] },
       *          { "orderData": [ 1, 0 ] },
       *          { "orderData": 2 },
       *          null,
       *          null
       *        ]
       *      } );
       *    } );
       */
      "aDataSort": null,
      "iDataSort": -1,

      /**
       * You can control the default ordering direction, and even alter the
       * behaviour of the sort handler (i.e. only allow ascending ordering etc)
       * using this parameter.
       *  @type array
       *  @default [ 'asc', 'desc' ]
       *
       *  @name DataTable.defaults.column.orderSequence
       *  @dtopt Columns
       *
       *  @example
       *    // Using `columnDefs`
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columnDefs": [
       *          { "orderSequence": [ "asc" ], "targets": [ 1 ] },
       *          { "orderSequence": [ "desc", "asc", "asc" ], "targets": [ 2 ] },
       *          { "orderSequence": [ "desc" ], "targets": [ 3 ] }
       *        ]
       *      } );
       *    } );
       *
       *  @example
       *    // Using `columns`
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columns": [
       *          null,
       *          { "orderSequence": [ "asc" ] },
       *          { "orderSequence": [ "desc", "asc", "asc" ] },
       *          { "orderSequence": [ "desc" ] },
       *          null
       *        ]
       *      } );
       *    } );
       */
      "asSorting": ['asc', 'desc'],

      /**
       * Enable or disable filtering on the data in this column.
       *  @type boolean
       *  @default true
       *
       *  @name DataTable.defaults.column.searchable
       *  @dtopt Columns
       *
       *  @example
       *    // Using `columnDefs`
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columnDefs": [
       *          { "searchable": false, "targets": [ 0 ] }
       *        ] } );
       *    } );
       *
       *  @example
       *    // Using `columns`
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columns": [
       *          { "searchable": false },
       *          null,
       *          null,
       *          null,
       *          null
       *        ] } );
       *    } );
       */
      "bSearchable": true,

      /**
       * Enable or disable ordering on this column.
       *  @type boolean
       *  @default true
       *
       *  @name DataTable.defaults.column.orderable
       *  @dtopt Columns
       *
       *  @example
       *    // Using `columnDefs`
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columnDefs": [
       *          { "orderable": false, "targets": [ 0 ] }
       *        ] } );
       *    } );
       *
       *  @example
       *    // Using `columns`
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columns": [
       *          { "orderable": false },
       *          null,
       *          null,
       *          null,
       *          null
       *        ] } );
       *    } );
       */
      "bSortable": true,

      /**
       * Enable or disable the display of this column.
       *  @type boolean
       *  @default true
       *
       *  @name DataTable.defaults.column.visible
       *  @dtopt Columns
       *
       *  @example
       *    // Using `columnDefs`
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columnDefs": [
       *          { "visible": false, "targets": [ 0 ] }
       *        ] } );
       *    } );
       *
       *  @example
       *    // Using `columns`
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columns": [
       *          { "visible": false },
       *          null,
       *          null,
       *          null,
       *          null
       *        ] } );
       *    } );
       */
      "bVisible": true,

      /**
       * Developer definable function that is called whenever a cell is created (Ajax source,
       * etc) or processed for input (DOM source). This can be used as a compliment to mRender
       * allowing you to modify the DOM element (add background colour for example) when the
       * element is available.
       *  @type function
       *  @param {element} td The TD node that has been created
       *  @param {*} cellData The Data for the cell
       *  @param {array|object} rowData The data for the whole row
       *  @param {int} row The row index for the aoData data store
       *  @param {int} col The column index for aoColumns
       *
       *  @name DataTable.defaults.column.createdCell
       *  @dtopt Columns
       *
       *  @example
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columnDefs": [ {
       *          "targets": [3],
       *          "createdCell": function (td, cellData, rowData, row, col) {
       *            if ( cellData == "1.7" ) {
       *              $(td).css('color', 'blue')
       *            }
       *          }
       *        } ]
       *      });
       *    } );
       */
      "fnCreatedCell": null,

      /**
       * This parameter has been replaced by `data` in DataTables to ensure naming
       * consistency. `dataProp` can still be used, as there is backwards
       * compatibility in DataTables for this option, but it is strongly
       * recommended that you use `data` in preference to `dataProp`.
       *  @name DataTable.defaults.column.dataProp
       */

      /**
       * This property can be used to read data from any data source property,
       * including deeply nested objects / properties. `data` can be given in a
       * number of different ways which effect its behaviour:
       *
       * * `integer` - treated as an array index for the data source. This is the
       *   default that DataTables uses (incrementally increased for each column).
       * * `string` - read an object property from the data source. There are
       *   three 'special' options that can be used in the string to alter how
       *   DataTables reads the data from the source object:
       *    * `.` - Dotted Javascript notation. Just as you use a `.` in
       *      Javascript to read from nested objects, so to can the options
       *      specified in `data`. For example: `browser.version` or
       *      `browser.name`. If your object parameter name contains a period, use
       *      `\\` to escape it - i.e. `first\\.name`.
       *    * `[]` - Array notation. DataTables can automatically combine data
       *      from and array source, joining the data with the characters provided
       *      between the two brackets. For example: `name[, ]` would provide a
       *      comma-space separated list from the source array. If no characters
       *      are provided between the brackets, the original array source is
       *      returned.
       *    * `()` - Function notation. Adding `()` to the end of a parameter will
       *      execute a function of the name given. For example: `browser()` for a
       *      simple function on the data source, `browser.version()` for a
       *      function in a nested property or even `browser().version` to get an
       *      object property if the function called returns an object. Note that
       *      function notation is recommended for use in `render` rather than
       *      `data` as it is much simpler to use as a renderer.
       * * `null` - use the original data source for the row rather than plucking
       *   data directly from it. This action has effects on two other
       *   initialisation options:
       *    * `defaultContent` - When null is given as the `data` option and
       *      `defaultContent` is specified for the column, the value defined by
       *      `defaultContent` will be used for the cell.
       *    * `render` - When null is used for the `data` option and the `render`
       *      option is specified for the column, the whole data source for the
       *      row is used for the renderer.
       * * `function` - the function given will be executed whenever DataTables
       *   needs to set or get the data for a cell in the column. The function
       *   takes three parameters:
       *    * Parameters:
       *      * `{array|object}` The data source for the row
       *      * `{string}` The type call data requested - this will be 'set' when
       *        setting data or 'filter', 'display', 'type', 'sort' or undefined
       *        when gathering data. Note that when `undefined` is given for the
       *        type DataTables expects to get the raw data for the object back<
       *      * `{*}` Data to set when the second parameter is 'set'.
       *    * Return:
       *      * The return value from the function is not required when 'set' is
       *        the type of call, but otherwise the return is what will be used
       *        for the data requested.
       *
       * Note that `data` is a getter and setter option. If you just require
       * formatting of data for output, you will likely want to use `render` which
       * is simply a getter and thus simpler to use.
       *
       * Note that prior to DataTables 1.9.2 `data` was called `mDataProp`. The
       * name change reflects the flexibility of this property and is consistent
       * with the naming of mRender. If 'mDataProp' is given, then it will still
       * be used by DataTables, as it automatically maps the old name to the new
       * if required.
       *
       *  @type string|int|function|null
       *  @default null <i>Use automatically calculated column index</i>
       *
       *  @name DataTable.defaults.column.data
       *  @dtopt Columns
       *
       *  @example
       *    // Read table data from objects
       *    // JSON structure for each row:
       *    //   {
       *    //      "engine": {value},
       *    //      "browser": {value},
       *    //      "platform": {value},
       *    //      "version": {value},
       *    //      "grade": {value}
       *    //   }
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "ajaxSource": "sources/objects.txt",
       *        "columns": [
       *          { "data": "engine" },
       *          { "data": "browser" },
       *          { "data": "platform" },
       *          { "data": "version" },
       *          { "data": "grade" }
       *        ]
       *      } );
       *    } );
       *
       *  @example
       *    // Read information from deeply nested objects
       *    // JSON structure for each row:
       *    //   {
       *    //      "engine": {value},
       *    //      "browser": {value},
       *    //      "platform": {
       *    //         "inner": {value}
       *    //      },
       *    //      "details": [
       *    //         {value}, {value}
       *    //      ]
       *    //   }
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "ajaxSource": "sources/deep.txt",
       *        "columns": [
       *          { "data": "engine" },
       *          { "data": "browser" },
       *          { "data": "platform.inner" },
       *          { "data": "details.0" },
       *          { "data": "details.1" }
       *        ]
       *      } );
       *    } );
       *
       *  @example
       *    // Using `data` as a function to provide different information for
       *    // sorting, filtering and display. In this case, currency (price)
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columnDefs": [ {
       *          "targets": [ 0 ],
       *          "data": function ( source, type, val ) {
       *            if (type === 'set') {
       *              source.price = val;
       *              // Store the computed dislay and filter values for efficiency
       *              source.price_display = val=="" ? "" : "$"+numberFormat(val);
       *              source.price_filter  = val=="" ? "" : "$"+numberFormat(val)+" "+val;
       *              return;
       *            }
       *            else if (type === 'display') {
       *              return source.price_display;
       *            }
       *            else if (type === 'filter') {
       *              return source.price_filter;
       *            }
       *            // 'sort', 'type' and undefined all just use the integer
       *            return source.price;
       *          }
       *        } ]
       *      } );
       *    } );
       *
       *  @example
       *    // Using default content
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columnDefs": [ {
       *          "targets": [ 0 ],
       *          "data": null,
       *          "defaultContent": "Click to edit"
       *        } ]
       *      } );
       *    } );
       *
       *  @example
       *    // Using array notation - outputting a list from an array
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columnDefs": [ {
       *          "targets": [ 0 ],
       *          "data": "name[, ]"
       *        } ]
       *      } );
       *    } );
       *
       */
      "mData": null,

      /**
       * This property is the rendering partner to `data` and it is suggested that
       * when you want to manipulate data for display (including filtering,
       * sorting etc) without altering the underlying data for the table, use this
       * property. `render` can be considered to be the the read only companion to
       * `data` which is read / write (then as such more complex). Like `data`
       * this option can be given in a number of different ways to effect its
       * behaviour:
       *
       * * `integer` - treated as an array index for the data source. This is the
       *   default that DataTables uses (incrementally increased for each column).
       * * `string` - read an object property from the data source. There are
       *   three 'special' options that can be used in the string to alter how
       *   DataTables reads the data from the source object:
       *    * `.` - Dotted Javascript notation. Just as you use a `.` in
       *      Javascript to read from nested objects, so to can the options
       *      specified in `data`. For example: `browser.version` or
       *      `browser.name`. If your object parameter name contains a period, use
       *      `\\` to escape it - i.e. `first\\.name`.
       *    * `[]` - Array notation. DataTables can automatically combine data
       *      from and array source, joining the data with the characters provided
       *      between the two brackets. For example: `name[, ]` would provide a
       *      comma-space separated list from the source array. If no characters
       *      are provided between the brackets, the original array source is
       *      returned.
       *    * `()` - Function notation. Adding `()` to the end of a parameter will
       *      execute a function of the name given. For example: `browser()` for a
       *      simple function on the data source, `browser.version()` for a
       *      function in a nested property or even `browser().version` to get an
       *      object property if the function called returns an object.
       * * `object` - use different data for the different data types requested by
       *   DataTables ('filter', 'display', 'type' or 'sort'). The property names
       *   of the object is the data type the property refers to and the value can
       *   defined using an integer, string or function using the same rules as
       *   `render` normally does. Note that an `_` option _must_ be specified.
       *   This is the default value to use if you haven't specified a value for
       *   the data type requested by DataTables.
       * * `function` - the function given will be executed whenever DataTables
       *   needs to set or get the data for a cell in the column. The function
       *   takes three parameters:
       *    * Parameters:
       *      * {array|object} The data source for the row (based on `data`)
       *      * {string} The type call data requested - this will be 'filter',
       *        'display', 'type' or 'sort'.
       *      * {array|object} The full data source for the row (not based on
       *        `data`)
       *    * Return:
       *      * The return value from the function is what will be used for the
       *        data requested.
       *
       *  @type string|int|function|object|null
       *  @default null Use the data source value.
       *
       *  @name DataTable.defaults.column.render
       *  @dtopt Columns
       *
       *  @example
       *    // Create a comma separated list from an array of objects
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "ajaxSource": "sources/deep.txt",
       *        "columns": [
       *          { "data": "engine" },
       *          { "data": "browser" },
       *          {
       *            "data": "platform",
       *            "render": "[, ].name"
       *          }
       *        ]
       *      } );
       *    } );
       *
       *  @example
       *    // Execute a function to obtain data
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columnDefs": [ {
       *          "targets": [ 0 ],
       *          "data": null, // Use the full data source object for the renderer's source
       *          "render": "browserName()"
       *        } ]
       *      } );
       *    } );
       *
       *  @example
       *    // As an object, extracting different data for the different types
       *    // This would be used with a data source such as:
       *    //   { "phone": 5552368, "phone_filter": "5552368 555-2368", "phone_display": "555-2368" }
       *    // Here the `phone` integer is used for sorting and type detection, while `phone_filter`
       *    // (which has both forms) is used for filtering for if a user inputs either format, while
       *    // the formatted phone number is the one that is shown in the table.
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columnDefs": [ {
       *          "targets": [ 0 ],
       *          "data": null, // Use the full data source object for the renderer's source
       *          "render": {
       *            "_": "phone",
       *            "filter": "phone_filter",
       *            "display": "phone_display"
       *          }
       *        } ]
       *      } );
       *    } );
       *
       *  @example
       *    // Use as a function to create a link from the data source
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columnDefs": [ {
       *          "targets": [ 0 ],
       *          "data": "download_link",
       *          "render": function ( data, type, full ) {
       *            return '<a href="'+data+'">Download</a>';
       *          }
       *        } ]
       *      } );
       *    } );
       */
      "mRender": null,

      /**
       * Change the cell type created for the column - either TD cells or TH cells. This
       * can be useful as TH cells have semantic meaning in the table body, allowing them
       * to act as a header for a row (you may wish to add scope='row' to the TH elements).
       *  @type string
       *  @default td
       *
       *  @name DataTable.defaults.column.cellType
       *  @dtopt Columns
       *
       *  @example
       *    // Make the first column use TH cells
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columnDefs": [ {
       *          "targets": [ 0 ],
       *          "cellType": "th"
       *        } ]
       *      } );
       *    } );
       */
      "sCellType": "td",

      /**
       * Class to give to each cell in this column.
       *  @type string
       *  @default <i>Empty string</i>
       *
       *  @name DataTable.defaults.column.class
       *  @dtopt Columns
       *
       *  @example
       *    // Using `columnDefs`
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columnDefs": [
       *          { "class": "my_class", "targets": [ 0 ] }
       *        ]
       *      } );
       *    } );
       *
       *  @example
       *    // Using `columns`
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columns": [
       *          { "class": "my_class" },
       *          null,
       *          null,
       *          null,
       *          null
       *        ]
       *      } );
       *    } );
       */
      "sClass": "",

      /**
       * When DataTables calculates the column widths to assign to each column,
       * it finds the longest string in each column and then constructs a
       * temporary table and reads the widths from that. The problem with this
       * is that "mmm" is much wider then "iiii", but the latter is a longer
       * string - thus the calculation can go wrong (doing it properly and putting
       * it into an DOM object and measuring that is horribly(!) slow). Thus as
       * a "work around" we provide this option. It will append its value to the
       * text that is found to be the longest string for the column - i.e. padding.
       * Generally you shouldn't need this!
       *  @type string
       *  @default <i>Empty string<i>
       *
       *  @name DataTable.defaults.column.contentPadding
       *  @dtopt Columns
       *
       *  @example
       *    // Using `columns`
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columns": [
       *          null,
       *          null,
       *          null,
       *          {
       *            "contentPadding": "mmm"
       *          }
       *        ]
       *      } );
       *    } );
       */
      "sContentPadding": "",

      /**
       * Allows a default value to be given for a column's data, and will be used
       * whenever a null data source is encountered (this can be because `data`
       * is set to null, or because the data source itself is null).
       *  @type string
       *  @default null
       *
       *  @name DataTable.defaults.column.defaultContent
       *  @dtopt Columns
       *
       *  @example
       *    // Using `columnDefs`
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columnDefs": [
       *          {
       *            "data": null,
       *            "defaultContent": "Edit",
       *            "targets": [ -1 ]
       *          }
       *        ]
       *      } );
       *    } );
       *
       *  @example
       *    // Using `columns`
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columns": [
       *          null,
       *          null,
       *          null,
       *          {
       *            "data": null,
       *            "defaultContent": "Edit"
       *          }
       *        ]
       *      } );
       *    } );
       */
      "sDefaultContent": null,

      /**
       * This parameter is only used in DataTables' server-side processing. It can
       * be exceptionally useful to know what columns are being displayed on the
       * client side, and to map these to database fields. When defined, the names
       * also allow DataTables to reorder information from the server if it comes
       * back in an unexpected order (i.e. if you switch your columns around on the
       * client-side, your server-side code does not also need updating).
       *  @type string
       *  @default <i>Empty string</i>
       *
       *  @name DataTable.defaults.column.name
       *  @dtopt Columns
       *
       *  @example
       *    // Using `columnDefs`
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columnDefs": [
       *          { "name": "engine", "targets": [ 0 ] },
       *          { "name": "browser", "targets": [ 1 ] },
       *          { "name": "platform", "targets": [ 2 ] },
       *          { "name": "version", "targets": [ 3 ] },
       *          { "name": "grade", "targets": [ 4 ] }
       *        ]
       *      } );
       *    } );
       *
       *  @example
       *    // Using `columns`
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columns": [
       *          { "name": "engine" },
       *          { "name": "browser" },
       *          { "name": "platform" },
       *          { "name": "version" },
       *          { "name": "grade" }
       *        ]
       *      } );
       *    } );
       */
      "sName": "",

      /**
       * Defines a data source type for the ordering which can be used to read
       * real-time information from the table (updating the internally cached
       * version) prior to ordering. This allows ordering to occur on user
       * editable elements such as form inputs.
       *  @type string
       *  @default std
       *
       *  @name DataTable.defaults.column.orderDataType
       *  @dtopt Columns
       *
       *  @example
       *    // Using `columnDefs`
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columnDefs": [
       *          { "orderDataType": "dom-text", "targets": [ 2, 3 ] },
       *          { "type": "numeric", "targets": [ 3 ] },
       *          { "orderDataType": "dom-select", "targets": [ 4 ] },
       *          { "orderDataType": "dom-checkbox", "targets": [ 5 ] }
       *        ]
       *      } );
       *    } );
       *
       *  @example
       *    // Using `columns`
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columns": [
       *          null,
       *          null,
       *          { "orderDataType": "dom-text" },
       *          { "orderDataType": "dom-text", "type": "numeric" },
       *          { "orderDataType": "dom-select" },
       *          { "orderDataType": "dom-checkbox" }
       *        ]
       *      } );
       *    } );
       */
      "sSortDataType": "std",

      /**
       * The title of this column.
       *  @type string
       *  @default null <i>Derived from the 'TH' value for this column in the
       *    original HTML table.</i>
       *
       *  @name DataTable.defaults.column.title
       *  @dtopt Columns
       *
       *  @example
       *    // Using `columnDefs`
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columnDefs": [
       *          { "title": "My column title", "targets": [ 0 ] }
       *        ]
       *      } );
       *    } );
       *
       *  @example
       *    // Using `columns`
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columns": [
       *          { "title": "My column title" },
       *          null,
       *          null,
       *          null,
       *          null
       *        ]
       *      } );
       *    } );
       */
      "sTitle": null,

      /**
       * The type allows you to specify how the data for this column will be
       * ordered. Four types (string, numeric, date and html (which will strip
       * HTML tags before ordering)) are currently available. Note that only date
       * formats understood by Javascript's Date() object will be accepted as type
       * date. For example: "Mar 26, 2008 5:03 PM". May take the values: 'string',
       * 'numeric', 'date' or 'html' (by default). Further types can be adding
       * through plug-ins.
       *  @type string
       *  @default null <i>Auto-detected from raw data</i>
       *
       *  @name DataTable.defaults.column.type
       *  @dtopt Columns
       *
       *  @example
       *    // Using `columnDefs`
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columnDefs": [
       *          { "type": "html", "targets": [ 0 ] }
       *        ]
       *      } );
       *    } );
       *
       *  @example
       *    // Using `columns`
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columns": [
       *          { "type": "html" },
       *          null,
       *          null,
       *          null,
       *          null
       *        ]
       *      } );
       *    } );
       */
      "sType": null,

      /**
       * Defining the width of the column, this parameter may take any CSS value
       * (3em, 20px etc). DataTables applies 'smart' widths to columns which have not
       * been given a specific width through this interface ensuring that the table
       * remains readable.
       *  @type string
       *  @default null <i>Automatic</i>
       *
       *  @name DataTable.defaults.column.width
       *  @dtopt Columns
       *
       *  @example
       *    // Using `columnDefs`
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columnDefs": [
       *          { "width": "20%", "targets": [ 0 ] }
       *        ]
       *      } );
       *    } );
       *
       *  @example
       *    // Using `columns`
       *    $(document).ready( function() {
       *      $('#example').dataTable( {
       *        "columns": [
       *          { "width": "20%" },
       *          null,
       *          null,
       *          null,
       *          null
       *        ]
       *      } );
       *    } );
       */
      "sWidth": null
    };

    _fnHungarianMap(DataTable.defaults.column);
    /**
     * DataTables settings object - this holds all the information needed for a
     * given table, including configuration, data and current application of the
     * table options. DataTables does not have a single instance for each DataTable
     * with the settings attached to that instance, but rather instances of the
     * DataTable "class" are created on-the-fly as needed (typically by a
     * $().dataTable() call) and the settings object is then applied to that
     * instance.
     *
     * Note that this object is related to {@link DataTable.defaults} but this
     * one is the internal data store for DataTables's cache of columns. It should
     * NOT be manipulated outside of DataTables. Any configuration should be done
     * through the initialisation options.
     *  @namespace
     *  @todo Really should attach the settings object to individual instances so we
     *    don't need to create new instances on each $().dataTable() call (if the
     *    table already exists). It would also save passing oSettings around and
     *    into every single function. However, this is a very significant
     *    architecture change for DataTables and will almost certainly break
     *    backwards compatibility with older installations. This is something that
     *    will be done in 2.0.
     */


    DataTable.models.oSettings = {
      /**
       * Primary features of DataTables and their enablement state.
       *  @namespace
       */
      "oFeatures": {
        /**
         * Flag to say if DataTables should automatically try to calculate the
         * optimum table and columns widths (true) or not (false).
         * Note that this parameter will be set by the initialisation routine. To
         * set a default use {@link DataTable.defaults}.
         *  @type boolean
         */
        "bAutoWidth": null,

        /**
         * Delay the creation of TR and TD elements until they are actually
         * needed by a driven page draw. This can give a significant speed
         * increase for Ajax source and Javascript source data, but makes no
         * difference at all fro DOM and server-side processing tables.
         * Note that this parameter will be set by the initialisation routine. To
         * set a default use {@link DataTable.defaults}.
         *  @type boolean
         */
        "bDeferRender": null,

        /**
         * Enable filtering on the table or not. Note that if this is disabled
         * then there is no filtering at all on the table, including fnFilter.
         * To just remove the filtering input use sDom and remove the 'f' option.
         * Note that this parameter will be set by the initialisation routine. To
         * set a default use {@link DataTable.defaults}.
         *  @type boolean
         */
        "bFilter": null,

        /**
         * Table information element (the 'Showing x of y records' div) enable
         * flag.
         * Note that this parameter will be set by the initialisation routine. To
         * set a default use {@link DataTable.defaults}.
         *  @type boolean
         */
        "bInfo": null,

        /**
         * Present a user control allowing the end user to change the page size
         * when pagination is enabled.
         * Note that this parameter will be set by the initialisation routine. To
         * set a default use {@link DataTable.defaults}.
         *  @type boolean
         */
        "bLengthChange": null,

        /**
         * Pagination enabled or not. Note that if this is disabled then length
         * changing must also be disabled.
         * Note that this parameter will be set by the initialisation routine. To
         * set a default use {@link DataTable.defaults}.
         *  @type boolean
         */
        "bPaginate": null,

        /**
         * Processing indicator enable flag whenever DataTables is enacting a
         * user request - typically an Ajax request for server-side processing.
         * Note that this parameter will be set by the initialisation routine. To
         * set a default use {@link DataTable.defaults}.
         *  @type boolean
         */
        "bProcessing": null,

        /**
         * Server-side processing enabled flag - when enabled DataTables will
         * get all data from the server for every draw - there is no filtering,
         * sorting or paging done on the client-side.
         * Note that this parameter will be set by the initialisation routine. To
         * set a default use {@link DataTable.defaults}.
         *  @type boolean
         */
        "bServerSide": null,

        /**
         * Sorting enablement flag.
         * Note that this parameter will be set by the initialisation routine. To
         * set a default use {@link DataTable.defaults}.
         *  @type boolean
         */
        "bSort": null,

        /**
         * Multi-column sorting
         * Note that this parameter will be set by the initialisation routine. To
         * set a default use {@link DataTable.defaults}.
         *  @type boolean
         */
        "bSortMulti": null,

        /**
         * Apply a class to the columns which are being sorted to provide a
         * visual highlight or not. This can slow things down when enabled since
         * there is a lot of DOM interaction.
         * Note that this parameter will be set by the initialisation routine. To
         * set a default use {@link DataTable.defaults}.
         *  @type boolean
         */
        "bSortClasses": null,

        /**
         * State saving enablement flag.
         * Note that this parameter will be set by the initialisation routine. To
         * set a default use {@link DataTable.defaults}.
         *  @type boolean
         */
        "bStateSave": null
      },

      /**
       * Scrolling settings for a table.
       *  @namespace
       */
      "oScroll": {
        /**
         * When the table is shorter in height than sScrollY, collapse the
         * table container down to the height of the table (when true).
         * Note that this parameter will be set by the initialisation routine. To
         * set a default use {@link DataTable.defaults}.
         *  @type boolean
         */
        "bCollapse": null,

        /**
         * Width of the scrollbar for the web-browser's platform. Calculated
         * during table initialisation.
         *  @type int
         *  @default 0
         */
        "iBarWidth": 0,

        /**
         * Viewport width for horizontal scrolling. Horizontal scrolling is
         * disabled if an empty string.
         * Note that this parameter will be set by the initialisation routine. To
         * set a default use {@link DataTable.defaults}.
         *  @type string
         */
        "sX": null,

        /**
         * Width to expand the table to when using x-scrolling. Typically you
         * should not need to use this.
         * Note that this parameter will be set by the initialisation routine. To
         * set a default use {@link DataTable.defaults}.
         *  @type string
         *  @deprecated
         */
        "sXInner": null,

        /**
         * Viewport height for vertical scrolling. Vertical scrolling is disabled
         * if an empty string.
         * Note that this parameter will be set by the initialisation routine. To
         * set a default use {@link DataTable.defaults}.
         *  @type string
         */
        "sY": null
      },

      /**
       * Language information for the table.
       *  @namespace
       *  @extends DataTable.defaults.oLanguage
       */
      "oLanguage": {
        /**
         * Information callback function. See
         * {@link DataTable.defaults.fnInfoCallback}
         *  @type function
         *  @default null
         */
        "fnInfoCallback": null
      },

      /**
       * Browser support parameters
       *  @namespace
       */
      "oBrowser": {
        /**
         * Indicate if the browser incorrectly calculates width:100% inside a
         * scrolling element (IE6/7)
         *  @type boolean
         *  @default false
         */
        "bScrollOversize": false,

        /**
         * Determine if the vertical scrollbar is on the right or left of the
         * scrolling container - needed for rtl language layout, although not
         * all browsers move the scrollbar (Safari).
         *  @type boolean
         *  @default false
         */
        "bScrollbarLeft": false,

        /**
         * Flag for if `getBoundingClientRect` is fully supported or not
         *  @type boolean
         *  @default false
         */
        "bBounding": false,

        /**
         * Browser scrollbar width
         *  @type integer
         *  @default 0
         */
        "barWidth": 0
      },
      "ajax": null,

      /**
       * Array referencing the nodes which are used for the features. The
       * parameters of this object match what is allowed by sDom - i.e.
       *   <ul>
       *     <li>'l' - Length changing</li>
       *     <li>'f' - Filtering input</li>
       *     <li>'t' - The table!</li>
       *     <li>'i' - Information</li>
       *     <li>'p' - Pagination</li>
       *     <li>'r' - pRocessing</li>
       *   </ul>
       *  @type array
       *  @default []
       */
      "aanFeatures": [],

      /**
       * Store data information - see {@link DataTable.models.oRow} for detailed
       * information.
       *  @type array
       *  @default []
       */
      "aoData": [],

      /**
       * Array of indexes which are in the current display (after filtering etc)
       *  @type array
       *  @default []
       */
      "aiDisplay": [],

      /**
       * Array of indexes for display - no filtering
       *  @type array
       *  @default []
       */
      "aiDisplayMaster": [],

      /**
       * Map of row ids to data indexes
       *  @type object
       *  @default {}
       */
      "aIds": {},

      /**
       * Store information about each column that is in use
       *  @type array
       *  @default []
       */
      "aoColumns": [],

      /**
       * Store information about the table's header
       *  @type array
       *  @default []
       */
      "aoHeader": [],

      /**
       * Store information about the table's footer
       *  @type array
       *  @default []
       */
      "aoFooter": [],

      /**
       * Store the applied global search information in case we want to force a
       * research or compare the old search to a new one.
       * Note that this parameter will be set by the initialisation routine. To
       * set a default use {@link DataTable.defaults}.
       *  @namespace
       *  @extends DataTable.models.oSearch
       */
      "oPreviousSearch": {},

      /**
       * Store the applied search for each column - see
       * {@link DataTable.models.oSearch} for the format that is used for the
       * filtering information for each column.
       *  @type array
       *  @default []
       */
      "aoPreSearchCols": [],

      /**
       * Sorting that is applied to the table. Note that the inner arrays are
       * used in the following manner:
       * <ul>
       *   <li>Index 0 - column number</li>
       *   <li>Index 1 - current sorting direction</li>
       * </ul>
       * Note that this parameter will be set by the initialisation routine. To
       * set a default use {@link DataTable.defaults}.
       *  @type array
       *  @todo These inner arrays should really be objects
       */
      "aaSorting": null,

      /**
       * Sorting that is always applied to the table (i.e. prefixed in front of
       * aaSorting).
       * Note that this parameter will be set by the initialisation routine. To
       * set a default use {@link DataTable.defaults}.
       *  @type array
       *  @default []
       */
      "aaSortingFixed": [],

      /**
       * Classes to use for the striping of a table.
       * Note that this parameter will be set by the initialisation routine. To
       * set a default use {@link DataTable.defaults}.
       *  @type array
       *  @default []
       */
      "asStripeClasses": null,

      /**
       * If restoring a table - we should restore its striping classes as well
       *  @type array
       *  @default []
       */
      "asDestroyStripes": [],

      /**
       * If restoring a table - we should restore its width
       *  @type int
       *  @default 0
       */
      "sDestroyWidth": 0,

      /**
       * Callback functions array for every time a row is inserted (i.e. on a draw).
       *  @type array
       *  @default []
       */
      "aoRowCallback": [],

      /**
       * Callback functions for the header on each draw.
       *  @type array
       *  @default []
       */
      "aoHeaderCallback": [],

      /**
       * Callback function for the footer on each draw.
       *  @type array
       *  @default []
       */
      "aoFooterCallback": [],

      /**
       * Array of callback functions for draw callback functions
       *  @type array
       *  @default []
       */
      "aoDrawCallback": [],

      /**
       * Array of callback functions for row created function
       *  @type array
       *  @default []
       */
      "aoRowCreatedCallback": [],

      /**
       * Callback functions for just before the table is redrawn. A return of
       * false will be used to cancel the draw.
       *  @type array
       *  @default []
       */
      "aoPreDrawCallback": [],

      /**
       * Callback functions for when the table has been initialised.
       *  @type array
       *  @default []
       */
      "aoInitComplete": [],

      /**
       * Callbacks for modifying the settings to be stored for state saving, prior to
       * saving state.
       *  @type array
       *  @default []
       */
      "aoStateSaveParams": [],

      /**
       * Callbacks for modifying the settings that have been stored for state saving
       * prior to using the stored values to restore the state.
       *  @type array
       *  @default []
       */
      "aoStateLoadParams": [],

      /**
       * Callbacks for operating on the settings object once the saved state has been
       * loaded
       *  @type array
       *  @default []
       */
      "aoStateLoaded": [],

      /**
       * Cache the table ID for quick access
       *  @type string
       *  @default <i>Empty string</i>
       */
      "sTableId": "",

      /**
       * The TABLE node for the main table
       *  @type node
       *  @default null
       */
      "nTable": null,

      /**
       * Permanent ref to the thead element
       *  @type node
       *  @default null
       */
      "nTHead": null,

      /**
       * Permanent ref to the tfoot element - if it exists
       *  @type node
       *  @default null
       */
      "nTFoot": null,

      /**
       * Permanent ref to the tbody element
       *  @type node
       *  @default null
       */
      "nTBody": null,

      /**
       * Cache the wrapper node (contains all DataTables controlled elements)
       *  @type node
       *  @default null
       */
      "nTableWrapper": null,

      /**
       * Indicate if when using server-side processing the loading of data
       * should be deferred until the second draw.
       * Note that this parameter will be set by the initialisation routine. To
       * set a default use {@link DataTable.defaults}.
       *  @type boolean
       *  @default false
       */
      "bDeferLoading": false,

      /**
       * Indicate if all required information has been read in
       *  @type boolean
       *  @default false
       */
      "bInitialised": false,

      /**
       * Information about open rows. Each object in the array has the parameters
       * 'nTr' and 'nParent'
       *  @type array
       *  @default []
       */
      "aoOpenRows": [],

      /**
       * Dictate the positioning of DataTables' control elements - see
       * {@link DataTable.model.oInit.sDom}.
       * Note that this parameter will be set by the initialisation routine. To
       * set a default use {@link DataTable.defaults}.
       *  @type string
       *  @default null
       */
      "sDom": null,

      /**
       * Search delay (in mS)
       *  @type integer
       *  @default null
       */
      "searchDelay": null,

      /**
       * Which type of pagination should be used.
       * Note that this parameter will be set by the initialisation routine. To
       * set a default use {@link DataTable.defaults}.
       *  @type string
       *  @default two_button
       */
      "sPaginationType": "two_button",

      /**
       * The state duration (for `stateSave`) in seconds.
       * Note that this parameter will be set by the initialisation routine. To
       * set a default use {@link DataTable.defaults}.
       *  @type int
       *  @default 0
       */
      "iStateDuration": 0,

      /**
       * Array of callback functions for state saving. Each array element is an
       * object with the following parameters:
       *   <ul>
       *     <li>function:fn - function to call. Takes two parameters, oSettings
       *       and the JSON string to save that has been thus far created. Returns
       *       a JSON string to be inserted into a json object
       *       (i.e. '"param": [ 0, 1, 2]')</li>
       *     <li>string:sName - name of callback</li>
       *   </ul>
       *  @type array
       *  @default []
       */
      "aoStateSave": [],

      /**
       * Array of callback functions for state loading. Each array element is an
       * object with the following parameters:
       *   <ul>
       *     <li>function:fn - function to call. Takes two parameters, oSettings
       *       and the object stored. May return false to cancel state loading</li>
       *     <li>string:sName - name of callback</li>
       *   </ul>
       *  @type array
       *  @default []
       */
      "aoStateLoad": [],

      /**
       * State that was saved. Useful for back reference
       *  @type object
       *  @default null
       */
      "oSavedState": null,

      /**
       * State that was loaded. Useful for back reference
       *  @type object
       *  @default null
       */
      "oLoadedState": null,

      /**
       * Source url for AJAX data for the table.
       * Note that this parameter will be set by the initialisation routine. To
       * set a default use {@link DataTable.defaults}.
       *  @type string
       *  @default null
       */
      "sAjaxSource": null,

      /**
       * Property from a given object from which to read the table data from. This
       * can be an empty string (when not server-side processing), in which case
       * it is  assumed an an array is given directly.
       * Note that this parameter will be set by the initialisation routine. To
       * set a default use {@link DataTable.defaults}.
       *  @type string
       */
      "sAjaxDataProp": null,

      /**
       * Note if draw should be blocked while getting data
       *  @type boolean
       *  @default true
       */
      "bAjaxDataGet": true,

      /**
       * The last jQuery XHR object that was used for server-side data gathering.
       * This can be used for working with the XHR information in one of the
       * callbacks
       *  @type object
       *  @default null
       */
      "jqXHR": null,

      /**
       * JSON returned from the server in the last Ajax request
       *  @type object
       *  @default undefined
       */
      "json": undefined,

      /**
       * Data submitted as part of the last Ajax request
       *  @type object
       *  @default undefined
       */
      "oAjaxData": undefined,

      /**
       * Function to get the server-side data.
       * Note that this parameter will be set by the initialisation routine. To
       * set a default use {@link DataTable.defaults}.
       *  @type function
       */
      "fnServerData": null,

      /**
       * Functions which are called prior to sending an Ajax request so extra
       * parameters can easily be sent to the server
       *  @type array
       *  @default []
       */
      "aoServerParams": [],

      /**
       * Send the XHR HTTP method - GET or POST (could be PUT or DELETE if
       * required).
       * Note that this parameter will be set by the initialisation routine. To
       * set a default use {@link DataTable.defaults}.
       *  @type string
       */
      "sServerMethod": null,

      /**
       * Format numbers for display.
       * Note that this parameter will be set by the initialisation routine. To
       * set a default use {@link DataTable.defaults}.
       *  @type function
       */
      "fnFormatNumber": null,

      /**
       * List of options that can be used for the user selectable length menu.
       * Note that this parameter will be set by the initialisation routine. To
       * set a default use {@link DataTable.defaults}.
       *  @type array
       *  @default []
       */
      "aLengthMenu": null,

      /**
       * Counter for the draws that the table does. Also used as a tracker for
       * server-side processing
       *  @type int
       *  @default 0
       */
      "iDraw": 0,

      /**
       * Indicate if a redraw is being done - useful for Ajax
       *  @type boolean
       *  @default false
       */
      "bDrawing": false,

      /**
       * Draw index (iDraw) of the last error when parsing the returned data
       *  @type int
       *  @default -1
       */
      "iDrawError": -1,

      /**
       * Paging display length
       *  @type int
       *  @default 10
       */
      "_iDisplayLength": 10,

      /**
       * Paging start point - aiDisplay index
       *  @type int
       *  @default 0
       */
      "_iDisplayStart": 0,

      /**
       * Server-side processing - number of records in the result set
       * (i.e. before filtering), Use fnRecordsTotal rather than
       * this property to get the value of the number of records, regardless of
       * the server-side processing setting.
       *  @type int
       *  @default 0
       *  @private
       */
      "_iRecordsTotal": 0,

      /**
       * Server-side processing - number of records in the current display set
       * (i.e. after filtering). Use fnRecordsDisplay rather than
       * this property to get the value of the number of records, regardless of
       * the server-side processing setting.
       *  @type boolean
       *  @default 0
       *  @private
       */
      "_iRecordsDisplay": 0,

      /**
       * The classes to use for the table
       *  @type object
       *  @default {}
       */
      "oClasses": {},

      /**
       * Flag attached to the settings object so you can check in the draw
       * callback if filtering has been done in the draw. Deprecated in favour of
       * events.
       *  @type boolean
       *  @default false
       *  @deprecated
       */
      "bFiltered": false,

      /**
       * Flag attached to the settings object so you can check in the draw
       * callback if sorting has been done in the draw. Deprecated in favour of
       * events.
       *  @type boolean
       *  @default false
       *  @deprecated
       */
      "bSorted": false,

      /**
       * Indicate that if multiple rows are in the header and there is more than
       * one unique cell per column, if the top one (true) or bottom one (false)
       * should be used for sorting / title by DataTables.
       * Note that this parameter will be set by the initialisation routine. To
       * set a default use {@link DataTable.defaults}.
       *  @type boolean
       */
      "bSortCellsTop": null,

      /**
       * Initialisation object that is used for the table
       *  @type object
       *  @default null
       */
      "oInit": null,

      /**
       * Destroy callback functions - for plug-ins to attach themselves to the
       * destroy so they can clean up markup and events.
       *  @type array
       *  @default []
       */
      "aoDestroyCallback": [],

      /**
       * Get the number of records in the current record set, before filtering
       *  @type function
       */
      "fnRecordsTotal": function fnRecordsTotal() {
        return _fnDataSource(this) == 'ssp' ? this._iRecordsTotal * 1 : this.aiDisplayMaster.length;
      },

      /**
       * Get the number of records in the current record set, after filtering
       *  @type function
       */
      "fnRecordsDisplay": function fnRecordsDisplay() {
        return _fnDataSource(this) == 'ssp' ? this._iRecordsDisplay * 1 : this.aiDisplay.length;
      },

      /**
       * Get the display end point - aiDisplay index
       *  @type function
       */
      "fnDisplayEnd": function fnDisplayEnd() {
        var len = this._iDisplayLength,
            start = this._iDisplayStart,
            calc = start + len,
            records = this.aiDisplay.length,
            features = this.oFeatures,
            paginate = features.bPaginate;

        if (features.bServerSide) {
          return paginate === false || len === -1 ? start + records : Math.min(start + len, this._iRecordsDisplay);
        } else {
          return !paginate || calc > records || len === -1 ? records : calc;
        }
      },

      /**
       * The DataTables object for this table
       *  @type object
       *  @default null
       */
      "oInstance": null,

      /**
       * Unique identifier for each instance of the DataTables object. If there
       * is an ID on the table node, then it takes that value, otherwise an
       * incrementing internal counter is used.
       *  @type string
       *  @default null
       */
      "sInstance": null,

      /**
       * tabindex attribute value that is added to DataTables control elements, allowing
       * keyboard navigation of the table and its controls.
       */
      "iTabIndex": 0,

      /**
       * DIV container for the footer scrolling table if scrolling
       */
      "nScrollHead": null,

      /**
       * DIV container for the footer scrolling table if scrolling
       */
      "nScrollFoot": null,

      /**
       * Last applied sort
       *  @type array
       *  @default []
       */
      "aLastSort": [],

      /**
       * Stored plug-in instances
       *  @type object
       *  @default {}
       */
      "oPlugins": {},

      /**
       * Function used to get a row's id from the row's data
       *  @type function
       *  @default null
       */
      "rowIdFn": null,

      /**
       * Data location where to store a row's id
       *  @type string
       *  @default null
       */
      "rowId": null
    };
    /**
     * Extension object for DataTables that is used to provide all extension
     * options.
     *
     * Note that the `DataTable.ext` object is available through
     * `jQuery.fn.dataTable.ext` where it may be accessed and manipulated. It is
     * also aliased to `jQuery.fn.dataTableExt` for historic reasons.
     *  @namespace
     *  @extends DataTable.models.ext
     */

    /**
     * DataTables extensions
     * 
     * This namespace acts as a collection area for plug-ins that can be used to
     * extend DataTables capabilities. Indeed many of the build in methods
     * use this method to provide their own capabilities (sorting methods for
     * example).
     *
     * Note that this namespace is aliased to `jQuery.fn.dataTableExt` for legacy
     * reasons
     *
     *  @namespace
     */

    DataTable.ext = _ext = {
      /**
       * Buttons. For use with the Buttons extension for DataTables. This is
       * defined here so other extensions can define buttons regardless of load
       * order. It is _not_ used by DataTables core.
       *
       *  @type object
       *  @default {}
       */
      buttons: {},

      /**
       * Element class names
       *
       *  @type object
       *  @default {}
       */
      classes: {},

      /**
       * DataTables build type (expanded by the download builder)
       *
       *  @type string
       */
      build: "bs4/dt-1.10.18/r-2.2.2",

      /**
       * Error reporting.
       * 
       * How should DataTables report an error. Can take the value 'alert',
       * 'throw', 'none' or a function.
       *
       *  @type string|function
       *  @default alert
       */
      errMode: "alert",

      /**
       * Feature plug-ins.
       * 
       * This is an array of objects which describe the feature plug-ins that are
       * available to DataTables. These feature plug-ins are then available for
       * use through the `dom` initialisation option.
       * 
       * Each feature plug-in is described by an object which must have the
       * following properties:
       * 
       * * `fnInit` - function that is used to initialise the plug-in,
       * * `cFeature` - a character so the feature can be enabled by the `dom`
       *   instillation option. This is case sensitive.
       *
       * The `fnInit` function has the following input parameters:
       *
       * 1. `{object}` DataTables settings object: see
       *    {@link DataTable.models.oSettings}
       *
       * And the following return is expected:
       * 
       * * {node|null} The element which contains your feature. Note that the
       *   return may also be void if your plug-in does not require to inject any
       *   DOM elements into DataTables control (`dom`) - for example this might
       *   be useful when developing a plug-in which allows table control via
       *   keyboard entry
       *
       *  @type array
       *
       *  @example
       *    $.fn.dataTable.ext.features.push( {
       *      "fnInit": function( oSettings ) {
       *        return new TableTools( { "oDTSettings": oSettings } );
       *      },
       *      "cFeature": "T"
       *    } );
       */
      feature: [],

      /**
       * Row searching.
       * 
       * This method of searching is complimentary to the default type based
       * searching, and a lot more comprehensive as it allows you complete control
       * over the searching logic. Each element in this array is a function
       * (parameters described below) that is called for every row in the table,
       * and your logic decides if it should be included in the searching data set
       * or not.
       *
       * Searching functions have the following input parameters:
       *
       * 1. `{object}` DataTables settings object: see
       *    {@link DataTable.models.oSettings}
       * 2. `{array|object}` Data for the row to be processed (same as the
       *    original format that was passed in as the data source, or an array
       *    from a DOM data source
       * 3. `{int}` Row index ({@link DataTable.models.oSettings.aoData}), which
       *    can be useful to retrieve the `TR` element if you need DOM interaction.
       *
       * And the following return is expected:
       *
       * * {boolean} Include the row in the searched result set (true) or not
       *   (false)
       *
       * Note that as with the main search ability in DataTables, technically this
       * is "filtering", since it is subtractive. However, for consistency in
       * naming we call it searching here.
       *
       *  @type array
       *  @default []
       *
       *  @example
       *    // The following example shows custom search being applied to the
       *    // fourth column (i.e. the data[3] index) based on two input values
       *    // from the end-user, matching the data in a certain range.
       *    $.fn.dataTable.ext.search.push(
       *      function( settings, data, dataIndex ) {
       *        var min = document.getElementById('min').value * 1;
       *        var max = document.getElementById('max').value * 1;
       *        var version = data[3] == "-" ? 0 : data[3]*1;
       *
       *        if ( min == "" && max == "" ) {
       *          return true;
       *        }
       *        else if ( min == "" && version < max ) {
       *          return true;
       *        }
       *        else if ( min < version && "" == max ) {
       *          return true;
       *        }
       *        else if ( min < version && version < max ) {
       *          return true;
       *        }
       *        return false;
       *      }
       *    );
       */
      search: [],

      /**
       * Selector extensions
       *
       * The `selector` option can be used to extend the options available for the
       * selector modifier options (`selector-modifier` object data type) that
       * each of the three built in selector types offer (row, column and cell +
       * their plural counterparts). For example the Select extension uses this
       * mechanism to provide an option to select only rows, columns and cells
       * that have been marked as selected by the end user (`{selected: true}`),
       * which can be used in conjunction with the existing built in selector
       * options.
       *
       * Each property is an array to which functions can be pushed. The functions
       * take three attributes:
       *
       * * Settings object for the host table
       * * Options object (`selector-modifier` object type)
       * * Array of selected item indexes
       *
       * The return is an array of the resulting item indexes after the custom
       * selector has been applied.
       *
       *  @type object
       */
      selector: {
        cell: [],
        column: [],
        row: []
      },

      /**
       * Internal functions, exposed for used in plug-ins.
       * 
       * Please note that you should not need to use the internal methods for
       * anything other than a plug-in (and even then, try to avoid if possible).
       * The internal function may change between releases.
       *
       *  @type object
       *  @default {}
       */
      internal: {},

      /**
       * Legacy configuration options. Enable and disable legacy options that
       * are available in DataTables.
       *
       *  @type object
       */
      legacy: {
        /**
         * Enable / disable DataTables 1.9 compatible server-side processing
         * requests
         *
         *  @type boolean
         *  @default null
         */
        ajax: null
      },

      /**
       * Pagination plug-in methods.
       * 
       * Each entry in this object is a function and defines which buttons should
       * be shown by the pagination rendering method that is used for the table:
       * {@link DataTable.ext.renderer.pageButton}. The renderer addresses how the
       * buttons are displayed in the document, while the functions here tell it
       * what buttons to display. This is done by returning an array of button
       * descriptions (what each button will do).
       *
       * Pagination types (the four built in options and any additional plug-in
       * options defined here) can be used through the `paginationType`
       * initialisation parameter.
       *
       * The functions defined take two parameters:
       *
       * 1. `{int} page` The current page index
       * 2. `{int} pages` The number of pages in the table
       *
       * Each function is expected to return an array where each element of the
       * array can be one of:
       *
       * * `first` - Jump to first page when activated
       * * `last` - Jump to last page when activated
       * * `previous` - Show previous page when activated
       * * `next` - Show next page when activated
       * * `{int}` - Show page of the index given
       * * `{array}` - A nested array containing the above elements to add a
       *   containing 'DIV' element (might be useful for styling).
       *
       * Note that DataTables v1.9- used this object slightly differently whereby
       * an object with two functions would be defined for each plug-in. That
       * ability is still supported by DataTables 1.10+ to provide backwards
       * compatibility, but this option of use is now decremented and no longer
       * documented in DataTables 1.10+.
       *
       *  @type object
       *  @default {}
       *
       *  @example
       *    // Show previous, next and current page buttons only
       *    $.fn.dataTableExt.oPagination.current = function ( page, pages ) {
       *      return [ 'previous', page, 'next' ];
       *    };
       */
      pager: {},
      renderer: {
        pageButton: {},
        header: {}
      },

      /**
       * Ordering plug-ins - custom data source
       * 
       * The extension options for ordering of data available here is complimentary
       * to the default type based ordering that DataTables typically uses. It
       * allows much greater control over the the data that is being used to
       * order a column, but is necessarily therefore more complex.
       * 
       * This type of ordering is useful if you want to do ordering based on data
       * live from the DOM (for example the contents of an 'input' element) rather
       * than just the static string that DataTables knows of.
       * 
       * The way these plug-ins work is that you create an array of the values you
       * wish to be ordering for the column in question and then return that
       * array. The data in the array much be in the index order of the rows in
       * the table (not the currently ordering order!). Which order data gathering
       * function is run here depends on the `dt-init columns.orderDataType`
       * parameter that is used for the column (if any).
       *
       * The functions defined take two parameters:
       *
       * 1. `{object}` DataTables settings object: see
       *    {@link DataTable.models.oSettings}
       * 2. `{int}` Target column index
       *
       * Each function is expected to return an array:
       *
       * * `{array}` Data for the column to be ordering upon
       *
       *  @type array
       *
       *  @example
       *    // Ordering using `input` node values
       *    $.fn.dataTable.ext.order['dom-text'] = function  ( settings, col )
       *    {
       *      return this.api().column( col, {order:'index'} ).nodes().map( function ( td, i ) {
       *        return $('input', td).val();
       *      } );
       *    }
       */
      order: {},

      /**
       * Type based plug-ins.
       *
       * Each column in DataTables has a type assigned to it, either by automatic
       * detection or by direct assignment using the `type` option for the column.
       * The type of a column will effect how it is ordering and search (plug-ins
       * can also make use of the column type if required).
       *
       * @namespace
       */
      type: {
        /**
         * Type detection functions.
         *
         * The functions defined in this object are used to automatically detect
         * a column's type, making initialisation of DataTables super easy, even
         * when complex data is in the table.
         *
         * The functions defined take two parameters:
         *
            *  1. `{*}` Data from the column cell to be analysed
            *  2. `{settings}` DataTables settings object. This can be used to
            *     perform context specific type detection - for example detection
            *     based on language settings such as using a comma for a decimal
            *     place. Generally speaking the options from the settings will not
            *     be required
         *
         * Each function is expected to return:
         *
         * * `{string|null}` Data type detected, or null if unknown (and thus
         *   pass it on to the other type detection functions.
         *
         *  @type array
         *
         *  @example
         *    // Currency type detection plug-in:
         *    $.fn.dataTable.ext.type.detect.push(
         *      function ( data, settings ) {
         *        // Check the numeric part
         *        if ( ! data.substring(1).match(/[0-9]/) ) {
         *          return null;
         *        }
         *
         *        // Check prefixed by currency
         *        if ( data.charAt(0) == '$' || data.charAt(0) == '&pound;' ) {
         *          return 'currency';
         *        }
         *        return null;
         *      }
         *    );
         */
        detect: [],

        /**
         * Type based search formatting.
         *
         * The type based searching functions can be used to pre-format the
         * data to be search on. For example, it can be used to strip HTML
         * tags or to de-format telephone numbers for numeric only searching.
         *
         * Note that is a search is not defined for a column of a given type,
         * no search formatting will be performed.
         * 
         * Pre-processing of searching data plug-ins - When you assign the sType
         * for a column (or have it automatically detected for you by DataTables
         * or a type detection plug-in), you will typically be using this for
         * custom sorting, but it can also be used to provide custom searching
         * by allowing you to pre-processing the data and returning the data in
         * the format that should be searched upon. This is done by adding
         * functions this object with a parameter name which matches the sType
         * for that target column. This is the corollary of <i>afnSortData</i>
         * for searching data.
         *
         * The functions defined take a single parameter:
         *
            *  1. `{*}` Data from the column cell to be prepared for searching
         *
         * Each function is expected to return:
         *
         * * `{string|null}` Formatted string that will be used for the searching.
         *
         *  @type object
         *  @default {}
         *
         *  @example
         *    $.fn.dataTable.ext.type.search['title-numeric'] = function ( d ) {
         *      return d.replace(/\n/g," ").replace( /<.*?>/g, "" );
         *    }
         */
        search: {},

        /**
         * Type based ordering.
         *
         * The column type tells DataTables what ordering to apply to the table
         * when a column is sorted upon. The order for each type that is defined,
         * is defined by the functions available in this object.
         *
         * Each ordering option can be described by three properties added to
         * this object:
         *
         * * `{type}-pre` - Pre-formatting function
         * * `{type}-asc` - Ascending order function
         * * `{type}-desc` - Descending order function
         *
         * All three can be used together, only `{type}-pre` or only
         * `{type}-asc` and `{type}-desc` together. It is generally recommended
         * that only `{type}-pre` is used, as this provides the optimal
         * implementation in terms of speed, although the others are provided
         * for compatibility with existing Javascript sort functions.
         *
         * `{type}-pre`: Functions defined take a single parameter:
         *
            *  1. `{*}` Data from the column cell to be prepared for ordering
         *
         * And return:
         *
         * * `{*}` Data to be sorted upon
         *
         * `{type}-asc` and `{type}-desc`: Functions are typical Javascript sort
         * functions, taking two parameters:
         *
            *  1. `{*}` Data to compare to the second parameter
            *  2. `{*}` Data to compare to the first parameter
         *
         * And returning:
         *
         * * `{*}` Ordering match: <0 if first parameter should be sorted lower
         *   than the second parameter, ===0 if the two parameters are equal and
         *   >0 if the first parameter should be sorted height than the second
         *   parameter.
         * 
         *  @type object
         *  @default {}
         *
         *  @example
         *    // Numeric ordering of formatted numbers with a pre-formatter
         *    $.extend( $.fn.dataTable.ext.type.order, {
         *      "string-pre": function(x) {
         *        a = (a === "-" || a === "") ? 0 : a.replace( /[^\d\-\.]/g, "" );
         *        return parseFloat( a );
         *      }
         *    } );
         *
         *  @example
         *    // Case-sensitive string ordering, with no pre-formatting method
         *    $.extend( $.fn.dataTable.ext.order, {
         *      "string-case-asc": function(x,y) {
         *        return ((x < y) ? -1 : ((x > y) ? 1 : 0));
         *      },
         *      "string-case-desc": function(x,y) {
         *        return ((x < y) ? 1 : ((x > y) ? -1 : 0));
         *      }
         *    } );
         */
        order: {}
      },

      /**
       * Unique DataTables instance counter
       *
       * @type int
       * @private
       */
      _unique: 0,
      //
      // Depreciated
      // The following properties are retained for backwards compatiblity only.
      // The should not be used in new projects and will be removed in a future
      // version
      //

      /**
       * Version check function.
       *  @type function
       *  @depreciated Since 1.10
       */
      fnVersionCheck: DataTable.fnVersionCheck,

      /**
       * Index for what 'this' index API functions should use
       *  @type int
       *  @deprecated Since v1.10
       */
      iApiIndex: 0,

      /**
       * jQuery UI class container
       *  @type object
       *  @deprecated Since v1.10
       */
      oJUIClasses: {},

      /**
       * Software version
       *  @type string
       *  @deprecated Since v1.10
       */
      sVersion: DataTable.version
    }; //
    // Backwards compatibility. Alias to pre 1.10 Hungarian notation counter parts
    //

    $$$1.extend(_ext, {
      afnFiltering: _ext.search,
      aTypes: _ext.type.detect,
      ofnSearch: _ext.type.search,
      oSort: _ext.type.order,
      afnSortData: _ext.order,
      aoFeatures: _ext.feature,
      oApi: _ext.internal,
      oStdClasses: _ext.classes,
      oPagination: _ext.pager
    });
    $$$1.extend(DataTable.ext.classes, {
      "sTable": "dataTable",
      "sNoFooter": "no-footer",

      /* Paging buttons */
      "sPageButton": "paginate_button",
      "sPageButtonActive": "current",
      "sPageButtonDisabled": "disabled",

      /* Striping classes */
      "sStripeOdd": "odd",
      "sStripeEven": "even",

      /* Empty row */
      "sRowEmpty": "dataTables_empty",

      /* Features */
      "sWrapper": "dataTables_wrapper",
      "sFilter": "dataTables_filter",
      "sInfo": "dataTables_info",
      "sPaging": "dataTables_paginate paging_",

      /* Note that the type is postfixed */
      "sLength": "dataTables_length",
      "sProcessing": "dataTables_processing",

      /* Sorting */
      "sSortAsc": "sorting_asc",
      "sSortDesc": "sorting_desc",
      "sSortable": "sorting",

      /* Sortable in both directions */
      "sSortableAsc": "sorting_asc_disabled",
      "sSortableDesc": "sorting_desc_disabled",
      "sSortableNone": "sorting_disabled",
      "sSortColumn": "sorting_",

      /* Note that an int is postfixed for the sorting order */

      /* Filtering */
      "sFilterInput": "",

      /* Page length */
      "sLengthSelect": "",

      /* Scrolling */
      "sScrollWrapper": "dataTables_scroll",
      "sScrollHead": "dataTables_scrollHead",
      "sScrollHeadInner": "dataTables_scrollHeadInner",
      "sScrollBody": "dataTables_scrollBody",
      "sScrollFoot": "dataTables_scrollFoot",
      "sScrollFootInner": "dataTables_scrollFootInner",

      /* Misc */
      "sHeaderTH": "",
      "sFooterTH": "",
      // Deprecated
      "sSortJUIAsc": "",
      "sSortJUIDesc": "",
      "sSortJUI": "",
      "sSortJUIAscAllowed": "",
      "sSortJUIDescAllowed": "",
      "sSortJUIWrapper": "",
      "sSortIcon": "",
      "sJUIHeader": "",
      "sJUIFooter": ""
    });
    var extPagination = DataTable.ext.pager;

    function _numbers(page, pages) {
      var numbers = [],
          buttons = extPagination.numbers_length,
          half = Math.floor(buttons / 2);

      if (pages <= buttons) {
        numbers = _range(0, pages);
      } else if (page <= half) {
        numbers = _range(0, buttons - 2);
        numbers.push('ellipsis');
        numbers.push(pages - 1);
      } else if (page >= pages - 1 - half) {
        numbers = _range(pages - (buttons - 2), pages);
        numbers.splice(0, 0, 'ellipsis'); // no unshift in ie6

        numbers.splice(0, 0, 0);
      } else {
        numbers = _range(page - half + 2, page + half - 1);
        numbers.push('ellipsis');
        numbers.push(pages - 1);
        numbers.splice(0, 0, 'ellipsis');
        numbers.splice(0, 0, 0);
      }

      numbers.DT_el = 'span';
      return numbers;
    }

    $$$1.extend(extPagination, {
      simple: function simple(page, pages) {
        return ['previous', 'next'];
      },
      full: function full(page, pages) {
        return ['first', 'previous', 'next', 'last'];
      },
      numbers: function numbers(page, pages) {
        return [_numbers(page, pages)];
      },
      simple_numbers: function simple_numbers(page, pages) {
        return ['previous', _numbers(page, pages), 'next'];
      },
      full_numbers: function full_numbers(page, pages) {
        return ['first', 'previous', _numbers(page, pages), 'next', 'last'];
      },
      first_last_numbers: function first_last_numbers(page, pages) {
        return ['first', _numbers(page, pages), 'last'];
      },
      // For testing and plug-ins to use
      _numbers: _numbers,
      // Number of number buttons (including ellipsis) to show. _Must be odd!_
      numbers_length: 7
    });
    $$$1.extend(true, DataTable.ext.renderer, {
      pageButton: {
        _: function _(settings, host, idx, buttons, page, pages) {
          var classes = settings.oClasses;
          var lang = settings.oLanguage.oPaginate;
          var aria = settings.oLanguage.oAria.paginate || {};
          var btnDisplay,
              btnClass,
              counter = 0;

          var attach = function attach(container, buttons) {
            var i, ien, node, button;

            var clickHandler = function clickHandler(e) {
              _fnPageChange(settings, e.data.action, true);
            };

            for (i = 0, ien = buttons.length; i < ien; i++) {
              button = buttons[i];

              if ($$$1.isArray(button)) {
                var inner = $$$1('<' + (button.DT_el || 'div') + '/>').appendTo(container);
                attach(inner, button);
              } else {
                btnDisplay = null;
                btnClass = '';

                switch (button) {
                  case 'ellipsis':
                    container.append('<span class="ellipsis">&#x2026;</span>');
                    break;

                  case 'first':
                    btnDisplay = lang.sFirst;
                    btnClass = button + (page > 0 ? '' : ' ' + classes.sPageButtonDisabled);
                    break;

                  case 'previous':
                    btnDisplay = lang.sPrevious;
                    btnClass = button + (page > 0 ? '' : ' ' + classes.sPageButtonDisabled);
                    break;

                  case 'next':
                    btnDisplay = lang.sNext;
                    btnClass = button + (page < pages - 1 ? '' : ' ' + classes.sPageButtonDisabled);
                    break;

                  case 'last':
                    btnDisplay = lang.sLast;
                    btnClass = button + (page < pages - 1 ? '' : ' ' + classes.sPageButtonDisabled);
                    break;

                  default:
                    btnDisplay = button + 1;
                    btnClass = page === button ? classes.sPageButtonActive : '';
                    break;
                }

                if (btnDisplay !== null) {
                  node = $$$1('<a>', {
                    'class': classes.sPageButton + ' ' + btnClass,
                    'aria-controls': settings.sTableId,
                    'aria-label': aria[button],
                    'data-dt-idx': counter,
                    'tabindex': settings.iTabIndex,
                    'id': idx === 0 && typeof button === 'string' ? settings.sTableId + '_' + button : null
                  }).html(btnDisplay).appendTo(container);

                  _fnBindAction(node, {
                    action: button
                  }, clickHandler);

                  counter++;
                }
              }
            }
          }; // IE9 throws an 'unknown error' if document.activeElement is used
          // inside an iframe or frame. Try / catch the error. Not good for
          // accessibility, but neither are frames.


          var activeEl;

          try {
            // Because this approach is destroying and recreating the paging
            // elements, focus is lost on the select button which is bad for
            // accessibility. So we want to restore focus once the draw has
            // completed
            activeEl = $$$1(host).find(document.activeElement).data('dt-idx');
          } catch (e) {}

          attach($$$1(host).empty(), buttons);

          if (activeEl !== undefined) {
            $$$1(host).find('[data-dt-idx=' + activeEl + ']').focus();
          }
        }
      }
    }); // Built in type detection. See model.ext.aTypes for information about
    // what is required from this methods.

    $$$1.extend(DataTable.ext.type.detect, [// Plain numbers - first since V8 detects some plain numbers as dates
    // e.g. Date.parse('55') (but not all, e.g. Date.parse('22')...).
    function (d, settings) {
      var decimal = settings.oLanguage.sDecimal;
      return _isNumber(d, decimal) ? 'num' + decimal : null;
    }, // Dates (only those recognised by the browser's Date.parse)
    function (d, settings) {
      // V8 tries _very_ hard to make a string passed into `Date.parse()`
      // valid, so we need to use a regex to restrict date formats. Use a
      // plug-in for anything other than ISO8601 style strings
      if (d && !(d instanceof Date) && !_re_date.test(d)) {
        return null;
      }

      var parsed = Date.parse(d);
      return parsed !== null && !isNaN(parsed) || _empty(d) ? 'date' : null;
    }, // Formatted numbers
    function (d, settings) {
      var decimal = settings.oLanguage.sDecimal;
      return _isNumber(d, decimal, true) ? 'num-fmt' + decimal : null;
    }, // HTML numeric
    function (d, settings) {
      var decimal = settings.oLanguage.sDecimal;
      return _htmlNumeric(d, decimal) ? 'html-num' + decimal : null;
    }, // HTML numeric, formatted
    function (d, settings) {
      var decimal = settings.oLanguage.sDecimal;
      return _htmlNumeric(d, decimal, true) ? 'html-num-fmt' + decimal : null;
    }, // HTML (this is strict checking - there must be html)
    function (d, settings) {
      return _empty(d) || typeof d === 'string' && d.indexOf('<') !== -1 ? 'html' : null;
    }]); // Filter formatting functions. See model.ext.ofnSearch for information about
    // what is required from these methods.
    // 
    // Note that additional search methods are added for the html numbers and
    // html formatted numbers by `_addNumericSort()` when we know what the decimal
    // place is

    $$$1.extend(DataTable.ext.type.search, {
      html: function html(data) {
        return _empty(data) ? data : typeof data === 'string' ? data.replace(_re_new_lines, " ").replace(_re_html, "") : '';
      },
      string: function string(data) {
        return _empty(data) ? data : typeof data === 'string' ? data.replace(_re_new_lines, " ") : data;
      }
    });

    var __numericReplace = function __numericReplace(d, decimalPlace, re1, re2) {
      if (d !== 0 && (!d || d === '-')) {
        return -Infinity;
      } // If a decimal place other than `.` is used, it needs to be given to the
      // function so we can detect it and replace with a `.` which is the only
      // decimal place Javascript recognises - it is not locale aware.


      if (decimalPlace) {
        d = _numToDecimal(d, decimalPlace);
      }

      if (d.replace) {
        if (re1) {
          d = d.replace(re1, '');
        }

        if (re2) {
          d = d.replace(re2, '');
        }
      }

      return d * 1;
    }; // Add the numeric 'deformatting' functions for sorting and search. This is done
    // in a function to provide an easy ability for the language options to add
    // additional methods if a non-period decimal place is used.


    function _addNumericSort(decimalPlace) {
      $$$1.each({
        // Plain numbers
        "num": function num(d) {
          return __numericReplace(d, decimalPlace);
        },
        // Formatted numbers
        "num-fmt": function numFmt(d) {
          return __numericReplace(d, decimalPlace, _re_formatted_numeric);
        },
        // HTML numeric
        "html-num": function htmlNum(d) {
          return __numericReplace(d, decimalPlace, _re_html);
        },
        // HTML numeric, formatted
        "html-num-fmt": function htmlNumFmt(d) {
          return __numericReplace(d, decimalPlace, _re_html, _re_formatted_numeric);
        }
      }, function (key, fn) {
        // Add the ordering method
        _ext.type.order[key + decimalPlace + '-pre'] = fn; // For HTML types add a search formatter that will strip the HTML

        if (key.match(/^html\-/)) {
          _ext.type.search[key + decimalPlace] = _ext.type.search.html;
        }
      });
    } // Default sort methods


    $$$1.extend(_ext.type.order, {
      // Dates
      "date-pre": function datePre(d) {
        var ts = Date.parse(d);
        return isNaN(ts) ? -Infinity : ts;
      },
      // html
      "html-pre": function htmlPre(a) {
        return _empty(a) ? '' : a.replace ? a.replace(/<.*?>/g, "").toLowerCase() : a + '';
      },
      // string
      "string-pre": function stringPre(a) {
        // This is a little complex, but faster than always calling toString,
        // http://jsperf.com/tostring-v-check
        return _empty(a) ? '' : typeof a === 'string' ? a.toLowerCase() : !a.toString ? '' : a.toString();
      },
      // string-asc and -desc are retained only for compatibility with the old
      // sort methods
      "string-asc": function stringAsc(x, y) {
        return x < y ? -1 : x > y ? 1 : 0;
      },
      "string-desc": function stringDesc(x, y) {
        return x < y ? 1 : x > y ? -1 : 0;
      }
    }); // Numeric sorting types - order doesn't matter here

    _addNumericSort('');

    $$$1.extend(true, DataTable.ext.renderer, {
      header: {
        _: function _(settings, cell, column, classes) {
          // No additional mark-up required
          // Attach a sort listener to update on sort - note that using the
          // `DT` namespace will allow the event to be removed automatically
          // on destroy, while the `dt` namespaced event is the one we are
          // listening for
          $$$1(settings.nTable).on('order.dt.DT', function (e, ctx, sorting, columns) {
            if (settings !== ctx) {
              // need to check this this is the host
              return; // table, not a nested one
            }

            var colIdx = column.idx;
            cell.removeClass(column.sSortingClass + ' ' + classes.sSortAsc + ' ' + classes.sSortDesc).addClass(columns[colIdx] == 'asc' ? classes.sSortAsc : columns[colIdx] == 'desc' ? classes.sSortDesc : column.sSortingClass);
          });
        },
        jqueryui: function jqueryui(settings, cell, column, classes) {
          $$$1('<div/>').addClass(classes.sSortJUIWrapper).append(cell.contents()).append($$$1('<span/>').addClass(classes.sSortIcon + ' ' + column.sSortingClassJUI)).appendTo(cell); // Attach a sort listener to update on sort

          $$$1(settings.nTable).on('order.dt.DT', function (e, ctx, sorting, columns) {
            if (settings !== ctx) {
              return;
            }

            var colIdx = column.idx;
            cell.removeClass(classes.sSortAsc + " " + classes.sSortDesc).addClass(columns[colIdx] == 'asc' ? classes.sSortAsc : columns[colIdx] == 'desc' ? classes.sSortDesc : column.sSortingClass);
            cell.find('span.' + classes.sSortIcon).removeClass(classes.sSortJUIAsc + " " + classes.sSortJUIDesc + " " + classes.sSortJUI + " " + classes.sSortJUIAscAllowed + " " + classes.sSortJUIDescAllowed).addClass(columns[colIdx] == 'asc' ? classes.sSortJUIAsc : columns[colIdx] == 'desc' ? classes.sSortJUIDesc : column.sSortingClassJUI);
          });
        }
      }
    });
    /*
     * Public helper functions. These aren't used internally by DataTables, or
     * called by any of the options passed into DataTables, but they can be used
     * externally by developers working with DataTables. They are helper functions
     * to make working with DataTables a little bit easier.
     */

    var __htmlEscapeEntities = function __htmlEscapeEntities(d) {
      return typeof d === 'string' ? d.replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;') : d;
    };
    /**
     * Helpers for `columns.render`.
     *
     * The options defined here can be used with the `columns.render` initialisation
     * option to provide a display renderer. The following functions are defined:
     *
     * * `number` - Will format numeric data (defined by `columns.data`) for
     *   display, retaining the original unformatted data for sorting and filtering.
     *   It takes 5 parameters:
     *   * `string` - Thousands grouping separator
     *   * `string` - Decimal point indicator
     *   * `integer` - Number of decimal points to show
     *   * `string` (optional) - Prefix.
     *   * `string` (optional) - Postfix (/suffix).
     * * `text` - Escape HTML to help prevent XSS attacks. It has no optional
     *   parameters.
     *
     * @example
     *   // Column definition using the number renderer
     *   {
     *     data: "salary",
     *     render: $.fn.dataTable.render.number( '\'', '.', 0, '$' )
     *   }
     *
     * @namespace
     */


    DataTable.render = {
      number: function number(thousands, decimal, precision, prefix, postfix) {
        return {
          display: function display(d) {
            if (typeof d !== 'number' && typeof d !== 'string') {
              return d;
            }

            var negative = d < 0 ? '-' : '';
            var flo = parseFloat(d); // If NaN then there isn't much formatting that we can do - just
            // return immediately, escaping any HTML (this was supposed to
            // be a number after all)

            if (isNaN(flo)) {
              return __htmlEscapeEntities(d);
            }

            flo = flo.toFixed(precision);
            d = Math.abs(flo);
            var intPart = parseInt(d, 10);
            var floatPart = precision ? decimal + (d - intPart).toFixed(precision).substring(2) : '';
            return negative + (prefix || '') + intPart.toString().replace(/\B(?=(\d{3})+(?!\d))/g, thousands) + floatPart + (postfix || '');
          }
        };
      },
      text: function text() {
        return {
          display: __htmlEscapeEntities
        };
      }
    };
    /*
     * This is really a good bit rubbish this method of exposing the internal methods
     * publicly... - To be fixed in 2.0 using methods on the prototype
     */

    /**
     * Create a wrapper function for exporting an internal functions to an external API.
     *  @param {string} fn API function name
     *  @returns {function} wrapped function
     *  @memberof DataTable#internal
     */

    function _fnExternApiFunc(fn) {
      return function () {
        var args = [_fnSettingsFromNode(this[DataTable.ext.iApiIndex])].concat(Array.prototype.slice.call(arguments));
        return DataTable.ext.internal[fn].apply(this, args);
      };
    }
    /**
     * Reference to internal functions for use by plug-in developers. Note that
     * these methods are references to internal functions and are considered to be
     * private. If you use these methods, be aware that they are liable to change
     * between versions.
     *  @namespace
     */


    $$$1.extend(DataTable.ext.internal, {
      _fnExternApiFunc: _fnExternApiFunc,
      _fnBuildAjax: _fnBuildAjax,
      _fnAjaxUpdate: _fnAjaxUpdate,
      _fnAjaxParameters: _fnAjaxParameters,
      _fnAjaxUpdateDraw: _fnAjaxUpdateDraw,
      _fnAjaxDataSrc: _fnAjaxDataSrc,
      _fnAddColumn: _fnAddColumn,
      _fnColumnOptions: _fnColumnOptions,
      _fnAdjustColumnSizing: _fnAdjustColumnSizing,
      _fnVisibleToColumnIndex: _fnVisibleToColumnIndex,
      _fnColumnIndexToVisible: _fnColumnIndexToVisible,
      _fnVisbleColumns: _fnVisbleColumns,
      _fnGetColumns: _fnGetColumns,
      _fnColumnTypes: _fnColumnTypes,
      _fnApplyColumnDefs: _fnApplyColumnDefs,
      _fnHungarianMap: _fnHungarianMap,
      _fnCamelToHungarian: _fnCamelToHungarian,
      _fnLanguageCompat: _fnLanguageCompat,
      _fnBrowserDetect: _fnBrowserDetect,
      _fnAddData: _fnAddData,
      _fnAddTr: _fnAddTr,
      _fnNodeToDataIndex: _fnNodeToDataIndex,
      _fnNodeToColumnIndex: _fnNodeToColumnIndex,
      _fnGetCellData: _fnGetCellData,
      _fnSetCellData: _fnSetCellData,
      _fnSplitObjNotation: _fnSplitObjNotation,
      _fnGetObjectDataFn: _fnGetObjectDataFn,
      _fnSetObjectDataFn: _fnSetObjectDataFn,
      _fnGetDataMaster: _fnGetDataMaster,
      _fnClearTable: _fnClearTable,
      _fnDeleteIndex: _fnDeleteIndex,
      _fnInvalidate: _fnInvalidate,
      _fnGetRowElements: _fnGetRowElements,
      _fnCreateTr: _fnCreateTr,
      _fnBuildHead: _fnBuildHead,
      _fnDrawHead: _fnDrawHead,
      _fnDraw: _fnDraw,
      _fnReDraw: _fnReDraw,
      _fnAddOptionsHtml: _fnAddOptionsHtml,
      _fnDetectHeader: _fnDetectHeader,
      _fnGetUniqueThs: _fnGetUniqueThs,
      _fnFeatureHtmlFilter: _fnFeatureHtmlFilter,
      _fnFilterComplete: _fnFilterComplete,
      _fnFilterCustom: _fnFilterCustom,
      _fnFilterColumn: _fnFilterColumn,
      _fnFilter: _fnFilter,
      _fnFilterCreateSearch: _fnFilterCreateSearch,
      _fnEscapeRegex: _fnEscapeRegex,
      _fnFilterData: _fnFilterData,
      _fnFeatureHtmlInfo: _fnFeatureHtmlInfo,
      _fnUpdateInfo: _fnUpdateInfo,
      _fnInfoMacros: _fnInfoMacros,
      _fnInitialise: _fnInitialise,
      _fnInitComplete: _fnInitComplete,
      _fnLengthChange: _fnLengthChange,
      _fnFeatureHtmlLength: _fnFeatureHtmlLength,
      _fnFeatureHtmlPaginate: _fnFeatureHtmlPaginate,
      _fnPageChange: _fnPageChange,
      _fnFeatureHtmlProcessing: _fnFeatureHtmlProcessing,
      _fnProcessingDisplay: _fnProcessingDisplay,
      _fnFeatureHtmlTable: _fnFeatureHtmlTable,
      _fnScrollDraw: _fnScrollDraw,
      _fnApplyToChildren: _fnApplyToChildren,
      _fnCalculateColumnWidths: _fnCalculateColumnWidths,
      _fnThrottle: _fnThrottle,
      _fnConvertToWidth: _fnConvertToWidth,
      _fnGetWidestNode: _fnGetWidestNode,
      _fnGetMaxLenString: _fnGetMaxLenString,
      _fnStringToCss: _fnStringToCss,
      _fnSortFlatten: _fnSortFlatten,
      _fnSort: _fnSort,
      _fnSortAria: _fnSortAria,
      _fnSortListener: _fnSortListener,
      _fnSortAttachListener: _fnSortAttachListener,
      _fnSortingClasses: _fnSortingClasses,
      _fnSortData: _fnSortData,
      _fnSaveState: _fnSaveState,
      _fnLoadState: _fnLoadState,
      _fnSettingsFromNode: _fnSettingsFromNode,
      _fnLog: _fnLog,
      _fnMap: _fnMap,
      _fnBindAction: _fnBindAction,
      _fnCallbackReg: _fnCallbackReg,
      _fnCallbackFire: _fnCallbackFire,
      _fnLengthOverflow: _fnLengthOverflow,
      _fnRenderer: _fnRenderer,
      _fnDataSource: _fnDataSource,
      _fnRowAttributes: _fnRowAttributes,
      _fnExtend: _fnExtend,
      _fnCalculateEnd: function _fnCalculateEnd() {} // Used by a lot of plug-ins, but redundant
      // in 1.10, so this dead-end function is
      // added to prevent errors

    }); // jQuery access

    $$$1.fn.dataTable = DataTable; // Provide access to the host jQuery object (circular reference)

    DataTable.$ = $$$1; // Legacy aliases

    $$$1.fn.dataTableSettings = DataTable.settings;
    $$$1.fn.dataTableExt = DataTable.ext; // With a capital `D` we return a DataTables API instance rather than a
    // jQuery object

    $$$1.fn.DataTable = function (opts) {
      return $$$1(this).dataTable(opts).api();
    }; // All properties that are available to $.fn.dataTable should also be
    // available on $.fn.DataTable


    $$$1.each(DataTable, function (prop, val) {
      $$$1.fn.DataTable[prop] = val;
    }); // Information about events fired by DataTables - for documentation.

    /**
     * Draw event, fired whenever the table is redrawn on the page, at the same
     * point as fnDrawCallback. This may be useful for binding events or
     * performing calculations when the table is altered at all.
     *  @name DataTable#draw.dt
     *  @event
     *  @param {event} e jQuery event object
     *  @param {object} o DataTables settings object {@link DataTable.models.oSettings}
     */

    /**
     * Search event, fired when the searching applied to the table (using the
     * built-in global search, or column filters) is altered.
     *  @name DataTable#search.dt
     *  @event
     *  @param {event} e jQuery event object
     *  @param {object} o DataTables settings object {@link DataTable.models.oSettings}
     */

    /**
     * Page change event, fired when the paging of the table is altered.
     *  @name DataTable#page.dt
     *  @event
     *  @param {event} e jQuery event object
     *  @param {object} o DataTables settings object {@link DataTable.models.oSettings}
     */

    /**
     * Order event, fired when the ordering applied to the table is altered.
     *  @name DataTable#order.dt
     *  @event
     *  @param {event} e jQuery event object
     *  @param {object} o DataTables settings object {@link DataTable.models.oSettings}
     */

    /**
     * DataTables initialisation complete event, fired when the table is fully
     * drawn, including Ajax data loaded, if Ajax data is required.
     *  @name DataTable#init.dt
     *  @event
     *  @param {event} e jQuery event object
     *  @param {object} oSettings DataTables settings object
     *  @param {object} json The JSON object request from the server - only
     *    present if client-side Ajax sourced data is used</li></ol>
     */

    /**
     * State save event, fired when the table has changed state a new state save
     * is required. This event allows modification of the state saving object
     * prior to actually doing the save, including addition or other state
     * properties (for plug-ins) or modification of a DataTables core property.
     *  @name DataTable#stateSaveParams.dt
     *  @event
     *  @param {event} e jQuery event object
     *  @param {object} oSettings DataTables settings object
     *  @param {object} json The state information to be saved
     */

    /**
     * State load event, fired when the table is loading state from the stored
     * data, but prior to the settings object being modified by the saved state
     * - allowing modification of the saved state is required or loading of
     * state for a plug-in.
     *  @name DataTable#stateLoadParams.dt
     *  @event
     *  @param {event} e jQuery event object
     *  @param {object} oSettings DataTables settings object
     *  @param {object} json The saved state information
     */

    /**
     * State loaded event, fired when state has been loaded from stored data and
     * the settings object has been modified by the loaded data.
     *  @name DataTable#stateLoaded.dt
     *  @event
     *  @param {event} e jQuery event object
     *  @param {object} oSettings DataTables settings object
     *  @param {object} json The saved state information
     */

    /**
     * Processing event, fired when DataTables is doing some kind of processing
     * (be it, order, searcg or anything else). It can be used to indicate to
     * the end user that there is something happening, or that something has
     * finished.
     *  @name DataTable#processing.dt
     *  @event
     *  @param {event} e jQuery event object
     *  @param {object} oSettings DataTables settings object
     *  @param {boolean} bShow Flag for if DataTables is doing processing or not
     */

    /**
     * Ajax (XHR) event, fired whenever an Ajax request is completed from a
     * request to made to the server for new data. This event is called before
     * DataTables processed the returned data, so it can also be used to pre-
     * process the data returned from the server, if needed.
     *
     * Note that this trigger is called in `fnServerData`, if you override
     * `fnServerData` and which to use this event, you need to trigger it in you
     * success function.
     *  @name DataTable#xhr.dt
     *  @event
     *  @param {event} e jQuery event object
     *  @param {object} o DataTables settings object {@link DataTable.models.oSettings}
     *  @param {object} json JSON returned from the server
     *
     *  @example
     *     // Use a custom property returned from the server in another DOM element
     *     $('#table').dataTable().on('xhr.dt', function (e, settings, json) {
     *       $('#status').html( json.status );
     *     } );
     *
     *  @example
     *     // Pre-process the data returned from the server
     *     $('#table').dataTable().on('xhr.dt', function (e, settings, json) {
     *       for ( var i=0, ien=json.aaData.length ; i<ien ; i++ ) {
     *         json.aaData[i].sum = json.aaData[i].one + json.aaData[i].two;
     *       }
     *       // Note no return - manipulate the data directly in the JSON object.
     *     } );
     */

    /**
     * Destroy event, fired when the DataTable is destroyed by calling fnDestroy
     * or passing the bDestroy:true parameter in the initialisation object. This
     * can be used to remove bound events, added DOM nodes, etc.
     *  @name DataTable#destroy.dt
     *  @event
     *  @param {event} e jQuery event object
     *  @param {object} o DataTables settings object {@link DataTable.models.oSettings}
     */

    /**
     * Page length change event, fired when number of records to show on each
     * page (the length) is changed.
     *  @name DataTable#length.dt
     *  @event
     *  @param {event} e jQuery event object
     *  @param {object} o DataTables settings object {@link DataTable.models.oSettings}
     *  @param {integer} len New length
     */

    /**
     * Column sizing has changed.
     *  @name DataTable#column-sizing.dt
     *  @event
     *  @param {event} e jQuery event object
     *  @param {object} o DataTables settings object {@link DataTable.models.oSettings}
     */

    /**
     * Column visibility has changed.
     *  @name DataTable#column-visibility.dt
     *  @event
     *  @param {event} e jQuery event object
     *  @param {object} o DataTables settings object {@link DataTable.models.oSettings}
     *  @param {int} column Column index
     *  @param {bool} vis `false` if column now hidden, or `true` if visible
     */

    return $$$1.fn.dataTable;
  });
  /*! DataTables Bootstrap 4 integration
   * ©2011-2017 SpryMedia Ltd - datatables.net/license
   */

  /**
   * DataTables integration for Bootstrap 4. This requires Bootstrap 4 and
   * DataTables 1.10 or newer.
   *
   * This file sets the defaults and adds options to DataTables to style its
   * controls using Bootstrap. See http://datatables.net/manual/styling/bootstrap
   * for further information.
   */


  (function (factory) {
    if (typeof define === 'function' && define.amd) {
      // AMD
      define(['jquery', 'datatables.net'], function ($$$1) {
        return factory($$$1, window, document);
      });
    } else if (typeof exports === 'object') {
      // CommonJS
      module.exports = function (root, $$$1) {
        if (!root) {
          root = window;
        }

        if (!$$$1 || !$$$1.fn.dataTable) {
          // Require DataTables, which attaches to jQuery, including
          // jQuery if needed and have a $ property so we can access the
          // jQuery object that is used
          $$$1 = require('datatables.net')(root, $$$1).$;
        }

        return factory($$$1, root, root.document);
      };
    } else {
      // Browser
      factory(jQuery, window, document);
    }
  })(function ($$$1, window, document, undefined) {

    var DataTable = $$$1.fn.dataTable;
    /* Set the defaults for DataTables initialisation */

    $$$1.extend(true, DataTable.defaults, {
      dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" + "<'row'<'col-sm-12'tr>>" + "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
      renderer: 'bootstrap'
    });
    /* Default class modification */

    $$$1.extend(DataTable.ext.classes, {
      sWrapper: "dataTables_wrapper dt-bootstrap4",
      sFilterInput: "form-control form-control-sm",
      sLengthSelect: "custom-select custom-select-sm form-control form-control-sm",
      sProcessing: "dataTables_processing card",
      sPageButton: "paginate_button page-item"
    });
    /* Bootstrap paging button renderer */

    DataTable.ext.renderer.pageButton.bootstrap = function (settings, host, idx, buttons, page, pages) {
      var api = new DataTable.Api(settings);
      var classes = settings.oClasses;
      var lang = settings.oLanguage.oPaginate;
      var aria = settings.oLanguage.oAria.paginate || {};
      var btnDisplay,
          btnClass,
          counter = 0;

      var attach = function attach(container, buttons) {
        var i, ien, node, button;

        var clickHandler = function clickHandler(e) {
          e.preventDefault();

          if (!$$$1(e.currentTarget).hasClass('disabled') && api.page() != e.data.action) {
            api.page(e.data.action).draw('page');
          }
        };

        for (i = 0, ien = buttons.length; i < ien; i++) {
          button = buttons[i];

          if ($$$1.isArray(button)) {
            attach(container, button);
          } else {
            btnDisplay = '';
            btnClass = '';

            switch (button) {
              case 'ellipsis':
                btnDisplay = '&#x2026;';
                btnClass = 'disabled';
                break;

              case 'first':
                btnDisplay = lang.sFirst;
                btnClass = button + (page > 0 ? '' : ' disabled');
                break;

              case 'previous':
                btnDisplay = lang.sPrevious;
                btnClass = button + (page > 0 ? '' : ' disabled');
                break;

              case 'next':
                btnDisplay = lang.sNext;
                btnClass = button + (page < pages - 1 ? '' : ' disabled');
                break;

              case 'last':
                btnDisplay = lang.sLast;
                btnClass = button + (page < pages - 1 ? '' : ' disabled');
                break;

              default:
                btnDisplay = button + 1;
                btnClass = page === button ? 'active' : '';
                break;
            }

            if (btnDisplay) {
              node = $$$1('<li>', {
                'class': classes.sPageButton + ' ' + btnClass,
                'id': idx === 0 && typeof button === 'string' ? settings.sTableId + '_' + button : null
              }).append($$$1('<a>', {
                'href': '#',
                'aria-controls': settings.sTableId,
                'aria-label': aria[button],
                'data-dt-idx': counter,
                'tabindex': settings.iTabIndex,
                'class': 'page-link'
              }).html(btnDisplay)).appendTo(container);

              settings.oApi._fnBindAction(node, {
                action: button
              }, clickHandler);

              counter++;
            }
          }
        }
      }; // IE9 throws an 'unknown error' if document.activeElement is used
      // inside an iframe or frame. 


      var activeEl;

      try {
        // Because this approach is destroying and recreating the paging
        // elements, focus is lost on the select button which is bad for
        // accessibility. So we want to restore focus once the draw has
        // completed
        activeEl = $$$1(host).find(document.activeElement).data('dt-idx');
      } catch (e) {}

      attach($$$1(host).empty().html('<ul class="pagination"/>').children('ul'), buttons);

      if (activeEl !== undefined) {
        $$$1(host).find('[data-dt-idx=' + activeEl + ']').focus();
      }
    };

    return DataTable;
  });
  /*! Responsive 2.2.2
   * 2014-2018 SpryMedia Ltd - datatables.net/license
   */

  /**
   * @summary     Responsive
   * @description Responsive tables plug-in for DataTables
   * @version     2.2.2
   * @file        dataTables.responsive.js
   * @author      SpryMedia Ltd (www.sprymedia.co.uk)
   * @contact     www.sprymedia.co.uk/contact
   * @copyright   Copyright 2014-2018 SpryMedia Ltd.
   *
   * This source file is free software, available under the following license:
   *   MIT license - http://datatables.net/license/mit
   *
   * This source file is distributed in the hope that it will be useful, but
   * WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
   * or FITNESS FOR A PARTICULAR PURPOSE. See the license files for details.
   *
   * For details please refer to: http://www.datatables.net
   */


  (function (factory) {
    if (typeof define === 'function' && define.amd) {
      // AMD
      define(['jquery', 'datatables.net'], function ($$$1) {
        return factory($$$1, window, document);
      });
    } else if (typeof exports === 'object') {
      // CommonJS
      module.exports = function (root, $$$1) {
        if (!root) {
          root = window;
        }

        if (!$$$1 || !$$$1.fn.dataTable) {
          $$$1 = require('datatables.net')(root, $$$1).$;
        }

        return factory($$$1, root, root.document);
      };
    } else {
      // Browser
      factory(jQuery, window, document);
    }
  })(function ($$$1, window, document, undefined) {

    var DataTable = $$$1.fn.dataTable;
    /**
     * Responsive is a plug-in for the DataTables library that makes use of
     * DataTables' ability to change the visibility of columns, changing the
     * visibility of columns so the displayed columns fit into the table container.
     * The end result is that complex tables will be dynamically adjusted to fit
     * into the viewport, be it on a desktop, tablet or mobile browser.
     *
     * Responsive for DataTables has two modes of operation, which can used
     * individually or combined:
     *
     * * Class name based control - columns assigned class names that match the
     *   breakpoint logic can be shown / hidden as required for each breakpoint.
     * * Automatic control - columns are automatically hidden when there is no
     *   room left to display them. Columns removed from the right.
     *
     * In additional to column visibility control, Responsive also has built into
     * options to use DataTables' child row display to show / hide the information
     * from the table that has been hidden. There are also two modes of operation
     * for this child row display:
     *
     * * Inline - when the control element that the user can use to show / hide
     *   child rows is displayed inside the first column of the table.
     * * Column - where a whole column is dedicated to be the show / hide control.
     *
     * Initialisation of Responsive is performed by:
     *
     * * Adding the class `responsive` or `dt-responsive` to the table. In this case
     *   Responsive will automatically be initialised with the default configuration
     *   options when the DataTable is created.
     * * Using the `responsive` option in the DataTables configuration options. This
     *   can also be used to specify the configuration options, or simply set to
     *   `true` to use the defaults.
     *
     *  @class
     *  @param {object} settings DataTables settings object for the host table
     *  @param {object} [opts] Configuration options
     *  @requires jQuery 1.7+
     *  @requires DataTables 1.10.3+
     *
     *  @example
     *      $('#example').DataTable( {
     *        responsive: true
     *      } );
     *    } );
     */

    var Responsive = function Responsive(settings, opts) {
      // Sanity check that we are using DataTables 1.10 or newer
      if (!DataTable.versionCheck || !DataTable.versionCheck('1.10.10')) {
        throw 'DataTables Responsive requires DataTables 1.10.10 or newer';
      }

      this.s = {
        dt: new DataTable.Api(settings),
        columns: [],
        current: []
      }; // Check if responsive has already been initialised on this table

      if (this.s.dt.settings()[0].responsive) {
        return;
      } // details is an object, but for simplicity the user can give it as a string
      // or a boolean


      if (opts && typeof opts.details === 'string') {
        opts.details = {
          type: opts.details
        };
      } else if (opts && opts.details === false) {
        opts.details = {
          type: false
        };
      } else if (opts && opts.details === true) {
        opts.details = {
          type: 'inline'
        };
      }

      this.c = $$$1.extend(true, {}, Responsive.defaults, DataTable.defaults.responsive, opts);
      settings.responsive = this;

      this._constructor();
    };

    $$$1.extend(Responsive.prototype, {
      /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
       * Constructor
       */

      /**
       * Initialise the Responsive instance
       *
       * @private
       */
      _constructor: function _constructor() {
        var that = this;
        var dt = this.s.dt;
        var dtPrivateSettings = dt.settings()[0];
        var oldWindowWidth = $$$1(window).width();
        dt.settings()[0]._responsive = this; // Use DataTables' throttle function to avoid processor thrashing on
        // resize

        $$$1(window).on('resize.dtr orientationchange.dtr', DataTable.util.throttle(function () {
          // iOS has a bug whereby resize can fire when only scrolling
          // See: http://stackoverflow.com/questions/8898412
          var width = $$$1(window).width();

          if (width !== oldWindowWidth) {
            that._resize();

            oldWindowWidth = width;
          }
        })); // DataTables doesn't currently trigger an event when a row is added, so
        // we need to hook into its private API to enforce the hidden rows when
        // new data is added

        dtPrivateSettings.oApi._fnCallbackReg(dtPrivateSettings, 'aoRowCreatedCallback', function (tr, data, idx) {
          if ($$$1.inArray(false, that.s.current) !== -1) {
            $$$1('>td, >th', tr).each(function (i) {
              var idx = dt.column.index('toData', i);

              if (that.s.current[idx] === false) {
                $$$1(this).css('display', 'none');
              }
            });
          }
        }); // Destroy event handler


        dt.on('destroy.dtr', function () {
          dt.off('.dtr');
          $$$1(dt.table().body()).off('.dtr');
          $$$1(window).off('resize.dtr orientationchange.dtr'); // Restore the columns that we've hidden

          $$$1.each(that.s.current, function (i, val) {
            if (val === false) {
              that._setColumnVis(i, true);
            }
          });
        }); // Reorder the breakpoints array here in case they have been added out
        // of order

        this.c.breakpoints.sort(function (a, b) {
          return a.width < b.width ? 1 : a.width > b.width ? -1 : 0;
        });

        this._classLogic();

        this._resizeAuto(); // Details handler


        var details = this.c.details;

        if (details.type !== false) {
          that._detailsInit(); // DataTables will trigger this event on every column it shows and
          // hides individually


          dt.on('column-visibility.dtr', function () {
            // Use a small debounce to allow multiple columns to be set together
            if (that._timer) {
              clearTimeout(that._timer);
            }

            that._timer = setTimeout(function () {
              that._timer = null;

              that._classLogic();

              that._resizeAuto();

              that._resize();

              that._redrawChildren();
            }, 100);
          }); // Redraw the details box on each draw which will happen if the data
          // has changed. This is used until DataTables implements a native
          // `updated` event for rows

          dt.on('draw.dtr', function () {
            that._redrawChildren();
          });
          $$$1(dt.table().node()).addClass('dtr-' + details.type);
        }

        dt.on('column-reorder.dtr', function (e, settings, details) {
          that._classLogic();

          that._resizeAuto();

          that._resize();
        }); // Change in column sizes means we need to calc

        dt.on('column-sizing.dtr', function () {
          that._resizeAuto();

          that._resize();
        }); // On Ajax reload we want to reopen any child rows which are displayed
        // by responsive

        dt.on('preXhr.dtr', function () {
          var rowIds = [];
          dt.rows().every(function () {
            if (this.child.isShown()) {
              rowIds.push(this.id(true));
            }
          });
          dt.one('draw.dtr', function () {
            that._resizeAuto();

            that._resize();

            dt.rows(rowIds).every(function () {
              that._detailsDisplay(this, false);
            });
          });
        });
        dt.on('init.dtr', function (e, settings, details) {
          that._resizeAuto();

          that._resize(); // If columns were hidden, then DataTables needs to adjust the
          // column sizing


          if ($$$1.inArray(false, that.s.current)) {
            dt.columns.adjust();
          }
        }); // First pass - draw the table for the current viewport size

        this._resize();
      },

      /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
       * Private methods
       */

      /**
       * Calculate the visibility for the columns in a table for a given
       * breakpoint. The result is pre-determined based on the class logic if
       * class names are used to control all columns, but the width of the table
       * is also used if there are columns which are to be automatically shown
       * and hidden.
       *
       * @param  {string} breakpoint Breakpoint name to use for the calculation
       * @return {array} Array of boolean values initiating the visibility of each
       *   column.
       *  @private
       */
      _columnsVisiblity: function _columnsVisiblity(breakpoint) {
        var dt = this.s.dt;
        var columns = this.s.columns;
        var i, ien; // Create an array that defines the column ordering based first on the
        // column's priority, and secondly the column index. This allows the
        // columns to be removed from the right if the priority matches

        var order = columns.map(function (col, idx) {
          return {
            columnIdx: idx,
            priority: col.priority
          };
        }).sort(function (a, b) {
          if (a.priority !== b.priority) {
            return a.priority - b.priority;
          }

          return a.columnIdx - b.columnIdx;
        }); // Class logic - determine which columns are in this breakpoint based
        // on the classes. If no class control (i.e. `auto`) then `-` is used
        // to indicate this to the rest of the function

        var display = $$$1.map(columns, function (col, i) {
          if (dt.column(i).visible() === false) {
            return 'not-visible';
          }

          return col.auto && col.minWidth === null ? false : col.auto === true ? '-' : $$$1.inArray(breakpoint, col.includeIn) !== -1;
        }); // Auto column control - first pass: how much width is taken by the
        // ones that must be included from the non-auto columns

        var requiredWidth = 0;

        for (i = 0, ien = display.length; i < ien; i++) {
          if (display[i] === true) {
            requiredWidth += columns[i].minWidth;
          }
        } // Second pass, use up any remaining width for other columns. For
        // scrolling tables we need to subtract the width of the scrollbar. It
        // may not be requires which makes this sub-optimal, but it would
        // require another full redraw to make complete use of those extra few
        // pixels


        var scrolling = dt.settings()[0].oScroll;
        var bar = scrolling.sY || scrolling.sX ? scrolling.iBarWidth : 0;
        var widthAvailable = dt.table().container().offsetWidth - bar;
        var usedWidth = widthAvailable - requiredWidth; // Control column needs to always be included. This makes it sub-
        // optimal in terms of using the available with, but to stop layout
        // thrashing or overflow. Also we need to account for the control column
        // width first so we know how much width is available for the other
        // columns, since the control column might not be the first one shown

        for (i = 0, ien = display.length; i < ien; i++) {
          if (columns[i].control) {
            usedWidth -= columns[i].minWidth;
          }
        } // Allow columns to be shown (counting by priority and then right to
        // left) until we run out of room


        var empty = false;

        for (i = 0, ien = order.length; i < ien; i++) {
          var colIdx = order[i].columnIdx;

          if (display[colIdx] === '-' && !columns[colIdx].control && columns[colIdx].minWidth) {
            // Once we've found a column that won't fit we don't let any
            // others display either, or columns might disappear in the
            // middle of the table
            if (empty || usedWidth - columns[colIdx].minWidth < 0) {
              empty = true;
              display[colIdx] = false;
            } else {
              display[colIdx] = true;
            }

            usedWidth -= columns[colIdx].minWidth;
          }
        } // Determine if the 'control' column should be shown (if there is one).
        // This is the case when there is a hidden column (that is not the
        // control column). The two loops look inefficient here, but they are
        // trivial and will fly through. We need to know the outcome from the
        // first , before the action in the second can be taken


        var showControl = false;

        for (i = 0, ien = columns.length; i < ien; i++) {
          if (!columns[i].control && !columns[i].never && display[i] === false) {
            showControl = true;
            break;
          }
        }

        for (i = 0, ien = columns.length; i < ien; i++) {
          if (columns[i].control) {
            display[i] = showControl;
          } // Replace not visible string with false from the control column detection above


          if (display[i] === 'not-visible') {
            display[i] = false;
          }
        } // Finally we need to make sure that there is at least one column that
        // is visible


        if ($$$1.inArray(true, display) === -1) {
          display[0] = true;
        }

        return display;
      },

      /**
       * Create the internal `columns` array with information about the columns
       * for the table. This includes determining which breakpoints the column
       * will appear in, based upon class names in the column, which makes up the
       * vast majority of this method.
       *
       * @private
       */
      _classLogic: function _classLogic() {
        var that = this;
        var breakpoints = this.c.breakpoints;
        var dt = this.s.dt;
        var columns = dt.columns().eq(0).map(function (i) {
          var column = this.column(i);
          var className = column.header().className;
          var priority = dt.settings()[0].aoColumns[i].responsivePriority;

          if (priority === undefined) {
            var dataPriority = $$$1(column.header()).data('priority');
            priority = dataPriority !== undefined ? dataPriority * 1 : 10000;
          }

          return {
            className: className,
            includeIn: [],
            auto: false,
            control: false,
            never: className.match(/\bnever\b/) ? true : false,
            priority: priority
          };
        }); // Simply add a breakpoint to `includeIn` array, ensuring that there are
        // no duplicates

        var add = function add(colIdx, name) {
          var includeIn = columns[colIdx].includeIn;

          if ($$$1.inArray(name, includeIn) === -1) {
            includeIn.push(name);
          }
        };

        var column = function column(colIdx, name, operator, matched) {
          var size, i, ien;

          if (!operator) {
            columns[colIdx].includeIn.push(name);
          } else if (operator === 'max-') {
            // Add this breakpoint and all smaller
            size = that._find(name).width;

            for (i = 0, ien = breakpoints.length; i < ien; i++) {
              if (breakpoints[i].width <= size) {
                add(colIdx, breakpoints[i].name);
              }
            }
          } else if (operator === 'min-') {
            // Add this breakpoint and all larger
            size = that._find(name).width;

            for (i = 0, ien = breakpoints.length; i < ien; i++) {
              if (breakpoints[i].width >= size) {
                add(colIdx, breakpoints[i].name);
              }
            }
          } else if (operator === 'not-') {
            // Add all but this breakpoint
            for (i = 0, ien = breakpoints.length; i < ien; i++) {
              if (breakpoints[i].name.indexOf(matched) === -1) {
                add(colIdx, breakpoints[i].name);
              }
            }
          }
        }; // Loop over each column and determine if it has a responsive control
        // class


        columns.each(function (col, i) {
          var classNames = col.className.split(' ');
          var hasClass = false; // Split the class name up so multiple rules can be applied if needed

          for (var k = 0, ken = classNames.length; k < ken; k++) {
            var className = $$$1.trim(classNames[k]);

            if (className === 'all') {
              // Include in all
              hasClass = true;
              col.includeIn = $$$1.map(breakpoints, function (a) {
                return a.name;
              });
              return;
            } else if (className === 'none' || col.never) {
              // Include in none (default) and no auto
              hasClass = true;
              return;
            } else if (className === 'control') {
              // Special column that is only visible, when one of the other
              // columns is hidden. This is used for the details control
              hasClass = true;
              col.control = true;
              return;
            }

            $$$1.each(breakpoints, function (j, breakpoint) {
              // Does this column have a class that matches this breakpoint?
              var brokenPoint = breakpoint.name.split('-');
              var re = new RegExp('(min\\-|max\\-|not\\-)?(' + brokenPoint[0] + ')(\\-[_a-zA-Z0-9])?');
              var match = className.match(re);

              if (match) {
                hasClass = true;

                if (match[2] === brokenPoint[0] && match[3] === '-' + brokenPoint[1]) {
                  // Class name matches breakpoint name fully
                  column(i, breakpoint.name, match[1], match[2] + match[3]);
                } else if (match[2] === brokenPoint[0] && !match[3]) {
                  // Class name matched primary breakpoint name with no qualifier
                  column(i, breakpoint.name, match[1], match[2]);
                }
              }
            });
          } // If there was no control class, then automatic sizing is used


          if (!hasClass) {
            col.auto = true;
          }
        });
        this.s.columns = columns;
      },

      /**
       * Show the details for the child row
       *
       * @param  {DataTables.Api} row    API instance for the row
       * @param  {boolean}        update Update flag
       * @private
       */
      _detailsDisplay: function _detailsDisplay(row, update) {
        var that = this;
        var dt = this.s.dt;
        var details = this.c.details;

        if (details && details.type !== false) {
          var res = details.display(row, update, function () {
            return details.renderer(dt, row[0], that._detailsObj(row[0]));
          });

          if (res === true || res === false) {
            $$$1(dt.table().node()).triggerHandler('responsive-display.dt', [dt, row, res, update]);
          }
        }
      },

      /**
       * Initialisation for the details handler
       *
       * @private
       */
      _detailsInit: function _detailsInit() {
        var that = this;
        var dt = this.s.dt;
        var details = this.c.details; // The inline type always uses the first child as the target

        if (details.type === 'inline') {
          details.target = 'td:first-child, th:first-child';
        } // Keyboard accessibility


        dt.on('draw.dtr', function () {
          that._tabIndexes();
        });

        that._tabIndexes(); // Initial draw has already happened


        $$$1(dt.table().body()).on('keyup.dtr', 'td, th', function (e) {
          if (e.keyCode === 13 && $$$1(this).data('dtr-keyboard')) {
            $$$1(this).click();
          }
        }); // type.target can be a string jQuery selector or a column index

        var target = details.target;
        var selector = typeof target === 'string' ? target : 'td, th'; // Click handler to show / hide the details rows when they are available

        $$$1(dt.table().body()).on('click.dtr mousedown.dtr mouseup.dtr', selector, function (e) {
          // If the table is not collapsed (i.e. there is no hidden columns)
          // then take no action
          if (!$$$1(dt.table().node()).hasClass('collapsed')) {
            return;
          } // Check that the row is actually a DataTable's controlled node


          if ($$$1.inArray($$$1(this).closest('tr').get(0), dt.rows().nodes().toArray()) === -1) {
            return;
          } // For column index, we determine if we should act or not in the
          // handler - otherwise it is already okay


          if (typeof target === 'number') {
            var targetIdx = target < 0 ? dt.columns().eq(0).length + target : target;

            if (dt.cell(this).index().column !== targetIdx) {
              return;
            }
          } // $().closest() includes itself in its check


          var row = dt.row($$$1(this).closest('tr')); // Check event type to do an action

          if (e.type === 'click') {
            // The renderer is given as a function so the caller can execute it
            // only when they need (i.e. if hiding there is no point is running
            // the renderer)
            that._detailsDisplay(row, false);
          } else if (e.type === 'mousedown') {
            // For mouse users, prevent the focus ring from showing
            $$$1(this).css('outline', 'none');
          } else if (e.type === 'mouseup') {
            // And then re-allow at the end of the click
            $$$1(this).blur().css('outline', '');
          }
        });
      },

      /**
       * Get the details to pass to a renderer for a row
       * @param  {int} rowIdx Row index
       * @private
       */
      _detailsObj: function _detailsObj(rowIdx) {
        var that = this;
        var dt = this.s.dt;
        return $$$1.map(this.s.columns, function (col, i) {
          // Never and control columns should not be passed to the renderer
          if (col.never || col.control) {
            return;
          }

          return {
            title: dt.settings()[0].aoColumns[i].sTitle,
            data: dt.cell(rowIdx, i).render(that.c.orthogonal),
            hidden: dt.column(i).visible() && !that.s.current[i],
            columnIndex: i,
            rowIndex: rowIdx
          };
        });
      },

      /**
       * Find a breakpoint object from a name
       *
       * @param  {string} name Breakpoint name to find
       * @return {object}      Breakpoint description object
       * @private
       */
      _find: function _find(name) {
        var breakpoints = this.c.breakpoints;

        for (var i = 0, ien = breakpoints.length; i < ien; i++) {
          if (breakpoints[i].name === name) {
            return breakpoints[i];
          }
        }
      },

      /**
       * Re-create the contents of the child rows as the display has changed in
       * some way.
       *
       * @private
       */
      _redrawChildren: function _redrawChildren() {
        var that = this;
        var dt = this.s.dt;
        dt.rows({
          page: 'current'
        }).iterator('row', function (settings, idx) {
          var row = dt.row(idx);

          that._detailsDisplay(dt.row(idx), true);
        });
      },

      /**
       * Alter the table display for a resized viewport. This involves first
       * determining what breakpoint the window currently is in, getting the
       * column visibilities to apply and then setting them.
       *
       * @private
       */
      _resize: function _resize() {
        var that = this;
        var dt = this.s.dt;
        var width = $$$1(window).width();
        var breakpoints = this.c.breakpoints;
        var breakpoint = breakpoints[0].name;
        var columns = this.s.columns;
        var i, ien;
        var oldVis = this.s.current.slice(); // Determine what breakpoint we are currently at

        for (i = breakpoints.length - 1; i >= 0; i--) {
          if (width <= breakpoints[i].width) {
            breakpoint = breakpoints[i].name;
            break;
          }
        } // Show the columns for that break point


        var columnsVis = this._columnsVisiblity(breakpoint);

        this.s.current = columnsVis; // Set the class before the column visibility is changed so event
        // listeners know what the state is. Need to determine if there are
        // any columns that are not visible but can be shown

        var collapsedClass = false;

        for (i = 0, ien = columns.length; i < ien; i++) {
          if (columnsVis[i] === false && !columns[i].never && !columns[i].control && !dt.column(i).visible() === false) {
            collapsedClass = true;
            break;
          }
        }

        $$$1(dt.table().node()).toggleClass('collapsed', collapsedClass);
        var changed = false;
        var visible = 0;
        dt.columns().eq(0).each(function (colIdx, i) {
          if (columnsVis[i] === true) {
            visible++;
          }

          if (columnsVis[i] !== oldVis[i]) {
            changed = true;

            that._setColumnVis(colIdx, columnsVis[i]);
          }
        });

        if (changed) {
          this._redrawChildren(); // Inform listeners of the change


          $$$1(dt.table().node()).trigger('responsive-resize.dt', [dt, this.s.current]); // If no records, update the "No records" display element

          if (dt.page.info().recordsDisplay === 0) {
            $$$1('td', dt.table().body()).eq(0).attr('colspan', visible);
          }
        }
      },

      /**
       * Determine the width of each column in the table so the auto column hiding
       * has that information to work with. This method is never going to be 100%
       * perfect since column widths can change slightly per page, but without
       * seriously compromising performance this is quite effective.
       *
       * @private
       */
      _resizeAuto: function _resizeAuto() {
        var dt = this.s.dt;
        var columns = this.s.columns; // Are we allowed to do auto sizing?

        if (!this.c.auto) {
          return;
        } // Are there any columns that actually need auto-sizing, or do they all
        // have classes defined


        if ($$$1.inArray(true, $$$1.map(columns, function (c) {
          return c.auto;
        })) === -1) {
          return;
        } // Need to restore all children. They will be reinstated by a re-render


        if (!$$$1.isEmptyObject(_childNodeStore)) {
          $$$1.each(_childNodeStore, function (key) {
            var idx = key.split('-');

            _childNodesRestore(dt, idx[0] * 1, idx[1] * 1);
          });
        } // Clone the table with the current data in it


        var tableWidth = dt.table().node().offsetWidth;
        var columnWidths = dt.columns;
        var clonedTable = dt.table().node().cloneNode(false);
        var clonedHeader = $$$1(dt.table().header().cloneNode(false)).appendTo(clonedTable);
        var clonedBody = $$$1(dt.table().body()).clone(false, false).empty().appendTo(clonedTable); // use jQuery because of IE8
        // Header

        var headerCells = dt.columns().header().filter(function (idx) {
          return dt.column(idx).visible();
        }).to$().clone(false).css('display', 'table-cell').css('min-width', 0); // Body rows - we don't need to take account of DataTables' column
        // visibility since we implement our own here (hence the `display` set)

        $$$1(clonedBody).append($$$1(dt.rows({
          page: 'current'
        }).nodes()).clone(false)).find('th, td').css('display', ''); // Footer

        var footer = dt.table().footer();

        if (footer) {
          var clonedFooter = $$$1(footer.cloneNode(false)).appendTo(clonedTable);
          var footerCells = dt.columns().footer().filter(function (idx) {
            return dt.column(idx).visible();
          }).to$().clone(false).css('display', 'table-cell');
          $$$1('<tr/>').append(footerCells).appendTo(clonedFooter);
        }

        $$$1('<tr/>').append(headerCells).appendTo(clonedHeader); // In the inline case extra padding is applied to the first column to
        // give space for the show / hide icon. We need to use this in the
        // calculation

        if (this.c.details.type === 'inline') {
          $$$1(clonedTable).addClass('dtr-inline collapsed');
        } // It is unsafe to insert elements with the same name into the DOM
        // multiple times. For example, cloning and inserting a checked radio
        // clears the chcecked state of the original radio.


        $$$1(clonedTable).find('[name]').removeAttr('name'); // A position absolute table would take the table out of the flow of
        // our container element, bypassing the height and width (Scroller)

        $$$1(clonedTable).css('position', 'relative');
        var inserted = $$$1('<div/>').css({
          width: 1,
          height: 1,
          overflow: 'hidden',
          clear: 'both'
        }).append(clonedTable);
        inserted.insertBefore(dt.table().node()); // The cloned header now contains the smallest that each column can be

        headerCells.each(function (i) {
          var idx = dt.column.index('fromVisible', i);
          columns[idx].minWidth = this.offsetWidth || 0;
        });
        inserted.remove();
      },

      /**
       * Set a column's visibility.
       *
       * We don't use DataTables' column visibility controls in order to ensure
       * that column visibility can Responsive can no-exist. Since only IE8+ is
       * supported (and all evergreen browsers of course) the control of the
       * display attribute works well.
       *
       * @param {integer} col      Column index
       * @param {boolean} showHide Show or hide (true or false)
       * @private
       */
      _setColumnVis: function _setColumnVis(col, showHide) {
        var dt = this.s.dt;
        var display = showHide ? '' : 'none'; // empty string will remove the attr

        $$$1(dt.column(col).header()).css('display', display);
        $$$1(dt.column(col).footer()).css('display', display);
        dt.column(col).nodes().to$().css('display', display); // If the are child nodes stored, we might need to reinsert them

        if (!$$$1.isEmptyObject(_childNodeStore)) {
          dt.cells(null, col).indexes().each(function (idx) {
            _childNodesRestore(dt, idx.row, idx.column);
          });
        }
      },

      /**
       * Update the cell tab indexes for keyboard accessibility. This is called on
       * every table draw - that is potentially inefficient, but also the least
       * complex option given that column visibility can change on the fly. Its a
       * shame user-focus was removed from CSS 3 UI, as it would have solved this
       * issue with a single CSS statement.
       *
       * @private
       */
      _tabIndexes: function _tabIndexes() {
        var dt = this.s.dt;
        var cells = dt.cells({
          page: 'current'
        }).nodes().to$();
        var ctx = dt.settings()[0];
        var target = this.c.details.target;
        cells.filter('[data-dtr-keyboard]').removeData('[data-dtr-keyboard]');

        if (typeof target === 'number') {
          dt.cells(null, target, {
            page: 'current'
          }).nodes().to$().attr('tabIndex', ctx.iTabIndex).data('dtr-keyboard', 1);
        } else {
          // This is a bit of a hack - we need to limit the selected nodes to just
          // those of this table
          if (target === 'td:first-child, th:first-child') {
            target = '>td:first-child, >th:first-child';
          }

          $$$1(target, dt.rows({
            page: 'current'
          }).nodes()).attr('tabIndex', ctx.iTabIndex).data('dtr-keyboard', 1);
        }
      }
    });
    /**
     * List of default breakpoints. Each item in the array is an object with two
     * properties:
     *
     * * `name` - the breakpoint name.
     * * `width` - the breakpoint width
     *
     * @name Responsive.breakpoints
     * @static
     */

    Responsive.breakpoints = [{
      name: 'desktop',
      width: Infinity
    }, {
      name: 'tablet-l',
      width: 1024
    }, {
      name: 'tablet-p',
      width: 768
    }, {
      name: 'mobile-l',
      width: 480
    }, {
      name: 'mobile-p',
      width: 320
    }];
    /**
     * Display methods - functions which define how the hidden data should be shown
     * in the table.
     *
     * @namespace
     * @name Responsive.defaults
     * @static
     */

    Responsive.display = {
      childRow: function childRow(row, update, render) {
        if (update) {
          if ($$$1(row.node()).hasClass('parent')) {
            row.child(render(), 'child').show();
            return true;
          }
        } else {
          if (!row.child.isShown()) {
            row.child(render(), 'child').show();
            $$$1(row.node()).addClass('parent');
            return true;
          } else {
            row.child(false);
            $$$1(row.node()).removeClass('parent');
            return false;
          }
        }
      },
      childRowImmediate: function childRowImmediate(row, update, render) {
        if (!update && row.child.isShown() || !row.responsive.hasHidden()) {
          // User interaction and the row is show, or nothing to show
          row.child(false);
          $$$1(row.node()).removeClass('parent');
          return false;
        } else {
          // Display
          row.child(render(), 'child').show();
          $$$1(row.node()).addClass('parent');
          return true;
        }
      },
      // This is a wrapper so the modal options for Bootstrap and jQuery UI can
      // have options passed into them. This specific one doesn't need to be a
      // function but it is for consistency in the `modal` name
      modal: function modal(options) {
        return function (row, update, render) {
          if (!update) {
            // Show a modal
            var close = function close() {
              modal.remove(); // will tidy events for us

              $$$1(document).off('keypress.dtr');
            };

            var modal = $$$1('<div class="dtr-modal"/>').append($$$1('<div class="dtr-modal-display"/>').append($$$1('<div class="dtr-modal-content"/>').append(render())).append($$$1('<div class="dtr-modal-close">&times;</div>').click(function () {
              close();
            }))).append($$$1('<div class="dtr-modal-background"/>').click(function () {
              close();
            })).appendTo('body');
            $$$1(document).on('keyup.dtr', function (e) {
              if (e.keyCode === 27) {
                e.stopPropagation();
                close();
              }
            });
          } else {
            $$$1('div.dtr-modal-content').empty().append(render());
          }

          if (options && options.header) {
            $$$1('div.dtr-modal-content').prepend('<h2>' + options.header(row) + '</h2>');
          }
        };
      }
    };
    var _childNodeStore = {};

    function _childNodes(dt, row, col) {
      var name = row + '-' + col;

      if (_childNodeStore[name]) {
        return _childNodeStore[name];
      } // https://jsperf.com/childnodes-array-slice-vs-loop


      var nodes = [];
      var children = dt.cell(row, col).node().childNodes;

      for (var i = 0, ien = children.length; i < ien; i++) {
        nodes.push(children[i]);
      }

      _childNodeStore[name] = nodes;
      return nodes;
    }

    function _childNodesRestore(dt, row, col) {
      var name = row + '-' + col;

      if (!_childNodeStore[name]) {
        return;
      }

      var node = dt.cell(row, col).node();
      var store = _childNodeStore[name];
      var parent = store[0].parentNode;
      var parentChildren = parent.childNodes;
      var a = [];

      for (var i = 0, ien = parentChildren.length; i < ien; i++) {
        a.push(parentChildren[i]);
      }

      for (var j = 0, jen = a.length; j < jen; j++) {
        node.appendChild(a[j]);
      }

      _childNodeStore[name] = undefined;
    }
    /**
     * Display methods - functions which define how the hidden data should be shown
     * in the table.
     *
     * @namespace
     * @name Responsive.defaults
     * @static
     */


    Responsive.renderer = {
      listHiddenNodes: function listHiddenNodes() {
        return function (api, rowIdx, columns) {
          var ul = $$$1('<ul data-dtr-index="' + rowIdx + '" class="dtr-details"/>');
          var found = false;
          var data = $$$1.each(columns, function (i, col) {
            if (col.hidden) {
              $$$1('<li data-dtr-index="' + col.columnIndex + '" data-dt-row="' + col.rowIndex + '" data-dt-column="' + col.columnIndex + '">' + '<span class="dtr-title">' + col.title + '</span> ' + '</li>').append($$$1('<span class="dtr-data"/>').append(_childNodes(api, col.rowIndex, col.columnIndex))) // api.cell( col.rowIndex, col.columnIndex ).node().childNodes ) )
              .appendTo(ul);
              found = true;
            }
          });
          return found ? ul : false;
        };
      },
      listHidden: function listHidden() {
        return function (api, rowIdx, columns) {
          var data = $$$1.map(columns, function (col) {
            return col.hidden ? '<li data-dtr-index="' + col.columnIndex + '" data-dt-row="' + col.rowIndex + '" data-dt-column="' + col.columnIndex + '">' + '<span class="dtr-title">' + col.title + '</span> ' + '<span class="dtr-data">' + col.data + '</span>' + '</li>' : '';
          }).join('');
          return data ? $$$1('<ul data-dtr-index="' + rowIdx + '" class="dtr-details"/>').append(data) : false;
        };
      },
      tableAll: function tableAll(options) {
        options = $$$1.extend({
          tableClass: ''
        }, options);
        return function (api, rowIdx, columns) {
          var data = $$$1.map(columns, function (col) {
            return '<tr data-dt-row="' + col.rowIndex + '" data-dt-column="' + col.columnIndex + '">' + '<td>' + col.title + ':' + '</td> ' + '<td>' + col.data + '</td>' + '</tr>';
          }).join('');
          return $$$1('<table class="' + options.tableClass + ' dtr-details" width="100%"/>').append(data);
        };
      }
    };
    /**
     * Responsive default settings for initialisation
     *
     * @namespace
     * @name Responsive.defaults
     * @static
     */

    Responsive.defaults = {
      /**
       * List of breakpoints for the instance. Note that this means that each
       * instance can have its own breakpoints. Additionally, the breakpoints
       * cannot be changed once an instance has been creased.
       *
       * @type {Array}
       * @default Takes the value of `Responsive.breakpoints`
       */
      breakpoints: Responsive.breakpoints,

      /**
       * Enable / disable auto hiding calculations. It can help to increase
       * performance slightly if you disable this option, but all columns would
       * need to have breakpoint classes assigned to them
       *
       * @type {Boolean}
       * @default  `true`
       */
      auto: true,

      /**
       * Details control. If given as a string value, the `type` property of the
       * default object is set to that value, and the defaults used for the rest
       * of the object - this is for ease of implementation.
       *
       * The object consists of the following properties:
       *
       * * `display` - A function that is used to show and hide the hidden details
       * * `renderer` - function that is called for display of the child row data.
       *   The default function will show the data from the hidden columns
       * * `target` - Used as the selector for what objects to attach the child
       *   open / close to
       * * `type` - `false` to disable the details display, `inline` or `column`
       *   for the two control types
       *
       * @type {Object|string}
       */
      details: {
        display: Responsive.display.childRow,
        renderer: Responsive.renderer.listHidden(),
        target: 0,
        type: 'inline'
      },

      /**
       * Orthogonal data request option. This is used to define the data type
       * requested when Responsive gets the data to show in the child row.
       *
       * @type {String}
       */
      orthogonal: 'display'
    };
    /*
     * API
     */

    var Api = $$$1.fn.dataTable.Api; // Doesn't do anything - work around for a bug in DT... Not documented

    Api.register('responsive()', function () {
      return this;
    });
    Api.register('responsive.index()', function (li) {
      li = $$$1(li);
      return {
        column: li.data('dtr-index'),
        row: li.parent().data('dtr-index')
      };
    });
    Api.register('responsive.rebuild()', function () {
      return this.iterator('table', function (ctx) {
        if (ctx._responsive) {
          ctx._responsive._classLogic();
        }
      });
    });
    Api.register('responsive.recalc()', function () {
      return this.iterator('table', function (ctx) {
        if (ctx._responsive) {
          ctx._responsive._resizeAuto();

          ctx._responsive._resize();
        }
      });
    });
    Api.register('responsive.hasHidden()', function () {
      var ctx = this.context[0];
      return ctx._responsive ? $$$1.inArray(false, ctx._responsive.s.current) !== -1 : false;
    });
    Api.registerPlural('columns().responsiveHidden()', 'column().responsiveHidden()', function () {
      return this.iterator('column', function (settings, column) {
        return settings._responsive ? settings._responsive.s.current[column] : false;
      }, 1);
    });
    /**
     * Version information
     *
     * @name Responsive.version
     * @static
     */

    Responsive.version = '2.2.2';
    $$$1.fn.dataTable.Responsive = Responsive;
    $$$1.fn.DataTable.Responsive = Responsive; // Attach a listener to the document which listens for DataTables initialisation
    // events so we can automatically initialise

    $$$1(document).on('preInit.dt.dtr', function (e, settings, json) {
      if (e.namespace !== 'dt') {
        return;
      }

      if ($$$1(settings.nTable).hasClass('responsive') || $$$1(settings.nTable).hasClass('dt-responsive') || settings.oInit.responsive || DataTable.defaults.responsive) {
        var init = settings.oInit.responsive;

        if (init !== false) {
          new Responsive(settings, $$$1.isPlainObject(init) ? init : {});
        }
      }
    });
    return Responsive;
  });

  /*! jquery-qrcode v0.14.0 - https://larsjung.de/jquery-qrcode/ */
  (function (vendor_qrcode) {

    var jq = window.jQuery; // Check if canvas is available in the browser (as Modernizr does)

    var hasCanvas = function () {
      var elem = document.createElement('canvas');
      return !!(elem.getContext && elem.getContext('2d'));
    }(); // Wrapper for the original QR code generator.


    function createQRCode(text, level, version, quiet) {
      var qr = {};
      var vqr = vendor_qrcode(version, level);
      vqr.addData(text);
      vqr.make();
      quiet = quiet || 0;
      var qrModuleCount = vqr.getModuleCount();
      var quietModuleCount = vqr.getModuleCount() + 2 * quiet;

      function isDark(row, col) {
        row -= quiet;
        col -= quiet;

        if (row < 0 || row >= qrModuleCount || col < 0 || col >= qrModuleCount) {
          return false;
        }

        return vqr.isDark(row, col);
      }

      function addBlank(l, t, r, b) {
        var prevIsDark = qr.isDark;
        var moduleSize = 1 / quietModuleCount;

        qr.isDark = function (row, col) {
          var ml = col * moduleSize;
          var mt = row * moduleSize;
          var mr = ml + moduleSize;
          var mb = mt + moduleSize;
          return prevIsDark(row, col) && (l > mr || ml > r || t > mb || mt > b);
        };
      }

      qr.text = text;
      qr.level = level;
      qr.version = version;
      qr.moduleCount = quietModuleCount;
      qr.isDark = isDark;
      qr.addBlank = addBlank;
      return qr;
    } // Returns a minimal QR code for the given text starting with version `minVersion`.
    // Returns `undefined` if `text` is too long to be encoded in `maxVersion`.


    function createMinQRCode(text, level, minVersion, maxVersion, quiet) {
      minVersion = Math.max(1, minVersion || 1);
      maxVersion = Math.min(40, maxVersion || 40);

      for (var version = minVersion; version <= maxVersion; version += 1) {
        try {
          return createQRCode(text, level, version, quiet);
        } catch (err) {
          /* empty */
        }
      }

      return undefined;
    }

    function drawBackgroundLabel(qr, context, settings) {
      var size = settings.size;
      var font = 'bold ' + settings.mSize * size + 'px ' + settings.fontname;
      var ctx = jq('<canvas/>')[0].getContext('2d');
      ctx.font = font;
      var w = ctx.measureText(settings.label).width;
      var sh = settings.mSize;
      var sw = w / size;
      var sl = (1 - sw) * settings.mPosX;
      var st = (1 - sh) * settings.mPosY;
      var sr = sl + sw;
      var sb = st + sh;
      var pad = 0.01;

      if (settings.mode === 1) {
        // Strip
        qr.addBlank(0, st - pad, size, sb + pad);
      } else {
        // Box
        qr.addBlank(sl - pad, st - pad, sr + pad, sb + pad);
      }

      context.fillStyle = settings.fontcolor;
      context.font = font;
      context.fillText(settings.label, sl * size, st * size + 0.75 * settings.mSize * size);
    }

    function drawBackgroundImage(qr, context, settings) {
      var size = settings.size;
      var w = settings.image.naturalWidth || 1;
      var h = settings.image.naturalHeight || 1;
      var sh = settings.mSize;
      var sw = sh * w / h;
      var sl = (1 - sw) * settings.mPosX;
      var st = (1 - sh) * settings.mPosY;
      var sr = sl + sw;
      var sb = st + sh;
      var pad = 0.01;

      if (settings.mode === 3) {
        // Strip
        qr.addBlank(0, st - pad, size, sb + pad);
      } else {
        // Box
        qr.addBlank(sl - pad, st - pad, sr + pad, sb + pad);
      }

      context.drawImage(settings.image, sl * size, st * size, sw * size, sh * size);
    }

    function drawBackground(qr, context, settings) {
      if (jq(settings.background).is('img')) {
        context.drawImage(settings.background, 0, 0, settings.size, settings.size);
      } else if (settings.background) {
        context.fillStyle = settings.background;
        context.fillRect(settings.left, settings.top, settings.size, settings.size);
      }

      var mode = settings.mode;

      if (mode === 1 || mode === 2) {
        drawBackgroundLabel(qr, context, settings);
      } else if (mode === 3 || mode === 4) {
        drawBackgroundImage(qr, context, settings);
      }
    }

    function drawModuleDefault(qr, context, settings, left, top, width, row, col) {
      if (qr.isDark(row, col)) {
        context.rect(left, top, width, width);
      }
    }

    function drawModuleRoundedDark(ctx, l, t, r, b, rad, nw, ne, se, sw) {
      if (nw) {
        ctx.moveTo(l + rad, t);
      } else {
        ctx.moveTo(l, t);
      }

      if (ne) {
        ctx.lineTo(r - rad, t);
        ctx.arcTo(r, t, r, b, rad);
      } else {
        ctx.lineTo(r, t);
      }

      if (se) {
        ctx.lineTo(r, b - rad);
        ctx.arcTo(r, b, l, b, rad);
      } else {
        ctx.lineTo(r, b);
      }

      if (sw) {
        ctx.lineTo(l + rad, b);
        ctx.arcTo(l, b, l, t, rad);
      } else {
        ctx.lineTo(l, b);
      }

      if (nw) {
        ctx.lineTo(l, t + rad);
        ctx.arcTo(l, t, r, t, rad);
      } else {
        ctx.lineTo(l, t);
      }
    }

    function drawModuleRoundendLight(ctx, l, t, r, b, rad, nw, ne, se, sw) {
      if (nw) {
        ctx.moveTo(l + rad, t);
        ctx.lineTo(l, t);
        ctx.lineTo(l, t + rad);
        ctx.arcTo(l, t, l + rad, t, rad);
      }

      if (ne) {
        ctx.moveTo(r - rad, t);
        ctx.lineTo(r, t);
        ctx.lineTo(r, t + rad);
        ctx.arcTo(r, t, r - rad, t, rad);
      }

      if (se) {
        ctx.moveTo(r - rad, b);
        ctx.lineTo(r, b);
        ctx.lineTo(r, b - rad);
        ctx.arcTo(r, b, r - rad, b, rad);
      }

      if (sw) {
        ctx.moveTo(l + rad, b);
        ctx.lineTo(l, b);
        ctx.lineTo(l, b - rad);
        ctx.arcTo(l, b, l + rad, b, rad);
      }
    }

    function drawModuleRounded(qr, context, settings, left, top, width, row, col) {
      var isDark = qr.isDark;
      var right = left + width;
      var bottom = top + width;
      var radius = settings.radius * width;
      var rowT = row - 1;
      var rowB = row + 1;
      var colL = col - 1;
      var colR = col + 1;
      var center = isDark(row, col);
      var northwest = isDark(rowT, colL);
      var north = isDark(rowT, col);
      var northeast = isDark(rowT, colR);
      var east = isDark(row, colR);
      var southeast = isDark(rowB, colR);
      var south = isDark(rowB, col);
      var southwest = isDark(rowB, colL);
      var west = isDark(row, colL);

      if (center) {
        drawModuleRoundedDark(context, left, top, right, bottom, radius, !north && !west, !north && !east, !south && !east, !south && !west);
      } else {
        drawModuleRoundendLight(context, left, top, right, bottom, radius, north && west && northwest, north && east && northeast, south && east && southeast, south && west && southwest);
      }
    }

    function drawModules(qr, context, settings) {
      var moduleCount = qr.moduleCount;
      var moduleSize = settings.size / moduleCount;
      var fn = drawModuleDefault;
      var row;
      var col;

      if (settings.radius > 0 && settings.radius <= 0.5) {
        fn = drawModuleRounded;
      }

      context.beginPath();

      for (row = 0; row < moduleCount; row += 1) {
        for (col = 0; col < moduleCount; col += 1) {
          var l = settings.left + col * moduleSize;
          var t = settings.top + row * moduleSize;
          var w = moduleSize;
          fn(qr, context, settings, l, t, w, row, col);
        }
      }

      if (jq(settings.fill).is('img')) {
        context.strokeStyle = 'rgba(0,0,0,0.5)';
        context.lineWidth = 2;
        context.stroke();
        var prev = context.globalCompositeOperation;
        context.globalCompositeOperation = 'destination-out';
        context.fill();
        context.globalCompositeOperation = prev;
        context.clip();
        context.drawImage(settings.fill, 0, 0, settings.size, settings.size);
        context.restore();
      } else {
        context.fillStyle = settings.fill;
        context.fill();
      }
    } // Draws QR code to the given `canvas` and returns it.


    function drawOnCanvas(canvas, settings) {
      var qr = createMinQRCode(settings.text, settings.ecLevel, settings.minVersion, settings.maxVersion, settings.quiet);

      if (!qr) {
        return null;
      }

      var $canvas = jq(canvas).data('qrcode', qr);
      var context = $canvas[0].getContext('2d');
      drawBackground(qr, context, settings);
      drawModules(qr, context, settings);
      return $canvas;
    } // Returns a `canvas` element representing the QR code for the given settings.


    function createCanvas(settings) {
      var $canvas = jq('<canvas/>').attr('width', settings.size).attr('height', settings.size);
      return drawOnCanvas($canvas, settings);
    } // Returns an `image` element representing the QR code for the given settings.


    function createImage(settings) {
      return jq('<img/>').attr('src', createCanvas(settings)[0].toDataURL('image/png'));
    } // Returns a `div` element representing the QR code for the given settings.


    function createDiv(settings) {
      var qr = createMinQRCode(settings.text, settings.ecLevel, settings.minVersion, settings.maxVersion, settings.quiet);

      if (!qr) {
        return null;
      } // some shortcuts to improve compression


      var settings_size = settings.size;
      var settings_bgColor = settings.background;
      var math_floor = Math.floor;
      var moduleCount = qr.moduleCount;
      var moduleSize = math_floor(settings_size / moduleCount);
      var offset = math_floor(0.5 * (settings_size - moduleSize * moduleCount));
      var row;
      var col;
      var containerCSS = {
        position: 'relative',
        left: 0,
        top: 0,
        padding: 0,
        margin: 0,
        width: settings_size,
        height: settings_size
      };
      var darkCSS = {
        position: 'absolute',
        padding: 0,
        margin: 0,
        width: moduleSize,
        height: moduleSize,
        'background-color': settings.fill
      };
      var $div = jq('<div/>').data('qrcode', qr).css(containerCSS);

      if (settings_bgColor) {
        $div.css('background-color', settings_bgColor);
      }

      for (row = 0; row < moduleCount; row += 1) {
        for (col = 0; col < moduleCount; col += 1) {
          if (qr.isDark(row, col)) {
            jq('<div/>').css(darkCSS).css({
              left: offset + col * moduleSize,
              top: offset + row * moduleSize
            }).appendTo($div);
          }
        }
      }

      return $div;
    }

    function createHTML(settings) {
      if (hasCanvas && settings.render === 'canvas') {
        return createCanvas(settings);
      } else if (hasCanvas && settings.render === 'image') {
        return createImage(settings);
      }

      return createDiv(settings);
    } // Plugin
    // ======
    // Default settings
    // ----------------


    var defaults = {
      // render method: `'canvas'`, `'image'` or `'div'`
      render: 'canvas',
      // version range somewhere in 1 .. 40
      minVersion: 1,
      maxVersion: 40,
      // error correction level: `'L'`, `'M'`, `'Q'` or `'H'`
      ecLevel: 'L',
      // offset in pixel if drawn onto existing canvas
      left: 0,
      top: 0,
      // size in pixel
      size: 200,
      // code color or image element
      fill: '#000',
      // background color or image element, `null` for transparent background
      background: null,
      // content
      text: 'no text',
      // corner radius relative to module width: 0.0 .. 0.5
      radius: 0,
      // quiet zone in modules
      quiet: 0,
      // modes
      // 0: normal
      // 1: label strip
      // 2: label box
      // 3: image strip
      // 4: image box
      mode: 0,
      mSize: 0.1,
      mPosX: 0.5,
      mPosY: 0.5,
      label: 'no label',
      fontname: 'sans',
      fontcolor: '#000',
      image: null
    }; // Register the plugin
    // -------------------

    jq.fn.qrcode = function (options) {
      var settings = jq.extend({}, defaults, options);
      return this.each(function (idx, el) {
        if (el.nodeName.toLowerCase() === 'canvas') {
          drawOnCanvas(el, settings);
        } else {
          jq(el).append(createHTML(settings));
        }
      });
    };
  })(function () {
    // `qrcode` is the single public function defined by the `QR Code Generator`
    //---------------------------------------------------------------------
    //
    // QR Code Generator for JavaScript
    //
    // Copyright (c) 2009 Kazuhiko Arase
    //
    // URL: http://www.d-project.com/
    //
    // Licensed under the MIT license:
    //  http://www.opensource.org/licenses/mit-license.php
    //
    // The word 'QR Code' is registered trademark of
    // DENSO WAVE INCORPORATED
    //  http://www.denso-wave.com/qrcode/faqpatent-e.html
    //
    //---------------------------------------------------------------------
    var qrcode = function () {
      //---------------------------------------------------------------------
      // qrcode
      //---------------------------------------------------------------------

      /**
       * qrcode
       * @param typeNumber 1 to 40
       * @param errorCorrectLevel 'L','M','Q','H'
       */
      var qrcode = function qrcode(typeNumber, errorCorrectLevel) {
        var PAD0 = 0xEC;
        var PAD1 = 0x11;
        var _typeNumber = typeNumber;
        var _errorCorrectLevel = QRErrorCorrectLevel[errorCorrectLevel];
        var _modules = null;
        var _moduleCount = 0;
        var _dataCache = null;

        var _dataList = new Array();

        var _this = {};

        var makeImpl = function makeImpl(test, maskPattern) {
          _moduleCount = _typeNumber * 4 + 17;

          _modules = function (moduleCount) {
            var modules = new Array(moduleCount);

            for (var row = 0; row < moduleCount; row += 1) {
              modules[row] = new Array(moduleCount);

              for (var col = 0; col < moduleCount; col += 1) {
                modules[row][col] = null;
              }
            }

            return modules;
          }(_moduleCount);

          setupPositionProbePattern(0, 0);
          setupPositionProbePattern(_moduleCount - 7, 0);
          setupPositionProbePattern(0, _moduleCount - 7);
          setupPositionAdjustPattern();
          setupTimingPattern();
          setupTypeInfo(test, maskPattern);

          if (_typeNumber >= 7) {
            setupTypeNumber(test);
          }

          if (_dataCache == null) {
            _dataCache = createData(_typeNumber, _errorCorrectLevel, _dataList);
          }

          mapData(_dataCache, maskPattern);
        };

        var setupPositionProbePattern = function setupPositionProbePattern(row, col) {
          for (var r = -1; r <= 7; r += 1) {
            if (row + r <= -1 || _moduleCount <= row + r) continue;

            for (var c = -1; c <= 7; c += 1) {
              if (col + c <= -1 || _moduleCount <= col + c) continue;

              if (0 <= r && r <= 6 && (c == 0 || c == 6) || 0 <= c && c <= 6 && (r == 0 || r == 6) || 2 <= r && r <= 4 && 2 <= c && c <= 4) {
                _modules[row + r][col + c] = true;
              } else {
                _modules[row + r][col + c] = false;
              }
            }
          }
        };

        var getBestMaskPattern = function getBestMaskPattern() {
          var minLostPoint = 0;
          var pattern = 0;

          for (var i = 0; i < 8; i += 1) {
            makeImpl(true, i);
            var lostPoint = QRUtil.getLostPoint(_this);

            if (i == 0 || minLostPoint > lostPoint) {
              minLostPoint = lostPoint;
              pattern = i;
            }
          }

          return pattern;
        };

        var setupTimingPattern = function setupTimingPattern() {
          for (var r = 8; r < _moduleCount - 8; r += 1) {
            if (_modules[r][6] != null) {
              continue;
            }

            _modules[r][6] = r % 2 == 0;
          }

          for (var c = 8; c < _moduleCount - 8; c += 1) {
            if (_modules[6][c] != null) {
              continue;
            }

            _modules[6][c] = c % 2 == 0;
          }
        };

        var setupPositionAdjustPattern = function setupPositionAdjustPattern() {
          var pos = QRUtil.getPatternPosition(_typeNumber);

          for (var i = 0; i < pos.length; i += 1) {
            for (var j = 0; j < pos.length; j += 1) {
              var row = pos[i];
              var col = pos[j];

              if (_modules[row][col] != null) {
                continue;
              }

              for (var r = -2; r <= 2; r += 1) {
                for (var c = -2; c <= 2; c += 1) {
                  if (r == -2 || r == 2 || c == -2 || c == 2 || r == 0 && c == 0) {
                    _modules[row + r][col + c] = true;
                  } else {
                    _modules[row + r][col + c] = false;
                  }
                }
              }
            }
          }
        };

        var setupTypeNumber = function setupTypeNumber(test) {
          var bits = QRUtil.getBCHTypeNumber(_typeNumber);

          for (var i = 0; i < 18; i += 1) {
            var mod = !test && (bits >> i & 1) == 1;
            _modules[Math.floor(i / 3)][i % 3 + _moduleCount - 8 - 3] = mod;
          }

          for (var i = 0; i < 18; i += 1) {
            var mod = !test && (bits >> i & 1) == 1;
            _modules[i % 3 + _moduleCount - 8 - 3][Math.floor(i / 3)] = mod;
          }
        };

        var setupTypeInfo = function setupTypeInfo(test, maskPattern) {
          var data = _errorCorrectLevel << 3 | maskPattern;
          var bits = QRUtil.getBCHTypeInfo(data); // vertical

          for (var i = 0; i < 15; i += 1) {
            var mod = !test && (bits >> i & 1) == 1;

            if (i < 6) {
              _modules[i][8] = mod;
            } else if (i < 8) {
              _modules[i + 1][8] = mod;
            } else {
              _modules[_moduleCount - 15 + i][8] = mod;
            }
          } // horizontal


          for (var i = 0; i < 15; i += 1) {
            var mod = !test && (bits >> i & 1) == 1;

            if (i < 8) {
              _modules[8][_moduleCount - i - 1] = mod;
            } else if (i < 9) {
              _modules[8][15 - i - 1 + 1] = mod;
            } else {
              _modules[8][15 - i - 1] = mod;
            }
          } // fixed module


          _modules[_moduleCount - 8][8] = !test;
        };

        var mapData = function mapData(data, maskPattern) {
          var inc = -1;
          var row = _moduleCount - 1;
          var bitIndex = 7;
          var byteIndex = 0;
          var maskFunc = QRUtil.getMaskFunction(maskPattern);

          for (var col = _moduleCount - 1; col > 0; col -= 2) {
            if (col == 6) col -= 1;

            while (true) {
              for (var c = 0; c < 2; c += 1) {
                if (_modules[row][col - c] == null) {
                  var dark = false;

                  if (byteIndex < data.length) {
                    dark = (data[byteIndex] >>> bitIndex & 1) == 1;
                  }

                  var mask = maskFunc(row, col - c);

                  if (mask) {
                    dark = !dark;
                  }

                  _modules[row][col - c] = dark;
                  bitIndex -= 1;

                  if (bitIndex == -1) {
                    byteIndex += 1;
                    bitIndex = 7;
                  }
                }
              }

              row += inc;

              if (row < 0 || _moduleCount <= row) {
                row -= inc;
                inc = -inc;
                break;
              }
            }
          }
        };

        var createBytes = function createBytes(buffer, rsBlocks) {
          var offset = 0;
          var maxDcCount = 0;
          var maxEcCount = 0;
          var dcdata = new Array(rsBlocks.length);
          var ecdata = new Array(rsBlocks.length);

          for (var r = 0; r < rsBlocks.length; r += 1) {
            var dcCount = rsBlocks[r].dataCount;
            var ecCount = rsBlocks[r].totalCount - dcCount;
            maxDcCount = Math.max(maxDcCount, dcCount);
            maxEcCount = Math.max(maxEcCount, ecCount);
            dcdata[r] = new Array(dcCount);

            for (var i = 0; i < dcdata[r].length; i += 1) {
              dcdata[r][i] = 0xff & buffer.getBuffer()[i + offset];
            }

            offset += dcCount;
            var rsPoly = QRUtil.getErrorCorrectPolynomial(ecCount);
            var rawPoly = qrPolynomial(dcdata[r], rsPoly.getLength() - 1);
            var modPoly = rawPoly.mod(rsPoly);
            ecdata[r] = new Array(rsPoly.getLength() - 1);

            for (var i = 0; i < ecdata[r].length; i += 1) {
              var modIndex = i + modPoly.getLength() - ecdata[r].length;
              ecdata[r][i] = modIndex >= 0 ? modPoly.getAt(modIndex) : 0;
            }
          }

          var totalCodeCount = 0;

          for (var i = 0; i < rsBlocks.length; i += 1) {
            totalCodeCount += rsBlocks[i].totalCount;
          }

          var data = new Array(totalCodeCount);
          var index = 0;

          for (var i = 0; i < maxDcCount; i += 1) {
            for (var r = 0; r < rsBlocks.length; r += 1) {
              if (i < dcdata[r].length) {
                data[index] = dcdata[r][i];
                index += 1;
              }
            }
          }

          for (var i = 0; i < maxEcCount; i += 1) {
            for (var r = 0; r < rsBlocks.length; r += 1) {
              if (i < ecdata[r].length) {
                data[index] = ecdata[r][i];
                index += 1;
              }
            }
          }

          return data;
        };

        var createData = function createData(typeNumber, errorCorrectLevel, dataList) {
          var rsBlocks = QRRSBlock.getRSBlocks(typeNumber, errorCorrectLevel);
          var buffer = qrBitBuffer();

          for (var i = 0; i < dataList.length; i += 1) {
            var data = dataList[i];
            buffer.put(data.getMode(), 4);
            buffer.put(data.getLength(), QRUtil.getLengthInBits(data.getMode(), typeNumber));
            data.write(buffer);
          } // calc num max data.


          var totalDataCount = 0;

          for (var i = 0; i < rsBlocks.length; i += 1) {
            totalDataCount += rsBlocks[i].dataCount;
          }

          if (buffer.getLengthInBits() > totalDataCount * 8) {
            throw new Error('code length overflow. (' + buffer.getLengthInBits() + '>' + totalDataCount * 8 + ')');
          } // end code


          if (buffer.getLengthInBits() + 4 <= totalDataCount * 8) {
            buffer.put(0, 4);
          } // padding


          while (buffer.getLengthInBits() % 8 != 0) {
            buffer.putBit(false);
          } // padding


          while (true) {
            if (buffer.getLengthInBits() >= totalDataCount * 8) {
              break;
            }

            buffer.put(PAD0, 8);

            if (buffer.getLengthInBits() >= totalDataCount * 8) {
              break;
            }

            buffer.put(PAD1, 8);
          }

          return createBytes(buffer, rsBlocks);
        };

        _this.addData = function (data) {
          var newData = qr8BitByte(data);

          _dataList.push(newData);

          _dataCache = null;
        };

        _this.isDark = function (row, col) {
          if (row < 0 || _moduleCount <= row || col < 0 || _moduleCount <= col) {
            throw new Error(row + ',' + col);
          }

          return _modules[row][col];
        };

        _this.getModuleCount = function () {
          return _moduleCount;
        };

        _this.make = function () {
          makeImpl(false, getBestMaskPattern());
        };

        _this.createTableTag = function (cellSize, margin) {
          cellSize = cellSize || 2;
          margin = typeof margin == 'undefined' ? cellSize * 4 : margin;
          var qrHtml = '';
          qrHtml += '<table style="';
          qrHtml += ' border-width: 0px; border-style: none;';
          qrHtml += ' border-collapse: collapse;';
          qrHtml += ' padding: 0px; margin: ' + margin + 'px;';
          qrHtml += '">';
          qrHtml += '<tbody>';

          for (var r = 0; r < _this.getModuleCount(); r += 1) {
            qrHtml += '<tr>';

            for (var c = 0; c < _this.getModuleCount(); c += 1) {
              qrHtml += '<td style="';
              qrHtml += ' border-width: 0px; border-style: none;';
              qrHtml += ' border-collapse: collapse;';
              qrHtml += ' padding: 0px; margin: 0px;';
              qrHtml += ' width: ' + cellSize + 'px;';
              qrHtml += ' height: ' + cellSize + 'px;';
              qrHtml += ' background-color: ';
              qrHtml += _this.isDark(r, c) ? '#000000' : '#ffffff';
              qrHtml += ';';
              qrHtml += '"/>';
            }

            qrHtml += '</tr>';
          }

          qrHtml += '</tbody>';
          qrHtml += '</table>';
          return qrHtml;
        };

        _this.createImgTag = function (cellSize, margin) {
          cellSize = cellSize || 2;
          margin = typeof margin == 'undefined' ? cellSize * 4 : margin;
          var size = _this.getModuleCount() * cellSize + margin * 2;
          var min = margin;
          var max = size - margin;
          return createImgTag(size, size, function (x, y) {
            if (min <= x && x < max && min <= y && y < max) {
              var c = Math.floor((x - min) / cellSize);
              var r = Math.floor((y - min) / cellSize);
              return _this.isDark(r, c) ? 0 : 1;
            } else {
              return 1;
            }
          });
        };

        return _this;
      }; //---------------------------------------------------------------------
      // qrcode.stringToBytes
      //---------------------------------------------------------------------


      qrcode.stringToBytes = function (s) {
        var bytes = new Array();

        for (var i = 0; i < s.length; i += 1) {
          var c = s.charCodeAt(i);
          bytes.push(c & 0xff);
        }

        return bytes;
      }; //---------------------------------------------------------------------
      // qrcode.createStringToBytes
      //---------------------------------------------------------------------

      /**
       * @param unicodeData base64 string of byte array.
       * [16bit Unicode],[16bit Bytes], ...
       * @param numChars
       */


      qrcode.createStringToBytes = function (unicodeData, numChars) {
        // create conversion map.
        var unicodeMap = function () {
          var bin = base64DecodeInputStream(unicodeData);

          var read = function read() {
            var b = bin.read();
            if (b == -1) throw new Error();
            return b;
          };

          var count = 0;
          var unicodeMap = {};

          while (true) {
            var b0 = bin.read();
            if (b0 == -1) break;
            var b1 = read();
            var b2 = read();
            var b3 = read();
            var k = String.fromCharCode(b0 << 8 | b1);
            var v = b2 << 8 | b3;
            unicodeMap[k] = v;
            count += 1;
          }

          if (count != numChars) {
            throw new Error(count + ' != ' + numChars);
          }

          return unicodeMap;
        }();

        var unknownChar = '?'.charCodeAt(0);
        return function (s) {
          var bytes = new Array();

          for (var i = 0; i < s.length; i += 1) {
            var c = s.charCodeAt(i);

            if (c < 128) {
              bytes.push(c);
            } else {
              var b = unicodeMap[s.charAt(i)];

              if (typeof b == 'number') {
                if ((b & 0xff) == b) {
                  // 1byte
                  bytes.push(b);
                } else {
                  // 2bytes
                  bytes.push(b >>> 8);
                  bytes.push(b & 0xff);
                }
              } else {
                bytes.push(unknownChar);
              }
            }
          }

          return bytes;
        };
      }; //---------------------------------------------------------------------
      // QRMode
      //---------------------------------------------------------------------


      var QRMode = {
        MODE_NUMBER: 1 << 0,
        MODE_ALPHA_NUM: 1 << 1,
        MODE_8BIT_BYTE: 1 << 2,
        MODE_KANJI: 1 << 3
      }; //---------------------------------------------------------------------
      // QRErrorCorrectLevel
      //---------------------------------------------------------------------

      var QRErrorCorrectLevel = {
        L: 1,
        M: 0,
        Q: 3,
        H: 2
      }; //---------------------------------------------------------------------
      // QRMaskPattern
      //---------------------------------------------------------------------

      var QRMaskPattern = {
        PATTERN000: 0,
        PATTERN001: 1,
        PATTERN010: 2,
        PATTERN011: 3,
        PATTERN100: 4,
        PATTERN101: 5,
        PATTERN110: 6,
        PATTERN111: 7
      }; //---------------------------------------------------------------------
      // QRUtil
      //---------------------------------------------------------------------

      var QRUtil = function () {
        var PATTERN_POSITION_TABLE = [[], [6, 18], [6, 22], [6, 26], [6, 30], [6, 34], [6, 22, 38], [6, 24, 42], [6, 26, 46], [6, 28, 50], [6, 30, 54], [6, 32, 58], [6, 34, 62], [6, 26, 46, 66], [6, 26, 48, 70], [6, 26, 50, 74], [6, 30, 54, 78], [6, 30, 56, 82], [6, 30, 58, 86], [6, 34, 62, 90], [6, 28, 50, 72, 94], [6, 26, 50, 74, 98], [6, 30, 54, 78, 102], [6, 28, 54, 80, 106], [6, 32, 58, 84, 110], [6, 30, 58, 86, 114], [6, 34, 62, 90, 118], [6, 26, 50, 74, 98, 122], [6, 30, 54, 78, 102, 126], [6, 26, 52, 78, 104, 130], [6, 30, 56, 82, 108, 134], [6, 34, 60, 86, 112, 138], [6, 30, 58, 86, 114, 142], [6, 34, 62, 90, 118, 146], [6, 30, 54, 78, 102, 126, 150], [6, 24, 50, 76, 102, 128, 154], [6, 28, 54, 80, 106, 132, 158], [6, 32, 58, 84, 110, 136, 162], [6, 26, 54, 82, 110, 138, 166], [6, 30, 58, 86, 114, 142, 170]];
        var G15 = 1 << 10 | 1 << 8 | 1 << 5 | 1 << 4 | 1 << 2 | 1 << 1 | 1 << 0;
        var G18 = 1 << 12 | 1 << 11 | 1 << 10 | 1 << 9 | 1 << 8 | 1 << 5 | 1 << 2 | 1 << 0;
        var G15_MASK = 1 << 14 | 1 << 12 | 1 << 10 | 1 << 4 | 1 << 1;
        var _this = {};

        var getBCHDigit = function getBCHDigit(data) {
          var digit = 0;

          while (data != 0) {
            digit += 1;
            data >>>= 1;
          }

          return digit;
        };

        _this.getBCHTypeInfo = function (data) {
          var d = data << 10;

          while (getBCHDigit(d) - getBCHDigit(G15) >= 0) {
            d ^= G15 << getBCHDigit(d) - getBCHDigit(G15);
          }

          return (data << 10 | d) ^ G15_MASK;
        };

        _this.getBCHTypeNumber = function (data) {
          var d = data << 12;

          while (getBCHDigit(d) - getBCHDigit(G18) >= 0) {
            d ^= G18 << getBCHDigit(d) - getBCHDigit(G18);
          }

          return data << 12 | d;
        };

        _this.getPatternPosition = function (typeNumber) {
          return PATTERN_POSITION_TABLE[typeNumber - 1];
        };

        _this.getMaskFunction = function (maskPattern) {
          switch (maskPattern) {
            case QRMaskPattern.PATTERN000:
              return function (i, j) {
                return (i + j) % 2 == 0;
              };

            case QRMaskPattern.PATTERN001:
              return function (i, j) {
                return i % 2 == 0;
              };

            case QRMaskPattern.PATTERN010:
              return function (i, j) {
                return j % 3 == 0;
              };

            case QRMaskPattern.PATTERN011:
              return function (i, j) {
                return (i + j) % 3 == 0;
              };

            case QRMaskPattern.PATTERN100:
              return function (i, j) {
                return (Math.floor(i / 2) + Math.floor(j / 3)) % 2 == 0;
              };

            case QRMaskPattern.PATTERN101:
              return function (i, j) {
                return i * j % 2 + i * j % 3 == 0;
              };

            case QRMaskPattern.PATTERN110:
              return function (i, j) {
                return (i * j % 2 + i * j % 3) % 2 == 0;
              };

            case QRMaskPattern.PATTERN111:
              return function (i, j) {
                return (i * j % 3 + (i + j) % 2) % 2 == 0;
              };

            default:
              throw new Error('bad maskPattern:' + maskPattern);
          }
        };

        _this.getErrorCorrectPolynomial = function (errorCorrectLength) {
          var a = qrPolynomial([1], 0);

          for (var i = 0; i < errorCorrectLength; i += 1) {
            a = a.multiply(qrPolynomial([1, QRMath.gexp(i)], 0));
          }

          return a;
        };

        _this.getLengthInBits = function (mode, type) {
          if (1 <= type && type < 10) {
            // 1 - 9
            switch (mode) {
              case QRMode.MODE_NUMBER:
                return 10;

              case QRMode.MODE_ALPHA_NUM:
                return 9;

              case QRMode.MODE_8BIT_BYTE:
                return 8;

              case QRMode.MODE_KANJI:
                return 8;

              default:
                throw new Error('mode:' + mode);
            }
          } else if (type < 27) {
            // 10 - 26
            switch (mode) {
              case QRMode.MODE_NUMBER:
                return 12;

              case QRMode.MODE_ALPHA_NUM:
                return 11;

              case QRMode.MODE_8BIT_BYTE:
                return 16;

              case QRMode.MODE_KANJI:
                return 10;

              default:
                throw new Error('mode:' + mode);
            }
          } else if (type < 41) {
            // 27 - 40
            switch (mode) {
              case QRMode.MODE_NUMBER:
                return 14;

              case QRMode.MODE_ALPHA_NUM:
                return 13;

              case QRMode.MODE_8BIT_BYTE:
                return 16;

              case QRMode.MODE_KANJI:
                return 12;

              default:
                throw new Error('mode:' + mode);
            }
          } else {
            throw new Error('type:' + type);
          }
        };

        _this.getLostPoint = function (qrcode) {
          var moduleCount = qrcode.getModuleCount();
          var lostPoint = 0; // LEVEL1

          for (var row = 0; row < moduleCount; row += 1) {
            for (var col = 0; col < moduleCount; col += 1) {
              var sameCount = 0;
              var dark = qrcode.isDark(row, col);

              for (var r = -1; r <= 1; r += 1) {
                if (row + r < 0 || moduleCount <= row + r) {
                  continue;
                }

                for (var c = -1; c <= 1; c += 1) {
                  if (col + c < 0 || moduleCount <= col + c) {
                    continue;
                  }

                  if (r == 0 && c == 0) {
                    continue;
                  }

                  if (dark == qrcode.isDark(row + r, col + c)) {
                    sameCount += 1;
                  }
                }
              }

              if (sameCount > 5) {
                lostPoint += 3 + sameCount - 5;
              }
            }
          }

          for (var row = 0; row < moduleCount - 1; row += 1) {
            for (var col = 0; col < moduleCount - 1; col += 1) {
              var count = 0;
              if (qrcode.isDark(row, col)) count += 1;
              if (qrcode.isDark(row + 1, col)) count += 1;
              if (qrcode.isDark(row, col + 1)) count += 1;
              if (qrcode.isDark(row + 1, col + 1)) count += 1;

              if (count == 0 || count == 4) {
                lostPoint += 3;
              }
            }
          } // LEVEL3


          for (var row = 0; row < moduleCount; row += 1) {
            for (var col = 0; col < moduleCount - 6; col += 1) {
              if (qrcode.isDark(row, col) && !qrcode.isDark(row, col + 1) && qrcode.isDark(row, col + 2) && qrcode.isDark(row, col + 3) && qrcode.isDark(row, col + 4) && !qrcode.isDark(row, col + 5) && qrcode.isDark(row, col + 6)) {
                lostPoint += 40;
              }
            }
          }

          for (var col = 0; col < moduleCount; col += 1) {
            for (var row = 0; row < moduleCount - 6; row += 1) {
              if (qrcode.isDark(row, col) && !qrcode.isDark(row + 1, col) && qrcode.isDark(row + 2, col) && qrcode.isDark(row + 3, col) && qrcode.isDark(row + 4, col) && !qrcode.isDark(row + 5, col) && qrcode.isDark(row + 6, col)) {
                lostPoint += 40;
              }
            }
          } // LEVEL4


          var darkCount = 0;

          for (var col = 0; col < moduleCount; col += 1) {
            for (var row = 0; row < moduleCount; row += 1) {
              if (qrcode.isDark(row, col)) {
                darkCount += 1;
              }
            }
          }

          var ratio = Math.abs(100 * darkCount / moduleCount / moduleCount - 50) / 5;
          lostPoint += ratio * 10;
          return lostPoint;
        };

        return _this;
      }(); //---------------------------------------------------------------------
      // QRMath
      //---------------------------------------------------------------------


      var QRMath = function () {
        var EXP_TABLE = new Array(256);
        var LOG_TABLE = new Array(256); // initialize tables

        for (var i = 0; i < 8; i += 1) {
          EXP_TABLE[i] = 1 << i;
        }

        for (var i = 8; i < 256; i += 1) {
          EXP_TABLE[i] = EXP_TABLE[i - 4] ^ EXP_TABLE[i - 5] ^ EXP_TABLE[i - 6] ^ EXP_TABLE[i - 8];
        }

        for (var i = 0; i < 255; i += 1) {
          LOG_TABLE[EXP_TABLE[i]] = i;
        }

        var _this = {};

        _this.glog = function (n) {
          if (n < 1) {
            throw new Error('glog(' + n + ')');
          }

          return LOG_TABLE[n];
        };

        _this.gexp = function (n) {
          while (n < 0) {
            n += 255;
          }

          while (n >= 256) {
            n -= 255;
          }

          return EXP_TABLE[n];
        };

        return _this;
      }(); //---------------------------------------------------------------------
      // qrPolynomial
      //---------------------------------------------------------------------


      function qrPolynomial(num, shift) {
        if (typeof num.length == 'undefined') {
          throw new Error(num.length + '/' + shift);
        }

        var _num = function () {
          var offset = 0;

          while (offset < num.length && num[offset] == 0) {
            offset += 1;
          }

          var _num = new Array(num.length - offset + shift);

          for (var i = 0; i < num.length - offset; i += 1) {
            _num[i] = num[i + offset];
          }

          return _num;
        }();

        var _this = {};

        _this.getAt = function (index) {
          return _num[index];
        };

        _this.getLength = function () {
          return _num.length;
        };

        _this.multiply = function (e) {
          var num = new Array(_this.getLength() + e.getLength() - 1);

          for (var i = 0; i < _this.getLength(); i += 1) {
            for (var j = 0; j < e.getLength(); j += 1) {
              num[i + j] ^= QRMath.gexp(QRMath.glog(_this.getAt(i)) + QRMath.glog(e.getAt(j)));
            }
          }

          return qrPolynomial(num, 0);
        };

        _this.mod = function (e) {
          if (_this.getLength() - e.getLength() < 0) {
            return _this;
          }

          var ratio = QRMath.glog(_this.getAt(0)) - QRMath.glog(e.getAt(0));
          var num = new Array(_this.getLength());

          for (var i = 0; i < _this.getLength(); i += 1) {
            num[i] = _this.getAt(i);
          }

          for (var i = 0; i < e.getLength(); i += 1) {
            num[i] ^= QRMath.gexp(QRMath.glog(e.getAt(i)) + ratio);
          } // recursive call


          return qrPolynomial(num, 0).mod(e);
        };

        return _this;
      }
      // QRRSBlock
      //---------------------------------------------------------------------

      var QRRSBlock = function () {
        var RS_BLOCK_TABLE = [// L
        // M
        // Q
        // H
        // 1
        [1, 26, 19], [1, 26, 16], [1, 26, 13], [1, 26, 9], // 2
        [1, 44, 34], [1, 44, 28], [1, 44, 22], [1, 44, 16], // 3
        [1, 70, 55], [1, 70, 44], [2, 35, 17], [2, 35, 13], // 4
        [1, 100, 80], [2, 50, 32], [2, 50, 24], [4, 25, 9], // 5
        [1, 134, 108], [2, 67, 43], [2, 33, 15, 2, 34, 16], [2, 33, 11, 2, 34, 12], // 6
        [2, 86, 68], [4, 43, 27], [4, 43, 19], [4, 43, 15], // 7
        [2, 98, 78], [4, 49, 31], [2, 32, 14, 4, 33, 15], [4, 39, 13, 1, 40, 14], // 8
        [2, 121, 97], [2, 60, 38, 2, 61, 39], [4, 40, 18, 2, 41, 19], [4, 40, 14, 2, 41, 15], // 9
        [2, 146, 116], [3, 58, 36, 2, 59, 37], [4, 36, 16, 4, 37, 17], [4, 36, 12, 4, 37, 13], // 10
        [2, 86, 68, 2, 87, 69], [4, 69, 43, 1, 70, 44], [6, 43, 19, 2, 44, 20], [6, 43, 15, 2, 44, 16], // 11
        [4, 101, 81], [1, 80, 50, 4, 81, 51], [4, 50, 22, 4, 51, 23], [3, 36, 12, 8, 37, 13], // 12
        [2, 116, 92, 2, 117, 93], [6, 58, 36, 2, 59, 37], [4, 46, 20, 6, 47, 21], [7, 42, 14, 4, 43, 15], // 13
        [4, 133, 107], [8, 59, 37, 1, 60, 38], [8, 44, 20, 4, 45, 21], [12, 33, 11, 4, 34, 12], // 14
        [3, 145, 115, 1, 146, 116], [4, 64, 40, 5, 65, 41], [11, 36, 16, 5, 37, 17], [11, 36, 12, 5, 37, 13], // 15
        [5, 109, 87, 1, 110, 88], [5, 65, 41, 5, 66, 42], [5, 54, 24, 7, 55, 25], [11, 36, 12, 7, 37, 13], // 16
        [5, 122, 98, 1, 123, 99], [7, 73, 45, 3, 74, 46], [15, 43, 19, 2, 44, 20], [3, 45, 15, 13, 46, 16], // 17
        [1, 135, 107, 5, 136, 108], [10, 74, 46, 1, 75, 47], [1, 50, 22, 15, 51, 23], [2, 42, 14, 17, 43, 15], // 18
        [5, 150, 120, 1, 151, 121], [9, 69, 43, 4, 70, 44], [17, 50, 22, 1, 51, 23], [2, 42, 14, 19, 43, 15], // 19
        [3, 141, 113, 4, 142, 114], [3, 70, 44, 11, 71, 45], [17, 47, 21, 4, 48, 22], [9, 39, 13, 16, 40, 14], // 20
        [3, 135, 107, 5, 136, 108], [3, 67, 41, 13, 68, 42], [15, 54, 24, 5, 55, 25], [15, 43, 15, 10, 44, 16], // 21
        [4, 144, 116, 4, 145, 117], [17, 68, 42], [17, 50, 22, 6, 51, 23], [19, 46, 16, 6, 47, 17], // 22
        [2, 139, 111, 7, 140, 112], [17, 74, 46], [7, 54, 24, 16, 55, 25], [34, 37, 13], // 23
        [4, 151, 121, 5, 152, 122], [4, 75, 47, 14, 76, 48], [11, 54, 24, 14, 55, 25], [16, 45, 15, 14, 46, 16], // 24
        [6, 147, 117, 4, 148, 118], [6, 73, 45, 14, 74, 46], [11, 54, 24, 16, 55, 25], [30, 46, 16, 2, 47, 17], // 25
        [8, 132, 106, 4, 133, 107], [8, 75, 47, 13, 76, 48], [7, 54, 24, 22, 55, 25], [22, 45, 15, 13, 46, 16], // 26
        [10, 142, 114, 2, 143, 115], [19, 74, 46, 4, 75, 47], [28, 50, 22, 6, 51, 23], [33, 46, 16, 4, 47, 17], // 27
        [8, 152, 122, 4, 153, 123], [22, 73, 45, 3, 74, 46], [8, 53, 23, 26, 54, 24], [12, 45, 15, 28, 46, 16], // 28
        [3, 147, 117, 10, 148, 118], [3, 73, 45, 23, 74, 46], [4, 54, 24, 31, 55, 25], [11, 45, 15, 31, 46, 16], // 29
        [7, 146, 116, 7, 147, 117], [21, 73, 45, 7, 74, 46], [1, 53, 23, 37, 54, 24], [19, 45, 15, 26, 46, 16], // 30
        [5, 145, 115, 10, 146, 116], [19, 75, 47, 10, 76, 48], [15, 54, 24, 25, 55, 25], [23, 45, 15, 25, 46, 16], // 31
        [13, 145, 115, 3, 146, 116], [2, 74, 46, 29, 75, 47], [42, 54, 24, 1, 55, 25], [23, 45, 15, 28, 46, 16], // 32
        [17, 145, 115], [10, 74, 46, 23, 75, 47], [10, 54, 24, 35, 55, 25], [19, 45, 15, 35, 46, 16], // 33
        [17, 145, 115, 1, 146, 116], [14, 74, 46, 21, 75, 47], [29, 54, 24, 19, 55, 25], [11, 45, 15, 46, 46, 16], // 34
        [13, 145, 115, 6, 146, 116], [14, 74, 46, 23, 75, 47], [44, 54, 24, 7, 55, 25], [59, 46, 16, 1, 47, 17], // 35
        [12, 151, 121, 7, 152, 122], [12, 75, 47, 26, 76, 48], [39, 54, 24, 14, 55, 25], [22, 45, 15, 41, 46, 16], // 36
        [6, 151, 121, 14, 152, 122], [6, 75, 47, 34, 76, 48], [46, 54, 24, 10, 55, 25], [2, 45, 15, 64, 46, 16], // 37
        [17, 152, 122, 4, 153, 123], [29, 74, 46, 14, 75, 47], [49, 54, 24, 10, 55, 25], [24, 45, 15, 46, 46, 16], // 38
        [4, 152, 122, 18, 153, 123], [13, 74, 46, 32, 75, 47], [48, 54, 24, 14, 55, 25], [42, 45, 15, 32, 46, 16], // 39
        [20, 147, 117, 4, 148, 118], [40, 75, 47, 7, 76, 48], [43, 54, 24, 22, 55, 25], [10, 45, 15, 67, 46, 16], // 40
        [19, 148, 118, 6, 149, 119], [18, 75, 47, 31, 76, 48], [34, 54, 24, 34, 55, 25], [20, 45, 15, 61, 46, 16]];

        var qrRSBlock = function qrRSBlock(totalCount, dataCount) {
          var _this = {};
          _this.totalCount = totalCount;
          _this.dataCount = dataCount;
          return _this;
        };

        var _this = {};

        var getRsBlockTable = function getRsBlockTable(typeNumber, errorCorrectLevel) {
          switch (errorCorrectLevel) {
            case QRErrorCorrectLevel.L:
              return RS_BLOCK_TABLE[(typeNumber - 1) * 4 + 0];

            case QRErrorCorrectLevel.M:
              return RS_BLOCK_TABLE[(typeNumber - 1) * 4 + 1];

            case QRErrorCorrectLevel.Q:
              return RS_BLOCK_TABLE[(typeNumber - 1) * 4 + 2];

            case QRErrorCorrectLevel.H:
              return RS_BLOCK_TABLE[(typeNumber - 1) * 4 + 3];

            default:
              return undefined;
          }
        };

        _this.getRSBlocks = function (typeNumber, errorCorrectLevel) {
          var rsBlock = getRsBlockTable(typeNumber, errorCorrectLevel);

          if (typeof rsBlock == 'undefined') {
            throw new Error('bad rs block @ typeNumber:' + typeNumber + '/errorCorrectLevel:' + errorCorrectLevel);
          }

          var length = rsBlock.length / 3;
          var list = new Array();

          for (var i = 0; i < length; i += 1) {
            var count = rsBlock[i * 3 + 0];
            var totalCount = rsBlock[i * 3 + 1];
            var dataCount = rsBlock[i * 3 + 2];

            for (var j = 0; j < count; j += 1) {
              list.push(qrRSBlock(totalCount, dataCount));
            }
          }

          return list;
        };

        return _this;
      }(); //---------------------------------------------------------------------
      // qrBitBuffer
      //---------------------------------------------------------------------


      var qrBitBuffer = function qrBitBuffer() {
        var _buffer = new Array();

        var _length = 0;
        var _this = {};

        _this.getBuffer = function () {
          return _buffer;
        };

        _this.getAt = function (index) {
          var bufIndex = Math.floor(index / 8);
          return (_buffer[bufIndex] >>> 7 - index % 8 & 1) == 1;
        };

        _this.put = function (num, length) {
          for (var i = 0; i < length; i += 1) {
            _this.putBit((num >>> length - i - 1 & 1) == 1);
          }
        };

        _this.getLengthInBits = function () {
          return _length;
        };

        _this.putBit = function (bit) {
          var bufIndex = Math.floor(_length / 8);

          if (_buffer.length <= bufIndex) {
            _buffer.push(0);
          }

          if (bit) {
            _buffer[bufIndex] |= 0x80 >>> _length % 8;
          }

          _length += 1;
        };

        return _this;
      }; //---------------------------------------------------------------------
      // qr8BitByte
      //---------------------------------------------------------------------


      var qr8BitByte = function qr8BitByte(data) {
        var _mode = QRMode.MODE_8BIT_BYTE;

        var _bytes = qrcode.stringToBytes(data);

        var _this = {};

        _this.getMode = function () {
          return _mode;
        };

        _this.getLength = function (buffer) {
          return _bytes.length;
        };

        _this.write = function (buffer) {
          for (var i = 0; i < _bytes.length; i += 1) {
            buffer.put(_bytes[i], 8);
          }
        };

        return _this;
      }; //=====================================================================
      // GIF Support etc.
      //
      //---------------------------------------------------------------------
      // byteArrayOutputStream
      //---------------------------------------------------------------------


      var byteArrayOutputStream = function byteArrayOutputStream() {
        var _bytes = new Array();

        var _this = {};

        _this.writeByte = function (b) {
          _bytes.push(b & 0xff);
        };

        _this.writeShort = function (i) {
          _this.writeByte(i);

          _this.writeByte(i >>> 8);
        };

        _this.writeBytes = function (b, off, len) {
          off = off || 0;
          len = len || b.length;

          for (var i = 0; i < len; i += 1) {
            _this.writeByte(b[i + off]);
          }
        };

        _this.writeString = function (s) {
          for (var i = 0; i < s.length; i += 1) {
            _this.writeByte(s.charCodeAt(i));
          }
        };

        _this.toByteArray = function () {
          return _bytes;
        };

        _this.toString = function () {
          var s = '';
          s += '[';

          for (var i = 0; i < _bytes.length; i += 1) {
            if (i > 0) {
              s += ',';
            }

            s += _bytes[i];
          }

          s += ']';
          return s;
        };

        return _this;
      }; //---------------------------------------------------------------------
      // base64EncodeOutputStream
      //---------------------------------------------------------------------


      var base64EncodeOutputStream = function base64EncodeOutputStream() {
        var _buffer = 0;
        var _buflen = 0;
        var _length = 0;
        var _base64 = '';
        var _this = {};

        var writeEncoded = function writeEncoded(b) {
          _base64 += String.fromCharCode(encode(b & 0x3f));
        };

        var encode = function encode(n) {
          if (n < 0) ; else if (n < 26) {
            return 0x41 + n;
          } else if (n < 52) {
            return 0x61 + (n - 26);
          } else if (n < 62) {
            return 0x30 + (n - 52);
          } else if (n == 62) {
            return 0x2b;
          } else if (n == 63) {
            return 0x2f;
          }

          throw new Error('n:' + n);
        };

        _this.writeByte = function (n) {
          _buffer = _buffer << 8 | n & 0xff;
          _buflen += 8;
          _length += 1;

          while (_buflen >= 6) {
            writeEncoded(_buffer >>> _buflen - 6);
            _buflen -= 6;
          }
        };

        _this.flush = function () {
          if (_buflen > 0) {
            writeEncoded(_buffer << 6 - _buflen);
            _buffer = 0;
            _buflen = 0;
          }

          if (_length % 3 != 0) {
            // padding
            var padlen = 3 - _length % 3;

            for (var i = 0; i < padlen; i += 1) {
              _base64 += '=';
            }
          }
        };

        _this.toString = function () {
          return _base64;
        };

        return _this;
      }; //---------------------------------------------------------------------
      // base64DecodeInputStream
      //---------------------------------------------------------------------


      var base64DecodeInputStream = function base64DecodeInputStream(str) {
        var _str = str;
        var _pos = 0;
        var _buffer = 0;
        var _buflen = 0;
        var _this = {};

        _this.read = function () {
          while (_buflen < 8) {
            if (_pos >= _str.length) {
              if (_buflen == 0) {
                return -1;
              }

              throw new Error('unexpected end of file./' + _buflen);
            }

            var c = _str.charAt(_pos);

            _pos += 1;

            if (c == '=') {
              _buflen = 0;
              return -1;
            } else if (c.match(/^\s$/)) {
              // ignore if whitespace.
              continue;
            }

            _buffer = _buffer << 6 | decode(c.charCodeAt(0));
            _buflen += 6;
          }

          var n = _buffer >>> _buflen - 8 & 0xff;
          _buflen -= 8;
          return n;
        };

        var decode = function decode(c) {
          if (0x41 <= c && c <= 0x5a) {
            return c - 0x41;
          } else if (0x61 <= c && c <= 0x7a) {
            return c - 0x61 + 26;
          } else if (0x30 <= c && c <= 0x39) {
            return c - 0x30 + 52;
          } else if (c == 0x2b) {
            return 62;
          } else if (c == 0x2f) {
            return 63;
          } else {
            throw new Error('c:' + c);
          }
        };

        return _this;
      }; //---------------------------------------------------------------------
      // gifImage (B/W)
      //---------------------------------------------------------------------


      var gifImage = function gifImage(width, height) {
        var _width = width;
        var _height = height;

        var _data = new Array(width * height);

        var _this = {};

        _this.setPixel = function (x, y, pixel) {
          _data[y * _width + x] = pixel;
        };

        _this.write = function (out) {
          //---------------------------------
          // GIF Signature
          out.writeString('GIF87a'); //---------------------------------
          // Screen Descriptor

          out.writeShort(_width);
          out.writeShort(_height);
          out.writeByte(0x80); // 2bit

          out.writeByte(0);
          out.writeByte(0); //---------------------------------
          // Global Color Map
          // black

          out.writeByte(0x00);
          out.writeByte(0x00);
          out.writeByte(0x00); // white

          out.writeByte(0xff);
          out.writeByte(0xff);
          out.writeByte(0xff); //---------------------------------
          // Image Descriptor

          out.writeString(',');
          out.writeShort(0);
          out.writeShort(0);
          out.writeShort(_width);
          out.writeShort(_height);
          out.writeByte(0); //---------------------------------
          // Local Color Map
          //---------------------------------
          // Raster Data

          var lzwMinCodeSize = 2;
          var raster = getLZWRaster(lzwMinCodeSize);
          out.writeByte(lzwMinCodeSize);
          var offset = 0;

          while (raster.length - offset > 255) {
            out.writeByte(255);
            out.writeBytes(raster, offset, 255);
            offset += 255;
          }

          out.writeByte(raster.length - offset);
          out.writeBytes(raster, offset, raster.length - offset);
          out.writeByte(0x00); //---------------------------------
          // GIF Terminator

          out.writeString(';');
        };

        var bitOutputStream = function bitOutputStream(out) {
          var _out = out;
          var _bitLength = 0;
          var _bitBuffer = 0;
          var _this = {};

          _this.write = function (data, length) {
            if (data >>> length != 0) {
              throw new Error('length over');
            }

            while (_bitLength + length >= 8) {
              _out.writeByte(0xff & (data << _bitLength | _bitBuffer));

              length -= 8 - _bitLength;
              data >>>= 8 - _bitLength;
              _bitBuffer = 0;
              _bitLength = 0;
            }

            _bitBuffer = data << _bitLength | _bitBuffer;
            _bitLength = _bitLength + length;
          };

          _this.flush = function () {
            if (_bitLength > 0) {
              _out.writeByte(_bitBuffer);
            }
          };

          return _this;
        };

        var getLZWRaster = function getLZWRaster(lzwMinCodeSize) {
          var clearCode = 1 << lzwMinCodeSize;
          var endCode = (1 << lzwMinCodeSize) + 1;
          var bitLength = lzwMinCodeSize + 1; // Setup LZWTable

          var table = lzwTable();

          for (var i = 0; i < clearCode; i += 1) {
            table.add(String.fromCharCode(i));
          }

          table.add(String.fromCharCode(clearCode));
          table.add(String.fromCharCode(endCode));
          var byteOut = byteArrayOutputStream();
          var bitOut = bitOutputStream(byteOut); // clear code

          bitOut.write(clearCode, bitLength);
          var dataIndex = 0;
          var s = String.fromCharCode(_data[dataIndex]);
          dataIndex += 1;

          while (dataIndex < _data.length) {
            var c = String.fromCharCode(_data[dataIndex]);
            dataIndex += 1;

            if (table.contains(s + c)) {
              s = s + c;
            } else {
              bitOut.write(table.indexOf(s), bitLength);

              if (table.size() < 0xfff) {
                if (table.size() == 1 << bitLength) {
                  bitLength += 1;
                }

                table.add(s + c);
              }

              s = c;
            }
          }

          bitOut.write(table.indexOf(s), bitLength); // end code

          bitOut.write(endCode, bitLength);
          bitOut.flush();
          return byteOut.toByteArray();
        };

        var lzwTable = function lzwTable() {
          var _map = {};
          var _size = 0;
          var _this = {};

          _this.add = function (key) {
            if (_this.contains(key)) {
              throw new Error('dup key:' + key);
            }

            _map[key] = _size;
            _size += 1;
          };

          _this.size = function () {
            return _size;
          };

          _this.indexOf = function (key) {
            return _map[key];
          };

          _this.contains = function (key) {
            return typeof _map[key] != 'undefined';
          };

          return _this;
        };

        return _this;
      };

      var createImgTag = function createImgTag(width, height, getPixel, alt) {
        var gif = gifImage(width, height);

        for (var y = 0; y < height; y += 1) {
          for (var x = 0; x < width; x += 1) {
            gif.setPixel(x, y, getPixel(x, y));
          }
        }

        var b = byteArrayOutputStream();
        gif.write(b);
        var base64 = base64EncodeOutputStream();
        var bytes = b.toByteArray();

        for (var i = 0; i < bytes.length; i += 1) {
          base64.writeByte(bytes[i]);
        }

        base64.flush();
        var img = '';
        img += '<img';
        img += " src=\"";
        img += 'data:image/gif;base64,';
        img += base64;
        img += '"';
        img += " width=\"";
        img += width;
        img += '"';
        img += " height=\"";
        img += height;
        img += '"';

        if (alt) {
          img += " alt=\"";
          img += alt;
          img += '"';
        }

        img += '/>';
        return img;
      }; //---------------------------------------------------------------------
      // returns qrcode function.


      return qrcode;
    }();

    (function (factory) {
      if (typeof define === 'function' && define.amd) {
        define([], factory);
      } else if (typeof exports === 'object') {
        module.exports = factory();
      }
    })(function () {
      return qrcode;
    }); //---------------------------------------------------------------------
    //
    // QR Code Generator for JavaScript UTF8 Support (optional)
    //
    // Copyright (c) 2011 Kazuhiko Arase
    //
    // URL: http://www.d-project.com/
    //
    // Licensed under the MIT license:
    //  http://www.opensource.org/licenses/mit-license.php
    //
    // The word 'QR Code' is registered trademark of
    // DENSO WAVE INCORPORATED
    //  http://www.denso-wave.com/qrcode/faqpatent-e.html
    //
    //---------------------------------------------------------------------


    !function (qrcode) {
      //---------------------------------------------------------------------
      // overwrite qrcode.stringToBytes
      //---------------------------------------------------------------------
      qrcode.stringToBytes = function (s) {
        // http://stackoverflow.com/questions/18729405/how-to-convert-utf8-string-to-byte-array
        function toUTF8Array(str) {
          var utf8 = [];

          for (var i = 0; i < str.length; i++) {
            var charcode = str.charCodeAt(i);
            if (charcode < 0x80) utf8.push(charcode);else if (charcode < 0x800) {
              utf8.push(0xc0 | charcode >> 6, 0x80 | charcode & 0x3f);
            } else if (charcode < 0xd800 || charcode >= 0xe000) {
              utf8.push(0xe0 | charcode >> 12, 0x80 | charcode >> 6 & 0x3f, 0x80 | charcode & 0x3f);
            } // surrogate pair
            else {
                i++; // UTF-16 encodes 0x10000-0x10FFFF by
                // subtracting 0x10000 and splitting the
                // 20 bits of 0x0-0xFFFFF into two halves

                charcode = 0x10000 + ((charcode & 0x3ff) << 10 | str.charCodeAt(i) & 0x3ff);
                utf8.push(0xf0 | charcode >> 18, 0x80 | charcode >> 12 & 0x3f, 0x80 | charcode >> 6 & 0x3f, 0x80 | charcode & 0x3f);
              }
          }

          return utf8;
        }

        return toUTF8Array(s);
      };
    }(qrcode);
    return qrcode; // eslint-disable-line no-undef
  }());

  /*!
   * Fuel UX v3.17.0 
   * Copyright 2012-2018 ExactTarget
   * Licensed under the BSD-3-Clause license (https://github.com/ExactTarget/fuelux/blob/master/LICENSE)
   */
  // For more information on UMD visit: https://github.com/umdjs/umd/
  (function (factory) {
    if (typeof define === 'function' && define.amd) {
      define(['jquery', 'bootstrap'], factory);
    } else {
      factory(jQuery);
    }
  })(function (jQuery) {
    if (typeof jQuery === 'undefined') {
      throw new Error('Fuel UX\'s JavaScript requires jQuery');
    }

    if (typeof jQuery.fn.dropdown === 'undefined' || typeof jQuery.fn.collapse === 'undefined') {
      throw new Error('Fuel UX\'s JavaScript requires Bootstrap');
    }

    (function ($$$1) {
      /* global jQuery:true */

      /*
       * Fuel UX Checkbox
       * https://github.com/ExactTarget/fuelux
       *
       * Copyright (c) 2014 ExactTarget
       * Licensed under the BSD New license.
       */
      // -- BEGIN MODULE CODE HERE --
      var old = $$$1.fn.checkbox; // CHECKBOX CONSTRUCTOR AND PROTOTYPE

      var logError = function logError(error) {
        if (window && window.console && window.console.error) {
          window.console.error(error);
        }
      };

      var Checkbox = function Checkbox(element, options) {
        this.options = $$$1.extend({}, $$$1.fn.checkbox.defaults, options);
        var $element = $$$1(element);

        if (element.tagName.toLowerCase() !== 'label') {
          logError('Checkbox must be initialized on the `label` that wraps the `input` element. See https://github.com/ExactTarget/fuelux/blob/master/reference/markup/checkbox.html for example of proper markup. Call `.checkbox()` on the `<label>` not the `<input>`');
          return;
        } // cache elements


        this.$label = $element;
        this.$chk = this.$label.find('input[type="checkbox"]');
        this.$container = $element.parent('.checkbox'); // the container div

        if (!this.options.ignoreVisibilityCheck && this.$chk.css('visibility').match(/hidden|collapse/)) {
          logError('For accessibility reasons, in order for tab and space to function on checkbox, checkbox `<input />`\'s `visibility` must not be set to `hidden` or `collapse`. See https://github.com/ExactTarget/fuelux/pull/1996 for more details.');
        } // determine if a toggle container is specified


        var containerSelector = this.$chk.attr('data-toggle');
        this.$toggleContainer = $$$1(containerSelector); // handle internal events

        this.$chk.on('change', $$$1.proxy(this.itemchecked, this)); // set default state

        this.setInitialState();
      };

      Checkbox.prototype = {
        constructor: Checkbox,
        setInitialState: function setInitialState() {
          var $chk = this.$chk; // get current state of input

          var checked = $chk.prop('checked');
          var disabled = $chk.prop('disabled'); // sync label class with input state

          this.setCheckedState($chk, checked);
          this.setDisabledState($chk, disabled);
        },
        setCheckedState: function setCheckedState(element, checked) {
          var $chk = element;
          var $lbl = this.$label;
          var $containerToggle = this.$toggleContainer;

          if (checked) {
            $chk.prop('checked', true);
            $lbl.addClass('checked');
            $containerToggle.removeClass('hide hidden');
            $lbl.trigger('checked.fu.checkbox');
          } else {
            $chk.prop('checked', false);
            $lbl.removeClass('checked');
            $containerToggle.addClass('hidden');
            $lbl.trigger('unchecked.fu.checkbox');
          }

          $lbl.trigger('changed.fu.checkbox', checked);
        },
        setDisabledState: function setDisabledState(element, disabled) {
          var $chk = $$$1(element);
          var $lbl = this.$label;

          if (disabled) {
            $chk.prop('disabled', true);
            $lbl.addClass('disabled');
            $lbl.trigger('disabled.fu.checkbox');
          } else {
            $chk.prop('disabled', false);
            $lbl.removeClass('disabled');
            $lbl.trigger('enabled.fu.checkbox');
          }

          return $chk;
        },
        itemchecked: function itemchecked(evt) {
          var $chk = $$$1(evt.target);
          var checked = $chk.prop('checked');
          this.setCheckedState($chk, checked);
        },
        toggle: function toggle() {
          var checked = this.isChecked();

          if (checked) {
            this.uncheck();
          } else {
            this.check();
          }
        },
        check: function check() {
          this.setCheckedState(this.$chk, true);
        },
        uncheck: function uncheck() {
          this.setCheckedState(this.$chk, false);
        },
        isChecked: function isChecked() {
          var checked = this.$chk.prop('checked');
          return checked;
        },
        enable: function enable() {
          this.setDisabledState(this.$chk, false);
        },
        disable: function disable() {
          this.setDisabledState(this.$chk, true);
        },
        destroy: function destroy() {
          this.$label.remove();
          return this.$label[0].outerHTML;
        }
      };
      Checkbox.prototype.getValue = Checkbox.prototype.isChecked; // CHECKBOX PLUGIN DEFINITION

      $$$1.fn.checkbox = function checkbox(option) {
        var args = Array.prototype.slice.call(arguments, 1);
        var methodReturn;
        var $set = this.each(function applyData() {
          var $this = $$$1(this);
          var data = $this.data('fu.checkbox');
          var options = typeof option === 'object' && option;

          if (!data) {
            $this.data('fu.checkbox', data = new Checkbox(this, options));
          }

          if (typeof option === 'string') {
            methodReturn = data[option].apply(data, args);
          }
        });
        return methodReturn === undefined ? $set : methodReturn;
      };

      $$$1.fn.checkbox.defaults = {
        ignoreVisibilityCheck: false
      };
      $$$1.fn.checkbox.Constructor = Checkbox;

      $$$1.fn.checkbox.noConflict = function noConflict() {
        $$$1.fn.checkbox = old;
        return this;
      }; // DATA-API


      $$$1(document).on('mouseover.fu.checkbox.data-api', '[data-initialize=checkbox]', function initializeCheckboxes(e) {
        var $control = $$$1(e.target);

        if (!$control.data('fu.checkbox')) {
          $control.checkbox($control.data());
        }
      }); // Must be domReady for AMD compatibility

      $$$1(function onReadyInitializeCheckboxes() {
        $$$1('[data-initialize=checkbox]').each(function initializeCheckbox() {
          var $this = $$$1(this);

          if (!$this.data('fu.checkbox')) {
            $this.checkbox($this.data());
          }
        });
      });
    })(jQuery);

    (function ($$$1) {
      /* global jQuery:true */

      /*
       * Fuel UX Combobox
       * https://github.com/ExactTarget/fuelux
       *
       * Copyright (c) 2014 ExactTarget
       * Licensed under the BSD New license.
       */
      // -- BEGIN MODULE CODE HERE --
      var old = $$$1.fn.combobox; // COMBOBOX CONSTRUCTOR AND PROTOTYPE

      var Combobox = function Combobox(element, options) {
        this.$element = $$$1(element);
        this.options = $$$1.extend({}, $$$1.fn.combobox.defaults, options);
        this.$dropMenu = this.$element.find('.dropdown-menu');
        this.$input = this.$element.find('input');
        this.$button = this.$element.find('.btn');
        this.$inputGroupBtn = this.$element.find('.input-group-btn');
        this.$element.on('click.fu.combobox', 'a', $$$1.proxy(this.itemclicked, this));
        this.$element.on('change.fu.combobox', 'input', $$$1.proxy(this.inputchanged, this));
        this.$element.on('shown.bs.dropdown', $$$1.proxy(this.menuShown, this));
        this.$input.on('keyup.fu.combobox', $$$1.proxy(this.keypress, this)); // set default selection

        this.setDefaultSelection(); // if dropdown is empty, disable it

        var items = this.$dropMenu.children('li');

        if (items.length === 0) {
          this.$button.addClass('disabled');
        } // filter on load in case the first thing they do is press navigational key to pop open the menu


        if (this.options.filterOnKeypress) {
          this.options.filter(this.$dropMenu.find('li'), this.$input.val(), this);
        }
      };

      Combobox.prototype = {
        constructor: Combobox,
        destroy: function destroy() {
          this.$element.remove(); // remove any external bindings
          // [none]
          // set input value attrbute in markup

          this.$element.find('input').each(function () {
            $$$1(this).attr('value', $$$1(this).val());
          }); // empty elements to return to original markup
          // [none]

          return this.$element[0].outerHTML;
        },
        doSelect: function doSelect($item) {
          if (typeof $item[0] !== 'undefined') {
            // remove selection from old item, may result in remove and
            // re-addition of class if item is the same
            this.$element.find('li.selected:first').removeClass('selected'); // add selection to new item

            this.$selectedItem = $item;
            this.$selectedItem.addClass('selected'); // update input

            this.$input.val(this.$selectedItem.text().trim());
          } else {
            // this is a custom input, not in the menu
            this.$selectedItem = null;
            this.$element.find('li.selected:first').removeClass('selected');
          }
        },
        clearSelection: function clearSelection() {
          this.$selectedItem = null;
          this.$input.val('');
          this.$dropMenu.find('li').removeClass('selected');
        },
        menuShown: function menuShown() {
          if (this.options.autoResizeMenu) {
            this.resizeMenu();
          }
        },
        resizeMenu: function resizeMenu() {
          var width = this.$element.outerWidth();
          this.$dropMenu.outerWidth(width);
        },
        selectedItem: function selectedItem() {
          var item = this.$selectedItem;
          var data = {};

          if (item) {
            var txt = this.$selectedItem.text().trim();
            data = $$$1.extend({
              text: txt
            }, this.$selectedItem.data());
          } else {
            data = {
              text: this.$input.val().trim(),
              notFound: true
            };
          }

          return data;
        },
        selectByText: function selectByText(text) {
          var $item = $$$1([]);
          this.$element.find('li').each(function () {
            if ((this.textContent || this.innerText || $$$1(this).text() || '').trim().toLowerCase() === (text || '').trim().toLowerCase()) {
              $item = $$$1(this);
              return false;
            }
          });
          this.doSelect($item);
        },
        selectByValue: function selectByValue(value) {
          var selector = 'li[data-value="' + value + '"]';
          this.selectBySelector(selector);
        },
        selectByIndex: function selectByIndex(index) {
          // zero-based index
          var selector = 'li:eq(' + index + ')';
          this.selectBySelector(selector);
        },
        selectBySelector: function selectBySelector(selector) {
          var $item = this.$element.find(selector);
          this.doSelect($item);
        },
        setDefaultSelection: function setDefaultSelection() {
          var selector = 'li[data-selected=true]:first';
          var item = this.$element.find(selector);

          if (item.length > 0) {
            // select by data-attribute
            this.selectBySelector(selector);
            item.removeData('selected');
            item.removeAttr('data-selected');
          }
        },
        enable: function enable() {
          this.$element.removeClass('disabled');
          this.$input.removeAttr('disabled');
          this.$button.removeClass('disabled');
        },
        disable: function disable() {
          this.$element.addClass('disabled');
          this.$input.attr('disabled', true);
          this.$button.addClass('disabled');
        },
        itemclicked: function itemclicked(e) {
          this.$selectedItem = $$$1(e.target).parent(); // set input text and trigger input change event marked as synthetic

          this.$input.val(this.$selectedItem.text().trim()).trigger('change', {
            synthetic: true
          }); // pass object including text and any data-attributes
          // to onchange event

          var data = this.selectedItem(); // trigger changed event

          this.$element.trigger('changed.fu.combobox', data);
          e.preventDefault(); // return focus to control after selecting an option

          this.$element.find('.dropdown-toggle').focus();
        },
        keypress: function keypress(e) {
          var ENTER = 13; //var TAB = 9;

          var ESC = 27;
          var LEFT = 37;
          var UP = 38;
          var RIGHT = 39;
          var DOWN = 40;
          var IS_NAVIGATIONAL = e.which === UP || e.which === DOWN || e.which === LEFT || e.which === RIGHT;

          if (this.options.showOptionsOnKeypress && !this.$inputGroupBtn.hasClass('open')) {
            this.$button.dropdown('toggle');
            this.$input.focus();
          }

          if (e.which === ENTER) {
            e.preventDefault();
            var selected = this.$dropMenu.find('li.selected').text().trim();

            if (selected.length > 0) {
              this.selectByText(selected);
            } else {
              this.selectByText(this.$input.val());
            }

            this.$inputGroupBtn.removeClass('open');
          } else if (e.which === ESC) {
            e.preventDefault();
            this.clearSelection();
            this.$inputGroupBtn.removeClass('open');
          } else if (this.options.showOptionsOnKeypress) {
            if (e.which === DOWN || e.which === UP) {
              e.preventDefault();
              var $selected = this.$dropMenu.find('li.selected');

              if ($selected.length > 0) {
                if (e.which === DOWN) {
                  $selected = $selected.next(':not(.hidden)');
                } else {
                  $selected = $selected.prev(':not(.hidden)');
                }
              }

              if ($selected.length === 0) {
                if (e.which === DOWN) {
                  $selected = this.$dropMenu.find('li:not(.hidden):first');
                } else {
                  $selected = this.$dropMenu.find('li:not(.hidden):last');
                }
              }

              this.doSelect($selected);
            }
          } // Avoid filtering on navigation key presses


          if (this.options.filterOnKeypress && !IS_NAVIGATIONAL) {
            this.options.filter(this.$dropMenu.find('li'), this.$input.val(), this);
          }

          this.previousKeyPress = e.which;
        },
        inputchanged: function inputchanged(e, extra) {
          var val = $$$1(e.target).val(); // skip processing for internally-generated synthetic event
          // to avoid double processing

          if (extra && extra.synthetic) {
            this.selectByText(val);
            return;
          }

          this.selectByText(val); // find match based on input
          // if no match, pass the input value

          var data = this.selectedItem();

          if (data.text.length === 0) {
            data = {
              text: val
            };
          } // trigger changed event


          this.$element.trigger('changed.fu.combobox', data);
        }
      };
      Combobox.prototype.getValue = Combobox.prototype.selectedItem; // COMBOBOX PLUGIN DEFINITION

      $$$1.fn.combobox = function (option) {
        var args = Array.prototype.slice.call(arguments, 1);
        var methodReturn;
        var $set = this.each(function () {
          var $this = $$$1(this);
          var data = $this.data('fu.combobox');
          var options = typeof option === 'object' && option;

          if (!data) {
            $this.data('fu.combobox', data = new Combobox(this, options));
          }

          if (typeof option === 'string') {
            methodReturn = data[option].apply(data, args);
          }
        });
        return methodReturn === undefined ? $set : methodReturn;
      };

      $$$1.fn.combobox.defaults = {
        autoResizeMenu: true,
        filterOnKeypress: false,
        showOptionsOnKeypress: false,
        filter: function filter(list, predicate, self) {
          var visible = 0;
          self.$dropMenu.find('.empty-indicator').remove();
          list.each(function (i) {
            var $li = $$$1(this);
            var text = $$$1(this).text().trim();
            $li.removeClass();

            if (text === predicate) {
              $li.addClass('text-success');
              visible++;
            } else if (text.substr(0, predicate.length) === predicate) {
              $li.addClass('text-info');
              visible++;
            } else {
              $li.addClass('hidden');
            }
          });

          if (visible === 0) {
            self.$dropMenu.append('<li class="empty-indicator text-muted"><em>No Matches</em></li>');
          }
        }
      };
      $$$1.fn.combobox.Constructor = Combobox;

      $$$1.fn.combobox.noConflict = function () {
        $$$1.fn.combobox = old;
        return this;
      }; // DATA-API


      $$$1(document).on('mousedown.fu.combobox.data-api', '[data-initialize=combobox]', function (e) {
        var $control = $$$1(e.target).closest('.combobox');

        if (!$control.data('fu.combobox')) {
          $control.combobox($control.data());
        }
      }); // Must be domReady for AMD compatibility

      $$$1(function () {
        $$$1('[data-initialize=combobox]').each(function () {
          var $this = $$$1(this);

          if (!$this.data('fu.combobox')) {
            $this.combobox($this.data());
          }
        });
      });
    })(jQuery);

    (function ($$$1) {
      /* global jQuery:true */

      /*
       * Fuel UX Datepicker
       * https://github.com/ExactTarget/fuelux
       *
       * Copyright (c) 2014 ExactTarget
       * Licensed under the BSD New license.
       */
      // -- BEGIN MODULE CODE HERE --
      var INVALID_DATE = 'Invalid Date';
      var MOMENT_NOT_AVAILABLE = 'moment.js is not available so you cannot use this function';
      var datepickerStack = [];
      var moment = false;
      var old = $$$1.fn.datepicker;
      var requestedMoment = false;

      var runStack = function runStack() {
        var i, l;
        requestedMoment = true;

        for (i = 0, l = datepickerStack.length; i < l; i++) {
          datepickerStack[i].init.call(datepickerStack[i].scope);
        }

        datepickerStack = [];
      }; //only load moment if it's there. otherwise we'll look for it in window.moment


      if (typeof define === 'function' && define.amd) {
        //check if AMD is available
        require(['moment'], function (amdMoment) {
          moment = amdMoment;
          runStack();
        }, function (err) {
          var failedId = err.requireModules && err.requireModules[0];

          if (failedId === 'moment') {
            runStack();
          }
        });
      } else {
        runStack();
      } // DATEPICKER CONSTRUCTOR AND PROTOTYPE


      var Datepicker = function Datepicker(element, options) {
        this.$element = $$$1(element);
        this.options = $$$1.extend(true, {}, $$$1.fn.datepicker.defaults, options);
        this.$calendar = this.$element.find('.datepicker-calendar');
        this.$days = this.$calendar.find('.datepicker-calendar-days');
        this.$header = this.$calendar.find('.datepicker-calendar-header');
        this.$headerTitle = this.$header.find('.title');
        this.$input = this.$element.find('input');
        this.$inputGroupBtn = this.$element.find('.input-group-btn');
        this.$wheels = this.$element.find('.datepicker-wheels');
        this.$wheelsMonth = this.$element.find('.datepicker-wheels-month');
        this.$wheelsYear = this.$element.find('.datepicker-wheels-year');
        this.artificialScrolling = false;
        this.formatDate = this.options.formatDate || this.formatDate;
        this.inputValue = null;
        this.moment = false;
        this.momentFormat = null;
        this.parseDate = this.options.parseDate || this.parseDate;
        this.preventBlurHide = false;
        this.restricted = this.options.restricted || [];
        this.restrictedParsed = [];
        this.restrictedText = this.options.restrictedText;
        this.sameYearOnly = this.options.sameYearOnly;
        this.selectedDate = null;
        this.yearRestriction = null;
        this.$calendar.find('.datepicker-today').on('click.fu.datepicker', $$$1.proxy(this.todayClicked, this));
        this.$days.on('click.fu.datepicker', 'tr td button', $$$1.proxy(this.dateClicked, this));
        this.$header.find('.next').on('click.fu.datepicker', $$$1.proxy(this.next, this));
        this.$header.find('.prev').on('click.fu.datepicker', $$$1.proxy(this.prev, this));
        this.$headerTitle.on('click.fu.datepicker', $$$1.proxy(this.titleClicked, this));
        this.$input.on('change.fu.datepicker', $$$1.proxy(this.inputChanged, this));
        this.$input.on('mousedown.fu.datepicker', $$$1.proxy(this.showDropdown, this));
        this.$inputGroupBtn.on('hidden.bs.dropdown', $$$1.proxy(this.hide, this));
        this.$inputGroupBtn.on('shown.bs.dropdown', $$$1.proxy(this.show, this));
        this.$wheels.find('.datepicker-wheels-back').on('click.fu.datepicker', $$$1.proxy(this.backClicked, this));
        this.$wheels.find('.datepicker-wheels-select').on('click.fu.datepicker', $$$1.proxy(this.selectClicked, this));
        this.$wheelsMonth.on('click.fu.datepicker', 'ul button', $$$1.proxy(this.monthClicked, this));
        this.$wheelsYear.on('click.fu.datepicker', 'ul button', $$$1.proxy(this.yearClicked, this));
        this.$wheelsYear.find('ul').on('scroll.fu.datepicker', $$$1.proxy(this.onYearScroll, this));

        var init = function init() {
          if (this.checkForMomentJS()) {
            moment = moment || window.moment; // need to pull in the global moment if they didn't do it via require

            this.moment = true;
            this.momentFormat = this.options.momentConfig.format;
            this.setCulture(this.options.momentConfig.culture); // support moment with lang (< v2.8) or locale

            moment.locale = moment.locale || moment.lang;
          }

          this.setRestrictedDates(this.restricted);

          if (!this.setDate(this.options.date)) {
            this.$input.val('');
            this.inputValue = this.$input.val();
          }

          if (this.sameYearOnly) {
            this.yearRestriction = this.selectedDate ? this.selectedDate.getFullYear() : new Date().getFullYear();
          }
        };

        if (requestedMoment) {
          init.call(this);
        } else {
          datepickerStack.push({
            init: init,
            scope: this
          });
        }
      };

      Datepicker.prototype = {
        constructor: Datepicker,
        backClicked: function backClicked() {
          this.changeView('calendar');
        },
        changeView: function changeView(view, date) {
          if (view === 'wheels') {
            this.$calendar.hide().attr('aria-hidden', 'true');
            this.$wheels.show().removeAttr('aria-hidden', '');

            if (date) {
              this.renderWheel(date);
            }
          } else {
            this.$wheels.hide().attr('aria-hidden', 'true');
            this.$calendar.show().removeAttr('aria-hidden', '');

            if (date) {
              this.renderMonth(date);
            }
          }
        },
        checkForMomentJS: function checkForMomentJS() {
          if (($$$1.isFunction(window.moment) || typeof moment !== 'undefined' && $$$1.isFunction(moment)) && $$$1.isPlainObject(this.options.momentConfig) && typeof this.options.momentConfig.culture === 'string' && typeof this.options.momentConfig.format === 'string') {
            return true;
          } else {
            return false;
          }
        },
        dateClicked: function dateClicked(e) {
          var $td = $$$1(e.currentTarget).parents('td:first');
          var date;

          if ($td.hasClass('restricted')) {
            return;
          }

          this.$days.find('td.selected').removeClass('selected');
          $td.addClass('selected');
          date = new Date($td.attr('data-year'), $td.attr('data-month'), $td.attr('data-date'));
          this.selectedDate = date;
          this.$input.val(this.formatDate(date));
          this.inputValue = this.$input.val();
          this.hide();
          this.$input.focus();
          this.$element.trigger('dateClicked.fu.datepicker', date);
        },
        destroy: function destroy() {
          this.$element.remove(); // any external bindings
          // [none]
          // empty elements to return to original markup

          this.$days.find('tbody').empty();
          this.$wheelsYear.find('ul').empty();
          return this.$element[0].outerHTML;
        },
        disable: function disable() {
          this.$element.addClass('disabled');
          this.$element.find('input, button').attr('disabled', 'disabled');
          this.$inputGroupBtn.removeClass('open');
        },
        enable: function enable() {
          this.$element.removeClass('disabled');
          this.$element.find('input, button').removeAttr('disabled');
        },
        formatDate: function formatDate(date) {
          var padTwo = function padTwo(value) {
            var s = '0' + value;
            return s.substr(s.length - 2);
          };

          if (this.moment) {
            return moment(date).format(this.momentFormat);
          } else {
            return padTwo(date.getMonth() + 1) + '/' + padTwo(date.getDate()) + '/' + date.getFullYear();
          }
        },
        getCulture: function getCulture() {
          if (this.moment) {
            return moment.locale();
          } else {
            throw MOMENT_NOT_AVAILABLE;
          }
        },
        getDate: function getDate() {
          return !this.selectedDate ? new Date(NaN) : this.selectedDate;
        },
        getFormat: function getFormat() {
          if (this.moment) {
            return this.momentFormat;
          } else {
            throw MOMENT_NOT_AVAILABLE;
          }
        },
        getFormattedDate: function getFormattedDate() {
          return !this.selectedDate ? INVALID_DATE : this.formatDate(this.selectedDate);
        },
        getRestrictedDates: function getRestrictedDates() {
          return this.restricted;
        },
        inputChanged: function inputChanged() {
          var inputVal = this.$input.val();
          var date;

          if (inputVal !== this.inputValue) {
            date = this.setDate(inputVal);

            if (date === null) {
              this.$element.trigger('inputParsingFailed.fu.datepicker', inputVal);
            } else if (date === false) {
              this.$element.trigger('inputRestrictedDate.fu.datepicker', date);
            } else {
              this.$element.trigger('changed.fu.datepicker', date);
            }
          }
        },
        show: function show() {
          var date = this.selectedDate ? this.selectedDate : new Date();
          this.changeView('calendar', date);
          this.$inputGroupBtn.addClass('open');
          this.$element.trigger('shown.fu.datepicker');
        },
        showDropdown: function showDropdown(e) {
          //input mousedown handler, name retained for legacy support of showDropdown
          if (!this.$input.is(':focus') && !this.$inputGroupBtn.hasClass('open')) {
            this.show();
          }
        },
        hide: function hide() {
          this.$inputGroupBtn.removeClass('open');
          this.$element.trigger('hidden.fu.datepicker');
        },
        hideDropdown: function hideDropdown() {
          //for legacy support of hideDropdown
          this.hide();
        },
        isInvalidDate: function isInvalidDate(date) {
          var dateString = date.toString();

          if (dateString === INVALID_DATE || dateString === 'NaN') {
            return true;
          }

          return false;
        },
        isRestricted: function isRestricted(date, month, year) {
          var restricted = this.restrictedParsed;
          var i, from, l, to;

          if (this.sameYearOnly && this.yearRestriction !== null && year !== this.yearRestriction) {
            return true;
          }

          for (i = 0, l = restricted.length; i < l; i++) {
            from = restricted[i].from;
            to = restricted[i].to;

            if ((year > from.year || year === from.year && month > from.month || year === from.year && month === from.month && date >= from.date) && (year < to.year || year === to.year && month < to.month || year === to.year && month === to.month && date <= to.date)) {
              return true;
            }
          }

          return false;
        },
        monthClicked: function monthClicked(e) {
          this.$wheelsMonth.find('.selected').removeClass('selected');
          $$$1(e.currentTarget).parent().addClass('selected');
        },
        next: function next() {
          var month = this.$headerTitle.attr('data-month');
          var year = this.$headerTitle.attr('data-year');
          month++;

          if (month > 11) {
            if (this.sameYearOnly) {
              return;
            }

            month = 0;
            year++;
          }

          this.renderMonth(new Date(year, month, 1));
        },
        onYearScroll: function onYearScroll(e) {
          if (this.artificialScrolling) {
            return;
          }

          var $yearUl = $$$1(e.currentTarget);
          var height = $yearUl.css('box-sizing') === 'border-box' ? $yearUl.outerHeight() : $yearUl.height();
          var scrollHeight = $yearUl.get(0).scrollHeight;
          var scrollTop = $yearUl.scrollTop();
          var bottomPercentage = height / (scrollHeight - scrollTop) * 100;
          var topPercentage = scrollTop / scrollHeight * 100;
          var i, start;

          if (topPercentage < 5) {
            start = parseInt($yearUl.find('li:first').attr('data-year'), 10);

            for (i = start - 1; i > start - 11; i--) {
              $yearUl.prepend('<li data-year="' + i + '"><button type="button">' + i + '</button></li>');
            }

            this.artificialScrolling = true;
            $yearUl.scrollTop($yearUl.get(0).scrollHeight - scrollHeight + scrollTop);
            this.artificialScrolling = false;
          } else if (bottomPercentage > 90) {
            start = parseInt($yearUl.find('li:last').attr('data-year'), 10);

            for (i = start + 1; i < start + 11; i++) {
              $yearUl.append('<li data-year="' + i + '"><button type="button">' + i + '</button></li>');
            }
          }
        },
        //some code ripped from http://stackoverflow.com/questions/2182246/javascript-dates-in-ie-nan-firefox-chrome-ok
        parseDate: function parseDate(date) {
          var self = this;
          var BAD_DATE = new Date(NaN);
          var dt, isoExp, momentParse, momentParseWithFormat, tryMomentParseAll, month, parts;

          if (date) {
            if (this.moment) {
              //if we have moment, use that to parse the dates
              momentParseWithFormat = function momentParseWithFormat(d) {
                var md = moment(d, self.momentFormat);
                return true === md.isValid() ? md.toDate() : BAD_DATE;
              };

              momentParse = function momentParse(d) {
                var md = moment(new Date(d));
                return true === md.isValid() ? md.toDate() : BAD_DATE;
              };

              tryMomentParseAll = function tryMomentParseAll(rawDateString, parseFunc1, parseFunc2) {
                var pd = parseFunc1(rawDateString);

                if (!self.isInvalidDate(pd)) {
                  return pd;
                }

                pd = parseFunc2(rawDateString);

                if (!self.isInvalidDate(pd)) {
                  return pd;
                }

                return BAD_DATE;
              };

              if ('string' === typeof date) {
                // Attempts to parse date strings using this.momentFormat, falling back on newing a date
                return tryMomentParseAll(date, momentParseWithFormat, momentParse);
              } else {
                // Attempts to parse date by newing a date object directly, falling back on parsing using this.momentFormat
                return tryMomentParseAll(date, momentParse, momentParseWithFormat);
              }
            } else {
              //if moment isn't present, use previous date parsing strategy
              if (typeof date === 'string') {
                dt = new Date(Date.parse(date));

                if (!this.isInvalidDate(dt)) {
                  return dt;
                } else {
                  date = date.split('T')[0];
                  isoExp = /^\s*(\d{4})-(\d\d)-(\d\d)\s*$/;
                  parts = isoExp.exec(date);

                  if (parts) {
                    month = parseInt(parts[2], 10);
                    dt = new Date(parts[1], month - 1, parts[3]);

                    if (month === dt.getMonth() + 1) {
                      return dt;
                    }
                  }
                }
              } else {
                dt = new Date(date);

                if (!this.isInvalidDate(dt)) {
                  return dt;
                }
              }
            }
          }

          return new Date(NaN);
        },
        prev: function prev() {
          var month = this.$headerTitle.attr('data-month');
          var year = this.$headerTitle.attr('data-year');
          month--;

          if (month < 0) {
            if (this.sameYearOnly) {
              return;
            }

            month = 11;
            year--;
          }

          this.renderMonth(new Date(year, month, 1));
        },
        renderMonth: function renderMonth(date) {
          date = date || new Date();
          var firstDay = new Date(date.getFullYear(), date.getMonth(), 1).getDay();
          var lastDate = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
          var lastMonthDate = new Date(date.getFullYear(), date.getMonth(), 0).getDate();
          var $month = this.$headerTitle.find('.month');
          var month = date.getMonth();
          var now = new Date();
          var nowDate = now.getDate();
          var nowMonth = now.getMonth();
          var nowYear = now.getFullYear();
          var selected = this.selectedDate;
          var $tbody = this.$days.find('tbody');
          var year = date.getFullYear();
          var curDate, curMonth, curYear, i, j, rows, stage, previousStage, lastStage, $td, $tr;

          if (selected) {
            selected = {
              date: selected.getDate(),
              month: selected.getMonth(),
              year: selected.getFullYear()
            };
          }

          $month.find('.current').removeClass('current');
          $month.find('span[data-month="' + month + '"]').addClass('current');
          this.$headerTitle.find('.year').text(year);
          this.$headerTitle.attr({
            'data-month': month,
            'data-year': year
          });
          $tbody.empty();

          if (firstDay !== 0) {
            curDate = lastMonthDate - firstDay + 1;
            stage = -1;
          } else {
            curDate = 1;
            stage = 0;
          }

          rows = lastDate <= 35 - firstDay ? 5 : 6;

          for (i = 0; i < rows; i++) {
            $tr = $$$1('<tr></tr>');

            for (j = 0; j < 7; j++) {
              $td = $$$1('<td></td>');

              if (stage === -1) {
                $td.addClass('last-month');

                if (previousStage !== stage) {
                  $td.addClass('first');
                }
              } else if (stage === 1) {
                $td.addClass('next-month');

                if (previousStage !== stage) {
                  $td.addClass('first');
                }
              }

              curMonth = month + stage;
              curYear = year;

              if (curMonth < 0) {
                curMonth = 11;
                curYear--;
              } else if (curMonth > 11) {
                curMonth = 0;
                curYear++;
              }

              $td.attr({
                'data-date': curDate,
                'data-month': curMonth,
                'data-year': curYear
              });

              if (curYear === nowYear && curMonth === nowMonth && curDate === nowDate) {
                $td.addClass('current-day');
              } else if (curYear < nowYear || curYear === nowYear && curMonth < nowMonth || curYear === nowYear && curMonth === nowMonth && curDate < nowDate) {
                $td.addClass('past');

                if (!this.options.allowPastDates) {
                  $td.addClass('restricted').attr('title', this.restrictedText);
                }
              }

              if (this.isRestricted(curDate, curMonth, curYear)) {
                $td.addClass('restricted').attr('title', this.restrictedText);
              }

              if (selected && curYear === selected.year && curMonth === selected.month && curDate === selected.date) {
                $td.addClass('selected');
              }

              if ($td.hasClass('restricted')) {
                $td.html('<span><b class="datepicker-date">' + curDate + '</b></span>');
              } else {
                $td.html('<span><button type="button" class="datepicker-date">' + curDate + '</button></span>');
              }

              curDate++;
              lastStage = previousStage;
              previousStage = stage;

              if (stage === -1 && curDate > lastMonthDate) {
                curDate = 1;
                stage = 0;

                if (lastStage !== stage) {
                  $td.addClass('last');
                }
              } else if (stage === 0 && curDate > lastDate) {
                curDate = 1;
                stage = 1;

                if (lastStage !== stage) {
                  $td.addClass('last');
                }
              }

              if (i === rows - 1 && j === 6) {
                $td.addClass('last');
              }

              $tr.append($td);
            }

            $tbody.append($tr);
          }
        },
        renderWheel: function renderWheel(date) {
          var month = date.getMonth();
          var $monthUl = this.$wheelsMonth.find('ul');
          var year = date.getFullYear();
          var $yearUl = this.$wheelsYear.find('ul');
          var i, $monthSelected, $yearSelected;

          if (this.sameYearOnly) {
            this.$wheelsMonth.addClass('full');
            this.$wheelsYear.addClass('hidden');
          } else {
            this.$wheelsMonth.removeClass('full');
            this.$wheelsYear.removeClass('hide hidden'); // .hide is deprecated
          }

          $monthUl.find('.selected').removeClass('selected');
          $monthSelected = $monthUl.find('li[data-month="' + month + '"]');
          $monthSelected.addClass('selected');
          $monthUl.scrollTop($monthUl.scrollTop() + ($monthSelected.position().top - $monthUl.outerHeight() / 2 - $monthSelected.outerHeight(true) / 2));
          $yearUl.empty();

          for (i = year - 10; i < year + 11; i++) {
            $yearUl.append('<li data-year="' + i + '"><button type="button">' + i + '</button></li>');
          }

          $yearSelected = $yearUl.find('li[data-year="' + year + '"]');
          $yearSelected.addClass('selected');
          this.artificialScrolling = true;
          $yearUl.scrollTop($yearUl.scrollTop() + ($yearSelected.position().top - $yearUl.outerHeight() / 2 - $yearSelected.outerHeight(true) / 2));
          this.artificialScrolling = false;
          $monthSelected.find('button').focus();
        },
        selectClicked: function selectClicked() {
          var month = this.$wheelsMonth.find('.selected').attr('data-month');
          var year = this.$wheelsYear.find('.selected').attr('data-year');
          this.changeView('calendar', new Date(year, month, 1));
        },
        setCulture: function setCulture(cultureCode) {
          if (!cultureCode) {
            return false;
          }

          if (this.moment) {
            moment.locale(cultureCode);
          } else {
            throw MOMENT_NOT_AVAILABLE;
          }
        },
        setDate: function setDate(date) {
          var parsed = this.parseDate(date);

          if (!this.isInvalidDate(parsed)) {
            if (!this.isRestricted(parsed.getDate(), parsed.getMonth(), parsed.getFullYear())) {
              this.selectedDate = parsed;
              this.renderMonth(parsed);
              this.$input.val(this.formatDate(parsed));
            } else {
              this.selectedDate = false;
              this.renderMonth();
            }
          } else {
            this.selectedDate = null;
            this.renderMonth();
          }

          this.inputValue = this.$input.val();
          return this.selectedDate;
        },
        setFormat: function setFormat(format) {
          if (!format) {
            return false;
          }

          if (this.moment) {
            this.momentFormat = format;
          } else {
            throw MOMENT_NOT_AVAILABLE;
          }
        },
        setRestrictedDates: function setRestrictedDates(restricted) {
          var parsed = [];
          var self = this;
          var i, l;

          var parseItem = function parseItem(val) {
            if (val === -Infinity) {
              return {
                date: -Infinity,
                month: -Infinity,
                year: -Infinity
              };
            } else if (val === Infinity) {
              return {
                date: Infinity,
                month: Infinity,
                year: Infinity
              };
            } else {
              val = self.parseDate(val);
              return {
                date: val.getDate(),
                month: val.getMonth(),
                year: val.getFullYear()
              };
            }
          };

          this.restricted = restricted;

          for (i = 0, l = restricted.length; i < l; i++) {
            parsed.push({
              from: parseItem(restricted[i].from),
              to: parseItem(restricted[i].to)
            });
          }

          this.restrictedParsed = parsed;
        },
        titleClicked: function titleClicked(e) {
          this.changeView('wheels', new Date(this.$headerTitle.attr('data-year'), this.$headerTitle.attr('data-month'), 1));
        },
        todayClicked: function todayClicked(e) {
          var date = new Date();

          if (date.getMonth() + '' !== this.$headerTitle.attr('data-month') || date.getFullYear() + '' !== this.$headerTitle.attr('data-year')) {
            this.renderMonth(date);
          }
        },
        yearClicked: function yearClicked(e) {
          this.$wheelsYear.find('.selected').removeClass('selected');
          $$$1(e.currentTarget).parent().addClass('selected');
        }
      }; //for control library consistency

      Datepicker.prototype.getValue = Datepicker.prototype.getDate; // DATEPICKER PLUGIN DEFINITION

      $$$1.fn.datepicker = function (option) {
        var args = Array.prototype.slice.call(arguments, 1);
        var methodReturn;
        var $set = this.each(function () {
          var $this = $$$1(this);
          var data = $this.data('fu.datepicker');
          var options = typeof option === 'object' && option;

          if (!data) {
            $this.data('fu.datepicker', data = new Datepicker(this, options));
          }

          if (typeof option === 'string') {
            methodReturn = data[option].apply(data, args);
          }
        });
        return methodReturn === undefined ? $set : methodReturn;
      };

      $$$1.fn.datepicker.defaults = {
        allowPastDates: false,
        date: new Date(),
        formatDate: null,
        momentConfig: {
          culture: 'en',
          format: 'L' // more formats can be found here http://momentjs.com/docs/#/customization/long-date-formats/.

        },
        parseDate: null,
        restricted: [],
        //accepts an array of objects formatted as so: { from: {{date}}, to: {{date}} }  (ex: [ { from: new Date('12/11/2014'), to: new Date('03/31/2015') } ])
        restrictedText: 'Restricted',
        sameYearOnly: false
      };
      $$$1.fn.datepicker.Constructor = Datepicker;

      $$$1.fn.datepicker.noConflict = function () {
        $$$1.fn.datepicker = old;
        return this;
      }; // DATA-API


      $$$1(document).on('mousedown.fu.datepicker.data-api', '[data-initialize=datepicker]', function (e) {
        var $control = $$$1(e.target).closest('.datepicker');

        if (!$control.data('datepicker')) {
          $control.datepicker($control.data());
        }
      }); //used to prevent the dropdown from closing when clicking within it's bounds

      $$$1(document).on('click.fu.datepicker.data-api', '.datepicker .dropdown-menu', function (e) {
        var $target = $$$1(e.target);

        if (!$target.is('.datepicker-date') || $target.closest('.restricted').length) {
          e.stopPropagation();
        }
      }); //used to prevent the dropdown from closing when clicking on the input

      $$$1(document).on('click.fu.datepicker.data-api', '.datepicker input', function (e) {
        e.stopPropagation();
      });
      $$$1(function () {
        $$$1('[data-initialize=datepicker]').each(function () {
          var $this = $$$1(this);

          if ($this.data('datepicker')) {
            return;
          }

          $this.datepicker($this.data());
        });
      });
    })(jQuery);

    (function ($$$1) {
      /* global jQuery:true */

      /*
       * Fuel UX Dropdown Auto Flip
       * https://github.com/ExactTarget/fuelux
       *
       * Copyright (c) 2014 ExactTarget
       * Licensed under the BSD New license.
       */
      // -- BEGIN MODULE CODE HERE --
      $$$1(document).on('click.fu.dropdown-autoflip', '[data-toggle=dropdown][data-flip]', function (event) {
        if ($$$1(this).data().flip === "auto") {
          // have the drop down decide where to place itself
          _autoFlip($$$1(this).next('.dropdown-menu'));
        }
      }); // For pillbox suggestions dropdown

      $$$1(document).on('suggested.fu.pillbox', function (event, element) {
        _autoFlip($$$1(element));

        $$$1(element).parent().addClass('open');
      });

      function _autoFlip(menu) {
        // hide while the browser thinks
        $$$1(menu).css({
          visibility: "hidden"
        }); // decide where to put menu

        if (dropUpCheck(menu)) {
          menu.parent().addClass("dropup");
        } else {
          menu.parent().removeClass("dropup");
        } // show again


        $$$1(menu).css({
          visibility: "visible"
        });
      }

      function dropUpCheck(element) {
        // caching container
        var $container = _getContainer(element); // building object with measurementsances for later use


        var measurements = {};
        measurements.parentHeight = element.parent().outerHeight();
        measurements.parentOffsetTop = element.parent().offset().top;
        measurements.dropdownHeight = element.outerHeight();
        measurements.containerHeight = $container.overflowElement.outerHeight(); // this needs to be different if the window is the container or another element is

        measurements.containerOffsetTop = !!$container.isWindow ? $container.overflowElement.scrollTop() : $container.overflowElement.offset().top; // doing the calculations

        measurements.fromTop = measurements.parentOffsetTop - measurements.containerOffsetTop;
        measurements.fromBottom = measurements.containerHeight - measurements.parentHeight - (measurements.parentOffsetTop - measurements.containerOffsetTop); // actual determination of where to put menu
        // false = drop down
        // true = drop up

        if (measurements.dropdownHeight < measurements.fromBottom) {
          return false;
        } else if (measurements.dropdownHeight < measurements.fromTop) {
          return true;
        } else if (measurements.dropdownHeight >= measurements.fromTop && measurements.dropdownHeight >= measurements.fromBottom) {
          // decide which one is bigger and put it there
          if (measurements.fromTop >= measurements.fromBottom) {
            return true;
          } else {
            return false;
          }
        }
      }

      function _getContainer(element) {
        var targetSelector = element.attr('data-target');
        var isWindow = true;
        var containerElement;

        if (!targetSelector) {
          // no selection so find the relevant ancestor
          $$$1.each(element.parents(), function (index, parentElement) {
            if ($$$1(parentElement).css('overflow') !== 'visible') {
              containerElement = parentElement;
              isWindow = false;
              return false;
            }
          });
        } else if (targetSelector !== 'window') {
          containerElement = $$$1(targetSelector);
          isWindow = false;
        } // fallback to window


        if (isWindow) {
          containerElement = window;
        }

        return {
          overflowElement: $$$1(containerElement),
          isWindow: isWindow
        };
      } // register empty plugin


      $$$1.fn.dropdownautoflip = function () {
        /* empty */
      };
    })(jQuery);

    (function ($$$1) {
      /* global jQuery:true */

      /*
       * Fuel UX Loader
       * https://github.com/ExactTarget/fuelux
       *
       * Copyright (c) 2014 ExactTarget
       * Licensed under the BSD New license.
       */
      // -- BEGIN MODULE CODE HERE --
      var old = $$$1.fn.loader; // LOADER CONSTRUCTOR AND PROTOTYPE

      var Loader = function Loader(element, options) {
        this.$element = $$$1(element);
        this.options = $$$1.extend({}, $$$1.fn.loader.defaults, options);
      };

      Loader.prototype = {
        constructor: Loader,
        destroy: function destroy() {
          this.$element.remove(); // any external bindings
          // [none]
          // empty elements to return to original markup
          // [none]
          // returns string of markup

          return this.$element[0].outerHTML;
        },
        ieRepaint: function ieRepaint() {},
        msieVersion: function msieVersion() {},
        next: function next() {},
        pause: function pause() {},
        play: function play() {},
        previous: function previous() {},
        reset: function reset() {}
      }; // LOADER PLUGIN DEFINITION

      $$$1.fn.loader = function (option) {
        var args = Array.prototype.slice.call(arguments, 1);
        var methodReturn;
        var $set = this.each(function () {
          var $this = $$$1(this);
          var data = $this.data('fu.loader');
          var options = typeof option === 'object' && option;

          if (!data) {
            $this.data('fu.loader', data = new Loader(this, options));
          }

          if (typeof option === 'string') {
            methodReturn = data[option].apply(data, args);
          }
        });
        return methodReturn === undefined ? $set : methodReturn;
      };

      $$$1.fn.loader.defaults = {};
      $$$1.fn.loader.Constructor = Loader;

      $$$1.fn.loader.noConflict = function () {
        $$$1.fn.loader = old;
        return this;
      }; // INIT LOADER ON DOMCONTENTLOADED


      $$$1(function () {
        $$$1('[data-initialize=loader]').each(function () {
          var $this = $$$1(this);

          if (!$this.data('fu.loader')) {
            $this.loader($this.data());
          }
        });
      });
    })(jQuery);

    (function ($$$1) {
      /* global jQuery:true */

      /*
       * Fuel UX Placard
       * https://github.com/ExactTarget/fuelux
       *
       * Copyright (c) 2014 ExactTarget
       * Licensed under the BSD New license.
       */
      // -- BEGIN MODULE CODE HERE --
      var old = $$$1.fn.placard;
      var EVENT_CALLBACK_MAP = {
        'accepted': 'onAccept',
        'cancelled': 'onCancel'
      }; // PLACARD CONSTRUCTOR AND PROTOTYPE

      var Placard = function Placard(element, options) {
        var self = this;
        this.$element = $$$1(element);
        this.options = $$$1.extend({}, $$$1.fn.placard.defaults, options);

        if (this.$element.attr('data-ellipsis') === 'true') {
          this.options.applyEllipsis = true;
        }

        this.$accept = this.$element.find('.placard-accept');
        this.$cancel = this.$element.find('.placard-cancel');
        this.$field = this.$element.find('.placard-field');
        this.$footer = this.$element.find('.placard-footer');
        this.$header = this.$element.find('.placard-header');
        this.$popup = this.$element.find('.placard-popup');
        this.actualValue = null;
        this.clickStamp = '_';
        this.previousValue = '';

        if (this.options.revertOnCancel === -1) {
          this.options.revertOnCancel = this.$accept.length > 0;
        } // Placard supports inputs, textareas, or contenteditable divs. These checks determine which is being used


        this.isContentEditableDiv = this.$field.is('div');
        this.isInput = this.$field.is('input');
        this.divInTextareaMode = this.isContentEditableDiv && this.$field.attr('data-textarea') === 'true';
        this.$field.on('focus.fu.placard', $$$1.proxy(this.show, this));
        this.$field.on('keydown.fu.placard', $$$1.proxy(this.keyComplete, this));
        this.$element.on('close.fu.placard', $$$1.proxy(this.hide, this));
        this.$accept.on('click.fu.placard', $$$1.proxy(this.complete, this, 'accepted'));
        this.$cancel.on('click.fu.placard', function (e) {
          e.preventDefault();
          self.complete('cancelled');
        });
        this.applyEllipsis();
      };

      var _isShown = function _isShown(placard) {
        return placard.$element.hasClass('showing');
      };

      var _closeOtherPlacards = function _closeOtherPlacards() {
        var otherPlacards;
        otherPlacards = $$$1(document).find('.placard.showing');

        if (otherPlacards.length > 0) {
          if (otherPlacards.data('fu.placard') && otherPlacards.data('fu.placard').options.explicit) {
            return false; //failed
          }

          otherPlacards.placard('externalClickListener', {}, true);
        }

        return true; //succeeded
      };

      Placard.prototype = {
        constructor: Placard,
        complete: function complete(action) {
          var func = this.options[EVENT_CALLBACK_MAP[action]];
          var obj = {
            previousValue: this.previousValue,
            value: this.getValue()
          };

          if (func) {
            func(obj);
            this.$element.trigger(action + '.fu.placard', obj);
          } else {
            if (action === 'cancelled' && this.options.revertOnCancel) {
              this.setValue(this.previousValue, true);
            }

            this.$element.trigger(action + '.fu.placard', obj);
            this.hide();
          }
        },
        keyComplete: function keyComplete(e) {
          if ((this.isContentEditableDiv && !this.divInTextareaMode || this.isInput) && e.keyCode === 13) {
            this.complete('accepted');
            this.$field.blur();
          } else if (e.keyCode === 27) {
            this.complete('cancelled');
            this.$field.blur();
          }
        },
        destroy: function destroy() {
          this.$element.remove(); // remove any external bindings

          $$$1(document).off('click.fu.placard.externalClick.' + this.clickStamp); // set input value attribute

          this.$element.find('input').each(function () {
            $$$1(this).attr('value', $$$1(this).val());
          }); // empty elements to return to original markup
          // [none]
          // return string of markup

          return this.$element[0].outerHTML;
        },
        disable: function disable() {
          this.$element.addClass('disabled');
          this.$field.attr('disabled', 'disabled');

          if (this.isContentEditableDiv) {
            this.$field.removeAttr('contenteditable');
          }

          this.hide();
        },
        applyEllipsis: function applyEllipsis() {
          var field, i, str;

          if (this.options.applyEllipsis) {
            field = this.$field.get(0);

            if (this.isContentEditableDiv && !this.divInTextareaMode || this.isInput) {
              field.scrollLeft = 0;
            } else {
              field.scrollTop = 0;

              if (field.clientHeight < field.scrollHeight) {
                this.actualValue = this.getValue();
                this.setValue('', true);
                str = '';
                i = 0;

                while (field.clientHeight >= field.scrollHeight) {
                  str += this.actualValue[i];
                  this.setValue(str + '...', true);
                  i++;
                }

                str = str.length > 0 ? str.substring(0, str.length - 1) : '';
                this.setValue(str + '...', true);
              }
            }
          }
        },
        enable: function enable() {
          this.$element.removeClass('disabled');
          this.$field.removeAttr('disabled');

          if (this.isContentEditableDiv) {
            this.$field.attr('contenteditable', 'true');
          }
        },
        externalClickListener: function externalClickListener(e, force) {
          if (force === true || this.isExternalClick(e)) {
            this.complete(this.options.externalClickAction);
          }
        },
        getValue: function getValue() {
          if (this.actualValue !== null) {
            return this.actualValue;
          } else if (this.isContentEditableDiv) {
            return this.$field.html();
          } else {
            return this.$field.val();
          }
        },
        hide: function hide() {
          if (!this.$element.hasClass('showing')) {
            return;
          }

          this.$element.removeClass('showing');
          this.applyEllipsis();
          $$$1(document).off('click.fu.placard.externalClick.' + this.clickStamp);
          this.$element.trigger('hidden.fu.placard');
        },
        isExternalClick: function isExternalClick(e) {
          var el = this.$element.get(0);
          var exceptions = this.options.externalClickExceptions || [];
          var $originEl = $$$1(e.target);
          var i, l;

          if (e.target === el || $originEl.parents('.placard:first').get(0) === el) {
            return false;
          } else {
            for (i = 0, l = exceptions.length; i < l; i++) {
              if ($originEl.is(exceptions[i]) || $originEl.parents(exceptions[i]).length > 0) {
                return false;
              }
            }
          }

          return true;
        },

        /**
         * setValue() sets the Placard triggering DOM element's display value
         *
         * @param {String} the value to be displayed
         * @param {Boolean} If you want to explicitly suppress the application
         *					of ellipsis, pass `true`. This would typically only be
         *					done from internal functions (like `applyEllipsis`)
         *					that want to avoid circular logic. Otherwise, the
         *					value of the option applyEllipsis will be used.
         * @return {Object} jQuery object representing the DOM element whose
         *					value was set
         */
        setValue: function setValue(val, suppressEllipsis) {
          //if suppressEllipsis is undefined, check placards init settings
          if (typeof suppressEllipsis === 'undefined') {
            suppressEllipsis = !this.options.applyEllipsis;
          }

          if (this.isContentEditableDiv) {
            this.$field.empty().append(val);
          } else {
            this.$field.val(val);
          }

          if (!suppressEllipsis && !_isShown(this)) {
            this.applyEllipsis();
          }

          return this.$field;
        },
        show: function show() {
          if (_isShown(this)) {
            return;
          }

          if (!_closeOtherPlacards()) {
            return;
          }

          this.previousValue = this.isContentEditableDiv ? this.$field.html() : this.$field.val();

          if (this.actualValue !== null) {
            this.setValue(this.actualValue, true);
            this.actualValue = null;
          }

          this.showPlacard();
        },
        showPlacard: function showPlacard() {
          this.$element.addClass('showing');

          if (this.$header.length > 0) {
            this.$popup.css('top', '-' + this.$header.outerHeight(true) + 'px');
          }

          if (this.$footer.length > 0) {
            this.$popup.css('bottom', '-' + this.$footer.outerHeight(true) + 'px');
          }

          this.$element.trigger('shown.fu.placard');
          this.clickStamp = new Date().getTime() + (Math.floor(Math.random() * 100) + 1);

          if (!this.options.explicit) {
            $$$1(document).on('click.fu.placard.externalClick.' + this.clickStamp, $$$1.proxy(this.externalClickListener, this));
          }
        }
      }; // PLACARD PLUGIN DEFINITION

      $$$1.fn.placard = function (option) {
        var args = Array.prototype.slice.call(arguments, 1);
        var methodReturn;
        var $set = this.each(function () {
          var $this = $$$1(this);
          var data = $this.data('fu.placard');
          var options = typeof option === 'object' && option;

          if (!data) {
            $this.data('fu.placard', data = new Placard(this, options));
          }

          if (typeof option === 'string') {
            methodReturn = data[option].apply(data, args);
          }
        });
        return methodReturn === undefined ? $set : methodReturn;
      };

      $$$1.fn.placard.defaults = {
        onAccept: undefined,
        onCancel: undefined,
        externalClickAction: 'cancelled',
        externalClickExceptions: [],
        explicit: false,
        revertOnCancel: -1,
        //negative 1 will check for an '.placard-accept' button. Also can be set to true or false
        applyEllipsis: false
      };
      $$$1.fn.placard.Constructor = Placard;

      $$$1.fn.placard.noConflict = function () {
        $$$1.fn.placard = old;
        return this;
      }; // DATA-API


      $$$1(document).on('focus.fu.placard.data-api', '[data-initialize=placard]', function (e) {
        var $control = $$$1(e.target).closest('.placard');

        if (!$control.data('fu.placard')) {
          $control.placard($control.data());
        }
      }); // Must be domReady for AMD compatibility

      $$$1(function () {
        $$$1('[data-initialize=placard]').each(function () {
          var $this = $$$1(this);
          if ($this.data('fu.placard')) return;
          $this.placard($this.data());
        });
      });
    })(jQuery);

    (function ($$$1) {
      /* global jQuery:true */

      /*
       * Fuel UX Radio
       * https://github.com/ExactTarget/fuelux
       *
       * Copyright (c) 2014 ExactTarget
       * Licensed under the BSD New license.
       */
      // -- BEGIN MODULE CODE HERE --
      var old = $$$1.fn.radio; // RADIO CONSTRUCTOR AND PROTOTYPE

      var logError = function logError(error) {
        if (window && window.console && window.console.error) {
          window.console.error(error);
        }
      };

      var Radio = function Radio(element, options) {
        this.options = $$$1.extend({}, $$$1.fn.radio.defaults, options);

        if (element.tagName.toLowerCase() !== 'label') {
          logError('Radio must be initialized on the `label` that wraps the `input` element. See https://github.com/ExactTarget/fuelux/blob/master/reference/markup/radio.html for example of proper markup. Call `.radio()` on the `<label>` not the `<input>`');
          return;
        } // cache elements


        this.$label = $$$1(element);
        this.$radio = this.$label.find('input[type="radio"]');
        this.groupName = this.$radio.attr('name'); // don't cache group itself since items can be added programmatically

        if (!this.options.ignoreVisibilityCheck && this.$radio.css('visibility').match(/hidden|collapse/)) {
          logError('For accessibility reasons, in order for tab and space to function on radio, `visibility` must not be set to `hidden` or `collapse`. See https://github.com/ExactTarget/fuelux/pull/1996 for more details.');
        } // determine if a toggle container is specified


        var containerSelector = this.$radio.attr('data-toggle');
        this.$toggleContainer = $$$1(containerSelector); // handle internal events

        this.$radio.on('change', $$$1.proxy(this.itemchecked, this)); // set default state

        this.setInitialState();
      };

      Radio.prototype = {
        constructor: Radio,
        setInitialState: function setInitialState() {
          var $radio = this.$radio; // get current state of input

          var checked = $radio.prop('checked');
          var disabled = $radio.prop('disabled'); // sync label class with input state

          this.setCheckedState($radio, checked);
          this.setDisabledState($radio, disabled);
        },
        resetGroup: function resetGroup() {
          var $radios = $$$1('input[name="' + this.groupName + '"]');
          $radios.each(function resetRadio(index, item) {
            var $radio = $$$1(item);
            var $lbl = $radio.parent();
            var containerSelector = $radio.attr('data-toggle');
            var $containerToggle = $$$1(containerSelector);
            $lbl.removeClass('checked');
            $containerToggle.addClass('hidden');
          });
        },
        setCheckedState: function setCheckedState(element, checked) {
          var $radio = element;
          var $lbl = $radio.parent();
          var containerSelector = $radio.attr('data-toggle');
          var $containerToggle = $$$1(containerSelector);

          if (checked) {
            // reset all items in group
            this.resetGroup();
            $radio.prop('checked', true);
            $lbl.addClass('checked');
            $containerToggle.removeClass('hide hidden');
            $lbl.trigger('checked.fu.radio');
          } else {
            $radio.prop('checked', false);
            $lbl.removeClass('checked');
            $containerToggle.addClass('hidden');
            $lbl.trigger('unchecked.fu.radio');
          }

          $lbl.trigger('changed.fu.radio', checked);
        },
        setDisabledState: function setDisabledState(element, disabled) {
          var $radio = $$$1(element);
          var $lbl = this.$label;

          if (disabled) {
            $radio.prop('disabled', true);
            $lbl.addClass('disabled');
            $lbl.trigger('disabled.fu.radio');
          } else {
            $radio.prop('disabled', false);
            $lbl.removeClass('disabled');
            $lbl.trigger('enabled.fu.radio');
          }

          return $radio;
        },
        itemchecked: function itemchecked(evt) {
          var $radio = $$$1(evt.target);
          this.setCheckedState($radio, true);
        },
        check: function check() {
          this.setCheckedState(this.$radio, true);
        },
        uncheck: function uncheck() {
          this.setCheckedState(this.$radio, false);
        },
        isChecked: function isChecked() {
          var checked = this.$radio.prop('checked');
          return checked;
        },
        enable: function enable() {
          this.setDisabledState(this.$radio, false);
        },
        disable: function disable() {
          this.setDisabledState(this.$radio, true);
        },
        destroy: function destroy() {
          this.$label.remove();
          return this.$label[0].outerHTML;
        }
      };
      Radio.prototype.getValue = Radio.prototype.isChecked; // RADIO PLUGIN DEFINITION

      $$$1.fn.radio = function radio(option) {
        var args = Array.prototype.slice.call(arguments, 1);
        var methodReturn;
        var $set = this.each(function applyData() {
          var $this = $$$1(this);
          var data = $this.data('fu.radio');
          var options = typeof option === 'object' && option;

          if (!data) {
            $this.data('fu.radio', data = new Radio(this, options));
          }

          if (typeof option === 'string') {
            methodReturn = data[option].apply(data, args);
          }
        });
        return methodReturn === undefined ? $set : methodReturn;
      };

      $$$1.fn.radio.defaults = {
        ignoreVisibilityCheck: false
      };
      $$$1.fn.radio.Constructor = Radio;

      $$$1.fn.radio.noConflict = function noConflict() {
        $$$1.fn.radio = old;
        return this;
      }; // DATA-API


      $$$1(document).on('mouseover.fu.radio.data-api', '[data-initialize=radio]', function initializeRadios(e) {
        var $control = $$$1(e.target);

        if (!$control.data('fu.radio')) {
          $control.radio($control.data());
        }
      }); // Must be domReady for AMD compatibility

      $$$1(function onReadyInitializeRadios() {
        $$$1('[data-initialize=radio]').each(function initializeRadio() {
          var $this = $$$1(this);

          if (!$this.data('fu.radio')) {
            $this.radio($this.data());
          }
        });
      });
    })(jQuery);

    (function ($$$1) {
      /* global jQuery:true */

      /*
       * Fuel UX Search
       * https://github.com/ExactTarget/fuelux
       *
       * Copyright (c) 2014 ExactTarget
       * Licensed under the BSD New license.
       */
      // -- BEGIN MODULE CODE HERE --
      var old = $$$1.fn.search; // SEARCH CONSTRUCTOR AND PROTOTYPE

      var Search = function Search(element, options) {
        this.$element = $$$1(element);
        this.$repeater = $$$1(element).closest('.repeater');
        this.options = $$$1.extend({}, $$$1.fn.search.defaults, options);

        if (this.$element.attr('data-searchOnKeyPress') === 'true') {
          this.options.searchOnKeyPress = true;
        }

        this.$button = this.$element.find('button');
        this.$input = this.$element.find('input');
        this.$icon = this.$element.find('.glyphicon, .fuelux-icon');
        this.$button.on('click.fu.search', $$$1.proxy(this.buttonclicked, this));
        this.$input.on('keyup.fu.search', $$$1.proxy(this.keypress, this));

        if (this.$repeater.length > 0) {
          this.$repeater.on('rendered.fu.repeater', $$$1.proxy(this.clearPending, this));
        }

        this.activeSearch = '';
      };

      Search.prototype = {
        constructor: Search,
        destroy: function destroy() {
          this.$element.remove(); // any external bindings
          // [none]
          // set input value attrbute

          this.$element.find('input').each(function () {
            $$$1(this).attr('value', $$$1(this).val());
          }); // empty elements to return to original markup
          // [none]
          // returns string of markup

          return this.$element[0].outerHTML;
        },
        search: function search(searchText) {
          if (this.$icon.hasClass('glyphicon')) {
            this.$icon.removeClass('glyphicon-search').addClass('glyphicon-remove');
          }

          if (this.$icon.hasClass('fuelux-icon')) {
            this.$icon.removeClass('fuelux-icon-search').addClass('fuelux-icon-remove');
          }

          this.activeSearch = searchText;
          this.$element.addClass('searched pending');
          this.$element.trigger('searched.fu.search', searchText);
        },
        clear: function clear() {
          if (this.$icon.hasClass('glyphicon')) {
            this.$icon.removeClass('glyphicon-remove').addClass('glyphicon-search');
          }

          if (this.$icon.hasClass('fuelux-icon')) {
            this.$icon.removeClass('fuelux-icon-remove').addClass('fuelux-icon-search');
          }

          if (this.$element.hasClass('pending')) {
            this.$element.trigger('canceled.fu.search');
          }

          this.activeSearch = '';
          this.$input.val('');
          this.$element.trigger('cleared.fu.search');
          this.$element.removeClass('searched pending');
        },
        clearPending: function clearPending() {
          this.$element.removeClass('pending');
        },
        action: function action() {
          var val = this.$input.val();

          if (val && val.length > 0) {
            this.search(val);
          } else {
            this.clear();
          }
        },
        buttonclicked: function buttonclicked(e) {
          e.preventDefault();
          if ($$$1(e.currentTarget).is('.disabled, :disabled')) return;

          if (this.$element.hasClass('pending') || this.$element.hasClass('searched')) {
            this.clear();
          } else {
            this.action();
          }
        },
        keypress: function keypress(e) {
          var ENTER_KEY_CODE = 13;
          var TAB_KEY_CODE = 9;
          var ESC_KEY_CODE = 27;

          if (e.which === ENTER_KEY_CODE) {
            e.preventDefault();
            this.action();
          } else if (e.which === TAB_KEY_CODE) {
            e.preventDefault();
          } else if (e.which === ESC_KEY_CODE) {
            e.preventDefault();
            this.clear();
          } else if (this.options.searchOnKeyPress) {
            // search on other keypress
            this.action();
          }
        },
        disable: function disable() {
          this.$element.addClass('disabled');
          this.$input.attr('disabled', 'disabled');

          if (!this.options.allowCancel) {
            this.$button.addClass('disabled');
          }
        },
        enable: function enable() {
          this.$element.removeClass('disabled');
          this.$input.removeAttr('disabled');
          this.$button.removeClass('disabled');
        }
      }; // SEARCH PLUGIN DEFINITION

      $$$1.fn.search = function (option) {
        var args = Array.prototype.slice.call(arguments, 1);
        var methodReturn;
        var $set = this.each(function () {
          var $this = $$$1(this);
          var data = $this.data('fu.search');
          var options = typeof option === 'object' && option;

          if (!data) {
            $this.data('fu.search', data = new Search(this, options));
          }

          if (typeof option === 'string') {
            methodReturn = data[option].apply(data, args);
          }
        });
        return methodReturn === undefined ? $set : methodReturn;
      };

      $$$1.fn.search.defaults = {
        clearOnEmpty: false,
        searchOnKeyPress: false,
        allowCancel: false
      };
      $$$1.fn.search.Constructor = Search;

      $$$1.fn.search.noConflict = function () {
        $$$1.fn.search = old;
        return this;
      }; // DATA-API


      $$$1(document).on('mousedown.fu.search.data-api', '[data-initialize=search]', function (e) {
        var $control = $$$1(e.target).closest('.search');

        if (!$control.data('fu.search')) {
          $control.search($control.data());
        }
      }); // Must be domReady for AMD compatibility

      $$$1(function () {
        $$$1('[data-initialize=search]').each(function () {
          var $this = $$$1(this);
          if ($this.data('fu.search')) return;
          $this.search($this.data());
        });
      });
    })(jQuery);

    (function ($$$1) {
      /* global jQuery:true */

      /*
       * Fuel UX Selectlist
       * https://github.com/ExactTarget/fuelux
       *
       * Copyright (c) 2014 ExactTarget
       * Licensed under the BSD New license.
       */
      // -- BEGIN MODULE CODE HERE --
      var old = $$$1.fn.selectlist; // SELECT CONSTRUCTOR AND PROTOTYPE

      var Selectlist = function Selectlist(element, options) {
        this.$element = $$$1(element);
        this.options = $$$1.extend({}, $$$1.fn.selectlist.defaults, options);
        this.$button = this.$element.find('.btn.dropdown-toggle');
        this.$hiddenField = this.$element.find('.hidden-field');
        this.$label = this.$element.find('.selected-label');
        this.$dropdownMenu = this.$element.find('.dropdown-menu');
        this.$element.on('click.fu.selectlist', '.dropdown-menu a', $$$1.proxy(this.itemClicked, this));
        this.setDefaultSelection();

        if (options.resize === 'auto' || this.$element.attr('data-resize') === 'auto') {
          this.resize();
        } // if selectlist is empty or is one item, disable it


        var items = this.$dropdownMenu.children('li');

        if (items.length === 0) {
          this.disable();
          this.doSelect($$$1(this.options.emptyLabelHTML));
        } // support jumping focus to first letter in dropdown when key is pressed


        this.$element.on('shown.bs.dropdown', function () {
          var $this = $$$1(this); // attach key listener when dropdown is shown

          $$$1(document).on('keypress.fu.selectlist', function (e) {
            // get the key that was pressed
            var key = String.fromCharCode(e.which); // look the items to find the first item with the first character match and set focus

            $this.find("li").each(function (idx, item) {
              if ($$$1(item).text().charAt(0).toLowerCase() === key) {
                $$$1(item).children('a').focus();
                return false;
              }
            });
          });
        }); // unbind key event when dropdown is hidden

        this.$element.on('hide.bs.dropdown', function () {
          $$$1(document).off('keypress.fu.selectlist');
        });
      };

      Selectlist.prototype = {
        constructor: Selectlist,
        destroy: function destroy() {
          this.$element.remove(); // any external bindings
          // [none]
          // empty elements to return to original markup
          // [none]
          // returns string of markup

          return this.$element[0].outerHTML;
        },
        doSelect: function doSelect($item) {
          var $selectedItem;
          this.$selectedItem = $selectedItem = $item;
          this.$hiddenField.val(this.$selectedItem.attr('data-value'));
          this.$label.html($$$1(this.$selectedItem.children()[0]).html()); // clear and set selected item to allow declarative init state
          // unlike other controls, selectlist's value is stored internal, not in an input

          this.$element.find('li').each(function () {
            if ($selectedItem.is($$$1(this))) {
              $$$1(this).attr('data-selected', true);
            } else {
              $$$1(this).removeData('selected').removeAttr('data-selected');
            }
          });
        },
        itemClicked: function itemClicked(e) {
          this.$element.trigger('clicked.fu.selectlist', this.$selectedItem);
          e.preventDefault(); // ignore if a disabled item is clicked

          if ($$$1(e.currentTarget).parent('li').is('.disabled, :disabled')) {
            return;
          } // is clicked element different from currently selected element?


          if (!$$$1(e.target).parent().is(this.$selectedItem)) {
            this.itemChanged(e);
          } // return focus to control after selecting an option


          this.$element.find('.dropdown-toggle').focus();
        },
        itemChanged: function itemChanged(e) {
          //selectedItem needs to be <li> since the data is stored there, not in <a>
          this.doSelect($$$1(e.target).closest('li')); // pass object including text and any data-attributes
          // to onchange event

          var data = this.selectedItem(); // trigger changed event

          this.$element.trigger('changed.fu.selectlist', data);
        },
        resize: function resize() {
          var width = 0;
          var newWidth = 0;
          var sizer = $$$1('<div/>').addClass('selectlist-sizer');

          if (Boolean($$$1(document).find('html').hasClass('fuelux'))) {
            // default behavior for fuel ux setup. means fuelux was a class on the html tag
            $$$1(document.body).append(sizer);
          } else {
            // fuelux is not a class on the html tag. So we'll look for the first one we find so the correct styles get applied to the sizer
            $$$1('.fuelux:first').append(sizer);
          }

          sizer.append(this.$element.clone());
          this.$element.find('a').each(function () {
            sizer.find('.selected-label').text($$$1(this).text());
            newWidth = sizer.find('.selectlist').outerWidth();
            newWidth = newWidth + sizer.find('.sr-only').outerWidth();

            if (newWidth > width) {
              width = newWidth;
            }
          });

          if (width <= 1) {
            return;
          }

          this.$button.css('width', width);
          this.$dropdownMenu.css('width', width);
          sizer.remove();
        },
        selectedItem: function selectedItem() {
          var txt = this.$selectedItem.text();
          return $$$1.extend({
            text: txt
          }, this.$selectedItem.data());
        },
        selectByText: function selectByText(text) {
          var $item = $$$1([]);
          this.$element.find('li').each(function () {
            if ((this.textContent || this.innerText || $$$1(this).text() || '').toLowerCase() === (text || '').toLowerCase()) {
              $item = $$$1(this);
              return false;
            }
          });
          this.doSelect($item);
        },
        selectByValue: function selectByValue(value) {
          var selector = 'li[data-value="' + value + '"]';
          this.selectBySelector(selector);
        },
        selectByIndex: function selectByIndex(index) {
          // zero-based index
          var selector = 'li:eq(' + index + ')';
          this.selectBySelector(selector);
        },
        selectBySelector: function selectBySelector(selector) {
          var $item = this.$element.find(selector);
          this.doSelect($item);
        },
        setDefaultSelection: function setDefaultSelection() {
          var $item = this.$element.find('li[data-selected=true]').eq(0);

          if ($item.length === 0) {
            $item = this.$element.find('li').has('a').eq(0);
          }

          this.doSelect($item);
        },
        enable: function enable() {
          this.$element.removeClass('disabled');
          this.$button.removeClass('disabled');
        },
        disable: function disable() {
          this.$element.addClass('disabled');
          this.$button.addClass('disabled');
        }
      };
      Selectlist.prototype.getValue = Selectlist.prototype.selectedItem; // SELECT PLUGIN DEFINITION

      $$$1.fn.selectlist = function (option) {
        var args = Array.prototype.slice.call(arguments, 1);
        var methodReturn;
        var $set = this.each(function () {
          var $this = $$$1(this);
          var data = $this.data('fu.selectlist');
          var options = typeof option === 'object' && option;

          if (!data) {
            $this.data('fu.selectlist', data = new Selectlist(this, options));
          }

          if (typeof option === 'string') {
            methodReturn = data[option].apply(data, args);
          }
        });
        return methodReturn === undefined ? $set : methodReturn;
      };

      $$$1.fn.selectlist.defaults = {
        emptyLabelHTML: '<li data-value=""><a href="#">No items</a></li>'
      };
      $$$1.fn.selectlist.Constructor = Selectlist;

      $$$1.fn.selectlist.noConflict = function () {
        $$$1.fn.selectlist = old;
        return this;
      }; // DATA-API


      $$$1(document).on('mousedown.fu.selectlist.data-api', '[data-initialize=selectlist]', function (e) {
        var $control = $$$1(e.target).closest('.selectlist');

        if (!$control.data('fu.selectlist')) {
          $control.selectlist($control.data());
        }
      }); // Must be domReady for AMD compatibility

      $$$1(function () {
        $$$1('[data-initialize=selectlist]').each(function () {
          var $this = $$$1(this);

          if (!$this.data('fu.selectlist')) {
            $this.selectlist($this.data());
          }
        });
      });
    })(jQuery);

    (function ($$$1) {
      /* global jQuery:true */

      /*
       * Fuel UX Spinbox
       * https://github.com/ExactTarget/fuelux
       *
       * Copyright (c) 2014 ExactTarget
       * Licensed under the BSD New license.
       */
      // -- BEGIN MODULE CODE HERE --
      var old = $$$1.fn.spinbox; // SPINBOX CONSTRUCTOR AND PROTOTYPE

      var Spinbox = function Spinbox(element, options) {
        this.$element = $$$1(element);
        this.$element.find('.btn').on('click', function (e) {
          //keep spinbox from submitting if they forgot to say type="button" on their spinner buttons
          e.preventDefault();
        });
        this.options = $$$1.extend({}, $$$1.fn.spinbox.defaults, options);
        this.options.step = this.$element.data('step') || this.options.step;

        if (this.options.value < this.options.min) {
          this.options.value = this.options.min;
        } else if (this.options.max < this.options.value) {
          this.options.value = this.options.max;
        }

        this.$input = this.$element.find('.spinbox-input');
        this.$input.on('focusout.fu.spinbox', this.$input, $$$1.proxy(this.change, this));
        this.$element.on('keydown.fu.spinbox', this.$input, $$$1.proxy(this.keydown, this));
        this.$element.on('keyup.fu.spinbox', this.$input, $$$1.proxy(this.keyup, this));

        if (this.options.hold) {
          this.$element.on('mousedown.fu.spinbox', '.spinbox-up', $$$1.proxy(function () {
            this.startSpin(true);
          }, this));
          this.$element.on('mouseup.fu.spinbox', '.spinbox-up, .spinbox-down', $$$1.proxy(this.stopSpin, this));
          this.$element.on('mouseout.fu.spinbox', '.spinbox-up, .spinbox-down', $$$1.proxy(this.stopSpin, this));
          this.$element.on('mousedown.fu.spinbox', '.spinbox-down', $$$1.proxy(function () {
            this.startSpin(false);
          }, this));
        } else {
          this.$element.on('click.fu.spinbox', '.spinbox-up', $$$1.proxy(function () {
            this.step(true);
          }, this));
          this.$element.on('click.fu.spinbox', '.spinbox-down', $$$1.proxy(function () {
            this.step(false);
          }, this));
        }

        this.switches = {
          count: 1,
          enabled: true
        };

        if (this.options.speed === 'medium') {
          this.switches.speed = 300;
        } else if (this.options.speed === 'fast') {
          this.switches.speed = 100;
        } else {
          this.switches.speed = 500;
        }

        this.options.defaultUnit = _isUnitLegal(this.options.defaultUnit, this.options.units) ? this.options.defaultUnit : '';
        this.unit = this.options.defaultUnit;
        this.lastValue = this.options.value;
        this.render();

        if (this.options.disabled) {
          this.disable();
        }
      }; // Truly private methods


      var _limitToStep = function _limitToStep(number, step) {
        return Math.round(number / step) * step;
      };

      var _isUnitLegal = function _isUnitLegal(unit, validUnits) {
        var legalUnit = false;
        var suspectUnit = unit.toLowerCase();
        $$$1.each(validUnits, function (i, validUnit) {
          validUnit = validUnit.toLowerCase();

          if (suspectUnit === validUnit) {
            legalUnit = true;
            return false; //break out of the loop
          }
        });
        return legalUnit;
      };

      var _applyLimits = function _applyLimits(value) {
        // if unreadable
        if (isNaN(parseFloat(value))) {
          return value;
        } // if not within range return the limit


        if (value > this.options.max) {
          if (this.options.cycle) {
            value = this.options.min;
          } else {
            value = this.options.max;
          }
        } else if (value < this.options.min) {
          if (this.options.cycle) {
            value = this.options.max;
          } else {
            value = this.options.min;
          }
        }

        if (this.options.limitToStep && this.options.step) {
          value = _limitToStep(value, this.options.step); //force round direction so that it stays within bounds

          if (value > this.options.max) {
            value = value - this.options.step;
          } else if (value < this.options.min) {
            value = value + this.options.step;
          }
        }

        return value;
      };

      Spinbox.prototype = {
        constructor: Spinbox,
        destroy: function destroy() {
          this.$element.remove(); // any external bindings
          // [none]
          // set input value attrbute

          this.$element.find('input').each(function () {
            $$$1(this).attr('value', $$$1(this).val());
          }); // empty elements to return to original markup
          // [none]
          // returns string of markup

          return this.$element[0].outerHTML;
        },
        render: function render() {
          this._setValue(this.getDisplayValue());
        },
        change: function change() {
          this._setValue(this.getDisplayValue());

          this.triggerChangedEvent();
        },
        stopSpin: function stopSpin() {
          if (this.switches.timeout !== undefined) {
            clearTimeout(this.switches.timeout);
            this.switches.count = 1;
            this.triggerChangedEvent();
          }
        },
        triggerChangedEvent: function triggerChangedEvent() {
          var currentValue = this.getValue();
          if (currentValue === this.lastValue) return;
          this.lastValue = currentValue; // Primary changed event

          this.$element.trigger('changed.fu.spinbox', currentValue);
        },
        startSpin: function startSpin(type) {
          if (!this.options.disabled) {
            var divisor = this.switches.count;

            if (divisor === 1) {
              this.step(type);
              divisor = 1;
            } else if (divisor < 3) {
              divisor = 1.5;
            } else if (divisor < 8) {
              divisor = 2.5;
            } else {
              divisor = 4;
            }

            this.switches.timeout = setTimeout($$$1.proxy(function () {
              this.iterate(type);
            }, this), this.switches.speed / divisor);
            this.switches.count++;
          }
        },
        iterate: function iterate(type) {
          this.step(type);
          this.startSpin(type);
        },
        step: function step(isIncrease) {
          //refresh value from display before trying to increment in case they have just been typing before clicking the nubbins
          this._setValue(this.getDisplayValue());

          var newVal;

          if (isIncrease) {
            newVal = this.options.value + this.options.step;
          } else {
            newVal = this.options.value - this.options.step;
          }

          newVal = newVal.toFixed(5);

          this._setValue(newVal + this.unit);
        },
        getDisplayValue: function getDisplayValue() {
          var inputValue = this.parseInput(this.$input.val());
          var value = !!inputValue ? inputValue : this.options.value;
          return value;
        },
        setDisplayValue: function setDisplayValue(value) {
          this.$input.val(value);
        },
        getValue: function getValue() {
          var val = this.options.value;

          if (this.options.decimalMark !== '.') {
            val = (val + '').split('.').join(this.options.decimalMark);
          }

          return val + this.unit;
        },
        setValue: function setValue(val) {
          return this._setValue(val, true);
        },
        _setValue: function _setValue(val, shouldSetLastValue) {
          //remove any i18n on the number
          if (this.options.decimalMark !== '.') {
            val = this.parseInput(val);
          } //are we dealing with united numbers?


          if (typeof val !== "number") {
            var potentialUnit = val.replace(/[0-9.-]/g, ''); //make sure unit is valid, or else drop it in favor of current unit, or default unit (potentially nothing)

            this.unit = _isUnitLegal(potentialUnit, this.options.units) ? potentialUnit : this.options.defaultUnit;
          }

          var intVal = this.getIntValue(val); //make sure we are dealing with a number

          if (isNaN(intVal) && !isFinite(intVal)) {
            return this._setValue(this.options.value, shouldSetLastValue);
          } //conform


          intVal = _applyLimits.call(this, intVal); //cache the pure int value

          this.options.value = intVal; //prepare number for display

          val = intVal + this.unit;

          if (this.options.decimalMark !== '.') {
            val = (val + '').split('.').join(this.options.decimalMark);
          } //display number


          this.setDisplayValue(val);

          if (shouldSetLastValue) {
            this.lastValue = val;
          }

          return this;
        },
        value: function value(val) {
          if (val || val === 0) {
            return this.setValue(val);
          } else {
            return this.getValue();
          }
        },
        parseInput: function parseInput(value) {
          value = (value + '').split(this.options.decimalMark).join('.');
          return value;
        },
        getIntValue: function getIntValue(value) {
          //if they didn't pass in a number, try and get the number
          value = typeof value === "undefined" ? this.getValue() : value; // if there still isn't a number, abort

          if (typeof value === "undefined") {
            return;
          }

          if (typeof value === 'string') {
            value = this.parseInput(value);
          }

          value = parseFloat(value, 10);
          return value;
        },
        disable: function disable() {
          this.options.disabled = true;
          this.$element.addClass('disabled');
          this.$input.attr('disabled', '');
          this.$element.find('button').addClass('disabled');
        },
        enable: function enable() {
          this.options.disabled = false;
          this.$element.removeClass('disabled');
          this.$input.removeAttr('disabled');
          this.$element.find('button').removeClass('disabled');
        },
        keydown: function keydown(event) {
          var keyCode = event.keyCode;

          if (keyCode === 38) {
            this.step(true);
          } else if (keyCode === 40) {
            this.step(false);
          } else if (keyCode === 13) {
            this.change();
          }
        },
        keyup: function keyup(event) {
          var keyCode = event.keyCode;

          if (keyCode === 38 || keyCode === 40) {
            this.triggerChangedEvent();
          }
        }
      }; // SPINBOX PLUGIN DEFINITION

      $$$1.fn.spinbox = function spinbox(option) {
        var args = Array.prototype.slice.call(arguments, 1);
        var methodReturn;
        var $set = this.each(function () {
          var $this = $$$1(this);
          var data = $this.data('fu.spinbox');
          var options = typeof option === 'object' && option;

          if (!data) {
            $this.data('fu.spinbox', data = new Spinbox(this, options));
          }

          if (typeof option === 'string') {
            methodReturn = data[option].apply(data, args);
          }
        });
        return methodReturn === undefined ? $set : methodReturn;
      }; // value needs to be 0 for this.render();


      $$$1.fn.spinbox.defaults = {
        value: 0,
        min: 0,
        max: 999,
        step: 1,
        hold: true,
        speed: 'medium',
        disabled: false,
        cycle: false,
        units: [],
        decimalMark: '.',
        defaultUnit: '',
        limitToStep: false
      };
      $$$1.fn.spinbox.Constructor = Spinbox;

      $$$1.fn.spinbox.noConflict = function noConflict() {
        $$$1.fn.spinbox = old;
        return this;
      }; // DATA-API


      $$$1(document).on('mousedown.fu.spinbox.data-api', '[data-initialize=spinbox]', function (e) {
        var $control = $$$1(e.target).closest('.spinbox');

        if (!$control.data('fu.spinbox')) {
          $control.spinbox($control.data());
        }
      }); // Must be domReady for AMD compatibility

      $$$1(function () {
        $$$1('[data-initialize=spinbox]').each(function () {
          var $this = $$$1(this);

          if (!$this.data('fu.spinbox')) {
            $this.spinbox($this.data());
          }
        });
      });
    })(jQuery);

    (function ($$$1) {
      /* global jQuery:true */

      /*
       * Fuel UX Tree
       * https://github.com/ExactTarget/fuelux
       *
       * Copyright (c) 2014 ExactTarget
       * Licensed under the BSD New license.
       */
      // -- BEGIN MODULE CODE HERE --
      var old = $$$1.fn.tree; // TREE CONSTRUCTOR AND PROTOTYPE

      var Tree = function Tree(element, options) {
        this.$element = $$$1(element);
        this.options = $$$1.extend({}, $$$1.fn.tree.defaults, options);
        this.$element.attr('tabindex', '0');

        if (this.options.itemSelect) {
          this.$element.on('click.fu.tree', '.tree-item', $$$1.proxy(function callSelect(ev) {
            this.selectItem(ev.currentTarget);
          }, this));
        }

        this.$element.on('click.fu.tree', '.tree-branch-name', $$$1.proxy(function callToggle(ev) {
          this.toggleFolder(ev.currentTarget);
        }, this));
        this.$element.on('click.fu.tree', '.tree-overflow', $$$1.proxy(function callPopulate(ev) {
          this.populate($$$1(ev.currentTarget));
        }, this)); // folderSelect default is true

        if (this.options.folderSelect) {
          this.$element.addClass('tree-folder-select');
          this.$element.off('click.fu.tree', '.tree-branch-name');
          this.$element.on('click.fu.tree', '.icon-caret', $$$1.proxy(function callToggle(ev) {
            this.toggleFolder($$$1(ev.currentTarget).parent());
          }, this));
          this.$element.on('click.fu.tree', '.tree-branch-name', $$$1.proxy(function callSelect(ev) {
            this.selectFolder($$$1(ev.currentTarget));
          }, this));
        }

        this.$element.on('focus', function setFocusOnTab() {
          var $tree = $$$1(this);
          focusIn($tree, $tree);
        });
        this.$element.on('keydown', function processKeypress(e) {
          return navigateTree($$$1(this), e);
        });
        this.render();
      };

      Tree.prototype = {
        constructor: Tree,
        deselectAll: function deselectAll(n) {
          // clear all child tree nodes and style as deselected
          var nodes = n || this.$element;
          var $selectedElements = $$$1(nodes).find('.tree-selected');
          $selectedElements.each(function callStyleNodeDeselected(index, element) {
            var $element = $$$1(element);
            ariaDeselect($element);
            styleNodeDeselected($element, $element.find('.glyphicon'));
          });
          return $selectedElements;
        },
        destroy: function destroy() {
          // any external bindings [none]
          // empty elements to return to original markup
          this.$element.find('li:not([data-template])').remove();
          this.$element.remove(); // returns string of markup

          return this.$element[0].outerHTML;
        },
        render: function render() {
          this.populate(this.$element);
        },
        populate: function populate($el, ibp) {
          var self = this; // populate was initiated based on clicking overflow link

          var isOverflow = $el.hasClass('tree-overflow');
          var $parent = $el.hasClass('tree') ? $el : $el.parent();
          var atRoot = $parent.hasClass('tree');

          if (isOverflow && !atRoot) {
            $parent = $parent.parent();
          }

          var treeData = $parent.data(); // expose overflow data to datasource so it can be responded to appropriately.

          if (isOverflow) {
            treeData.overflow = $el.data();
          }

          var isBackgroundProcess = ibp || false; // no user affordance needed (ex.- "loading")

          if (isOverflow) {
            if (atRoot) {
              // the loader at the root level needs to continually replace the overflow trigger
              // otherwise, when loader is shown below, it will be the loader for the last folder
              // in the tree, instead of the loader at the root level.
              $el.replaceWith($parent.find('> .tree-loader').remove());
            } else {
              $el.remove();
            }
          }

          var $loader = $parent.find('.tree-loader:last');

          if (isBackgroundProcess === false) {
            $loader.removeClass('hide hidden'); // jQuery deprecated hide in 3.0. Use hidden instead. Leaving hide here to support previous markup
          }

          this.options.dataSource(treeData ? treeData : {}, function populateNodes(items) {
            $$$1.each(items.data, function buildNode(i, treeNode) {
              var nodeType = treeNode.type; // 'item' and 'overflow' remain consistent, but 'folder' maps to 'branch'

              if (treeNode.type === 'folder') {
                nodeType = 'branch';
              }

              var $entity = self.$element.find('[data-template=tree' + nodeType + ']:eq(0)').clone().removeClass('hide hidden') // jQuery deprecated hide in 3.0. Use hidden instead. Leaving hide here to support previous markup
              .removeData('template').removeAttr('data-template');
              $entity.find('.tree-' + nodeType + '-name > .tree-label')[self.options.html ? 'html' : 'text'](treeNode.text || treeNode.name);
              $entity.data(treeNode); // Decorate $entity with data or other attributes making the
              // element easily accessible with libraries like jQuery.
              //
              // Values are contained within the object returned
              // for folders and items as attr:
              //
              // {
              //     text: "An Item",
              //     type: 'item',
              //     attr = {
              //         'classes': 'required-item red-text',
              //         'data-parent': parentId,
              //         'guid': guid,
              //         'id': guid
              //     }
              // };
              //
              // the "name" attribute is also supported but is deprecated for "text".
              // add attributes to tree-branch or tree-item

              var attrs = treeNode.attr || treeNode.dataAttributes || [];
              $$$1.each(attrs, function setAttribute(attr, setTo) {
                switch (attr) {
                  case 'cssClass':
                  case 'class':
                  case 'className':
                    $entity.addClass(setTo);
                    break;
                  // allow custom icons

                  case 'data-icon':
                    $entity.find('.icon-item').removeClass().addClass('icon-item ' + setTo);
                    $entity.attr(attr, setTo);
                    break;
                  // ARIA support

                  case 'id':
                    $entity.attr(attr, setTo);
                    $entity.attr('aria-labelledby', setTo + '-label');
                    $entity.find('.tree-branch-name > .tree-label').attr('id', setTo + '-label');
                    break;
                  // style, data-*

                  default:
                    $entity.attr(attr, setTo);
                    break;
                }
              }); // add child node

              if (atRoot) {
                // For accessibility reasons, the root element is the only tab-able element (see https://github.com/ExactTarget/fuelux/issues/1964)
                $parent.append($entity);
              } else {
                $parent.find('.tree-branch-children:eq(0)').append($entity);
              }
            });
            $parent.find('.tree-loader').addClass('hidden'); // return newly populated folder

            self.$element.trigger('loaded.fu.tree', $parent);
          });
        },
        selectTreeNode: function selectItem(clickedElement, nodeType) {
          var clicked = {}; // object for clicked element

          clicked.$element = $$$1(clickedElement);
          var selected = {}; // object for selected elements

          selected.$elements = this.$element.find('.tree-selected');
          selected.dataForEvent = []; // determine clicked element and it's icon

          if (nodeType === 'folder') {
            // make the clicked.$element the container branch
            clicked.$element = clicked.$element.closest('.tree-branch');
            clicked.$icon = clicked.$element.find('.icon-folder');
          } else {
            clicked.$icon = clicked.$element.find('.icon-item');
          }

          clicked.elementData = clicked.$element.data();
          ariaSelect(clicked.$element); // the below functions pass objects by copy/reference and use modified object in this function

          if (this.options.multiSelect) {
            selected = multiSelectSyncNodes(this, clicked, selected);
          } else {
            selected = singleSelectSyncNodes(this, clicked, selected);
          }

          setFocus(this.$element, clicked.$element); // all done with the DOM, now fire events

          this.$element.trigger(selected.eventType + '.fu.tree', {
            target: clicked.elementData,
            selected: selected.dataForEvent
          });
          clicked.$element.trigger('updated.fu.tree', {
            selected: selected.dataForEvent,
            item: clicked.$element,
            eventType: selected.eventType
          });
        },
        discloseFolder: function discloseFolder(folder) {
          var $folder = $$$1(folder);
          var $branch = $folder.closest('.tree-branch');
          var $treeFolderContent = $branch.find('.tree-branch-children');
          var $treeFolderContentFirstChild = $treeFolderContent.eq(0); // take care of the styles

          $branch.addClass('tree-open');
          $branch.attr('aria-expanded', 'true');
          $treeFolderContentFirstChild.removeClass('hide hidden'); // jQuery deprecated hide in 3.0. Use hidden instead. Leaving hide here to support previous markup

          $branch.find('> .tree-branch-header .icon-folder').eq(0).removeClass('glyphicon-folder-close').addClass('glyphicon-folder-open');
          var $tree = this.$element;

          var disclosedCompleted = function disclosedCompleted() {
            $tree.trigger('disclosedFolder.fu.tree', $branch.data());
          }; // add the children to the folder


          if (!$treeFolderContent.children().length) {
            $tree.one('loaded.fu.tree', disclosedCompleted);
            this.populate($treeFolderContent);
          } else {
            disclosedCompleted();
          }
        },
        closeFolder: function closeFolder(el) {
          var $el = $$$1(el);
          var $branch = $el.closest('.tree-branch');
          var $treeFolderContent = $branch.find('.tree-branch-children');
          var $treeFolderContentFirstChild = $treeFolderContent.eq(0); // take care of the styles

          $branch.removeClass('tree-open');
          $branch.attr('aria-expanded', 'false');
          $treeFolderContentFirstChild.addClass('hidden');
          $branch.find('> .tree-branch-header .icon-folder').eq(0).removeClass('glyphicon-folder-open').addClass('glyphicon-folder-close'); // remove chidren if no cache

          if (!this.options.cacheItems) {
            $treeFolderContentFirstChild.empty();
          }

          this.$element.trigger('closed.fu.tree', $branch.data());
        },
        toggleFolder: function toggleFolder(el) {
          var $el = $$$1(el);

          if ($el.find('.glyphicon-folder-close').length) {
            this.discloseFolder(el);
          } else if ($el.find('.glyphicon-folder-open').length) {
            this.closeFolder(el);
          }
        },
        selectFolder: function selectFolder(el) {
          if (this.options.folderSelect) {
            this.selectTreeNode(el, 'folder');
          }
        },
        selectItem: function selectItem(el) {
          if (this.options.itemSelect) {
            this.selectTreeNode(el, 'item');
          }
        },
        selectedItems: function selectedItems() {
          var $sel = this.$element.find('.tree-selected');
          var selected = [];
          $$$1.each($sel, function buildSelectedArray(i, value) {
            selected.push($$$1(value).data());
          });
          return selected;
        },
        // collapses open folders
        collapse: function collapse() {
          var self = this;
          var reportedClosed = [];

          var closedReported = function closedReported(event, closed) {
            reportedClosed.push(closed); // jQuery deprecated hide in 3.0. Use hidden instead. Leaving hide here to support previous markup

            if (self.$element.find(".tree-branch.tree-open:not('.hidden, .hide')").length === 0) {
              self.$element.trigger('closedAll.fu.tree', {
                tree: self.$element,
                reportedClosed: reportedClosed
              });
              self.$element.off('loaded.fu.tree', self.$element, closedReported);
            }
          }; // trigger callback when all folders have reported closed


          self.$element.on('closed.fu.tree', closedReported);
          self.$element.find(".tree-branch.tree-open:not('.hidden, .hide')").each(function closeFolder() {
            self.closeFolder(this);
          });
        },
        // disclose visible will only disclose visible tree folders
        discloseVisible: function discloseVisible() {
          var self = this;
          var $openableFolders = self.$element.find(".tree-branch:not('.tree-open, .hidden, .hide')");
          var reportedOpened = [];

          var openReported = function openReported(event, opened) {
            reportedOpened.push(opened);

            if (reportedOpened.length === $openableFolders.length) {
              self.$element.trigger('disclosedVisible.fu.tree', {
                tree: self.$element,
                reportedOpened: reportedOpened
              });
              /*
               * Unbind the `openReported` event. `discloseAll` may be running and we want to reset this
               * method for the next iteration.
               */

              self.$element.off('loaded.fu.tree', self.$element, openReported);
            }
          }; // trigger callback when all folders have reported opened


          self.$element.on('loaded.fu.tree', openReported); // open all visible folders

          self.$element.find(".tree-branch:not('.tree-open, .hidden, .hide')").each(function triggerOpen() {
            self.discloseFolder($$$1(this).find('.tree-branch-header'));
          });
        },

        /*
         * Disclose all will keep listening for `loaded.fu.tree` and if `$(tree-el).data('ignore-disclosures-limit')`
         * is `true` (defaults to `true`) it will attempt to disclose any new closed folders than were
         * loaded in during the last disclosure.
         */
        discloseAll: function discloseAll() {
          var self = this; // first time

          if (typeof self.$element.data('disclosures') === 'undefined') {
            self.$element.data('disclosures', 0);
          }

          var isExceededLimit = self.options.disclosuresUpperLimit >= 1 && self.$element.data('disclosures') >= self.options.disclosuresUpperLimit;
          var isAllDisclosed = self.$element.find(".tree-branch:not('.tree-open, .hidden, .hide')").length === 0;

          if (!isAllDisclosed) {
            if (isExceededLimit) {
              self.$element.trigger('exceededDisclosuresLimit.fu.tree', {
                tree: self.$element,
                disclosures: self.$element.data('disclosures')
              });
              /*
               * If you've exceeded the limit, the loop will be killed unless you
               * explicitly ignore the limit and start the loop again:
               *
               *    $tree.one('exceededDisclosuresLimit.fu.tree', function () {
               *        $tree.data('ignore-disclosures-limit', true);
               *        $tree.tree('discloseAll');
               *    });
               */

              if (!self.$element.data('ignore-disclosures-limit')) {
                return;
              }
            }

            self.$element.data('disclosures', self.$element.data('disclosures') + 1);
            /*
             * A new branch that is closed might be loaded in, make sure those get handled too.
             * This attachment needs to occur before calling `discloseVisible` to make sure that
             * if the execution of `discloseVisible` happens _super fast_ (as it does in our QUnit tests
             * this will still be called. However, make sure this only gets called _once_, because
             * otherwise, every single time we go through this loop, _another_ event will be bound
             * and then when the trigger happens, this will fire N times, where N equals the number
             * of recursive `discloseAll` executions (instead of just one)
             */

            self.$element.one('disclosedVisible.fu.tree', function callDiscloseAll() {
              self.discloseAll();
            });
            /*
             * If the page is very fast, calling this first will cause `disclosedVisible.fu.tree` to not
             * be bound in time to be called, so, we need to call this last so that the things bound
             * and triggered above can have time to take place before the next execution of the
             * `discloseAll` method.
             */

            self.discloseVisible();
          } else {
            self.$element.trigger('disclosedAll.fu.tree', {
              tree: self.$element,
              disclosures: self.$element.data('disclosures')
            }); // if `cacheItems` is false, and they call closeAll, the data is trashed and therefore
            // disclosures needs to accurately reflect that

            if (!self.options.cacheItems) {
              self.$element.one('closeAll.fu.tree', function updateDisclosuresData() {
                self.$element.data('disclosures', 0);
              });
            }
          }
        },
        // This refreshes the children of a folder. Please destroy and re-initilize for "root level" refresh.
        // The data of the refreshed folder is not updated. This control's architecture only allows updating of children.
        // Folder renames should probably be handled directly on the node.
        refreshFolder: function refreshFolder($el) {
          var $treeFolder = $el.closest('.tree-branch');
          var $treeFolderChildren = $treeFolder.find('.tree-branch-children');
          $treeFolderChildren.eq(0).empty();

          if ($treeFolder.hasClass('tree-open')) {
            this.populate($treeFolderChildren, false);
          } else {
            this.populate($treeFolderChildren, true);
          }

          this.$element.trigger('refreshedFolder.fu.tree', $treeFolder.data());
        }
      }; // ALIASES
      // alias for collapse for consistency. "Collapse" is an ambiguous term (collapse what? All? One specific branch?)

      Tree.prototype.closeAll = Tree.prototype.collapse; // alias for backwards compatibility because there's no reason not to.

      Tree.prototype.openFolder = Tree.prototype.discloseFolder; // For library consistency

      Tree.prototype.getValue = Tree.prototype.selectedItems; // PRIVATE FUNCTIONS

      var fixFocusability = function fixFocusability($tree, $branch) {
        /*
        When tree initializes on page, the `<ul>` element should have tabindex=0 and all sub-elements should have
        tabindex=-1. When focus leaves the tree, whatever the last focused on element was will keep the tabindex=0. The
        tree itself will have a tabindex=-1. The reason for this is that if you are inside of the tree and press
        shift+tab, it will try and focus on the tree you are already in, which will cause focus to shift immediately
        back to the element you are already focused on. That will make it seem like the event is getting "Swallowed up"
        by an aggressive event listener trap.
        	For this reason, only one element in the entire tree, including the tree itself, should ever have tabindex=0.
        If somewhere down the line problems are being caused by this, the only further potential improvement I can
        envision at this time is listening for the tree to lose focus and reseting the tabindexes of all children to -1
        and setting the tabindex of the tree itself back to 0. This seems overly complicated with no benefit that I can
        imagine at this time, so instead I am leaving the last focused element with the tabindex of 0, even upon blur of
        the tree.
        	One benefit to leaving the last focused element in a tree with a tabindex=0 is that if you accidentally tab out
        of the tree and then want to tab back in, you will be placed exactly where you left off instead of at the
        beginning of the tree.
        */
        $tree.attr('tabindex', -1);
        $tree.find('li').attr('tabindex', -1);

        if ($branch && $branch.length > 0) {
          $branch.attr('tabindex', 0); // if tabindex is not set to 0 (or greater), node is not able to receive focus
        }
      }; // focuses into (onto one of the children of) the provided branch


      var focusIn = function focusIn($tree, $branch) {
        var $focusCandidate = $branch.find('.tree-selected:first'); // if no node is selected, set focus to first visible node

        if ($focusCandidate.length <= 0) {
          $focusCandidate = $branch.find('li:not(".hidden"):first');
        }

        setFocus($tree, $focusCandidate);
      }; // focuses on provided branch


      var setFocus = function setFocus($tree, $branch) {
        fixFocusability($tree, $branch);
        $tree.attr('aria-activedescendant', $branch.attr('id'));
        $branch.focus();
        $tree.trigger('setFocus.fu.tree', $branch);
      };

      var navigateTree = function navigateTree($tree, e) {
        if (e.isDefaultPrevented() || e.isPropagationStopped()) {
          return false;
        }

        var targetNode = e.originalEvent.target;
        var $targetNode = $$$1(targetNode);
        var isOpen = $targetNode.hasClass('tree-open');
        var handled = false; // because es5 lacks promises and fuelux has no polyfil (and I'm not adding one just for this change)
        // I am faking up promises here through callbacks and listeners. Done will be fired immediately at the end of
        // the navigateTree method if there is no (fake) promise, but will be fired by an event listener that will
        // be triggered by another function if necessary. This way when done runs, and fires keyboardNavigated.fu.tree
        // anything listening for that event can be sure that everything tied to that event is actually completed.

        var fireDoneImmediately = true;

        var done = function done() {
          $tree.trigger('keyboardNavigated.fu.tree', e, $targetNode);
        };

        switch (e.which) {
          case 13: // enter

          case 32:
            // space
            // activates a node, i.e., performs its default action.
            // For parent nodes, one possible default action is to open or close the node.
            // In single-select trees where selection does not follow focus, the default action is typically to select the focused node.
            var foldersSelectable = $tree.hasClass('tree-folder-select');
            var isFolder = $targetNode.hasClass('tree-branch');
            var isItem = $targetNode.hasClass('tree-item'); // var isOverflow = $targetNode.hasClass('tree-overflow');

            fireDoneImmediately = false;

            if (isFolder) {
              if (foldersSelectable) {
                $tree.one('selected.fu.tree deselected.fu.tree', done);
                $tree.tree('selectFolder', $targetNode.find('.tree-branch-header')[0]);
              } else {
                $tree.one('loaded.fu.tree closed.fu.tree', done);
                $tree.tree('toggleFolder', $targetNode.find('.tree-branch-header')[0]);
              }
            } else if (isItem) {
              $tree.one('selected.fu.tree', done);
              $tree.tree('selectItem', $targetNode);
            } else {
              // should be isOverflow... Try and click on it either way.
              $prev = $$$1($targetNode.prevAll().not('.hidden')[0]);
              $targetNode.click();
              $tree.one('loaded.fu.tree', function selectFirstNewlyLoadedNode() {
                $next = $$$1($prev.nextAll().not('.hidden')[0]);
                setFocus($tree, $next);
                done();
              });
            }

            handled = true;
            break;

          case 35:
            // end
            // Set focus to the last node in the tree that is focusable without opening a node.
            setFocus($tree, $tree.find('li:not(".hidden"):last'));
            handled = true;
            break;

          case 36:
            // home
            // set focus to the first node in the tree without opening or closing a node.
            setFocus($tree, $tree.find('li:not(".hidden"):first'));
            handled = true;
            break;

          case 37:
            // left
            if (isOpen) {
              fireDoneImmediately = false;
              $tree.one('closed.fu.tree', done);
              $tree.tree('closeFolder', targetNode);
            } else {
              setFocus($tree, $$$1($targetNode.parents('li')[0]));
            }

            handled = true;
            break;

          case 38:
            // up
            // move focus to previous sibling
            var $prev = []; // move to previous li not hidden

            $prev = $$$1($targetNode.prevAll().not('.hidden')[0]); // if the previous li is open, and has children, move selection to its last child so selection
            // appears to move to the next "thing" up

            if ($prev.hasClass('tree-open')) {
              var $prevChildren = $prev.find('li:not(".hidden"):last');

              if ($prevChildren.length > 0) {
                $prev = $$$1($prevChildren[0]);
              }
            } // if nothing has been selected, we are presumably at the top of an open li, select the immediate parent


            if ($prev.length < 1) {
              $prev = $$$1($targetNode.parents('li')[0]);
            }

            setFocus($tree, $prev);
            handled = true;
            break;

          case 39:
            // right
            if (isOpen) {
              focusIn($tree, $targetNode);
            } else {
              fireDoneImmediately = false;
              $tree.one('disclosed.fu.tree', done);
              $tree.tree('discloseFolder', targetNode);
            }

            handled = true;
            break;

          case 40:
            // down
            // move focus to next selectable tree node
            var $next = $$$1($targetNode.find('li:not(".hidden"):first')[0]);

            if (!isOpen || $next.length <= 0) {
              $next = $$$1($targetNode.nextAll().not('.hidden')[0]);
            }

            if ($next.length < 1) {
              $next = $$$1($$$1($targetNode.parents('li')[0]).nextAll().not('.hidden')[0]);
            }

            setFocus($tree, $next);
            handled = true;
            break;

          default:
            // console.log(e.which);
            return true;
          // exit this handler for other keys
        } // if we didn't handle the event, allow propagation to continue so something else might.


        if (handled) {
          e.preventDefault();
          e.stopPropagation();

          if (fireDoneImmediately) {
            done();
          }
        }

        return true;
      };

      var ariaSelect = function ariaSelect($element) {
        $element.attr('aria-selected', true);
      };

      var ariaDeselect = function ariaDeselect($element) {
        $element.attr('aria-selected', false);
      };

      function styleNodeSelected($element, $icon) {
        $element.addClass('tree-selected');

        if ($element.data('type') === 'item' && $icon.hasClass('fueluxicon-bullet')) {
          $icon.removeClass('fueluxicon-bullet').addClass('glyphicon-ok'); // make checkmark
        }
      }

      function styleNodeDeselected($element, $icon) {
        $element.removeClass('tree-selected');

        if ($element.data('type') === 'item' && $icon.hasClass('glyphicon-ok')) {
          $icon.removeClass('glyphicon-ok').addClass('fueluxicon-bullet'); // make bullet
        }
      }

      function multiSelectSyncNodes(self, clicked, selected) {
        // search for currently selected and add to selected data list if needed
        $$$1.each(selected.$elements, function findCurrentlySelected(index, element) {
          var $element = $$$1(element);

          if ($element[0] !== clicked.$element[0]) {
            selected.dataForEvent.push($$$1($element).data());
          }
        });

        if (clicked.$element.hasClass('tree-selected')) {
          styleNodeDeselected(clicked.$element, clicked.$icon); // set event data

          selected.eventType = 'deselected';
        } else {
          styleNodeSelected(clicked.$element, clicked.$icon); // set event data

          selected.eventType = 'selected';
          selected.dataForEvent.push(clicked.elementData);
        }

        return selected;
      }

      function singleSelectSyncNodes(self, clicked, selected) {
        // element is not currently selected
        if (selected.$elements[0] !== clicked.$element[0]) {
          self.deselectAll(self.$element);
          styleNodeSelected(clicked.$element, clicked.$icon); // set event data

          selected.eventType = 'selected';
          selected.dataForEvent = [clicked.elementData];
        } else {
          styleNodeDeselected(clicked.$element, clicked.$icon); // set event data

          selected.eventType = 'deselected';
          selected.dataForEvent = [];
        }

        return selected;
      } // TREE PLUGIN DEFINITION


      $$$1.fn.tree = function fntree(option) {
        var args = Array.prototype.slice.call(arguments, 1);
        var methodReturn;
        var $set = this.each(function eachThis() {
          var $this = $$$1(this);
          var data = $this.data('fu.tree');
          var options = typeof option === 'object' && option;

          if (!data) {
            $this.data('fu.tree', data = new Tree(this, options));
            $this.trigger('initialized.fu.tree');
          }

          if (typeof option === 'string') {
            methodReturn = data[option].apply(data, args);
          }
        });
        return methodReturn === undefined ? $set : methodReturn;
      };
      /*
       * Private method used only by the default dataSource for the tree, which is used to consume static
       * tree data.
       *
       * Find children of supplied parent in rootData. You can pass in an entire deeply nested tree
       * and this will look through it recursively until it finds the child data you are looking for.
       *
       * For extremely large trees, this could cause the browser to crash, as there is no protection
       * or limit on the amount of branches that will be searched through.
       */


      var findChildData = function findChildData(targetParent, rootData) {
        var isRootOfTree = $$$1.isEmptyObject(targetParent);

        if (isRootOfTree) {
          return rootData;
        }

        if (rootData === undefined) {
          return false;
        }

        for (var i = 0; i < rootData.length; i++) {
          var potentialMatch = rootData[i];

          if (potentialMatch.attr && targetParent.attr && potentialMatch.attr.id === targetParent.attr.id) {
            return potentialMatch.children;
          } else if (potentialMatch.children) {
            var foundChild = findChildData(targetParent, potentialMatch.children);

            if (foundChild) {
              return foundChild;
            }
          }
        }

        return false;
      };

      $$$1.fn.tree.defaults = {
        /*
         * A static data representation of your full tree data. If you do not override the tree's
         * default dataSource method, this will just make the tree work out of the box without
         * you having to bring your own dataSource.
         *
         * Array of Objects representing tree branches (folder) and leaves (item):
        	[
        		{
        			name: '',
        			type: 'folder',
        			attr: {
        				id: ''
        			},
        			children: [
        				{
        					name: '',
        					type: 'item',
        					attr: {
        						id: '',
        						'data-icon': 'glyphicon glyphicon-file'
        					}
        				}
        			]
        		},
        		{
        			name: '',
        			type: 'item',
        			attr: {
        				id: '',
        				'data-icon': 'glyphicon glyphicon-file'
        			}
        		}
        	];
         */
        staticData: [],

        /*
         * If you set the full tree data on options.staticData, you can use this default dataSource
         * to consume that data. This allows you to just pass in a JSON array representation
         * of your full tree data and the tree will just work out of the box.
         */
        dataSource: function staticDataSourceConsumer(openedParentData, callback) {
          if (this.staticData.length > 0) {
            var childData = findChildData(openedParentData, this.staticData);
            callback({
              data: childData
            });
          }
        },
        multiSelect: false,
        cacheItems: true,
        folderSelect: true,
        itemSelect: true,

        /*
         * How many times `discloseAll` should be called before a stopping and firing
         * an `exceededDisclosuresLimit` event. You can force it to continue by
         * listening for this event, setting `ignore-disclosures-limit` to `true` and
         * starting `discloseAll` back up again. This lets you make more decisions
         * about if/when/how/why/how many times `discloseAll` will be started back
         * up after it exceeds the limit.
         *
         *    $tree.one('exceededDisclosuresLimit.fu.tree', function () {
         *        $tree.data('ignore-disclosures-limit', true);
         *        $tree.tree('discloseAll');
         *    });
         *
         * `disclusuresUpperLimit` defaults to `0`, so by default this trigger
         * will never fire. The true hard the upper limit is the browser's
         * ability to load new items (i.e. it will keep loading until the browser
         * falls over and dies). On the Fuel UX `index.html` page, the point at
         * which the page became super slow (enough to seem almost unresponsive)
         * was `4`, meaning 256 folders had been opened, and 1024 were attempting to open.
         */
        disclosuresUpperLimit: 0
      };
      $$$1.fn.tree.Constructor = Tree;

      $$$1.fn.tree.noConflict = function noConflict() {
        $$$1.fn.tree = old;
        return this;
      }; // NO DATA-API DUE TO NEED OF DATA-SOURCE

    })(jQuery);

    (function ($$$1) {
      /* global jQuery:true */

      /*
       * Fuel UX Utilities
       * https://github.com/ExactTarget/fuelux
       *
       * Copyright (c) 2016 ExactTarget
       * Licensed under the BSD New license.
       */
      // -- BEGIN MODULE CODE HERE --
      var CONST = {
        BACKSPACE_KEYCODE: 8,
        COMMA_KEYCODE: 188,
        // `,` & `<`
        DELETE_KEYCODE: 46,
        DOWN_ARROW_KEYCODE: 40,
        ENTER_KEYCODE: 13,
        TAB_KEYCODE: 9,
        UP_ARROW_KEYCODE: 38
      };

      var isShiftHeld = function isShiftHeld(e) {
        return e.shiftKey === true;
      };

      var isKey = function isKey(keyCode) {
        return function compareKeycodes(e) {
          return e.keyCode === keyCode;
        };
      };

      var isBackspaceKey = isKey(CONST.BACKSPACE_KEYCODE);
      var isDeleteKey = isKey(CONST.DELETE_KEYCODE);
      var isTabKey = isKey(CONST.TAB_KEYCODE);
      var isUpArrow = isKey(CONST.UP_ARROW_KEYCODE);
      var isDownArrow = isKey(CONST.DOWN_ARROW_KEYCODE);
      var ENCODED_REGEX = /&[^\s]*;/;
      /*
       * to prevent double encoding decodes content in loop until content is encoding free
       */

      var cleanInput = function cleanInput(questionableMarkup) {
        // check for encoding and decode
        while (ENCODED_REGEX.test(questionableMarkup)) {
          questionableMarkup = $$$1('<i>').html(questionableMarkup).text();
        } // string completely decoded now encode it


        return $$$1('<i>').text(questionableMarkup).html();
      };

      $$$1.fn.utilities = {
        CONST: CONST,
        cleanInput: cleanInput,
        isBackspaceKey: isBackspaceKey,
        isDeleteKey: isDeleteKey,
        isShiftHeld: isShiftHeld,
        isTabKey: isTabKey,
        isUpArrow: isUpArrow,
        isDownArrow: isDownArrow
      };
    })(jQuery);

    (function ($$$1) {
      /* global jQuery:true */

      /*
       * Fuel UX Wizard
       * https://github.com/ExactTarget/fuelux
       *
       * Copyright (c) 2014 ExactTarget
       * Licensed under the BSD New license.
       */
      // -- BEGIN MODULE CODE HERE --
      var old = $$$1.fn.wizard; // WIZARD CONSTRUCTOR AND PROTOTYPE

      var Wizard = function Wizard(element, options) {
        this.$element = $$$1(element);
        this.options = $$$1.extend({}, $$$1.fn.wizard.defaults, options);
        this.options.disablePreviousStep = this.$element.attr('data-restrict') === 'previous' ? true : this.options.disablePreviousStep;
        this.currentStep = this.options.selectedItem.step;
        this.numSteps = this.$element.find('.steps li').length;
        this.$prevBtn = this.$element.find('button.btn-prev');
        this.$nextBtn = this.$element.find('button.btn-next');
        var kids = this.$nextBtn.children().detach();
        this.nextText = $$$1.trim(this.$nextBtn.text());
        this.$nextBtn.append(kids);
        var steps = this.$element.children('.steps-container'); // maintains backwards compatibility with < 3.8, will be removed in the future

        if (steps.length === 0) {
          steps = this.$element;
          this.$element.addClass('no-steps-container');

          if (window && window.console && window.console.warn) {
            window.console.warn('please update your wizard markup to include ".steps-container" as seen in http://getfuelux.com/javascript.html#wizard-usage-markup');
          }
        }

        steps = steps.find('.steps'); // handle events

        this.$prevBtn.on('click.fu.wizard', $$$1.proxy(this.previous, this));
        this.$nextBtn.on('click.fu.wizard', $$$1.proxy(this.next, this));
        steps.on('click.fu.wizard', 'li.complete', $$$1.proxy(this.stepclicked, this));
        this.selectedItem(this.options.selectedItem);

        if (this.options.disablePreviousStep) {
          this.$prevBtn.attr('disabled', true);
          this.$element.find('.steps').addClass('previous-disabled');
        }
      };

      Wizard.prototype = {
        constructor: Wizard,
        destroy: function destroy() {
          this.$element.remove(); // any external bindings [none]
          // empty elements to return to original markup [none]
          // returns string of markup

          return this.$element[0].outerHTML;
        },
        //index is 1 based
        //second parameter can be array of objects [{ ... }, { ... }] or you can pass n additional objects as args
        //object structure is as follows (all params are optional): { badge: '', label: '', pane: '' }
        addSteps: function addSteps(index) {
          var items = [].slice.call(arguments).slice(1);
          var $steps = this.$element.find('.steps');
          var $stepContent = this.$element.find('.step-content');
          var i, l, $pane, $startPane, $startStep, $step;
          index = index === -1 || index > this.numSteps + 1 ? this.numSteps + 1 : index;

          if (items[0] instanceof Array) {
            items = items[0];
          }

          $startStep = $steps.find('li:nth-child(' + index + ')');
          $startPane = $stepContent.find('.step-pane:nth-child(' + index + ')');

          if ($startStep.length < 1) {
            $startStep = null;
          }

          for (i = 0, l = items.length; i < l; i++) {
            $step = $$$1('<li data-step="' + index + '"><span class="badge badge-info"></span></li>');
            $step.append(items[i].label || '').append('<span class="chevron"></span>');
            $step.find('.badge').append(items[i].badge || index);
            $pane = $$$1('<div class="step-pane" data-step="' + index + '"></div>');
            $pane.append(items[i].pane || '');

            if (!$startStep) {
              $steps.append($step);
              $stepContent.append($pane);
            } else {
              $startStep.before($step);
              $startPane.before($pane);
            }

            index++;
          }

          this.syncSteps();
          this.numSteps = $steps.find('li').length;
          this.setState();
        },
        //index is 1 based, howMany is number to remove
        removeSteps: function removeSteps(index, howMany) {
          var action = 'nextAll';
          var i = 0;
          var $steps = this.$element.find('.steps');
          var $stepContent = this.$element.find('.step-content');
          var $start;
          howMany = howMany !== undefined ? howMany : 1;

          if (index > $steps.find('li').length) {
            $start = $steps.find('li:last');
          } else {
            $start = $steps.find('li:nth-child(' + index + ')').prev();

            if ($start.length < 1) {
              action = 'children';
              $start = $steps;
            }
          }

          $start[action]().each(function () {
            var item = $$$1(this);
            var step = item.attr('data-step');

            if (i < howMany) {
              item.remove();
              $stepContent.find('.step-pane[data-step="' + step + '"]:first').remove();
            } else {
              return false;
            }

            i++;
          });
          this.syncSteps();
          this.numSteps = $steps.find('li').length;
          this.setState();
        },
        setState: function setState() {
          var canMovePrev = this.currentStep > 1; //remember, steps index is 1 based...

          var isFirstStep = this.currentStep === 1;
          var isLastStep = this.currentStep === this.numSteps; // disable buttons based on current step

          if (!this.options.disablePreviousStep) {
            this.$prevBtn.attr('disabled', isFirstStep === true || canMovePrev === false);
          } // change button text of last step, if specified


          var last = this.$nextBtn.attr('data-last');

          if (last) {
            this.lastText = last; // replace text

            var text = this.nextText;

            if (isLastStep === true) {
              text = this.lastText; // add status class to wizard

              this.$element.addClass('complete');
            } else {
              this.$element.removeClass('complete');
            }

            var kids = this.$nextBtn.children().detach();
            this.$nextBtn.text(text).append(kids);
          } // reset classes for all steps


          var $steps = this.$element.find('.steps li');
          $steps.removeClass('active').removeClass('complete');
          $steps.find('span.badge').removeClass('badge-info').removeClass('badge-success'); // set class for all previous steps

          var prevSelector = '.steps li:lt(' + (this.currentStep - 1) + ')';
          var $prevSteps = this.$element.find(prevSelector);
          $prevSteps.addClass('complete');
          $prevSteps.find('span.badge').addClass('badge-success'); // set class for current step

          var currentSelector = '.steps li:eq(' + (this.currentStep - 1) + ')';
          var $currentStep = this.$element.find(currentSelector);
          $currentStep.addClass('active');
          $currentStep.find('span.badge').addClass('badge-info'); // set display of target element

          var $stepContent = this.$element.find('.step-content');
          var target = $currentStep.attr('data-step');
          $stepContent.find('.step-pane').removeClass('active');
          $stepContent.find('.step-pane[data-step="' + target + '"]:first').addClass('active'); // reset the wizard position to the left

          this.$element.find('.steps').first().attr('style', 'margin-left: 0'); // check if the steps are wider than the container div

          var totalWidth = 0;
          this.$element.find('.steps > li').each(function () {
            totalWidth += $$$1(this).outerWidth();
          });
          var containerWidth = 0;

          if (this.$element.find('.actions').length) {
            containerWidth = this.$element.width() - this.$element.find('.actions').first().outerWidth();
          } else {
            containerWidth = this.$element.width();
          }

          if (totalWidth > containerWidth) {
            // set the position so that the last step is on the right
            var newMargin = totalWidth - containerWidth;
            this.$element.find('.steps').first().attr('style', 'margin-left: -' + newMargin + 'px'); // set the position so that the active step is in a good
            // position if it has been moved out of view

            if (this.$element.find('li.active').first().position().left < 200) {
              newMargin += this.$element.find('li.active').first().position().left - 200;

              if (newMargin < 1) {
                this.$element.find('.steps').first().attr('style', 'margin-left: 0');
              } else {
                this.$element.find('.steps').first().attr('style', 'margin-left: -' + newMargin + 'px');
              }
            }
          } // only fire changed event after initializing


          if (typeof this.initialized !== 'undefined') {
            var e = $$$1.Event('changed.fu.wizard');
            this.$element.trigger(e, {
              step: this.currentStep
            });
          }

          this.initialized = true;
        },
        stepclicked: function stepclicked(e) {
          var li = $$$1(e.currentTarget);
          var index = this.$element.find('.steps li').index(li);

          if (index < this.currentStep && this.options.disablePreviousStep) {
            //enforce restrictions
            return;
          } else {
            var evt = $$$1.Event('stepclicked.fu.wizard');
            this.$element.trigger(evt, {
              step: index + 1
            });

            if (evt.isDefaultPrevented()) {
              return;
            }

            this.currentStep = index + 1;
            this.setState();
          }
        },
        syncSteps: function syncSteps() {
          var i = 1;
          var $steps = this.$element.find('.steps');
          var $stepContent = this.$element.find('.step-content');
          $steps.children().each(function () {
            var item = $$$1(this);
            var badge = item.find('.badge');
            var step = item.attr('data-step');

            if (!isNaN(parseInt(badge.html(), 10))) {
              badge.html(i);
            }

            item.attr('data-step', i);
            $stepContent.find('.step-pane[data-step="' + step + '"]:last').attr('data-step', i);
            i++;
          });
        },
        previous: function previous() {
          if (this.options.disablePreviousStep || this.currentStep === 1) {
            return;
          }

          var e = $$$1.Event('actionclicked.fu.wizard');
          this.$element.trigger(e, {
            step: this.currentStep,
            direction: 'previous'
          });

          if (e.isDefaultPrevented()) {
            return;
          } // don't increment ...what? Why?


          this.currentStep -= 1;
          this.setState(); // only set focus if focus is still on the $nextBtn (avoid stomping on a focus set programmatically in actionclicked callback)

          if (this.$prevBtn.is(':focus')) {
            var firstFormField = this.$element.find('.active').find('input, select, textarea')[0];

            if (typeof firstFormField !== 'undefined') {
              // allow user to start typing immediately instead of having to click on the form field.
              $$$1(firstFormField).focus();
            } else if (this.$element.find('.active input:first').length === 0 && this.$prevBtn.is(':disabled')) {
              //only set focus on a button as the last resort if no form fields exist and the just clicked button is now disabled
              this.$nextBtn.focus();
            }
          }
        },
        next: function next() {
          var e = $$$1.Event('actionclicked.fu.wizard');
          this.$element.trigger(e, {
            step: this.currentStep,
            direction: 'next'
          });

          if (e.isDefaultPrevented()) {
            return;
          } // respect preventDefault in case dev has attached validation to step and wants to stop propagation based on it.


          if (this.currentStep < this.numSteps) {
            this.currentStep += 1;
            this.setState();
          } else {
            //is last step
            this.$element.trigger('finished.fu.wizard');
          } // only set focus if focus is still on the $nextBtn (avoid stomping on a focus set programmatically in actionclicked callback)


          if (this.$nextBtn.is(':focus')) {
            var firstFormField = this.$element.find('.active').find('input, select, textarea')[0];

            if (typeof firstFormField !== 'undefined') {
              // allow user to start typing immediately instead of having to click on the form field.
              $$$1(firstFormField).focus();
            } else if (this.$element.find('.active input:first').length === 0 && this.$nextBtn.is(':disabled')) {
              //only set focus on a button as the last resort if no form fields exist and the just clicked button is now disabled
              this.$prevBtn.focus();
            }
          }
        },
        selectedItem: function selectedItem(_selectedItem) {
          var retVal, step;

          if (_selectedItem) {
            step = _selectedItem.step || -1; //allow selection of step by data-name

            step = Number(this.$element.find('.steps li[data-name="' + step + '"]').first().attr('data-step')) || Number(step);

            if (1 <= step && step <= this.numSteps) {
              this.currentStep = step;
              this.setState();
            } else {
              step = this.$element.find('.steps li.active:first').attr('data-step');

              if (!isNaN(step)) {
                this.currentStep = parseInt(step, 10);
                this.setState();
              }
            }

            retVal = this;
          } else {
            retVal = {
              step: this.currentStep
            };

            if (this.$element.find('.steps li.active:first[data-name]').length) {
              retVal.stepname = this.$element.find('.steps li.active:first').attr('data-name');
            }
          }

          return retVal;
        }
      }; // WIZARD PLUGIN DEFINITION

      $$$1.fn.wizard = function (option) {
        var args = Array.prototype.slice.call(arguments, 1);
        var methodReturn;
        var $set = this.each(function () {
          var $this = $$$1(this);
          var data = $this.data('fu.wizard');
          var options = typeof option === 'object' && option;

          if (!data) {
            $this.data('fu.wizard', data = new Wizard(this, options));
          }

          if (typeof option === 'string') {
            methodReturn = data[option].apply(data, args);
          }
        });
        return methodReturn === undefined ? $set : methodReturn;
      };

      $$$1.fn.wizard.defaults = {
        disablePreviousStep: false,
        selectedItem: {
          step: -1 //-1 means it will attempt to look for "active" class in order to set the step

        }
      };
      $$$1.fn.wizard.Constructor = Wizard;

      $$$1.fn.wizard.noConflict = function () {
        $$$1.fn.wizard = old;
        return this;
      }; // DATA-API


      $$$1(document).on('mouseover.fu.wizard.data-api', '[data-initialize=wizard]', function (e) {
        var $control = $$$1(e.target).closest('.wizard');

        if (!$control.data('fu.wizard')) {
          $control.wizard($control.data());
        }
      }); // Must be domReady for AMD compatibility

      $$$1(function () {
        $$$1('[data-initialize=wizard]').each(function () {
          var $this = $$$1(this);
          if ($this.data('fu.wizard')) return;
          $this.wizard($this.data());
        });
      });
    })(jQuery);

    (function ($$$1) {
      /* global jQuery:true */

      /*
       * Fuel UX Infinite Scroll
       * https://github.com/ExactTarget/fuelux
       *
       * Copyright (c) 2014 ExactTarget
       * Licensed under the BSD New license.
       */
      // -- BEGIN MODULE CODE HERE --
      var old = $$$1.fn.infinitescroll; // INFINITE SCROLL CONSTRUCTOR AND PROTOTYPE

      var InfiniteScroll = function InfiniteScroll(element, options) {
        this.$element = $$$1(element);
        this.$element.addClass('infinitescroll');
        this.options = $$$1.extend({}, $$$1.fn.infinitescroll.defaults, options);
        this.curScrollTop = this.$element.scrollTop();
        this.curPercentage = this.getPercentage();
        this.fetchingData = false;
        this.$element.on('scroll.fu.infinitescroll', $$$1.proxy(this.onScroll, this));
        this.onScroll();
      };

      InfiniteScroll.prototype = {
        constructor: InfiniteScroll,
        destroy: function destroy() {
          this.$element.remove(); // any external bindings
          // [none]
          // empty elements to return to original markup

          this.$element.empty();
          return this.$element[0].outerHTML;
        },
        disable: function disable() {
          this.$element.off('scroll.fu.infinitescroll');
        },
        enable: function enable() {
          this.$element.on('scroll.fu.infinitescroll', $$$1.proxy(this.onScroll, this));
        },
        end: function end(content) {
          var end = $$$1('<div class="infinitescroll-end"></div>');

          if (content) {
            end.append(content);
          } else {
            end.append('---------');
          }

          this.$element.append(end);
          this.disable();
        },
        getPercentage: function getPercentage() {
          var height = this.$element.css('box-sizing') === 'border-box' ? this.$element.outerHeight() : this.$element.height();
          var scrollHeight = this.$element.get(0).scrollHeight; // If we cannot compute the height, then we end up fetching all pages (ends up #/0 = Infinity).
          // This can happen if the repeater is loaded, but is not in the dom

          if (scrollHeight === 0 || scrollHeight - this.curScrollTop === 0) {
            return 0;
          }

          return height / (scrollHeight - this.curScrollTop) * 100;
        },
        fetchData: function fetchData(force) {
          var load = $$$1('<div class="infinitescroll-load"></div>');
          var self = this;
          var moreBtn;

          var fetch = function fetch() {
            var helpers = {
              percentage: self.curPercentage,
              scrollTop: self.curScrollTop
            };
            var $loader = $$$1('<div class="loader"></div>');
            load.append($loader);
            $loader.loader();

            if (self.options.dataSource) {
              self.options.dataSource(helpers, function (resp) {
                var end;
                load.remove();

                if (resp.content) {
                  self.$element.append(resp.content);
                }

                if (resp.end) {
                  end = resp.end !== true ? resp.end : undefined;
                  self.end(end);
                }

                self.fetchingData = false;
              });
            }
          };

          this.fetchingData = true;
          this.$element.append(load);

          if (this.options.hybrid && force !== true) {
            moreBtn = $$$1('<button type="button" class="btn btn-primary"></button>');

            if (typeof this.options.hybrid === 'object') {
              moreBtn.append(this.options.hybrid.label);
            } else {
              moreBtn.append('<span class="glyphicon glyphicon-repeat"></span>');
            }

            moreBtn.on('click.fu.infinitescroll', function () {
              moreBtn.remove();
              fetch();
            });
            load.append(moreBtn);
          } else {
            fetch();
          }
        },
        onScroll: function onScroll(e) {
          this.curScrollTop = this.$element.scrollTop();
          this.curPercentage = this.getPercentage();

          if (!this.fetchingData && this.curPercentage >= this.options.percentage) {
            this.fetchData();
          }
        }
      }; // INFINITE SCROLL PLUGIN DEFINITION

      $$$1.fn.infinitescroll = function (option) {
        var args = Array.prototype.slice.call(arguments, 1);
        var methodReturn;
        var $set = this.each(function () {
          var $this = $$$1(this);
          var data = $this.data('fu.infinitescroll');
          var options = typeof option === 'object' && option;

          if (!data) {
            $this.data('fu.infinitescroll', data = new InfiniteScroll(this, options));
          }

          if (typeof option === 'string') {
            methodReturn = data[option].apply(data, args);
          }
        });
        return methodReturn === undefined ? $set : methodReturn;
      };

      $$$1.fn.infinitescroll.defaults = {
        dataSource: null,
        hybrid: false,
        //can be true or an object with structure: { 'label': (markup or jQuery obj) }
        percentage: 95 //percentage scrolled to the bottom before more is loaded

      };
      $$$1.fn.infinitescroll.Constructor = InfiniteScroll;

      $$$1.fn.infinitescroll.noConflict = function () {
        $$$1.fn.infinitescroll = old;
        return this;
      }; // NO DATA-API DUE TO NEED OF DATA-SOURCE

    })(jQuery);

    (function ($$$1) {
      /* global jQuery:true utilities:true */

      /*
       * Fuel UX Pillbox
       * https://github.com/ExactTarget/fuelux
       *
       * Copyright (c) 2014 ExactTarget
       * Licensed under the BSD New license.
       */
      // -- BEGIN MODULE CODE HERE --
      var old = $$$1.fn.pillbox;
      var utilities = $$$1.fn.utilities;
      var CONST = $$$1.fn.utilities.CONST;
      var COMMA_KEYCODE = CONST.COMMA_KEYCODE;
      var ENTER_KEYCODE = CONST.ENTER_KEYCODE;
      var isBackspaceKey = utilities.isBackspaceKey;
      var isDeleteKey = utilities.isDeleteKey;
      var isTabKey = utilities.isTabKey;
      var isUpArrow = utilities.isUpArrow;
      var isDownArrow = utilities.isDownArrow;
      var cleanInput = utilities.cleanInput;
      var isShiftHeld = utilities.isShiftHeld; // PILLBOX CONSTRUCTOR AND PROTOTYPE

      var Pillbox = function Pillbox(element, options) {
        this.$element = $$$1(element);
        this.$moreCount = this.$element.find('.pillbox-more-count');
        this.$pillGroup = this.$element.find('.pill-group');
        this.$addItem = this.$element.find('.pillbox-add-item');
        this.$addItemWrap = this.$addItem.parent();
        this.$suggest = this.$element.find('.suggest');
        this.$pillHTML = '<li class="btn btn-default pill">' + '	<span></span>' + '	<span class="glyphicon glyphicon-close">' + '		<span class="sr-only">Remove</span>' + '	</span>' + '</li>';
        this.options = $$$1.extend({}, $$$1.fn.pillbox.defaults, options);

        if (this.options.readonly === -1) {
          if (this.$element.attr('data-readonly') !== undefined) {
            this.readonly(true);
          }
        } else if (this.options.readonly) {
          this.readonly(true);
        } // EVENTS


        this.acceptKeyCodes = this._generateObject(this.options.acceptKeyCodes); // Create an object out of the key code array, so we don't have to loop through it on every key stroke

        this.$element.on('click.fu.pillbox', '.pill-group > .pill', $$$1.proxy(this.itemClicked, this));
        this.$element.on('click.fu.pillbox', $$$1.proxy(this.inputFocus, this));
        this.$element.on('keydown.fu.pillbox', '.pillbox-add-item', $$$1.proxy(this.inputEvent, this));

        if (this.options.onKeyDown) {
          this.$element.on('mousedown.fu.pillbox', '.suggest > li', $$$1.proxy(this.suggestionClick, this));
        }

        if (this.options.edit) {
          this.$element.addClass('pills-editable');
          this.$element.on('blur.fu.pillbox', '.pillbox-add-item', $$$1.proxy(this.cancelEdit, this));
        }

        this.$element.on('blur.fu.pillbox', '.pillbox-add-item', $$$1.proxy(this.inputEvent, this));
      };

      Pillbox.prototype = {
        constructor: Pillbox,
        destroy: function destroy() {
          this.$element.remove(); // any external bindings
          // [none]
          // empty elements to return to original markup
          // [none]
          // returns string of markup

          return this.$element[0].outerHTML;
        },
        items: function items() {
          var self = this;
          return this.$pillGroup.children('.pill').map(function getItemsData() {
            return self.getItemData($$$1(this));
          }).get();
        },
        itemClicked: function itemClicked(e) {
          var $target = $$$1(e.target);
          var $item;
          e.preventDefault();
          e.stopPropagation();

          this._closeSuggestions();

          if (!$target.hasClass('pill')) {
            $item = $target.parent();

            if (this.$element.attr('data-readonly') === undefined) {
              if ($target.hasClass('glyphicon-close')) {
                if (this.options.onRemove) {
                  this.options.onRemove(this.getItemData($item, {
                    el: $item
                  }), $$$1.proxy(this._removeElement, this));
                } else {
                  this._removeElement(this.getItemData($item, {
                    el: $item
                  }));
                }

                return false;
              } else if (this.options.edit) {
                if ($item.find('.pillbox-list-edit').length) {
                  return false;
                }

                this.openEdit($item);
              }
            }
          } else {
            $item = $target;
          }

          this.$element.trigger('clicked.fu.pillbox', this.getItemData($item));
          return true;
        },
        readonly: function readonly(enable) {
          if (enable) {
            this.$element.attr('data-readonly', 'readonly');
          } else {
            this.$element.removeAttr('data-readonly');
          }

          if (this.options.truncate) {
            this.truncate(enable);
          }
        },
        suggestionClick: function suggestionClick(e) {
          var $item = $$$1(e.currentTarget);
          var item = {
            text: $item.html(),
            value: $item.data('value')
          };
          e.preventDefault();
          this.$addItem.val('');

          if ($item.data('attr')) {
            item.attr = JSON.parse($item.data('attr'));
          }

          item.data = $item.data('data');
          this.addItems(item, true); // needs to be after addItems for IE

          this._closeSuggestions();
        },
        itemCount: function itemCount() {
          return this.$pillGroup.children('.pill').length;
        },
        // First parameter is 1 based index (optional, if index is not passed all new items will be appended)
        // Second parameter can be array of objects [{ ... }, { ... }] or you can pass n additional objects as args
        // object structure is as follows (attr and value are optional): { text: '', value: '', attr: {}, data: {} }
        addItems: function addItems() {
          var self = this;
          var items;
          var index;
          var isInternal;

          if (isFinite(String(arguments[0])) && !(arguments[0] instanceof Array)) {
            items = [].slice.call(arguments).slice(1);
            index = arguments[0];
          } else {
            items = [].slice.call(arguments).slice(0);
            isInternal = items[1] && !items[1].text;
          } // If first argument is an array, use that, otherwise they probably passed each thing through as a separate arg, so use items as-is


          if (items[0] instanceof Array) {
            items = items[0];
          }

          if (items.length) {
            $$$1.each(items, function normalizeItemsObject(i, value) {
              var data = {
                text: value.text,
                value: value.value ? value.value : value.text,
                el: self.$pillHTML
              };

              if (value.attr) {
                data.attr = value.attr;
              }

              if (value.data) {
                data.data = value.data;
              }

              items[i] = data;
            });

            if (this.options.edit && this.currentEdit) {
              items[0].el = this.currentEdit.wrap('<div></div>').parent().html();
            }

            if (isInternal) {
              items.pop(1);
            }

            if (self.options.onAdd && isInternal) {
              if (this.options.edit && this.currentEdit) {
                self.options.onAdd(items[0], $$$1.proxy(self.saveEdit, this));
              } else {
                self.options.onAdd(items[0], $$$1.proxy(self.placeItems, this));
              }
            } else if (this.options.edit && this.currentEdit) {
              self.saveEdit(items);
            } else if (index) {
              self.placeItems(index, items);
            } else {
              self.placeItems(items, isInternal);
            }
          }
        },
        // First parameter is the index (1 based) to start removing items
        // Second parameter is the number of items to be removed
        removeItems: function removeItems(index, howMany) {
          var self = this;

          if (!index) {
            this.$pillGroup.find('.pill').remove();

            this._removePillTrigger({
              method: 'removeAll'
            });
          } else {
            var itemsToRemove = howMany ? howMany : 1;

            for (var item = 0; item < itemsToRemove; item++) {
              var $currentItem = self.$pillGroup.find('> .pill:nth-child(' + index + ')');

              if ($currentItem) {
                $currentItem.remove();
              } else {
                break;
              }
            }
          }
        },
        // First parameter is index (optional)
        // Second parameter is new arguments
        placeItems: function placeItems() {
          var items;
          var index;
          var $neighbor;
          var isInternal;

          if (isFinite(String(arguments[0])) && !(arguments[0] instanceof Array)) {
            items = [].slice.call(arguments).slice(1);
            index = arguments[0];
          } else {
            items = [].slice.call(arguments).slice(0);
            isInternal = items[1] && !items[1].text;
          }

          if (items[0] instanceof Array) {
            items = items[0];
          }

          if (items.length) {
            var newItems = [];
            $$$1.each(items, function prepareItemForAdd(i, item) {
              var $item = $$$1(item.el);
              $item.attr('data-value', item.value);
              $item.find('span:first').html(item.text); // DOM attributes

              if (item.attr) {
                $$$1.each(item.attr, function handleDOMAttributes(key, value) {
                  if (key === 'cssClass' || key === 'class') {
                    $item.addClass(value);
                  } else {
                    $item.attr(key, value);
                  }
                });
              }

              if (item.data) {
                $item.data('data', item.data);
              }

              newItems.push($item);
            });

            if (this.$pillGroup.children('.pill').length > 0) {
              if (index) {
                $neighbor = this.$pillGroup.find('.pill:nth-child(' + index + ')');

                if ($neighbor.length) {
                  $neighbor.before(newItems);
                } else {
                  this.$pillGroup.children('.pill:last').after(newItems);
                }
              } else {
                this.$pillGroup.children('.pill:last').after(newItems);
              }
            } else {
              this.$pillGroup.prepend(newItems);
            }

            if (isInternal) {
              this.$element.trigger('added.fu.pillbox', {
                text: items[0].text,
                value: items[0].value
              });
            }
          }
        },
        inputEvent: function inputEvent(e) {
          var self = this;
          var text = self.options.cleanInput(this.$addItem.val());
          var isFocusOutEvent = e.type === 'focusout';
          var blurredAfterInput = isFocusOutEvent && text.length > 0; // If we test for keycode only, it will match for `<` & `,` instead of just `,`
          // This way users can type `<3` and `1 < 3`, etc...

          var acceptKeyPressed = this.acceptKeyCodes[e.keyCode] && !isShiftHeld(e);

          if (acceptKeyPressed || blurredAfterInput) {
            var attr;
            var value;

            if (this.options.onKeyDown && this._isSuggestionsOpen()) {
              var $selection = this.$suggest.find('.pillbox-suggest-sel');

              if ($selection.length) {
                text = self.options.cleanInput($selection.html());
                value = self.options.cleanInput($selection.data('value'));
                attr = $selection.data('attr');
              }
            } // ignore comma and make sure text that has been entered (protects against " ,". https://github.com/ExactTarget/fuelux/issues/593), unless allowEmptyPills is true.


            if (text.replace(/[ ]*\,[ ]*/, '').match(/\S/) || this.options.allowEmptyPills && text.length) {
              this._closeSuggestions();

              this.$addItem.val('').hide();

              if (attr) {
                this.addItems({
                  text: text,
                  value: value,
                  attr: JSON.parse(attr)
                }, true);
              } else {
                this.addItems({
                  text: text,
                  value: value
                }, true);
              }

              setTimeout(function clearAddItemInput() {
                self.$addItem.show().attr({
                  size: 10
                }).focus();
              }, 0);
            }

            e.preventDefault();
            return true;
          } else if (isBackspaceKey(e) || isDeleteKey(e)) {
            if (!text.length) {
              e.preventDefault();

              if (this.options.edit && this.currentEdit) {
                this.cancelEdit();
                return true;
              }

              this._closeSuggestions();

              var $lastItem = this.$pillGroup.children('.pill:last');

              if ($lastItem.hasClass('pillbox-highlight')) {
                this._removeElement(this.getItemData($lastItem, {
                  el: $lastItem
                }));
              } else {
                $lastItem.addClass('pillbox-highlight');
              }

              return true;
            }
          } else if (text.length > 10) {
            if (this.$addItem.width() < this.$pillGroup.width() - 6) {
              this.$addItem.attr({
                size: text.length + 3
              });
            }
          }

          this.$pillGroup.find('.pill').removeClass('pillbox-highlight');

          if (this.options.onKeyDown && !isFocusOutEvent) {
            if (isTabKey(e) || isUpArrow(e) || isDownArrow(e)) {
              if (this._isSuggestionsOpen()) {
                this._keySuggestions(e);
              }

              return true;
            } // only allowing most recent event callback to register


            this.callbackId = e.timeStamp;
            this.options.onKeyDown({
              event: e,
              value: text
            }, function callOpenSuggestions(data) {
              self._openSuggestions(e, data);
            });
          }

          return true;
        },
        openEdit: function openEdit(el) {
          var targetChildIndex = el.index() + 1;
          var $addItemWrap = this.$addItemWrap.detach().hide();
          this.$pillGroup.find('.pill:nth-child(' + targetChildIndex + ')').before($addItemWrap);
          this.currentEdit = el.detach();
          $addItemWrap.addClass('editing');
          this.$addItem.val(el.find('span:first').html());
          $addItemWrap.show();
          this.$addItem.focus().select();
        },
        cancelEdit: function cancelEdit(e) {
          var $addItemWrap;

          if (!this.currentEdit) {
            return false;
          }

          this._closeSuggestions();

          if (e) {
            this.$addItemWrap.before(this.currentEdit);
          }

          this.currentEdit = false;
          $addItemWrap = this.$addItemWrap.detach();
          $addItemWrap.removeClass('editing');
          this.$addItem.val('');
          this.$pillGroup.append($addItemWrap);
          return true;
        },
        // Must match syntax of placeItem so addItem callback is called when an item is edited
        // expecting to receive an array back from the callback containing edited items
        saveEdit: function saveEdit() {
          var item = arguments[0][0] ? arguments[0][0] : arguments[0];
          this.currentEdit = $$$1(item.el);
          this.currentEdit.data('value', item.value);
          this.currentEdit.find('span:first').html(item.text);
          this.$addItemWrap.hide();
          this.$addItemWrap.before(this.currentEdit);
          this.currentEdit = false;
          this.$addItem.val('');
          this.$addItemWrap.removeClass('editing');
          this.$pillGroup.append(this.$addItemWrap.detach().show());
          this.$element.trigger('edited.fu.pillbox', {
            value: item.value,
            text: item.text
          });
        },
        removeBySelector: function removeBySelector() {
          var selectors = [].slice.call(arguments).slice(0);
          var self = this;
          $$$1.each(selectors, function doRemove(i, sel) {
            self.$pillGroup.find(sel).remove();
          });

          this._removePillTrigger({
            method: 'removeBySelector',
            removedSelectors: selectors
          });
        },
        removeByValue: function removeByValue() {
          var values = [].slice.call(arguments).slice(0);
          var self = this;
          $$$1.each(values, function doRemove(i, val) {
            self.$pillGroup.find('> .pill[data-value="' + val + '"]').remove();
          });

          this._removePillTrigger({
            method: 'removeByValue',
            removedValues: values
          });
        },
        removeByText: function removeByText() {
          var text = [].slice.call(arguments).slice(0);
          var self = this;
          $$$1.each(text, function doRemove(i, matchingText) {
            self.$pillGroup.find('> .pill:contains("' + matchingText + '")').remove();
          });

          this._removePillTrigger({
            method: 'removeByText',
            removedText: text
          });
        },
        truncate: function truncate(enable) {
          var self = this;
          this.$element.removeClass('truncate');
          this.$addItemWrap.removeClass('truncated');
          this.$pillGroup.find('.pill').removeClass('truncated');

          if (enable) {
            this.$element.addClass('truncate');
            var availableWidth = this.$element.width();
            var containerFull = false;
            var processedPills = 0;
            var totalPills = this.$pillGroup.find('.pill').length;
            var widthUsed = 0;
            this.$pillGroup.find('.pill').each(function processPills() {
              var pill = $$$1(this);

              if (!containerFull) {
                processedPills++;
                self.$moreCount.text(totalPills - processedPills);

                if (widthUsed + pill.outerWidth(true) + self.$addItemWrap.outerWidth(true) <= availableWidth) {
                  widthUsed += pill.outerWidth(true);
                } else {
                  self.$moreCount.text(totalPills - processedPills + 1);
                  pill.addClass('truncated');
                  containerFull = true;
                }
              } else {
                pill.addClass('truncated');
              }
            });

            if (processedPills === totalPills) {
              this.$addItemWrap.addClass('truncated');
            }
          }
        },
        inputFocus: function inputFocus() {
          this.$element.find('.pillbox-add-item').focus();
        },
        getItemData: function getItemData(el, data) {
          return $$$1.extend({
            text: el.find('span:first').html()
          }, el.data(), data);
        },
        _removeElement: function _removeElement(data) {
          data.el.remove();
          delete data.el;
          this.$element.trigger('removed.fu.pillbox', data);
        },
        _removePillTrigger: function _removePillTrigger(removedBy) {
          this.$element.trigger('removed.fu.pillbox', removedBy);
        },
        _generateObject: function _generateObject(data) {
          var obj = {};
          $$$1.each(data, function setObjectValue(index, value) {
            obj[value] = true;
          });
          return obj;
        },
        _openSuggestions: function _openSuggestions(e, data) {
          var $suggestionList = $$$1('<ul>');

          if (this.callbackId !== e.timeStamp) {
            return false;
          }

          if (data.data && data.data.length) {
            $$$1.each(data.data, function appendSuggestions(index, value) {
              var val = value.value ? value.value : value.text; // markup concatentation is 10x faster, but does not allow data store

              var $suggestion = $$$1('<li data-value="' + val + '">' + value.text + '</li>');

              if (value.attr) {
                $suggestion.data('attr', JSON.stringify(value.attr));
              }

              if (value.data) {
                $suggestion.data('data', value.data);
              }

              $suggestionList.append($suggestion);
            }); // suggestion dropdown

            this.$suggest.html('').append($suggestionList.children());
            $$$1(document).trigger('suggested.fu.pillbox', this.$suggest);
          }

          return true;
        },
        _closeSuggestions: function _closeSuggestions() {
          this.$suggest.html('').parent().removeClass('open');
        },
        _isSuggestionsOpen: function _isSuggestionsOpen() {
          return this.$suggest.parent().hasClass('open');
        },
        _keySuggestions: function _keySuggestions(e) {
          var $first = this.$suggest.find('li.pillbox-suggest-sel');
          var dir = isUpArrow(e);
          e.preventDefault();

          if (!$first.length) {
            $first = this.$suggest.find('li:first');
            $first.addClass('pillbox-suggest-sel');
          } else {
            var $next = dir ? $first.prev() : $first.next();

            if (!$next.length) {
              $next = dir ? this.$suggest.find('li:last') : this.$suggest.find('li:first');
            }

            if ($next) {
              $next.addClass('pillbox-suggest-sel');
              $first.removeClass('pillbox-suggest-sel');
            }
          }
        }
      };
      Pillbox.prototype.getValue = Pillbox.prototype.items; // PILLBOX PLUGIN DEFINITION

      $$$1.fn.pillbox = function pillbox(option) {
        var args = Array.prototype.slice.call(arguments, 1);
        var methodReturn;
        var $set = this.each(function set() {
          var $this = $$$1(this);
          var data = $this.data('fu.pillbox');
          var options = typeof option === 'object' && option;

          if (!data) {
            $this.data('fu.pillbox', data = new Pillbox(this, options));
          }

          if (typeof option === 'string') {
            methodReturn = data[option].apply(data, args);
          }
        });
        return methodReturn === undefined ? $set : methodReturn;
      };

      $$$1.fn.pillbox.defaults = {
        edit: false,
        readonly: -1,
        // can be true or false. -1 means it will check for data-readonly="readonly"
        truncate: false,
        acceptKeyCodes: [ENTER_KEYCODE, COMMA_KEYCODE],
        allowEmptyPills: false,
        cleanInput: cleanInput // example on remove

        /* onRemove: function(data,callback){
        	console.log('onRemove');
        	callback(data);
        } */
        // example on key down

        /* onKeyDown: function(event, data, callback ){
        	callback({data:[
        		{text: Math.random(),value:'sdfsdfsdf'},
        		{text: Math.random(),value:'sdfsdfsdf'}
        	]});
        }
        */
        // example onAdd

        /* onAdd: function( data, callback ){
        	console.log(data, callback);
        	callback(data);
        } */

      };
      $$$1.fn.pillbox.Constructor = Pillbox;

      $$$1.fn.pillbox.noConflict = function noConflict() {
        $$$1.fn.pillbox = old;
        return this;
      }; // DATA-API


      $$$1(document).on('mousedown.fu.pillbox.data-api', '[data-initialize=pillbox]', function dataAPI(e) {
        var $control = $$$1(e.target).closest('.pillbox');

        if (!$control.data('fu.pillbox')) {
          $control.pillbox($control.data());
        }
      }); // Must be domReady for AMD compatibility

      $$$1(function DOMReady() {
        $$$1('[data-initialize=pillbox]').each(function init() {
          var $this = $$$1(this);
          if ($this.data('fu.pillbox')) return;
          $this.pillbox($this.data());
        });
      });
    })(jQuery);

    (function ($$$1) {
      /* global jQuery:true */

      /*
       * Fuel UX Repeater
       * https://github.com/ExactTarget/fuelux
       *
       * Copyright (c) 2014 ExactTarget
       * Licensed under the BSD New license.
       */
      // -- BEGIN MODULE CODE HERE --
      var old = $$$1.fn.repeater; // REPEATER CONSTRUCTOR AND PROTOTYPE

      var Repeater = function Repeater(element, options) {
        var self = this;
        var $btn;
        var currentView;
        this.$element = $$$1(element);
        this.$canvas = this.$element.find('.repeater-canvas');
        this.$count = this.$element.find('.repeater-count');
        this.$end = this.$element.find('.repeater-end');
        this.$filters = this.$element.find('.repeater-filters');
        this.$loader = this.$element.find('.repeater-loader');
        this.$pageSize = this.$element.find('.repeater-itemization .selectlist');
        this.$nextBtn = this.$element.find('.repeater-next');
        this.$pages = this.$element.find('.repeater-pages');
        this.$prevBtn = this.$element.find('.repeater-prev');
        this.$primaryPaging = this.$element.find('.repeater-primaryPaging');
        this.$search = this.$element.find('.repeater-search').find('.search');
        this.$secondaryPaging = this.$element.find('.repeater-secondaryPaging');
        this.$start = this.$element.find('.repeater-start');
        this.$viewport = this.$element.find('.repeater-viewport');
        this.$views = this.$element.find('.repeater-views');
        this.currentPage = 0;
        this.currentView = null;
        this.isDisabled = false;

        this.infiniteScrollingCallback = function noop() {};

        this.infiniteScrollingCont = null;
        this.infiniteScrollingEnabled = false;
        this.infiniteScrollingEnd = null;
        this.infiniteScrollingOptions = {};
        this.lastPageInput = 0;
        this.options = $$$1.extend({}, $$$1.fn.repeater.defaults, options);
        this.pageIncrement = 0; // store direction navigated

        this.resizeTimeout = {};
        this.stamp = new Date().getTime() + (Math.floor(Math.random() * 100) + 1);
        this.storedDataSourceOpts = null;
        this.syncingViewButtonState = false;
        this.viewOptions = {};
        this.viewType = null;
        this.$filters.selectlist();
        this.$pageSize.selectlist();
        this.$primaryPaging.find('.combobox').combobox();
        this.$search.search({
          searchOnKeyPress: this.options.searchOnKeyPress,
          allowCancel: this.options.allowCancel
        });
        this.$filters.on('changed.fu.selectlist', function onFiltersChanged(e, value) {
          self.$element.trigger('filtered.fu.repeater', value);
          self.render({
            clearInfinite: true,
            pageIncrement: null
          });
        });
        this.$nextBtn.on('click.fu.repeater', $$$1.proxy(this.next, this));
        this.$pageSize.on('changed.fu.selectlist', function onPageSizeChanged(e, value) {
          self.$element.trigger('pageSizeChanged.fu.repeater', value);
          self.render({
            pageIncrement: null
          });
        });
        this.$prevBtn.on('click.fu.repeater', $$$1.proxy(this.previous, this));
        this.$primaryPaging.find('.combobox').on('changed.fu.combobox', function onPrimaryPagingChanged(evt, data) {
          self.pageInputChange(data.text, data);
        });
        this.$search.on('searched.fu.search cleared.fu.search', function onSearched(e, value) {
          self.$element.trigger('searchChanged.fu.repeater', value);
          self.render({
            clearInfinite: true,
            pageIncrement: null
          });
        });
        this.$search.on('canceled.fu.search', function onSearchCanceled(e, value) {
          self.$element.trigger('canceled.fu.repeater', value);
          self.render({
            clearInfinite: true,
            pageIncrement: null
          });
        });
        this.$secondaryPaging.on('blur.fu.repeater', function onSecondaryPagingBlur() {
          self.pageInputChange(self.$secondaryPaging.val());
        });
        this.$secondaryPaging.on('keyup', function onSecondaryPagingKeyup(e) {
          if (e.keyCode === 13) {
            self.pageInputChange(self.$secondaryPaging.val());
          }
        });
        this.$views.find('input').on('change.fu.repeater', $$$1.proxy(this.viewChanged, this));
        $$$1(window).on('resize.fu.repeater.' + this.stamp, function onResizeRepeater() {
          clearTimeout(self.resizeTimeout);
          self.resizeTimeout = setTimeout(function resizeTimeout() {
            self.resize();
            self.$element.trigger('resized.fu.repeater');
          }, 75);
        });
        this.$loader.loader();
        this.$loader.loader('pause');

        if (this.options.defaultView !== -1) {
          currentView = this.options.defaultView;
        } else {
          $btn = this.$views.find('label.active input');
          currentView = $btn.length > 0 ? $btn.val() : 'list';
        }

        this.setViewOptions(currentView);
        this.initViewTypes(function initViewTypes() {
          self.resize();
          self.$element.trigger('resized.fu.repeater');
          self.render({
            changeView: currentView
          });
        });
      };

      var logWarn = function logWarn(msg) {
        if (window.console && window.console.warn) {
          window.console.warn(msg);
        }
      };

      var scan = function scan(cont) {
        var keep = [];
        cont.children().each(function eachContainerChild() {
          var item = $$$1(this);
          var pres = item.attr('data-preserve');

          if (pres === 'deep') {
            item.detach();
            keep.push(item);
          } else if (pres === 'shallow') {
            scan(item);
            item.detach();
            keep.push(item);
          }
        });
        cont.empty();
        cont.append(keep);
      };

      var addItem = function addItem($parent, response) {
        var action;

        if (response) {
          action = response.action ? response.action : 'append';

          if (action !== 'none' && response.item !== undefined) {
            var $container = response.container !== undefined ? $$$1(response.container) : $parent;
            $container[action](response.item);
          }
        }
      };

      var callNextInit = function callNextInit(currentViewType, viewTypes, callback) {
        var nextViewType = currentViewType + 1;

        if (nextViewType < viewTypes.length) {
          initViewType.call(this, nextViewType, viewTypes, callback);
        } else {
          callback();
        }
      };

      var initViewType = function initViewType(currentViewtype, viewTypes, callback) {
        if (viewTypes[currentViewtype].initialize) {
          viewTypes[currentViewtype].initialize.call(this, {}, function afterInitialize() {
            callNextInit.call(this, currentViewtype, viewTypes, callback);
          });
        } else {
          callNextInit.call(this, currentViewtype, viewTypes, callback);
        }
      }; // Does all of our cleanup post-render


      var afterRender = function afterRender(state) {
        var data = state.data || {};

        if (this.infiniteScrollingEnabled) {
          if (state.viewChanged || state.options.clearInfinite) {
            this.initInfiniteScrolling();
          }

          this.infiniteScrollPaging(data, state.options);
        }

        this.$loader.hide().loader('pause');
        this.enable();
        this.$search.trigger('rendered.fu.repeater', {
          data: data,
          options: state.dataOptions,
          renderOptions: state.options
        });
        this.$element.trigger('rendered.fu.repeater', {
          data: data,
          options: state.dataOptions,
          renderOptions: state.options
        }); // for maintaining support of 'loaded' event

        this.$element.trigger('loaded.fu.repeater', state.dataOptions);
      }; // This does the actual rendering of the repeater


      var doRender = function doRender(state) {
        var data = state.data || {};

        if (this.infiniteScrollingEnabled) {
          // pass empty object because data handled in infiniteScrollPaging method
          this.infiniteScrollingCallback({});
        } else {
          this.itemization(data);
          this.pagination(data);
        }

        var self = this;
        this.renderItems(state.viewTypeObj, data, function callAfterRender(d) {
          state.data = d;
          afterRender.call(self, state);
        });
      };

      Repeater.prototype = {
        constructor: Repeater,
        clear: function clear(opts) {
          var options = opts || {};

          if (!options.preserve) {
            // Just trash everything because preserve is false
            this.$canvas.empty();
          } else if (!this.infiniteScrollingEnabled || options.clearInfinite) {
            // Preserve clear only if infiniteScrolling is disabled or if specifically told to do so
            scan(this.$canvas);
          } // Otherwise don't clear because infiniteScrolling is enabled
          // If viewChanged and current viewTypeObj has a cleared function, call it


          var viewChanged = options.viewChanged !== undefined ? options.viewChanged : false;
          var viewTypeObj = $$$1.fn.repeater.viewTypes[this.viewType] || {};

          if (!viewChanged && viewTypeObj.cleared) {
            viewTypeObj.cleared.call(this, {
              options: options
            });
          }
        },
        clearPreservedDataSourceOptions: function clearPreservedDataSourceOptions() {
          this.storedDataSourceOpts = null;
        },
        destroy: function destroy() {
          var markup; // set input value attrbute in markup

          this.$element.find('input').each(function eachInput() {
            $$$1(this).attr('value', $$$1(this).val());
          }); // empty elements to return to original markup

          this.$canvas.empty();
          markup = this.$element[0].outerHTML; // destroy components and remove leftover

          this.$element.find('.combobox').combobox('destroy');
          this.$element.find('.selectlist').selectlist('destroy');
          this.$element.find('.search').search('destroy');

          if (this.infiniteScrollingEnabled) {
            $$$1(this.infiniteScrollingCont).infinitescroll('destroy');
          }

          this.$element.remove(); // any external events

          $$$1(window).off('resize.fu.repeater.' + this.stamp);
          return markup;
        },
        disable: function disable() {
          var viewTypeObj = $$$1.fn.repeater.viewTypes[this.viewType] || {};
          this.$search.search('disable');
          this.$filters.selectlist('disable');
          this.$views.find('label, input').addClass('disabled').attr('disabled', 'disabled');
          this.$pageSize.selectlist('disable');
          this.$primaryPaging.find('.combobox').combobox('disable');
          this.$secondaryPaging.attr('disabled', 'disabled');
          this.$prevBtn.attr('disabled', 'disabled');
          this.$nextBtn.attr('disabled', 'disabled');

          if (viewTypeObj.enabled) {
            viewTypeObj.enabled.call(this, {
              status: false
            });
          }

          this.isDisabled = true;
          this.$element.addClass('disabled');
          this.$element.trigger('disabled.fu.repeater');
        },
        enable: function enable() {
          var viewTypeObj = $$$1.fn.repeater.viewTypes[this.viewType] || {};
          this.$search.search('enable');
          this.$filters.selectlist('enable');
          this.$views.find('label, input').removeClass('disabled').removeAttr('disabled');
          this.$pageSize.selectlist('enable');
          this.$primaryPaging.find('.combobox').combobox('enable');
          this.$secondaryPaging.removeAttr('disabled');

          if (!this.$prevBtn.hasClass('page-end')) {
            this.$prevBtn.removeAttr('disabled');
          }

          if (!this.$nextBtn.hasClass('page-end')) {
            this.$nextBtn.removeAttr('disabled');
          } // is 0 or 1 pages, if using $primaryPaging (combobox)
          // if using selectlist allow user to use selectlist to select 0 or 1


          if (this.$prevBtn.hasClass('page-end') && this.$nextBtn.hasClass('page-end')) {
            this.$primaryPaging.combobox('disable');
          } // if there are no items


          if (parseInt(this.$count.html(), 10) !== 0) {
            this.$pageSize.selectlist('enable');
          } else {
            this.$pageSize.selectlist('disable');
          }

          if (viewTypeObj.enabled) {
            viewTypeObj.enabled.call(this, {
              status: true
            });
          }

          this.isDisabled = false;
          this.$element.removeClass('disabled');
          this.$element.trigger('enabled.fu.repeater');
        },
        getDataOptions: function getDataOptions(opts) {
          var options = opts || {};

          if (options.pageIncrement !== undefined) {
            if (options.pageIncrement === null) {
              this.currentPage = 0;
            } else {
              this.currentPage += options.pageIncrement;
            }
          }

          var dataSourceOptions = {};

          if (options.dataSourceOptions) {
            dataSourceOptions = options.dataSourceOptions;

            if (options.preserveDataSourceOptions) {
              if (this.storedDataSourceOpts) {
                this.storedDataSourceOpts = $$$1.extend(this.storedDataSourceOpts, dataSourceOptions);
              } else {
                this.storedDataSourceOpts = dataSourceOptions;
              }
            }
          }

          if (this.storedDataSourceOpts) {
            dataSourceOptions = $$$1.extend(this.storedDataSourceOpts, dataSourceOptions);
          }

          var returnOptions = {
            view: this.currentView,
            pageIndex: this.currentPage,
            filter: {
              text: 'All',
              value: 'all'
            }
          };

          if (this.$filters.length > 0) {
            returnOptions.filter = this.$filters.selectlist('selectedItem');
          }

          if (!this.infiniteScrollingEnabled) {
            returnOptions.pageSize = 25;

            if (this.$pageSize.length > 0) {
              returnOptions.pageSize = parseInt(this.$pageSize.selectlist('selectedItem').value, 10);
            }
          }

          var searchValue = this.$search && this.$search.find('input') && this.$search.find('input').val();

          if (searchValue !== '') {
            returnOptions.search = searchValue;
          }

          var viewType = $$$1.fn.repeater.viewTypes[this.viewType] || {};
          var addViewTypeData = viewType.dataOptions;

          if (addViewTypeData) {
            returnOptions = addViewTypeData.call(this, returnOptions);
          }

          returnOptions = $$$1.extend(returnOptions, dataSourceOptions);
          return returnOptions;
        },
        infiniteScrolling: function infiniteScrolling(enable, opts) {
          var footer = this.$element.find('.repeater-footer');
          var viewport = this.$element.find('.repeater-viewport');
          var options = opts || {};

          if (enable) {
            this.infiniteScrollingEnabled = true;
            this.infiniteScrollingEnd = options.end;
            delete options.dataSource;
            delete options.end;
            this.infiniteScrollingOptions = options;
            viewport.css({
              height: viewport.height() + footer.outerHeight()
            });
            footer.hide();
          } else {
            var cont = this.infiniteScrollingCont;
            var data = cont.data();
            delete data.infinitescroll;
            cont.off('scroll');
            cont.removeClass('infinitescroll');
            this.infiniteScrollingCont = null;
            this.infiniteScrollingEnabled = false;
            this.infiniteScrollingEnd = null;
            this.infiniteScrollingOptions = {};
            viewport.css({
              height: viewport.height() - footer.outerHeight()
            });
            footer.show();
          }
        },
        infiniteScrollPaging: function infiniteScrollPaging(data) {
          var end = this.infiniteScrollingEnd !== true ? this.infiniteScrollingEnd : undefined;
          var page = data.page;
          var pages = data.pages;
          this.currentPage = page !== undefined ? page : NaN;

          if (this.infiniteScrollingCont) {
            if (data.end === true || this.currentPage + 1 >= pages) {
              this.infiniteScrollingCont.infinitescroll('end', end);
            } else {
              this.infiniteScrollingCont.infinitescroll('onScroll');
            }
          }
        },
        initInfiniteScrolling: function initInfiniteScrolling() {
          var cont = this.$canvas.find('[data-infinite="true"]:first');
          cont = cont.length < 1 ? this.$canvas : cont;

          if (cont.data('fu.infinitescroll')) {
            cont.infinitescroll('enable');
          } else {
            var self = this;
            var opts = $$$1.extend({}, this.infiniteScrollingOptions);

            opts.dataSource = function dataSource(helpers, callback) {
              self.infiniteScrollingCallback = callback;
              self.render({
                pageIncrement: 1
              });
            };

            cont.infinitescroll(opts);
            this.infiniteScrollingCont = cont;
          }
        },
        initViewTypes: function initViewTypes(callback) {
          var viewTypes = [];

          for (var key in $$$1.fn.repeater.viewTypes) {
            if ({}.hasOwnProperty.call($$$1.fn.repeater.viewTypes, key)) {
              viewTypes.push($$$1.fn.repeater.viewTypes[key]);
            }
          }

          if (viewTypes.length > 0) {
            initViewType.call(this, 0, viewTypes, callback);
          } else {
            callback();
          }
        },
        itemization: function itemization(data) {
          this.$count.html(data.count !== undefined ? data.count : '?');
          this.$end.html(data.end !== undefined ? data.end : '?');
          this.$start.html(data.start !== undefined ? data.start : '?');
        },
        next: function next() {
          this.$nextBtn.attr('disabled', 'disabled');
          this.$prevBtn.attr('disabled', 'disabled');
          this.pageIncrement = 1;
          this.$element.trigger('nextClicked.fu.repeater');
          this.render({
            pageIncrement: this.pageIncrement
          });
        },
        pageInputChange: function pageInputChange(val, dataFromCombobox) {
          // dataFromCombobox is a proxy for data from combobox's changed event,
          // if no combobox is present data will be undefined
          var pageInc;

          if (val !== this.lastPageInput) {
            this.lastPageInput = val;
            var value = parseInt(val, 10) - 1;
            pageInc = value - this.currentPage;
            this.$element.trigger('pageChanged.fu.repeater', [value, dataFromCombobox]);
            this.render({
              pageIncrement: pageInc
            });
          }
        },
        pagination: function pagination(data) {
          this.$primaryPaging.removeClass('active');
          this.$secondaryPaging.removeClass('active');
          var totalPages = data.pages;
          this.currentPage = data.page !== undefined ? data.page : NaN; // set paging to 0 if total pages is 0, otherwise use one-based index

          var currenPageOutput = totalPages === 0 ? 0 : this.currentPage + 1;

          if (totalPages <= this.viewOptions.dropPagingCap) {
            this.$primaryPaging.addClass('active');
            var dropMenu = this.$primaryPaging.find('.dropdown-menu');
            dropMenu.empty();

            for (var i = 0; i < totalPages; i++) {
              var l = i + 1;
              dropMenu.append('<li data-value="' + l + '"><a href="#">' + l + '</a></li>');
            }

            this.$primaryPaging.find('input.form-control').val(currenPageOutput);
          } else {
            this.$secondaryPaging.addClass('active');
            this.$secondaryPaging.val(currenPageOutput);
          }

          this.lastPageInput = this.currentPage + 1 + '';
          this.$pages.html('' + totalPages); // this is not the last page

          if (this.currentPage + 1 < totalPages) {
            this.$nextBtn.removeAttr('disabled');
            this.$nextBtn.removeClass('page-end');
          } else {
            this.$nextBtn.attr('disabled', 'disabled');
            this.$nextBtn.addClass('page-end');
          } // this is not the first page


          if (this.currentPage - 1 >= 0) {
            this.$prevBtn.removeAttr('disabled');
            this.$prevBtn.removeClass('page-end');
          } else {
            this.$prevBtn.attr('disabled', 'disabled');
            this.$prevBtn.addClass('page-end');
          } // return focus to next/previous buttons after navigating


          if (this.pageIncrement !== 0) {
            if (this.pageIncrement > 0) {
              if (this.$nextBtn.is(':disabled')) {
                // if you can't focus, go the other way
                this.$prevBtn.focus();
              } else {
                this.$nextBtn.focus();
              }
            } else if (this.$prevBtn.is(':disabled')) {
              // if you can't focus, go the other way
              this.$nextBtn.focus();
            } else {
              this.$prevBtn.focus();
            }
          }
        },
        previous: function previous() {
          this.$nextBtn.attr('disabled', 'disabled');
          this.$prevBtn.attr('disabled', 'disabled');
          this.pageIncrement = -1;
          this.$element.trigger('previousClicked.fu.repeater');
          this.render({
            pageIncrement: this.pageIncrement
          });
        },
        // This functions more as a "pre-render" than a true "render"
        render: function render(opts) {
          this.disable();
          var viewChanged = false;
          var viewTypeObj = $$$1.fn.repeater.viewTypes[this.viewType] || {};
          var options = opts || {};

          if (options.changeView && this.currentView !== options.changeView) {
            var prevView = this.currentView;
            this.currentView = options.changeView;
            this.viewType = this.currentView.split('.')[0];
            this.setViewOptions(this.currentView);
            this.$element.attr('data-currentview', this.currentView);
            this.$element.attr('data-viewtype', this.viewType);
            viewChanged = true;
            options.viewChanged = viewChanged;
            this.$element.trigger('viewChanged.fu.repeater', this.currentView);

            if (this.infiniteScrollingEnabled) {
              this.infiniteScrolling(false);
            }

            viewTypeObj = $$$1.fn.repeater.viewTypes[this.viewType] || {};

            if (viewTypeObj.selected) {
              viewTypeObj.selected.call(this, {
                prevView: prevView
              });
            }
          }

          this.syncViewButtonState();
          options.preserve = options.preserve !== undefined ? options.preserve : !viewChanged;
          this.clear(options);

          if (!this.infiniteScrollingEnabled || this.infiniteScrollingEnabled && viewChanged) {
            this.$loader.show().loader('play');
          }

          var dataOptions = this.getDataOptions(options);
          var beforeRender = this.viewOptions.dataSource;
          var repeaterPrototypeContext = this;
          beforeRender(dataOptions, // this serves as a bridge function to pass all required data through to the actual function
          // that does the rendering for us.
          function callDoRender(dataSourceReturnedData) {
            doRender.call(repeaterPrototypeContext, {
              data: dataSourceReturnedData,
              dataOptions: dataOptions,
              options: options,
              viewChanged: viewChanged,
              viewTypeObj: viewTypeObj
            });
          });
        },
        resize: function resize() {
          var staticHeight = this.viewOptions.staticHeight === -1 ? this.$element.attr('data-staticheight') : this.viewOptions.staticHeight;
          var viewTypeObj = {};
          var height;
          var viewportMargins;
          var scrubbedElements = [];
          var previousProperties = [];
          var $hiddenElements = this.$element.parentsUntil(':visible').addBack();
          var currentHiddenElement;
          var currentElementIndex = 0; // Set parents to 'display:block' until repeater is visible again

          while (currentElementIndex < $hiddenElements.length && this.$element.is(':hidden')) {
            currentHiddenElement = $hiddenElements[currentElementIndex]; // Only set display property on elements that are explicitly hidden (i.e. do not inherit it from their parent)

            if ($$$1(currentHiddenElement).is(':hidden')) {
              previousProperties.push(currentHiddenElement.style['display']);
              currentHiddenElement.style['display'] = 'block';
              scrubbedElements.push(currentHiddenElement);
            }

            currentElementIndex++;
          }

          if (this.viewType) {
            viewTypeObj = $$$1.fn.repeater.viewTypes[this.viewType] || {};
          }

          if (staticHeight !== undefined && staticHeight !== false && staticHeight !== 'false') {
            this.$canvas.addClass('scrolling');
            viewportMargins = {
              bottom: this.$viewport.css('margin-bottom'),
              top: this.$viewport.css('margin-top')
            };
            var staticHeightValue = staticHeight === 'true' || staticHeight === true ? this.$element.height() : parseInt(staticHeight, 10);
            var headerHeight = this.$element.find('.repeater-header').outerHeight();
            var footerHeight = this.$element.find('.repeater-footer').outerHeight();
            var bottomMargin = viewportMargins.bottom === 'auto' ? 0 : parseInt(viewportMargins.bottom, 10);
            var topMargin = viewportMargins.top === 'auto' ? 0 : parseInt(viewportMargins.top, 10);
            height = staticHeightValue - headerHeight - footerHeight - bottomMargin - topMargin;
            this.$viewport.outerHeight(height);
          } else {
            this.$canvas.removeClass('scrolling');
          }

          if (viewTypeObj.resize) {
            viewTypeObj.resize.call(this, {
              height: this.$element.outerHeight(),
              width: this.$element.outerWidth()
            });
          }

          scrubbedElements.forEach(function (element, i) {
            element.style['display'] = previousProperties[i];
          });
        },
        // e.g. "Rows" or "Thumbnails"
        renderItems: function renderItems(viewTypeObj, data, callback) {
          if (!viewTypeObj.render) {
            if (viewTypeObj.before) {
              var addBefore = viewTypeObj.before.call(this, {
                container: this.$canvas,
                data: data
              });
              addItem(this.$canvas, addBefore);
            }

            var $dataContainer = this.$canvas.find('[data-container="true"]:last');
            var $container = $dataContainer.length > 0 ? $dataContainer : this.$canvas; // It appears that the following code would theoretically allow you to pass a deeply
            // nested value to "repeat on" to be added to the repeater.
            // eg. `data.foo.bar.items`

            if (viewTypeObj.renderItem) {
              var subset;
              var objectAndPropsToRepeatOnString = viewTypeObj.repeat || 'data.items';
              var objectAndPropsToRepeatOn = objectAndPropsToRepeatOnString.split('.');
              var objectToRepeatOn = objectAndPropsToRepeatOn[0];

              if (objectToRepeatOn === 'data' || objectToRepeatOn === 'this') {
                subset = objectToRepeatOn === 'this' ? this : data; // Extracts subset from object chain (get `items` out of `foo.bar.items`). I think....

                var propsToRepeatOn = objectAndPropsToRepeatOn.slice(1);

                for (var prop = 0; prop < propsToRepeatOn.length; prop++) {
                  if (subset[propsToRepeatOn[prop]] !== undefined) {
                    subset = subset[propsToRepeatOn[prop]];
                  } else {
                    subset = [];
                    logWarn('WARNING: Repeater unable to find property to iterate renderItem on.');
                    break;
                  }
                }

                for (var subItemIndex = 0; subItemIndex < subset.length; subItemIndex++) {
                  var addSubItem = viewTypeObj.renderItem.call(this, {
                    container: $container,
                    data: data,
                    index: subItemIndex,
                    subset: subset
                  });
                  addItem($container, addSubItem);
                }
              } else {
                logWarn('WARNING: Repeater plugin "repeat" value must start with either "data" or "this"');
              }
            }

            if (viewTypeObj.after) {
              var addAfter = viewTypeObj.after.call(this, {
                container: this.$canvas,
                data: data
              });
              addItem(this.$canvas, addAfter);
            }

            callback(data);
          } else {
            viewTypeObj.render.call(this, {
              container: this.$canvas,
              data: data
            }, callback);
          }
        },
        setViewOptions: function setViewOptions(curView) {
          var opts = {};
          var viewName = curView.split('.')[1];

          if (this.options.views) {
            opts = this.options.views[viewName] || this.options.views[curView] || {};
          } else {
            opts = {};
          }

          this.viewOptions = $$$1.extend({}, this.options, opts);
        },
        viewChanged: function viewChanged(e) {
          var $selected = $$$1(e.target);
          var val = $selected.val();

          if (!this.syncingViewButtonState) {
            if (this.isDisabled || $selected.parents('label:first').hasClass('disabled')) {
              this.syncViewButtonState();
            } else {
              this.render({
                changeView: val,
                pageIncrement: null
              });
            }
          }
        },
        syncViewButtonState: function syncViewButtonState() {
          var $itemToCheck = this.$views.find('input[value="' + this.currentView + '"]');
          this.syncingViewButtonState = true;
          this.$views.find('input').prop('checked', false);
          this.$views.find('label.active').removeClass('active');

          if ($itemToCheck.length > 0) {
            $itemToCheck.prop('checked', true);
            $itemToCheck.parents('label:first').addClass('active');
          }

          this.syncingViewButtonState = false;
        }
      }; // For backwards compatibility.

      Repeater.prototype.runRenderer = Repeater.prototype.renderItems; // REPEATER PLUGIN DEFINITION

      $$$1.fn.repeater = function fnrepeater(option) {
        var args = Array.prototype.slice.call(arguments, 1);
        var methodReturn;
        var $set = this.each(function eachThis() {
          var $this = $$$1(this);
          var data = $this.data('fu.repeater');
          var options = typeof option === 'object' && option;

          if (!data) {
            $this.data('fu.repeater', data = new Repeater(this, options));
          }

          if (typeof option === 'string') {
            methodReturn = data[option].apply(data, args);
          }
        });
        return methodReturn === undefined ? $set : methodReturn;
      };

      $$$1.fn.repeater.defaults = {
        dataSource: function dataSource(options, callback) {
          callback({
            count: 0,
            end: 0,
            items: [],
            page: 0,
            pages: 1,
            start: 0
          });
        },
        defaultView: -1,
        // should be a string value. -1 means it will grab the active view from the view controls
        dropPagingCap: 10,
        staticHeight: -1,
        // normally true or false. -1 means it will look for data-staticheight on the element
        views: null,
        // can be set to an object to configure multiple views of the same type,
        searchOnKeyPress: false,
        allowCancel: true
      };
      $$$1.fn.repeater.viewTypes = {};
      $$$1.fn.repeater.Constructor = Repeater;

      $$$1.fn.repeater.noConflict = function noConflict() {
        $$$1.fn.repeater = old;
        return this;
      };
    })(jQuery);

    (function ($$$1) {
      /* global jQuery:true */

      /*
       * Fuel UX Repeater - List View Plugin
       * https://github.com/ExactTarget/fuelux
       *
       * Copyright (c) 2014 ExactTarget
       * Licensed under the BSD New license.
       */
      // -- BEGIN MODULE CODE HERE --
      if ($$$1.fn.repeater) {
        // ADDITIONAL METHODS
        $$$1.fn.repeater.Constructor.prototype.list_clearSelectedItems = function listClearSelectedItems() {
          this.$canvas.find('.repeater-list-check').remove();
          this.$canvas.find('.repeater-list table tbody tr.selected').removeClass('selected');
        };

        $$$1.fn.repeater.Constructor.prototype.list_highlightColumn = function listHighlightColumn(index, force) {
          var tbody = this.$canvas.find('.repeater-list-wrapper > table tbody');

          if (this.viewOptions.list_highlightSortedColumn || force) {
            tbody.find('td.sorted').removeClass('sorted');
            tbody.find('tr').each(function eachTR() {
              var col = $$$1(this).find('td:nth-child(' + (index + 1) + ')').filter(function filterChildren() {
                return !$$$1(this).parent().hasClass('empty');
              });
              col.addClass('sorted');
            });
          }
        };

        $$$1.fn.repeater.Constructor.prototype.list_getSelectedItems = function listGetSelectedItems() {
          var selected = [];
          this.$canvas.find('.repeater-list .repeater-list-wrapper > table tbody tr.selected').each(function eachSelectedTR() {
            var $item = $$$1(this);
            selected.push({
              data: $item.data('item_data'),
              element: $item
            });
          });
          return selected;
        };

        $$$1.fn.repeater.Constructor.prototype.getValue = $$$1.fn.repeater.Constructor.prototype.list_getSelectedItems;

        $$$1.fn.repeater.Constructor.prototype.list_positionHeadings = function listPositionHeadings() {
          var $wrapper = this.$element.find('.repeater-list-wrapper');
          var offsetLeft = $wrapper.offset().left;
          var scrollLeft = $wrapper.scrollLeft();

          if (scrollLeft > 0) {
            $wrapper.find('.repeater-list-heading').each(function eachListHeading() {
              var $heading = $$$1(this);
              var left = $heading.parents('th:first').offset().left - offsetLeft + 'px';
              $heading.addClass('shifted').css('left', left);
            });
          } else {
            $wrapper.find('.repeater-list-heading').each(function eachListHeading() {
              $$$1(this).removeClass('shifted').css('left', '');
            });
          }
        };

        $$$1.fn.repeater.Constructor.prototype.list_setSelectedItems = function listSetSelectedItems(itms, force) {
          var selectable = this.viewOptions.list_selectable;
          var self = this;
          var data;
          var i;
          var $item;
          var length;
          var items = itms;

          if (!$$$1.isArray(items)) {
            items = [items];
          } // this function is necessary because lint yells when a function is in a loop


          var checkIfItemMatchesValue = function checkIfItemMatchesValue(rowIndex) {
            $item = $$$1(this);
            data = $item.data('item_data') || {};

            if (data[items[i].property] === items[i].value) {
              selectItem($item, items[i].selected, rowIndex);
            }
          };

          var selectItem = function selectItem($itm, slct, index) {
            var $frozenCols;
            var select = slct !== undefined ? slct : true;

            if (select) {
              if (!force && selectable !== 'multi') {
                self.list_clearSelectedItems();
              }

              if (!$itm.hasClass('selected')) {
                $itm.addClass('selected');

                if (self.viewOptions.list_frozenColumns || self.viewOptions.list_selectable === 'multi') {
                  $frozenCols = self.$element.find('.frozen-column-wrapper tr:nth-child(' + (index + 1) + ')');
                  $frozenCols.addClass('selected');
                  $frozenCols.find('.repeater-select-checkbox').addClass('checked');
                }

                if (self.viewOptions.list_actions) {
                  self.$element.find('.actions-column-wrapper tr:nth-child(' + (index + 1) + ')').addClass('selected');
                }

                $itm.find('td:first').prepend('<div class="repeater-list-check"><span class="glyphicon glyphicon-ok"></span></div>');
              }
            } else {
              if (self.viewOptions.list_frozenColumns) {
                $frozenCols = self.$element.find('.frozen-column-wrapper tr:nth-child(' + (index + 1) + ')');
                $frozenCols.addClass('selected');
                $frozenCols.find('.repeater-select-checkbox').removeClass('checked');
              }

              if (self.viewOptions.list_actions) {
                self.$element.find('.actions-column-wrapper tr:nth-child(' + (index + 1) + ')').removeClass('selected');
              }

              $itm.find('.repeater-list-check').remove();
              $itm.removeClass('selected');
            }
          };

          if (force === true || selectable === 'multi') {
            length = items.length;
          } else if (selectable) {
            length = items.length > 0 ? 1 : 0;
          } else {
            length = 0;
          }

          for (i = 0; i < length; i++) {
            if (items[i].index !== undefined) {
              $item = this.$canvas.find('.repeater-list .repeater-list-wrapper > table tbody tr:nth-child(' + (items[i].index + 1) + ')');

              if ($item.length > 0) {
                selectItem($item, items[i].selected, items[i].index);
              }
            } else if (items[i].property !== undefined && items[i].value !== undefined) {
              this.$canvas.find('.repeater-list .repeater-list-wrapper > table tbody tr').each(checkIfItemMatchesValue);
            }
          }
        };

        $$$1.fn.repeater.Constructor.prototype.list_sizeHeadings = function listSizeHeadings() {
          var $table = this.$element.find('.repeater-list table');
          $table.find('thead th').each(function eachTH() {
            var $th = $$$1(this);
            var $heading = $th.find('.repeater-list-heading');
            $heading.css({
              height: $th.outerHeight()
            });
            $heading.outerWidth($heading.data('forced-width') || $th.outerWidth());
          });
        };

        $$$1.fn.repeater.Constructor.prototype.list_setFrozenColumns = function listSetFrozenColumns() {
          var frozenTable = this.$canvas.find('.table-frozen');
          var $wrapper = this.$element.find('.repeater-canvas');
          var $table = this.$element.find('.repeater-list .repeater-list-wrapper > table');
          var repeaterWrapper = this.$element.find('.repeater-list');
          var numFrozenColumns = this.viewOptions.list_frozenColumns;
          var self = this;

          if (this.viewOptions.list_selectable === 'multi') {
            numFrozenColumns = numFrozenColumns + 1;
            $wrapper.addClass('multi-select-enabled');
          }

          if (frozenTable.length < 1) {
            // setup frozen column markup
            // main wrapper and remove unneeded columns
            var $frozenColumnWrapper = $$$1('<div class="frozen-column-wrapper"></div>').insertBefore($table);
            var $frozenColumn = $table.clone().addClass('table-frozen');
            $frozenColumn.find('th:not(:lt(' + numFrozenColumns + '))').remove();
            $frozenColumn.find('td:not(:nth-child(n+0):nth-child(-n+' + numFrozenColumns + '))').remove(); // need to set absolute heading for vertical scrolling

            var $frozenThead = $frozenColumn.clone().removeClass('table-frozen');
            $frozenThead.find('tbody').remove();
            var $frozenTheadWrapper = $$$1('<div class="frozen-thead-wrapper"></div>').append($frozenThead); // this gets a little messy with all the cloning. We need to make sure the ID and FOR
            // attribs are unique for the 'top most' cloned checkbox

            var $checkboxLabel = $frozenTheadWrapper.find('th label.checkbox-custom.checkbox-inline');
            $checkboxLabel.attr('id', $checkboxLabel.attr('id') + '_cloned');
            $frozenColumnWrapper.append($frozenColumn);
            repeaterWrapper.append($frozenTheadWrapper);
            this.$canvas.addClass('frozen-enabled');
          }

          this.list_sizeFrozenColumns();
          $$$1('.frozen-thead-wrapper .repeater-list-heading').on('click', function onClickHeading() {
            var index = $$$1(this).parent('th').index();
            index = index + 1;
            self.$element.find('.repeater-list-wrapper > table thead th:nth-child(' + index + ') .repeater-list-heading')[0].click();
          });
        };

        $$$1.fn.repeater.Constructor.prototype.list_positionColumns = function listPositionColumns() {
          var $wrapper = this.$element.find('.repeater-canvas');
          var scrollTop = $wrapper.scrollTop();
          var scrollLeft = $wrapper.scrollLeft();
          var frozenEnabled = this.viewOptions.list_frozenColumns || this.viewOptions.list_selectable === 'multi';
          var actionsEnabled = this.viewOptions.list_actions;
          var canvasWidth = this.$element.find('.repeater-canvas').outerWidth();
          var tableWidth = this.$element.find('.repeater-list .repeater-list-wrapper > table').outerWidth();
          var actionsWidth = this.$element.find('.table-actions') ? this.$element.find('.table-actions').outerWidth() : 0;
          var shouldScroll = tableWidth - (canvasWidth - actionsWidth) >= scrollLeft;

          if (scrollTop > 0) {
            $wrapper.find('.repeater-list-heading').css('top', scrollTop);
          } else {
            $wrapper.find('.repeater-list-heading').css('top', '0');
          }

          if (scrollLeft > 0) {
            if (frozenEnabled) {
              $wrapper.find('.frozen-thead-wrapper').css('left', scrollLeft);
              $wrapper.find('.frozen-column-wrapper').css('left', scrollLeft);
            }

            if (actionsEnabled && shouldScroll) {
              $wrapper.find('.actions-thead-wrapper').css('right', -scrollLeft);
              $wrapper.find('.actions-column-wrapper').css('right', -scrollLeft);
            }
          } else {
            if (frozenEnabled) {
              $wrapper.find('.frozen-thead-wrapper').css('left', '0');
              $wrapper.find('.frozen-column-wrapper').css('left', '0');
            }

            if (actionsEnabled) {
              $wrapper.find('.actions-thead-wrapper').css('right', '0');
              $wrapper.find('.actions-column-wrapper').css('right', '0');
            }
          }
        };

        $$$1.fn.repeater.Constructor.prototype.list_createItemActions = function listCreateItemActions() {
          var actionsHtml = '';
          var self = this;
          var i;
          var length;
          var $table = this.$element.find('.repeater-list .repeater-list-wrapper > table');
          var $actionsTable = this.$canvas.find('.table-actions');

          for (i = 0, length = this.viewOptions.list_actions.items.length; i < length; i++) {
            var action = this.viewOptions.list_actions.items[i];
            var html = action.html;
            actionsHtml += '<li><a href="#" data-action="' + action.name + '" class="action-item"> ' + html + '</a></li>';
          }

          var actionsDropdown = '<div class="btn-group">' + '<button type="button" class="btn btn-xs btn-default dropdown-toggle repeater-actions-button" data-toggle="dropdown" data-flip="auto" aria-expanded="false">' + '<span class="caret"></span>' + '</button>' + '<ul class="dropdown-menu dropdown-menu-right" role="menu">' + actionsHtml + '</ul></div>';

          if ($actionsTable.length < 1) {
            var $actionsColumnWrapper = $$$1('<div class="actions-column-wrapper" style="width: ' + this.list_actions_width + 'px"></div>').insertBefore($table);
            var $actionsColumn = $table.clone().addClass('table-actions');
            $actionsColumn.find('th:not(:last-child)').remove();
            $actionsColumn.find('tr td:not(:last-child)').remove(); // Dont show actions dropdown in header if not multi select

            if (this.viewOptions.list_selectable === 'multi' || this.viewOptions.list_selectable === 'action') {
              $actionsColumn.find('thead tr').html('<th><div class="repeater-list-heading">' + actionsDropdown + '</div></th>');

              if (this.viewOptions.list_selectable !== 'action') {
                // disable the header dropdown until an item is selected
                $actionsColumn.find('thead .btn').attr('disabled', 'disabled');
              }
            } else {
              var label = this.viewOptions.list_actions.label || '<span class="actions-hidden">a</span>';
              $actionsColumn.find('thead tr').addClass('empty-heading').html('<th>' + label + '<div class="repeater-list-heading">' + label + '</div></th>');
            } // Create Actions dropdown for each cell in actions table


            var $actionsCells = $actionsColumn.find('td');
            $actionsCells.each(function addActionsDropdown(rowNumber) {
              $$$1(this).html(actionsDropdown);
              $$$1(this).find('a').attr('data-row', rowNumber + 1);
            });
            $actionsColumnWrapper.append($actionsColumn);
            this.$canvas.addClass('actions-enabled');
          }

          this.list_sizeActionsTable(); // row level actions click

          this.$element.find('.table-actions tbody .action-item').on('click', function onBodyActionItemClick(e) {
            if (!self.isDisabled) {
              var actionName = $$$1(this).data('action');
              var row = $$$1(this).data('row');
              var selected = {
                actionName: actionName,
                rows: [row]
              };
              self.list_getActionItems(selected, e);
            }
          }); // bulk actions click

          this.$element.find('.table-actions thead .action-item').on('click', function onHeadActionItemClick(e) {
            if (!self.isDisabled) {
              var actionName = $$$1(this).data('action');
              var selected = {
                actionName: actionName,
                rows: []
              };
              var selector = '.repeater-list-wrapper > table .selected';

              if (self.viewOptions.list_selectable === 'action') {
                selector = '.repeater-list-wrapper > table tr';
              }

              self.$element.find(selector).each(function eachSelector(selectorIndex) {
                selected.rows.push(selectorIndex + 1);
              });
              self.list_getActionItems(selected, e);
            }
          });
        };

        $$$1.fn.repeater.Constructor.prototype.list_getActionItems = function listGetActionItems(selected, e) {
          var selectedObj = [];
          var actionObj = $$$1.grep(this.viewOptions.list_actions.items, function matchedActions(actions) {
            return actions.name === selected.actionName;
          })[0];

          for (var i = 0, selectedRowsL = selected.rows.length; i < selectedRowsL; i++) {
            var clickedRow = this.$canvas.find('.repeater-list-wrapper > table tbody tr:nth-child(' + selected.rows[i] + ')');
            selectedObj.push({
              item: clickedRow,
              rowData: clickedRow.data('item_data')
            });
          }

          if (selectedObj.length === 1) {
            selectedObj = selectedObj[0];
          }

          if (actionObj.clickAction) {
            var callback = function noop() {}; // for backwards compatibility. No idea why this was originally here...


            actionObj.clickAction(selectedObj, callback, e);
          }
        };

        $$$1.fn.repeater.Constructor.prototype.list_sizeActionsTable = function listSizeActionsTable() {
          var $actionsTable = this.$element.find('.repeater-list table.table-actions');
          var $actionsTableHeader = $actionsTable.find('thead tr th');
          var $table = this.$element.find('.repeater-list-wrapper > table');
          $actionsTableHeader.outerHeight($table.find('thead tr th').outerHeight());
          $actionsTableHeader.find('.repeater-list-heading').outerHeight($actionsTableHeader.outerHeight());
          $actionsTable.find('tbody tr td:first-child').each(function eachFirstChild(i) {
            $$$1(this).outerHeight($table.find('tbody tr:eq(' + i + ') td').outerHeight());
          });
        };

        $$$1.fn.repeater.Constructor.prototype.list_sizeFrozenColumns = function listSizeFrozenColumns() {
          var $table = this.$element.find('.repeater-list .repeater-list-wrapper > table');
          this.$element.find('.repeater-list table.table-frozen tr').each(function eachTR(i) {
            $$$1(this).height($table.find('tr:eq(' + i + ')').height());
          });
          var columnWidth = $table.find('td:eq(0)').outerWidth();
          this.$element.find('.frozen-column-wrapper, .frozen-thead-wrapper').width(columnWidth);
        };

        $$$1.fn.repeater.Constructor.prototype.list_frozenOptionsInitialize = function listFrozenOptionsInitialize() {
          var $checkboxes = this.$element.find('.frozen-column-wrapper .checkbox-inline');
          var $headerCheckbox = this.$element.find('.header-checkbox .checkbox-custom');
          var $everyTable = this.$element.find('.repeater-list table');
          var self = this; // Make sure if row is hovered that it is shown in frozen column as well

          this.$element.find('tr.selectable').on('mouseover mouseleave', function onMouseEvents(e) {
            var index = $$$1(this).index();
            index = index + 1;

            if (e.type === 'mouseover') {
              $everyTable.find('tbody tr:nth-child(' + index + ')').addClass('hovered');
            } else {
              $everyTable.find('tbody tr:nth-child(' + index + ')').removeClass('hovered');
            }
          });
          $headerCheckbox.checkbox();
          $checkboxes.checkbox(); // Row checkboxes

          var $rowCheckboxes = this.$element.find('.table-frozen tbody .checkbox-inline');
          var $checkAll = this.$element.find('.frozen-thead-wrapper thead .checkbox-inline input');
          $rowCheckboxes.on('change', function onChangeRowCheckboxes(e) {
            e.preventDefault();

            if (!self.list_revertingCheckbox) {
              if (self.isDisabled) {
                revertCheckbox($$$1(e.currentTarget));
              } else {
                var row = $$$1(this).attr('data-row');
                row = parseInt(row, 10) + 1;
                self.$element.find('.repeater-list-wrapper > table tbody tr:nth-child(' + row + ')').click();
                var numSelected = self.$element.find('.table-frozen tbody .checkbox-inline.checked').length;

                if (numSelected === 0) {
                  $checkAll.prop('checked', false);
                  $checkAll.prop('indeterminate', false);
                } else if (numSelected === $rowCheckboxes.length) {
                  $checkAll.prop('checked', true);
                  $checkAll.prop('indeterminate', false);
                } else {
                  $checkAll.prop('checked', false);
                  $checkAll.prop('indeterminate', true);
                }
              }
            }
          }); // "Check All" checkbox

          $checkAll.on('change', function onChangeCheckAll(e) {
            if (!self.list_revertingCheckbox) {
              if (self.isDisabled) {
                revertCheckbox($$$1(e.currentTarget));
              } else if ($$$1(this).is(':checked')) {
                self.$element.find('.repeater-list-wrapper > table tbody tr:not(.selected)').click();
                self.$element.trigger('selected.fu.repeaterList', $checkboxes);
              } else {
                self.$element.find('.repeater-list-wrapper > table tbody tr.selected').click();
                self.$element.trigger('deselected.fu.repeaterList', $checkboxes);
              }
            }
          });

          function revertCheckbox($checkbox) {
            self.list_revertingCheckbox = true;
            $checkbox.checkbox('toggle');
            delete self.list_revertingCheckbox;
          }
        }; // ADDITIONAL DEFAULT OPTIONS


        $$$1.fn.repeater.defaults = $$$1.extend({}, $$$1.fn.repeater.defaults, {
          list_columnRendered: null,
          list_columnSizing: true,
          list_columnSyncing: true,
          list_highlightSortedColumn: true,
          list_infiniteScroll: false,
          list_noItemsHTML: 'no items found',
          list_selectable: false,
          list_sortClearing: false,
          list_rowRendered: null,
          list_frozenColumns: 0,
          list_actions: false
        }); // EXTENSION DEFINITION

        $$$1.fn.repeater.viewTypes.list = {
          cleared: function cleared() {
            if (this.viewOptions.list_columnSyncing) {
              this.list_sizeHeadings();
            }
          },
          dataOptions: function dataOptions(options) {
            if (this.list_sortDirection) {
              options.sortDirection = this.list_sortDirection;
            }

            if (this.list_sortProperty) {
              options.sortProperty = this.list_sortProperty;
            }

            return options;
          },
          enabled: function enabled(helpers) {
            if (this.viewOptions.list_actions) {
              if (!helpers.status) {
                this.$canvas.find('.repeater-actions-button').attr('disabled', 'disabled');
              } else {
                this.$canvas.find('.repeater-actions-button').removeAttr('disabled');
                toggleActionsHeaderButton.call(this);
              }
            }
          },
          initialize: function initialize(helpers, callback) {
            this.list_sortDirection = null;
            this.list_sortProperty = null;
            this.list_specialBrowserClass = specialBrowserClass();
            this.list_actions_width = this.viewOptions.list_actions.width !== undefined ? this.viewOptions.list_actions.width : 37;
            this.list_noItems = false;
            callback();
          },
          resize: function resize() {
            sizeColumns.call(this, this.$element.find('.repeater-list-wrapper > table thead tr'));

            if (this.viewOptions.list_actions) {
              this.list_sizeActionsTable();
            }

            if (this.viewOptions.list_frozenColumns || this.viewOptions.list_selectable === 'multi') {
              this.list_sizeFrozenColumns();
            }

            if (this.viewOptions.list_columnSyncing) {
              this.list_sizeHeadings();
            }
          },
          selected: function selected() {
            var infScroll = this.viewOptions.list_infiniteScroll;
            var opts;
            this.list_firstRender = true;
            this.$loader.addClass('noHeader');

            if (infScroll) {
              opts = typeof infScroll === 'object' ? infScroll : {};
              this.infiniteScrolling(true, opts);
            }
          },
          before: function before(helpers) {
            var $listContainer = helpers.container.find('.repeater-list');
            var self = this;
            var $table; // this is a patch, it was pulled out of `renderThead`

            if (helpers.data.count > 0) {
              this.list_noItems = false;
            } else {
              this.list_noItems = true;
            }

            if ($listContainer.length < 1) {
              $listContainer = $$$1('<div class="repeater-list ' + this.list_specialBrowserClass + '" data-preserve="shallow"><div class="repeater-list-wrapper" data-infinite="true" data-preserve="shallow"><table aria-readonly="true" class="table" data-preserve="shallow" role="grid"></table></div></div>');
              $listContainer.find('.repeater-list-wrapper').on('scroll.fu.repeaterList', function onScrollRepeaterList() {
                if (self.viewOptions.list_columnSyncing) {
                  self.list_positionHeadings();
                }
              });

              if (self.viewOptions.list_frozenColumns || self.viewOptions.list_actions || self.viewOptions.list_selectable === 'multi') {
                helpers.container.on('scroll.fu.repeaterList', function onScrollRepeaterList() {
                  self.list_positionColumns();
                });
              }

              helpers.container.append($listContainer);
            }

            helpers.container.removeClass('actions-enabled actions-enabled multi-select-enabled');
            $table = $listContainer.find('table');
            renderThead.call(this, $table, helpers.data);
            renderTbody.call(this, $table, helpers.data);
            return false;
          },
          renderItem: function renderItem(helpers) {
            renderRow.call(this, helpers.container, helpers.subset, helpers.index);
            return false;
          },
          after: function after() {
            var $sorted;

            if ((this.viewOptions.list_frozenColumns || this.viewOptions.list_selectable === 'multi') && !this.list_noItems) {
              this.list_setFrozenColumns();
            }

            if (this.viewOptions.list_actions && !this.list_noItems) {
              this.list_createItemActions();
              this.list_sizeActionsTable();
            }

            if ((this.viewOptions.list_frozenColumns || this.viewOptions.list_actions || this.viewOptions.list_selectable === 'multi') && !this.list_noItems) {
              this.list_positionColumns();
              this.list_frozenOptionsInitialize();
            }

            if (this.viewOptions.list_columnSyncing) {
              this.list_sizeHeadings();
              this.list_positionHeadings();
            }

            $sorted = this.$canvas.find('.repeater-list-wrapper > table .repeater-list-heading.sorted');

            if ($sorted.length > 0) {
              this.list_highlightColumn($sorted.data('fu_item_index'));
            }

            return false;
          }
        };
      } // ADDITIONAL METHODS


      var areDifferentColumns = function areDifferentColumns(oldCols, newCols) {
        if (!newCols) {
          return false;
        }

        if (!oldCols || newCols.length !== oldCols.length) {
          return true;
        }

        for (var i = 0, newColsL = newCols.length; i < newColsL; i++) {
          if (!oldCols[i]) {
            return true;
          }

          for (var j in newCols[i]) {
            if (newCols[i].hasOwnProperty(j) && oldCols[i][j] !== newCols[i][j]) {
              return true;
            }
          }
        }

        return false;
      };

      var renderColumn = function renderColumn($row, rows, rowIndex, columns, columnIndex) {
        var className = columns[columnIndex].className;
        var content = rows[rowIndex][columns[columnIndex].property];
        var $col = $$$1('<td></td>');
        var width = columns[columnIndex]._auto_width;
        var property = columns[columnIndex].property;

        if (this.viewOptions.list_actions !== false && property === '@_ACTIONS_@') {
          content = '<div class="repeater-list-actions-placeholder" style="width: ' + this.list_actions_width + 'px"></div>';
        }

        content = content !== undefined ? content : '';
        $col.addClass(className !== undefined ? className : '').append(content);

        if (width !== undefined) {
          $col.outerWidth(width);
        }

        $row.append($col);

        if (this.viewOptions.list_selectable === 'multi' && columns[columnIndex].property === '@_CHECKBOX_@') {
          var checkBoxMarkup = '<label data-row="' + rowIndex + '" class="checkbox-custom checkbox-inline body-checkbox repeater-select-checkbox">' + '<input class="sr-only" type="checkbox"></label>';
          $col.html(checkBoxMarkup);
        }

        return $col;
      };

      var renderHeader = function renderHeader($tr, columns, index) {
        var chevDown = 'glyphicon-chevron-down';
        var chevron = '.glyphicon.rlc:first';
        var chevUp = 'glyphicon-chevron-up';
        var $div = $$$1('<div class="repeater-list-heading"><span class="glyphicon rlc"></span></div>');
        var checkAllID = (this.$element.attr('id') + '_' || '') + 'checkall';
        var checkBoxMarkup = '<div class="repeater-list-heading header-checkbox">' + '<label id="' + checkAllID + '" class="checkbox-custom checkbox-inline">' + '<input class="sr-only" type="checkbox" value="">' + '<span class="checkbox-label">&nbsp;</span>' + '</label>' + '</div>';
        var $header = $$$1('<th></th>');
        var self = this;
        var $both;
        var className;
        var sortable;
        var $span;
        var $spans;
        $div.data('fu_item_index', index);
        $div.prepend(columns[index].label);
        $header.html($div.html()).find('[id]').removeAttr('id');

        if (columns[index].property !== '@_CHECKBOX_@') {
          $header.append($div);
        } else {
          $header.append(checkBoxMarkup);
        }

        $both = $header.add($div);
        $span = $div.find(chevron);
        $spans = $span.add($header.find(chevron));

        if (this.viewOptions.list_actions && columns[index].property === '@_ACTIONS_@') {
          var width = this.list_actions_width;
          $header.css('width', width);
          $div.css('width', width);
        }

        className = columns[index].className;

        if (className !== undefined) {
          $both.addClass(className);
        }

        sortable = columns[index].sortable;

        if (sortable) {
          $both.addClass('sortable');
          $div.on('click.fu.repeaterList', function onClickRepeaterList() {
            if (!self.isDisabled) {
              self.list_sortProperty = typeof sortable === 'string' ? sortable : columns[index].property;

              if ($div.hasClass('sorted')) {
                if ($span.hasClass(chevUp)) {
                  $spans.removeClass(chevUp).addClass(chevDown);
                  self.list_sortDirection = 'desc';
                } else if (!self.viewOptions.list_sortClearing) {
                  $spans.removeClass(chevDown).addClass(chevUp);
                  self.list_sortDirection = 'asc';
                } else {
                  $both.removeClass('sorted');
                  $spans.removeClass(chevDown);
                  self.list_sortDirection = null;
                  self.list_sortProperty = null;
                }
              } else {
                $tr.find('th, .repeater-list-heading').removeClass('sorted');
                $spans.removeClass(chevDown).addClass(chevUp);
                self.list_sortDirection = 'asc';
                $both.addClass('sorted');
              }

              self.render({
                clearInfinite: true,
                pageIncrement: null
              });
            }
          });
        }

        if (columns[index].sortDirection === 'asc' || columns[index].sortDirection === 'desc') {
          $tr.find('th, .repeater-list-heading').removeClass('sorted');
          $both.addClass('sortable sorted');

          if (columns[index].sortDirection === 'asc') {
            $spans.addClass(chevUp);
            this.list_sortDirection = 'asc';
          } else {
            $spans.addClass(chevDown);
            this.list_sortDirection = 'desc';
          }

          this.list_sortProperty = typeof sortable === 'string' ? sortable : columns[index].property;
        }

        $tr.append($header);
      };

      var onClickRowRepeaterList = function onClickRowRepeaterList(repeater) {
        var isMulti = repeater.viewOptions.list_selectable === 'multi';
        var isActions = repeater.viewOptions.list_actions;
        var $repeater = repeater.$element;

        if (!repeater.isDisabled) {
          var $item = $$$1(this);
          var index = $$$1(this).index() + 1;
          var $frozenRow = $repeater.find('.frozen-column-wrapper tr:nth-child(' + index + ')');
          var $actionsRow = $repeater.find('.actions-column-wrapper tr:nth-child(' + index + ')');
          var $checkBox = $repeater.find('.frozen-column-wrapper tr:nth-child(' + index + ') .checkbox-inline');

          if ($item.is('.selected')) {
            $item.removeClass('selected');

            if (isMulti) {
              $checkBox.click();
              $frozenRow.removeClass('selected');

              if (isActions) {
                $actionsRow.removeClass('selected');
              }
            } else {
              $item.find('.repeater-list-check').remove();
            }

            $repeater.trigger('deselected.fu.repeaterList', $item);
          } else {
            if (!isMulti) {
              repeater.$canvas.find('.repeater-list-check').remove();
              repeater.$canvas.find('.repeater-list tbody tr.selected').each(function deslectRow() {
                $$$1(this).removeClass('selected');
                $repeater.trigger('deselected.fu.repeaterList', $$$1(this));
              });
              $item.find('td:first').prepend('<div class="repeater-list-check"><span class="glyphicon glyphicon-ok"></span></div>');
              $item.addClass('selected');
              $frozenRow.addClass('selected');
            } else {
              $checkBox.click();
              $item.addClass('selected');
              $frozenRow.addClass('selected');

              if (isActions) {
                $actionsRow.addClass('selected');
              }
            }

            $repeater.trigger('selected.fu.repeaterList', $item);
          }

          toggleActionsHeaderButton.call(repeater);
        }
      };

      var renderRow = function renderRow($tbody, rows, index) {
        var $row = $$$1('<tr></tr>');

        if (this.viewOptions.list_selectable) {
          $row.data('item_data', rows[index]);

          if (this.viewOptions.list_selectable !== 'action') {
            $row.addClass('selectable');
            $row.attr('tabindex', 0); // allow items to be tabbed to / focused on

            var repeater = this;
            $row.on('click.fu.repeaterList', function callOnClickRowRepeaterList() {
              onClickRowRepeaterList.call(this, repeater);
            }); // allow selection via enter key

            $row.keyup(function onRowKeyup(e) {
              if (e.keyCode === 13) {
                // triggering a standard click event to be caught by the row click handler above
                $row.trigger('click.fu.repeaterList');
              }
            });
          }
        }

        if (this.viewOptions.list_actions && !this.viewOptions.list_selectable) {
          $row.data('item_data', rows[index]);
        }

        var columns = [];

        for (var i = 0, length = this.list_columns.length; i < length; i++) {
          columns.push(renderColumn.call(this, $row, rows, index, this.list_columns, i));
        }

        $tbody.append($row);

        if (this.viewOptions.list_columnRendered) {
          for (var columnIndex = 0, colLength = columns.length; columnIndex < colLength; columnIndex++) {
            if (!(this.list_columns[columnIndex].property === '@_CHECKBOX_@' || this.list_columns[columnIndex].property === '@_ACTIONS_@')) {
              this.viewOptions.list_columnRendered({
                container: $row,
                columnAttr: this.list_columns[columnIndex].property,
                item: columns[columnIndex],
                rowData: rows[index]
              }, function noop() {});
            }
          }
        }

        if (this.viewOptions.list_rowRendered) {
          this.viewOptions.list_rowRendered({
            container: $tbody,
            item: $row,
            rowData: rows[index]
          }, function noop() {});
        }
      };

      var renderTbody = function renderTbody($table, data) {
        var $tbody = $table.find('tbody');
        var $empty;

        if ($tbody.length < 1) {
          $tbody = $$$1('<tbody data-container="true"></tbody>');
          $table.append($tbody);
        }

        if (typeof data.error === 'string' && data.error.length > 0) {
          $empty = $$$1('<tr class="empty text-danger"><td colspan="' + this.list_columns.length + '"></td></tr>');
          $empty.find('td').append(data.error);
          $tbody.append($empty);
        } else if (data.items && data.items.length < 1) {
          $empty = $$$1('<tr class="empty"><td colspan="' + this.list_columns.length + '"></td></tr>');
          $empty.find('td').append(this.viewOptions.list_noItemsHTML);
          $tbody.append($empty);
        }
      };

      var renderThead = function renderThead($table, data) {
        var columns = data.columns || [];
        var $thead = $table.find('thead');
        var i;
        var length;
        var $tr;

        if (this.list_firstRender || areDifferentColumns(this.list_columns, columns) || $thead.length === 0) {
          $thead.remove(); // list_noItems is set in `before` method

          if (this.viewOptions.list_selectable === 'multi' && !this.list_noItems) {
            var checkboxColumn = {
              label: 'c',
              property: '@_CHECKBOX_@',
              sortable: false
            };
            columns.splice(0, 0, checkboxColumn);
          }

          this.list_columns = columns;
          this.list_firstRender = false;
          this.$loader.removeClass('noHeader'); // keep action column header even when empty, you'll need it later....

          if (this.viewOptions.list_actions) {
            var actionsColumn = {
              label: this.viewOptions.list_actions.label || '<span class="actions-hidden">a</span>',
              property: '@_ACTIONS_@',
              sortable: false,
              width: this.list_actions_width
            };
            columns.push(actionsColumn);
          }

          $thead = $$$1('<thead data-preserve="deep"><tr></tr></thead>');
          $tr = $thead.find('tr');

          for (i = 0, length = columns.length; i < length; i++) {
            renderHeader.call(this, $tr, columns, i);
          }

          $table.prepend($thead);

          if (this.viewOptions.list_selectable === 'multi' && !this.list_noItems) {
            // after checkbox column is created need to get width of checkbox column from
            // its css class
            var checkboxWidth = this.$element.find('.repeater-list-wrapper .header-checkbox').outerWidth();
            var selectColumn = $$$1.grep(columns, function grepColumn(column) {
              return column.property === '@_CHECKBOX_@';
            })[0];
            selectColumn.width = checkboxWidth;
          }

          sizeColumns.call(this, $tr);
        }
      };

      var sizeColumns = function sizeColumns($tr) {
        var automaticallyGeneratedWidths = [];
        var self = this;
        var i;
        var length;
        var newWidth;
        var widthTaken;

        if (this.viewOptions.list_columnSizing) {
          i = 0;
          widthTaken = 0;
          $tr.find('th').each(function eachTH() {
            var $th = $$$1(this);
            var width;

            if (self.list_columns[i].width !== undefined) {
              width = self.list_columns[i].width;
              $th.outerWidth(width);
              widthTaken += $th.outerWidth();
              self.list_columns[i]._auto_width = width;
            } else {
              var outerWidth = $th.find('.repeater-list-heading').outerWidth();
              automaticallyGeneratedWidths.push({
                col: $th,
                index: i,
                minWidth: outerWidth
              });
            }

            i++;
          });
          length = automaticallyGeneratedWidths.length;

          if (length > 0) {
            var canvasWidth = this.$canvas.find('.repeater-list-wrapper').outerWidth();
            newWidth = Math.floor((canvasWidth - widthTaken) / length);

            for (i = 0; i < length; i++) {
              if (automaticallyGeneratedWidths[i].minWidth > newWidth) {
                newWidth = automaticallyGeneratedWidths[i].minWidth;
              }

              automaticallyGeneratedWidths[i].col.outerWidth(newWidth);
              this.list_columns[automaticallyGeneratedWidths[i].index]._auto_width = newWidth;
            }
          }
        }
      };

      var specialBrowserClass = function specialBrowserClass() {
        var ua = window.navigator.userAgent;
        var msie = ua.indexOf('MSIE ');
        var firefox = ua.indexOf('Firefox');

        if (msie > 0) {
          return 'ie-' + parseInt(ua.substring(msie + 5, ua.indexOf('.', msie)), 10);
        } else if (firefox > 0) {
          return 'firefox';
        }

        return '';
      };

      var toggleActionsHeaderButton = function toggleActionsHeaderButton() {
        var selectedSelector = '.repeater-list-wrapper > table .selected';
        var $actionsColumn = this.$element.find('.table-actions');
        var $selected;

        if (this.viewOptions.list_selectable === 'action') {
          selectedSelector = '.repeater-list-wrapper > table tr';
        }

        $selected = this.$canvas.find(selectedSelector);

        if ($selected.length > 0) {
          $actionsColumn.find('thead .btn').removeAttr('disabled');
        } else {
          $actionsColumn.find('thead .btn').attr('disabled', 'disabled');
        }
      };
    })(jQuery);

    (function ($$$1) {
      /* global jQuery:true */

      /*
       * Fuel UX Repeater - Thumbnail View Plugin
       * https://github.com/ExactTarget/fuelux
       *
       * Copyright (c) 2014 ExactTarget
       * Licensed under the BSD New license.
       */
      // -- BEGIN MODULE CODE HERE --
      if ($$$1.fn.repeater) {
        //ADDITIONAL METHODS
        $$$1.fn.repeater.Constructor.prototype.thumbnail_clearSelectedItems = function () {
          this.$canvas.find('.repeater-thumbnail-cont .selectable.selected').removeClass('selected');
        };

        $$$1.fn.repeater.Constructor.prototype.thumbnail_getSelectedItems = function () {
          var selected = [];
          this.$canvas.find('.repeater-thumbnail-cont .selectable.selected').each(function () {
            selected.push($$$1(this));
          });
          return selected;
        };

        $$$1.fn.repeater.Constructor.prototype.thumbnail_setSelectedItems = function (items, force) {
          var selectable = this.viewOptions.thumbnail_selectable;
          var self = this;
          var i, $item, l, n; //this function is necessary because lint yells when a function is in a loop

          function compareItemIndex() {
            if (n === items[i].index) {
              $item = $$$1(this);
              return false;
            } else {
              n++;
            }
          } //this function is necessary because lint yells when a function is in a loop


          function compareItemSelector() {
            $item = $$$1(this);

            if ($item.is(items[i].selector)) {
              selectItem($item, items[i].selected);
            }
          }

          function selectItem($itm, select) {
            select = select !== undefined ? select : true;

            if (select) {
              if (!force && selectable !== 'multi') {
                self.thumbnail_clearSelectedItems();
              }

              $itm.addClass('selected');
            } else {
              $itm.removeClass('selected');
            }
          }

          if (!$$$1.isArray(items)) {
            items = [items];
          }

          if (force === true || selectable === 'multi') {
            l = items.length;
          } else if (selectable) {
            l = items.length > 0 ? 1 : 0;
          } else {
            l = 0;
          }

          for (i = 0; i < l; i++) {
            if (items[i].index !== undefined) {
              $item = $$$1();
              n = 0;
              this.$canvas.find('.repeater-thumbnail-cont .selectable').each(compareItemIndex);

              if ($item.length > 0) {
                selectItem($item, items[i].selected);
              }
            } else if (items[i].selector) {
              this.$canvas.find('.repeater-thumbnail-cont .selectable').each(compareItemSelector);
            }
          }
        }; //ADDITIONAL DEFAULT OPTIONS


        $$$1.fn.repeater.defaults = $$$1.extend({}, $$$1.fn.repeater.defaults, {
          thumbnail_alignment: 'left',
          thumbnail_infiniteScroll: false,
          thumbnail_itemRendered: null,
          thumbnail_noItemsHTML: 'no items found',
          thumbnail_selectable: false,
          thumbnail_template: '<div class="thumbnail repeater-thumbnail"><img height="75" src="{{src}}" width="65"><span>{{name}}</span></div>'
        }); //EXTENSION DEFINITION

        $$$1.fn.repeater.viewTypes.thumbnail = {
          selected: function selected() {
            var infScroll = this.viewOptions.thumbnail_infiniteScroll;
            var opts;

            if (infScroll) {
              opts = typeof infScroll === 'object' ? infScroll : {};
              this.infiniteScrolling(true, opts);
            }
          },
          before: function before(helpers) {
            var alignment = this.viewOptions.thumbnail_alignment;
            var $cont = this.$canvas.find('.repeater-thumbnail-cont');
            var data = helpers.data;
            var response = {};
            var $empty, validAlignments;

            if ($cont.length < 1) {
              $cont = $$$1('<div class="clearfix repeater-thumbnail-cont" data-container="true" data-infinite="true" data-preserve="shallow"></div>');

              if (alignment && alignment !== 'none') {
                validAlignments = {
                  'center': 1,
                  'justify': 1,
                  'left': 1,
                  'right': 1
                };
                alignment = validAlignments[alignment] ? alignment : 'justify';
                $cont.addClass('align-' + alignment);
                this.thumbnail_injectSpacers = true;
              } else {
                this.thumbnail_injectSpacers = false;
              }

              response.item = $cont;
            } else {
              response.action = 'none';
            }

            if (data.items && data.items.length < 1) {
              $empty = $$$1('<div class="empty"></div>');
              $empty.append(this.viewOptions.thumbnail_noItemsHTML);
              $cont.append($empty);
            } else {
              $cont.find('.empty:first').remove();
            }

            return response;
          },
          renderItem: function renderItem(helpers) {
            var selectable = this.viewOptions.thumbnail_selectable;
            var selected = 'selected';
            var self = this;
            var $thumbnail = $$$1(fillTemplate(helpers.subset[helpers.index], this.viewOptions.thumbnail_template));
            $thumbnail.data('item_data', helpers.data.items[helpers.index]);

            if (selectable) {
              $thumbnail.addClass('selectable');
              $thumbnail.on('click', function () {
                if (self.isDisabled) return;

                if (!$thumbnail.hasClass(selected)) {
                  if (selectable !== 'multi') {
                    self.$canvas.find('.repeater-thumbnail-cont .selectable.selected').each(function () {
                      var $itm = $$$1(this);
                      $itm.removeClass(selected);
                      self.$element.trigger('deselected.fu.repeaterThumbnail', $itm);
                    });
                  }

                  $thumbnail.addClass(selected);
                  self.$element.trigger('selected.fu.repeaterThumbnail', $thumbnail);
                } else {
                  $thumbnail.removeClass(selected);
                  self.$element.trigger('deselected.fu.repeaterThumbnail', $thumbnail);
                }
              });
            }

            helpers.container.append($thumbnail);

            if (this.thumbnail_injectSpacers) {
              $thumbnail.after('<span class="spacer">&nbsp;</span>');
            }

            if (this.viewOptions.thumbnail_itemRendered) {
              this.viewOptions.thumbnail_itemRendered({
                container: helpers.container,
                item: $thumbnail,
                itemData: helpers.subset[helpers.index]
              }, function () {});
            }

            return false;
          }
        };
      } //ADDITIONAL METHODS


      function fillTemplate(itemData, template) {
        var invalid = false;

        function replace() {
          var end, start, val;
          start = template.indexOf('{{');
          end = template.indexOf('}}', start + 2);

          if (start > -1 && end > -1) {
            val = $$$1.trim(template.substring(start + 2, end));
            val = itemData[val] !== undefined ? itemData[val] : '';
            template = template.substring(0, start) + val + template.substring(end + 2);
          } else {
            invalid = true;
          }
        }

        while (!invalid && template.search('{{') >= 0) {
          replace(template);
        }

        return template;
      }
    })(jQuery);

    (function ($$$1) {
      /* global jQuery:true */

      /*
       * Fuel UX Scheduler
       * https://github.com/ExactTarget/fuelux
       *
       * Copyright (c) 2014 ExactTarget
       * Licensed under the BSD New license.
       */
      // -- BEGIN MODULE CODE HERE --
      var old = $$$1.fn.scheduler; // SCHEDULER CONSTRUCTOR AND PROTOTYPE

      var Scheduler = function Scheduler(element, options) {
        var self = this;
        this.$element = $$$1(element);
        this.options = $$$1.extend({}, $$$1.fn.scheduler.defaults, options); // cache elements

        this.$startDate = this.$element.find('.start-datetime .start-date');
        this.$startTime = this.$element.find('.start-datetime .start-time');
        this.$timeZone = this.$element.find('.timezone-container .timezone');
        this.$repeatIntervalPanel = this.$element.find('.repeat-every-panel');
        this.$repeatIntervalSelect = this.$element.find('.repeat-options');
        this.$repeatIntervalSpinbox = this.$element.find('.repeat-every');
        this.$repeatIntervalTxt = this.$element.find('.repeat-every-text');
        this.$end = this.$element.find('.repeat-end');
        this.$endSelect = this.$end.find('.end-options');
        this.$endAfter = this.$end.find('.end-after');
        this.$endDate = this.$end.find('.end-on-date'); // panels

        this.$recurrencePanels = this.$element.find('.repeat-panel');
        this.$repeatIntervalSelect.selectlist(); //initialize sub-controls

        this.$element.find('.selectlist').selectlist();
        this.$startDate.datepicker(this.options.startDateOptions);
        var startDateResponse = typeof this.options.startDateChanged === "function" ? this.options.startDateChanged : this._guessEndDate;
        this.$startDate.on('change changed.fu.datepicker dateClicked.fu.datepicker', $$$1.proxy(startDateResponse, this));
        this.$startTime.combobox(); // init start time

        if (this.$startTime.find('input').val() === '') {
          this.$startTime.combobox('selectByIndex', 0);
        } // every 0 days/hours doesn't make sense, change if not set


        if (this.$repeatIntervalSpinbox.find('input').val() === '0') {
          this.$repeatIntervalSpinbox.spinbox({
            'value': 1,
            'min': 1,
            'limitToStep': true
          });
        } else {
          this.$repeatIntervalSpinbox.spinbox({
            'min': 1,
            'limitToStep': true
          });
        }

        this.$endAfter.spinbox({
          'value': 1,
          'min': 1,
          'limitToStep': true
        });
        this.$endDate.datepicker(this.options.endDateOptions);
        this.$element.find('.radio-custom').radio(); // bind events: 'change' is a Bootstrap JS fired event

        this.$repeatIntervalSelect.on('changed.fu.selectlist', $$$1.proxy(this.repeatIntervalSelectChanged, this));
        this.$endSelect.on('changed.fu.selectlist', $$$1.proxy(this.endSelectChanged, this));
        this.$element.find('.repeat-days-of-the-week .btn-group .btn').on('change.fu.scheduler', function (e, data) {
          self.changed(e, data, true);
        });
        this.$element.find('.combobox').on('changed.fu.combobox', $$$1.proxy(this.changed, this));
        this.$element.find('.datepicker').on('changed.fu.datepicker', $$$1.proxy(this.changed, this));
        this.$element.find('.datepicker').on('dateClicked.fu.datepicker', $$$1.proxy(this.changed, this));
        this.$element.find('.selectlist').on('changed.fu.selectlist', $$$1.proxy(this.changed, this));
        this.$element.find('.spinbox').on('changed.fu.spinbox', $$$1.proxy(this.changed, this));
        this.$element.find('.repeat-monthly .radio-custom, .repeat-yearly .radio-custom').on('change.fu.scheduler', $$$1.proxy(this.changed, this));
      };

      var _getFormattedDate = function _getFormattedDate(dateObj, dash) {
        var fdate = '';
        var item;
        fdate += dateObj.getFullYear();
        fdate += dash;
        item = dateObj.getMonth() + 1; //because 0 indexing makes sense when dealing with months /sarcasm

        fdate += item < 10 ? '0' + item : item;
        fdate += dash;
        item = dateObj.getDate();
        fdate += item < 10 ? '0' + item : item;
        return fdate;
      };

      var ONE_SECOND = 1000;
      var ONE_MINUTE = ONE_SECOND * 60;
      var ONE_HOUR = ONE_MINUTE * 60;
      var ONE_DAY = ONE_HOUR * 24;
      var ONE_WEEK = ONE_DAY * 7;
      var ONE_MONTH = ONE_WEEK * 5; // No good way to increment by one month using vanilla JS. Since this is an end date, we only need to ensure that this date occurs after at least one or more repeat increments, but there is no reason for it to be exact.

      var ONE_YEAR = ONE_WEEK * 52;
      var INTERVALS = {
        secondly: ONE_SECOND,
        minutely: ONE_MINUTE,
        hourly: ONE_HOUR,
        daily: ONE_DAY,
        weekly: ONE_WEEK,
        monthly: ONE_MONTH,
        yearly: ONE_YEAR
      };

      var _incrementDate = function _incrementDate(start, end, interval, increment) {
        return new Date(start.getTime() + INTERVALS[interval] * increment);
      };

      Scheduler.prototype = {
        constructor: Scheduler,
        destroy: function destroy() {
          var markup; // set input value attribute

          this.$element.find('input').each(function () {
            $$$1(this).attr('value', $$$1(this).val());
          }); // empty elements to return to original markup and store

          this.$element.find('.datepicker .calendar').empty();
          markup = this.$element[0].outerHTML; // destroy components

          this.$element.find('.combobox').combobox('destroy');
          this.$element.find('.datepicker').datepicker('destroy');
          this.$element.find('.selectlist').selectlist('destroy');
          this.$element.find('.spinbox').spinbox('destroy');
          this.$element.find('.radio-custom').radio('destroy');
          this.$element.remove(); // any external bindings
          // [none]

          return markup;
        },
        changed: function changed(e, data, propagate) {
          if (!propagate) {
            e.stopPropagation();
          }

          this.$element.trigger('changed.fu.scheduler', {
            data: data !== undefined ? data : $$$1(e.currentTarget).data(),
            originalEvent: e,
            value: this.getValue()
          });
        },
        disable: function disable() {
          this.toggleState('disable');
        },
        enable: function enable() {
          this.toggleState('enable');
        },
        setUtcTime: function setUtcTime(day, time, offset) {
          var dateSplit = day.split('-');
          var timeSplit = time.split(':');

          var utcDate = new Date(Date.UTC(dateSplit[0], dateSplit[1] - 1, dateSplit[2], timeSplit[0], timeSplit[1], timeSplit[2] ? timeSplit[2] : 0));

          if (offset === 'Z') {
            utcDate.setUTCHours(utcDate.getUTCHours() + 0);
          } else {
            var expression = [];
            expression[0] = '(.)'; // Any Single Character 1

            expression[1] = '.*?'; // Non-greedy match on filler

            expression[2] = '\\d'; // Uninteresting and ignored: d

            expression[3] = '.*?'; // Non-greedy match on filler

            expression[4] = '(\\d)'; // Any Single Digit 1

            var p = new RegExp(expression.join(''), ["i"]);
            var offsetMatch = p.exec(offset);

            if (offsetMatch !== null) {
              var offsetDirection = offsetMatch[1];
              var offsetInteger = offsetMatch[2];
              var modifier = offsetDirection === '+' ? 1 : -1;
              utcDate.setUTCHours(utcDate.getUTCHours() + modifier * parseInt(offsetInteger, 10));
            }
          }

          var localDifference = utcDate.getTimezoneOffset();
          utcDate.setMinutes(localDifference);
          return utcDate;
        },
        // called when the end range changes
        // (Never, After, On date)
        endSelectChanged: function endSelectChanged(e, data) {
          var selectedItem, val;

          if (!data) {
            selectedItem = this.$endSelect.selectlist('selectedItem');
            val = selectedItem.value;
          } else {
            val = data.value;
          } // hide all panels


          this.$endAfter.parent().addClass('hidden');
          this.$endAfter.parent().attr('aria-hidden', 'true');
          this.$endDate.parent().addClass('hidden');
          this.$endDate.parent().attr('aria-hidden', 'true');

          if (val === 'after') {
            this.$endAfter.parent().removeClass('hide hidden'); // jQuery deprecated hide in 3.0. Use hidden instead. Leaving hide here to support previous markup

            this.$endAfter.parent().attr('aria-hidden', 'false');
          } else if (val === 'date') {
            this.$endDate.parent().removeClass('hide hidden'); // jQuery deprecated hide in 3.0. Use hidden instead. Leaving hide here to support previous markup

            this.$endDate.parent().attr('aria-hidden', 'false');
          }
        },
        _guessEndDate: function _guessEndDate() {
          var interval = this.$repeatIntervalSelect.selectlist('selectedItem').value;
          var end = new Date(this.$endDate.datepicker('getDate'));
          var start = new Date(this.$startDate.datepicker('getDate'));
          var increment = this.$repeatIntervalSpinbox.find('input').val();

          if (interval !== "none" && end <= start) {
            // if increment spinbox is hidden, user has no idea what it is set to and it is probably not set to
            // something they intended. Safest option is to set date forward by an increment of 1.
            // this will keep monthly & yearly from auto-incrementing by more than a single interval
            if (!this.$repeatIntervalSpinbox.is(':visible')) {
              increment = 1;
            } // treat weekdays as weekly. This treats all "weekdays" as a single set, of which a single increment
            // is one week.


            if (interval === "weekdays") {
              increment = 1;
              interval = "weekly";
            }

            end = _incrementDate(start, end, interval, increment);
            this.$endDate.datepicker('setDate', end);
          }
        },
        getValue: function getValue() {
          // FREQ = frequency (secondly, minutely, hourly, daily, weekdays, weekly, monthly, yearly)
          // BYDAY = when picking days (MO,TU,WE,etc)
          // BYMONTH = when picking months (Jan,Feb,March) - note the values should be 1,2,3...
          // BYMONTHDAY = when picking days of the month (1,2,3...)
          // BYSETPOS = when picking First,Second,Third,Fourth,Last (1,2,3,4,-1)
          var interval = this.$repeatIntervalSpinbox.spinbox('value');
          var pattern = '';
          var repeat = this.$repeatIntervalSelect.selectlist('selectedItem').value;
          var startTime;

          if (this.$startTime.combobox('selectedItem').value) {
            startTime = this.$startTime.combobox('selectedItem').value;
            startTime = startTime.toLowerCase();
          } else {
            startTime = this.$startTime.combobox('selectedItem').text.toLowerCase();
          }

          var timeZone = this.$timeZone.selectlist('selectedItem');
          var day, days, hasAm, hasPm, month, pos, startDateTime, type;
          startDateTime = '' + _getFormattedDate(this.$startDate.datepicker('getDate'), '-');
          startDateTime += 'T';
          hasAm = startTime.search('am') >= 0;
          hasPm = startTime.search('pm') >= 0;
          startTime = $$$1.trim(startTime.replace(/am/g, '').replace(/pm/g, '')).split(':');
          startTime[0] = parseInt(startTime[0], 10);
          startTime[1] = parseInt(startTime[1], 10);

          if (hasAm && startTime[0] > 11) {
            startTime[0] = 0;
          } else if (hasPm && startTime[0] < 12) {
            startTime[0] += 12;
          }

          startDateTime += startTime[0] < 10 ? '0' + startTime[0] : startTime[0];
          startDateTime += ':';
          startDateTime += startTime[1] < 10 ? '0' + startTime[1] : startTime[1];
          startDateTime += timeZone.offset === '+00:00' ? 'Z' : timeZone.offset;

          if (repeat === 'none') {
            pattern = 'FREQ=DAILY;INTERVAL=1;COUNT=1;';
          } else if (repeat === 'secondly') {
            pattern = 'FREQ=SECONDLY;';
            pattern += 'INTERVAL=' + interval + ';';
          } else if (repeat === 'minutely') {
            pattern = 'FREQ=MINUTELY;';
            pattern += 'INTERVAL=' + interval + ';';
          } else if (repeat === 'hourly') {
            pattern = 'FREQ=HOURLY;';
            pattern += 'INTERVAL=' + interval + ';';
          } else if (repeat === 'daily') {
            pattern += 'FREQ=DAILY;';
            pattern += 'INTERVAL=' + interval + ';';
          } else if (repeat === 'weekdays') {
            pattern += 'FREQ=WEEKLY;';
            pattern += 'BYDAY=MO,TU,WE,TH,FR;';
            pattern += 'INTERVAL=1;';
          } else if (repeat === 'weekly') {
            days = [];
            this.$element.find('.repeat-days-of-the-week .btn-group input:checked').each(function () {
              days.push($$$1(this).data().value);
            });
            pattern += 'FREQ=WEEKLY;';
            pattern += 'BYDAY=' + days.join(',') + ';';
            pattern += 'INTERVAL=' + interval + ';';
          } else if (repeat === 'monthly') {
            pattern += 'FREQ=MONTHLY;';
            pattern += 'INTERVAL=' + interval + ';';
            type = this.$element.find('input[name=repeat-monthly]:checked').val();

            if (type === 'bymonthday') {
              day = parseInt(this.$element.find('.repeat-monthly-date .selectlist').selectlist('selectedItem').text, 10);
              pattern += 'BYMONTHDAY=' + day + ';';
            } else if (type === 'bysetpos') {
              days = this.$element.find('.repeat-monthly-day .month-days').selectlist('selectedItem').value;
              pos = this.$element.find('.repeat-monthly-day .month-day-pos').selectlist('selectedItem').value;
              pattern += 'BYDAY=' + days + ';';
              pattern += 'BYSETPOS=' + pos + ';';
            }
          } else if (repeat === 'yearly') {
            pattern += 'FREQ=YEARLY;';
            type = this.$element.find('input[name=repeat-yearly]:checked').val();

            if (type === 'bymonthday') {
              // there are multiple .year-month classed elements in scheduler markup
              month = this.$element.find('.repeat-yearly-date .year-month').selectlist('selectedItem').value;
              day = this.$element.find('.repeat-yearly-date .year-month-day').selectlist('selectedItem').text;
              pattern += 'BYMONTH=' + month + ';';
              pattern += 'BYMONTHDAY=' + day + ';';
            } else if (type === 'bysetpos') {
              days = this.$element.find('.repeat-yearly-day .year-month-days').selectlist('selectedItem').value;
              pos = this.$element.find('.repeat-yearly-day .year-month-day-pos').selectlist('selectedItem').value; // there are multiple .year-month classed elements in scheduler markup

              month = this.$element.find('.repeat-yearly-day .year-month').selectlist('selectedItem').value;
              pattern += 'BYDAY=' + days + ';';
              pattern += 'BYSETPOS=' + pos + ';';
              pattern += 'BYMONTH=' + month + ';';
            }
          }

          var end = this.$endSelect.selectlist('selectedItem').value;
          var duration = ''; // if both UNTIL and COUNT are not specified, the recurrence will repeat forever
          // http://tools.ietf.org/html/rfc2445#section-4.3.10

          if (repeat !== 'none') {
            if (end === 'after') {
              duration = 'COUNT=' + this.$endAfter.spinbox('value') + ';';
            } else if (end === 'date') {
              duration = 'UNTIL=' + _getFormattedDate(this.$endDate.datepicker('getDate'), '') + ';';
            }
          }

          pattern += duration; // remove trailing semicolon

          pattern = pattern.substring(pattern.length - 1) === ';' ? pattern.substring(0, pattern.length - 1) : pattern;
          var data = {
            startDateTime: startDateTime,
            timeZone: timeZone,
            recurrencePattern: pattern
          };
          return data;
        },
        // called when the repeat interval changes
        // (None, Hourly, Daily, Weekdays, Weekly, Monthly, Yearly
        repeatIntervalSelectChanged: function repeatIntervalSelectChanged(e, data) {
          var selectedItem, val, txt;

          if (!data) {
            selectedItem = this.$repeatIntervalSelect.selectlist('selectedItem');
            val = selectedItem.value || "";
            txt = selectedItem.text || "";
          } else {
            val = data.value;
            txt = data.text;
          } // set the text


          this.$repeatIntervalTxt.text(txt);

          switch (val.toLowerCase()) {
            case 'hourly':
            case 'daily':
            case 'weekly':
            case 'monthly':
              this.$repeatIntervalPanel.removeClass('hide hidden'); // jQuery deprecated hide in 3.0. Use hidden instead. Leaving hide here to support previous markup

              this.$repeatIntervalPanel.attr('aria-hidden', 'false');
              break;

            default:
              this.$repeatIntervalPanel.addClass('hidden'); // jQuery deprecated hide in 3.0. Use hidden instead. Leaving hide here to support previous markup

              this.$repeatIntervalPanel.attr('aria-hidden', 'true');
              break;
          } // hide all panels


          this.$recurrencePanels.addClass('hidden');
          this.$recurrencePanels.attr('aria-hidden', 'true'); // show panel for current selection

          this.$element.find('.repeat-' + val).removeClass('hide hidden'); // jQuery deprecated hide in 3.0. Use hidden instead. Leaving hide here to support previous markup

          this.$element.find('.repeat-' + val).attr('aria-hidden', 'false'); // the end selection should only be shown when
          // the repeat interval is not "None (run once)"

          if (val === 'none') {
            this.$end.addClass('hidden');
            this.$end.attr('aria-hidden', 'true');
          } else {
            this.$end.removeClass('hide hidden'); // jQuery deprecated hide in 3.0. Use hidden instead. Leaving hide here to support previous markup

            this.$end.attr('aria-hidden', 'false');
          }

          this._guessEndDate();
        },
        _parseAndSetRecurrencePattern: function _parseAndSetRecurrencePattern(recurrencePattern, startTime) {
          var recur = {};
          var i = 0;
          var item = '';
          var commaPatternSplit;
          var $repeatMonthlyDate, $repeatYearlyDate, $repeatYearlyDay;
          var semiColonPatternSplit = recurrencePattern.toUpperCase().split(';');

          for (i = 0; i < semiColonPatternSplit.length; i++) {
            if (semiColonPatternSplit[i] !== '') {
              item = semiColonPatternSplit[i].split('=');
              recur[item[0]] = item[1];
            }
          }

          if (recur.FREQ === 'DAILY') {
            if (recur.BYDAY === 'MO,TU,WE,TH,FR') {
              item = 'weekdays';
            } else {
              if (recur.INTERVAL === '1' && recur.COUNT === '1') {
                item = 'none';
              } else {
                item = 'daily';
              }
            }
          } else if (recur.FREQ === 'SECONDLY') {
            item = 'secondly';
          } else if (recur.FREQ === 'MINUTELY') {
            item = 'minutely';
          } else if (recur.FREQ === 'HOURLY') {
            item = 'hourly';
          } else if (recur.FREQ === 'WEEKLY') {
            item = 'weekly';

            if (recur.BYDAY) {
              if (recur.BYDAY === 'MO,TU,WE,TH,FR') {
                item = 'weekdays';
              } else {
                var el = this.$element.find('.repeat-days-of-the-week .btn-group');
                el.find('label').removeClass('active');
                commaPatternSplit = recur.BYDAY.split(',');

                for (i = 0; i < commaPatternSplit.length; i++) {
                  el.find('input[data-value="' + commaPatternSplit[i] + '"]').prop('checked', true).parent().addClass('active');
                }
              }
            }
          } else if (recur.FREQ === 'MONTHLY') {
            this.$element.find('.repeat-monthly input').removeAttr('checked').removeClass('checked');
            this.$element.find('.repeat-monthly label.radio-custom').removeClass('checked');

            if (recur.BYMONTHDAY) {
              $repeatMonthlyDate = this.$element.find('.repeat-monthly-date');
              $repeatMonthlyDate.find('input').addClass('checked').prop('checked', true);
              $repeatMonthlyDate.find('label.radio-custom').addClass('checked');
              $repeatMonthlyDate.find('.selectlist').selectlist('selectByValue', recur.BYMONTHDAY);
            } else if (recur.BYDAY) {
              var $repeatMonthlyDay = this.$element.find('.repeat-monthly-day');
              $repeatMonthlyDay.find('input').addClass('checked').prop('checked', true);
              $repeatMonthlyDay.find('label.radio-custom').addClass('checked');

              if (recur.BYSETPOS) {
                $repeatMonthlyDay.find('.month-day-pos').selectlist('selectByValue', recur.BYSETPOS);
              }

              $repeatMonthlyDay.find('.month-days').selectlist('selectByValue', recur.BYDAY);
            }

            item = 'monthly';
          } else if (recur.FREQ === 'YEARLY') {
            this.$element.find('.repeat-yearly input').removeAttr('checked').removeClass('checked');
            this.$element.find('.repeat-yearly label.radio-custom').removeClass('checked');

            if (recur.BYMONTHDAY) {
              $repeatYearlyDate = this.$element.find('.repeat-yearly-date');
              $repeatYearlyDate.find('input').addClass('checked').prop('checked', true);
              $repeatYearlyDate.find('label.radio-custom').addClass('checked');

              if (recur.BYMONTH) {
                $repeatYearlyDate.find('.year-month').selectlist('selectByValue', recur.BYMONTH);
              }

              $repeatYearlyDate.find('.year-month-day').selectlist('selectByValue', recur.BYMONTHDAY);
            } else if (recur.BYSETPOS) {
              $repeatYearlyDay = this.$element.find('.repeat-yearly-day');
              $repeatYearlyDay.find('input').addClass('checked').prop('checked', true);
              $repeatYearlyDay.find('label.radio-custom').addClass('checked');
              $repeatYearlyDay.find('.year-month-day-pos').selectlist('selectByValue', recur.BYSETPOS);

              if (recur.BYDAY) {
                $repeatYearlyDay.find('.year-month-days').selectlist('selectByValue', recur.BYDAY);
              }

              if (recur.BYMONTH) {
                $repeatYearlyDay.find('.year-month').selectlist('selectByValue', recur.BYMONTH);
              }
            }

            item = 'yearly';
          } else {
            item = 'none';
          }

          if (recur.COUNT) {
            this.$endAfter.spinbox('value', parseInt(recur.COUNT, 10));
            this.$endSelect.selectlist('selectByValue', 'after');
          } else if (recur.UNTIL) {
            var untilSplit, untilDate;

            if (recur.UNTIL.length === 8) {
              untilSplit = recur.UNTIL.split('');
              untilSplit.splice(4, 0, '-');
              untilSplit.splice(7, 0, '-');
              untilDate = untilSplit.join('');
            }

            var timeZone = this.$timeZone.selectlist('selectedItem');
            var timezoneOffset = timeZone.offset === '+00:00' ? 'Z' : timeZone.offset;
            var utcEndHours = this.setUtcTime(untilDate, startTime.time24HourFormat, timezoneOffset);
            this.$endDate.datepicker('setDate', utcEndHours);
            this.$endSelect.selectlist('selectByValue', 'date');
          } else {
            this.$endSelect.selectlist('selectByValue', 'never');
          }

          this.endSelectChanged();

          if (recur.INTERVAL) {
            this.$repeatIntervalSpinbox.spinbox('value', parseInt(recur.INTERVAL, 10));
          }

          this.$repeatIntervalSelect.selectlist('selectByValue', item);
          this.repeatIntervalSelectChanged();
        },
        _parseStartDateTime: function _parseStartDateTime(startTimeISO8601) {
          var startTime = {};
          var hours, minutes, period;
          startTime.time24HourFormat = startTimeISO8601.split('+')[0].split('-')[0];

          if (startTimeISO8601.search(/\+/) > -1) {
            startTime.timeZoneOffset = '+' + $$$1.trim(startTimeISO8601.split('+')[1]);
          } else if (startTimeISO8601.search(/\-/) > -1) {
            startTime.timeZoneOffset = '-' + $$$1.trim(startTimeISO8601.split('-')[1]);
          } else {
            startTime.timeZoneOffset = '+00:00';
          }

          startTime.time24HourFormatSplit = startTime.time24HourFormat.split(':');
          hours = parseInt(startTime.time24HourFormatSplit[0], 10);
          minutes = startTime.time24HourFormatSplit[1] ? parseInt(startTime.time24HourFormatSplit[1].split('+')[0].split('-')[0].split('Z')[0], 10) : 0;
          period = hours < 12 ? 'AM' : 'PM';

          if (hours === 0) {
            hours = 12;
          } else if (hours > 12) {
            hours -= 12;
          }

          minutes = minutes < 10 ? '0' + minutes : minutes;
          startTime.time12HourFormat = hours + ':' + minutes;
          startTime.time12HourFormatWithPeriod = hours + ':' + minutes + ' ' + period;
          return startTime;
        },
        _parseTimeZone: function _parseTimeZone(options, startTime) {
          startTime.timeZoneQuerySelector = '';

          if (options.timeZone) {
            if (typeof options.timeZone === 'string') {
              startTime.timeZoneQuerySelector += 'li[data-name="' + options.timeZone + '"]';
            } else {
              $$$1.each(options.timeZone, function (key, value) {
                startTime.timeZoneQuerySelector += 'li[data-' + key + '="' + value + '"]';
              });
            }

            startTime.timeZoneOffset = options.timeZone.offset;
          } else if (options.startDateTime) {
            // Time zone has not been specified via options object, therefore use the timeZoneOffset from _parseAndSetStartDateTime
            startTime.timeZoneOffset = startTime.timeZoneOffset === '+00:00' ? 'Z' : startTime.timeZoneOffset;
            startTime.timeZoneQuerySelector += 'li[data-offset="' + startTime.timeZoneOffset + '"]';
          } else {
            startTime.timeZoneOffset = 'Z';
          }

          return startTime.timeZoneOffset;
        },
        _setTimeUI: function _setTimeUI(time12HourFormatWithPeriod) {
          this.$startTime.find('input').val(time12HourFormatWithPeriod);
          this.$startTime.combobox('selectByText', time12HourFormatWithPeriod);
        },
        _setTimeZoneUI: function _setTimeZoneUI(querySelector) {
          this.$timeZone.selectlist('selectBySelector', querySelector);
        },
        setValue: function setValue(options) {
          var startTime = {};
          var startDateTime, startDate, startTimeISO8601, utcStartHours; // TIME

          if (options.startDateTime) {
            startDateTime = options.startDateTime.split('T');
            startDate = startDateTime[0];
            startTimeISO8601 = startDateTime[1];

            if (startTimeISO8601) {
              startTime = this._parseStartDateTime(startTimeISO8601);

              this._setTimeUI(startTime.time12HourFormatWithPeriod);
            } else {
              startTime.time12HourFormat = '00:00';
              startTime.time24HourFormat = '00:00';
            }
          } else {
            startTime.time12HourFormat = '00:00';
            startTime.time24HourFormat = '00:00';
            var currentDate = this.$startDate.datepicker('getDate');
            startDate = currentDate.getFullYear() + '-' + currentDate.getMonth() + '-' + currentDate.getDate();
          } // TIMEZONE


          this._parseTimeZone(options, startTime);

          if (startTime.timeZoneQuerySelector) {
            this._setTimeZoneUI(startTime.timeZoneQuerySelector);
          } // RECURRENCE PATTERN


          if (options.recurrencePattern) {
            this._parseAndSetRecurrencePattern(options.recurrencePattern, startTime);
          }

          utcStartHours = this.setUtcTime(startDate, startTime.time24HourFormat, startTime.timeZoneOffset);
          this.$startDate.datepicker('setDate', utcStartHours);
        },
        toggleState: function toggleState(action) {
          this.$element.find('.combobox').combobox(action);
          this.$element.find('.datepicker').datepicker(action);
          this.$element.find('.selectlist').selectlist(action);
          this.$element.find('.spinbox').spinbox(action);
          this.$element.find('.radio-custom').radio(action);

          if (action === 'disable') {
            action = 'addClass';
          } else {
            action = 'removeClass';
          }

          this.$element.find('.repeat-days-of-the-week .btn-group')[action]('disabled');
        },
        value: function value(options) {
          if (options) {
            return this.setValue(options);
          } else {
            return this.getValue();
          }
        }
      }; // SCHEDULER PLUGIN DEFINITION

      $$$1.fn.scheduler = function scheduler(option) {
        var args = Array.prototype.slice.call(arguments, 1);
        var methodReturn;
        var $set = this.each(function () {
          var $this = $$$1(this);
          var data = $this.data('fu.scheduler');
          var options = typeof option === 'object' && option;

          if (!data) {
            $this.data('fu.scheduler', data = new Scheduler(this, options));
          }

          if (typeof option === 'string') {
            methodReturn = data[option].apply(data, args);
          }
        });
        return methodReturn === undefined ? $set : methodReturn;
      };

      $$$1.fn.scheduler.defaults = {};
      $$$1.fn.scheduler.Constructor = Scheduler;

      $$$1.fn.scheduler.noConflict = function noConflict() {
        $$$1.fn.scheduler = old;
        return this;
      }; // DATA-API


      $$$1(document).on('mousedown.fu.scheduler.data-api', '[data-initialize=scheduler]', function (e) {
        var $control = $$$1(e.target).closest('.scheduler');

        if (!$control.data('fu.scheduler')) {
          $control.scheduler($control.data());
        }
      }); // Must be domReady for AMD compatibility

      $$$1(function () {
        $$$1('[data-initialize=scheduler]').each(function () {
          var $this = $$$1(this);
          if ($this.data('scheduler')) return;
          $this.scheduler($this.data());
        });
      });
    })(jQuery);

    (function ($$$1) {
      /* global jQuery:true */

      /*
       * Fuel UX Picker
       * https://github.com/ExactTarget/fuelux
       *
       * Copyright (c) 2014 ExactTarget
       * Licensed under the BSD New license.
       */
      // -- BEGIN MODULE CODE HERE --
      var old = $$$1.fn.picker; // PLACARD CONSTRUCTOR AND PROTOTYPE

      var Picker = function Picker(element, options) {
        var self = this;
        this.$element = $$$1(element);
        this.options = $$$1.extend({}, $$$1.fn.picker.defaults, options);
        this.$accept = this.$element.find('.picker-accept');
        this.$cancel = this.$element.find('.picker-cancel');
        this.$trigger = this.$element.find('.picker-trigger');
        this.$footer = this.$element.find('.picker-footer');
        this.$header = this.$element.find('.picker-header');
        this.$popup = this.$element.find('.picker-popup');
        this.$body = this.$element.find('.picker-body');
        this.clickStamp = '_';
        this.isInput = this.$trigger.is('input');
        this.$trigger.on('keydown.fu.picker', $$$1.proxy(this.keyComplete, this));
        this.$trigger.on('focus.fu.picker', $$$1.proxy(function inputFocus(e) {
          if (typeof e === "undefined" || $$$1(e.target).is('input[type=text]')) {
            $$$1.proxy(this.show(), this);
          }
        }, this));
        this.$trigger.on('click.fu.picker', $$$1.proxy(function triggerClick(e) {
          if (!$$$1(e.target).is('input[type=text]')) {
            $$$1.proxy(this.toggle(), this);
          } else {
            $$$1.proxy(this.show(), this);
          }
        }, this));
        this.$accept.on('click.fu.picker', $$$1.proxy(this.complete, this, 'accepted'));
        this.$cancel.on('click.fu.picker', function (e) {
          e.preventDefault();
          self.complete('cancelled');
        });
      };

      var _isOffscreen = function _isOffscreen(picker) {
        var windowHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
        var scrollTop = $$$1(document).scrollTop();
        var popupTop = picker.$popup.offset();
        var popupBottom = popupTop.top + picker.$popup.outerHeight(true); //if the bottom of the popup goes off the page, but the top does not, dropup.

        if (popupBottom > windowHeight + scrollTop || popupTop.top < scrollTop) {
          return true;
        } else {
          //otherwise, prefer showing the top of the popup only vs the bottom
          return false;
        }
      };

      var _display = function _display(picker) {
        picker.$popup.css('visibility', 'hidden');

        _showBelow(picker); //if part of the popup is offscreen try to show it above


        if (_isOffscreen(picker)) {
          _showAbove(picker); //if part of the popup is still offscreen, prefer cutting off the bottom


          if (_isOffscreen(picker)) {
            _showBelow(picker);
          }
        }

        picker.$popup.css('visibility', 'visible');
      };

      var _showAbove = function _showAbove(picker) {
        picker.$popup.css('top', -picker.$popup.outerHeight(true) + 'px');
      };

      var _showBelow = function _showBelow(picker) {
        picker.$popup.css('top', picker.$trigger.outerHeight(true) + 'px');
      };

      Picker.prototype = {
        constructor: Picker,
        complete: function complete(action) {
          var EVENT_CALLBACK_MAP = {
            'accepted': 'onAccept',
            'cancelled': 'onCancel',
            'exited': 'onExit'
          };
          var func = this.options[EVENT_CALLBACK_MAP[action]];
          var obj = {
            contents: this.$body
          };

          if (func) {
            func(obj);
            this.$element.trigger(action + '.fu.picker', obj);
          } else {
            this.$element.trigger(action + '.fu.picker', obj);
            this.hide();
          }
        },
        keyComplete: function keyComplete(e) {
          if (this.isInput && e.keyCode === 13) {
            this.complete('accepted');
            this.$trigger.blur();
          } else if (e.keyCode === 27) {
            this.complete('exited');
            this.$trigger.blur();
          }
        },
        destroy: function destroy() {
          this.$element.remove(); // remove any external bindings

          $$$1(document).off('click.fu.picker.externalClick.' + this.clickStamp); // empty elements to return to original markup
          // [none]
          // return string of markup

          return this.$element[0].outerHTML;
        },
        disable: function disable() {
          this.$element.addClass('disabled');
          this.$trigger.attr('disabled', 'disabled');
        },
        enable: function enable() {
          this.$element.removeClass('disabled');
          this.$trigger.removeAttr('disabled');
        },
        toggle: function toggle() {
          if (this.$element.hasClass('showing')) {
            this.hide();
          } else {
            this.show();
          }
        },
        hide: function hide() {
          if (!this.$element.hasClass('showing')) {
            return;
          }

          this.$element.removeClass('showing');
          $$$1(document).off('click.fu.picker.externalClick.' + this.clickStamp);
          this.$element.trigger('hidden.fu.picker');
        },
        externalClickListener: function externalClickListener(e, force) {
          if (force === true || this.isExternalClick(e)) {
            this.complete('exited');
          }
        },
        isExternalClick: function isExternalClick(e) {
          var el = this.$element.get(0);
          var exceptions = this.options.externalClickExceptions || [];
          var $originEl = $$$1(e.target);
          var i, l;

          if (e.target === el || $originEl.parents('.picker:first').get(0) === el) {
            return false;
          } else {
            for (i = 0, l = exceptions.length; i < l; i++) {
              if ($originEl.is(exceptions[i]) || $originEl.parents(exceptions[i]).length > 0) {
                return false;
              }
            }
          }

          return true;
        },
        show: function show() {
          var other;
          other = $$$1(document).find('.picker.showing');

          if (other.length > 0) {
            if (other.data('fu.picker') && other.data('fu.picker').options.explicit) {
              return;
            }

            other.picker('externalClickListener', {}, true);
          }

          this.$element.addClass('showing');

          _display(this);

          this.$element.trigger('shown.fu.picker');
          this.clickStamp = new Date().getTime() + (Math.floor(Math.random() * 100) + 1);

          if (!this.options.explicit) {
            $$$1(document).on('click.fu.picker.externalClick.' + this.clickStamp, $$$1.proxy(this.externalClickListener, this));
          }
        }
      }; // PLACARD PLUGIN DEFINITION

      $$$1.fn.picker = function picker(option) {
        var args = Array.prototype.slice.call(arguments, 1);
        var methodReturn;
        var $set = this.each(function () {
          var $this = $$$1(this);
          var data = $this.data('fu.picker');
          var options = typeof option === 'object' && option;

          if (!data) {
            $this.data('fu.picker', data = new Picker(this, options));
          }

          if (typeof option === 'string') {
            methodReturn = data[option].apply(data, args);
          }
        });
        return methodReturn === undefined ? $set : methodReturn;
      };

      $$$1.fn.picker.defaults = {
        onAccept: undefined,
        onCancel: undefined,
        onExit: undefined,
        externalClickExceptions: [],
        explicit: false
      };
      $$$1.fn.picker.Constructor = Picker;

      $$$1.fn.picker.noConflict = function noConflict() {
        $$$1.fn.picker = old;
        return this;
      }; // DATA-API


      $$$1(document).on('focus.fu.picker.data-api', '[data-initialize=picker]', function (e) {
        var $control = $$$1(e.target).closest('.picker');

        if (!$control.data('fu.picker')) {
          $control.picker($control.data());
        }
      }); // Must be domReady for AMD compatibility

      $$$1(function () {
        $$$1('[data-initialize=picker]').each(function () {
          var $this = $$$1(this);
          if ($this.data('fu.picker')) return;
          $this.picker($this.data());
        });
      });
    })(jQuery);
  });

  (function ($$$1) {
    if (typeof $$$1 === 'undefined') {
      throw new TypeError('CMDB\'s JavaScript requires jQuery. jQuery must be included before CMDB\'s JavaScript.');
    }
  })($);
  //import './vendors/form-render.js';

  $(document).ready(function () {
    $('.nav-dropdown-toggle').on('click', function (e) {
      e.preventDefault();
      $(this).parent().toggleClass('open');
    });
    $('ul.nav').find('a.active').parent().parent().parent().addClass('open');
    $('.sidebar-toggle').on('click', function (e) {
      e.preventDefault();
      $('body').toggleClass('sidebar-hidden');
    });
    $('.sidebar-mobile-toggle').on('click', function () {
      $('body').toggleClass('sidebar-mobile-show');
    });
    $('input#category_filter').quicksearch('#sidebar .sidebar-categories .nav-link');
    $('.data_table').each(function () {
      $(this).DataTable();
    });
    $('.data_table').quicksearch();
  });

})));
//# sourceMappingURL=cmdb.js.map
