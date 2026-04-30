/**
 * Store único para filtros / preferencias UI (localStorage) + suscripción tras persist.
 * Carga antes de app.js.
 */
(function (global) {
  const LS_FILTERS = "jmc_filters_v1";
  const listeners = new Set();

  function subscribe(fn) {
    listeners.add(fn);
    return function unsubscribe() {
      listeners.delete(fn);
    };
  }

  function notify() {
    listeners.forEach(function (fn) {
      try {
        fn();
      } catch (_) {}
    });
  }

  function read() {
    try {
      return JSON.parse(global.localStorage.getItem(LS_FILTERS) || "{}");
    } catch (_) {
      return {};
    }
  }

  function write(data) {
    try {
      global.localStorage.setItem(LS_FILTERS, JSON.stringify(data));
    } catch (_) {}
    notify();
  }

  global.jmcFilterStore = {
    LS_FILTERS: LS_FILTERS,
    subscribe: subscribe,
    read: read,
    write: write,
  };
})(typeof window !== "undefined" ? window : globalThis);
