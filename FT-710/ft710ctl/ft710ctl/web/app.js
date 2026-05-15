// ft710ctl frontend.
//
// Connects to /ws, mirrors the radio state, and dispatches user input back
// as `set` messages. Panels register render functions that read from
// `state` and update DOM nodes; render() is called after every state change.

const state = {
  scope: {},
  tuning: {},
  rx: {},
  meters: {},
};

const renderers = [];

function registerRenderer(fn) {
  renderers.push(fn);
}

function render() {
  for (const fn of renderers) {
    try {
      fn(state);
    } catch (err) {
      console.error("renderer threw:", err);
    }
  }
  const dump = document.getElementById("state-dump");
  if (dump) dump.textContent = JSON.stringify(state, null, 2);
}

// ---- WebSocket plumbing --------------------------------------------------

let ws = null;
let reconnectDelay = 500;
const RECONNECT_MAX = 5000;
const pendingRequests = new Map(); // request_id → {field, resolve, reject, timeout}

function setBanner(port_state) {
  const banner = document.getElementById("port-banner");
  if (!banner) return;
  banner.classList.remove(
    "banner--connected",
    "banner--disconnected",
    "banner--connecting",
  );
  banner.classList.add(`banner--${port_state}`);
  banner.dataset.state = port_state;
  const label = banner.querySelector(".banner__label");
  if (label) {
    label.textContent =
      port_state === "connected" ? "connected" :
      port_state === "disconnected" ? "disconnected (retrying…)" :
      "connecting…";
  }
}

function applySnapshot(snap) {
  Object.assign(state.scope, snap.scope || {});
  Object.assign(state.tuning, snap.tuning || {});
  Object.assign(state.rx, snap.rx || {});
  Object.assign(state.meters, snap.meters || {});
}

function applyPatch(field, value) {
  const [section, ...rest] = field.split(".");
  const path = rest.join(".");
  if (!state[section]) state[section] = {};
  // For dotted leaves like "scope.af_fft.mode", store under the dotted leaf
  // (keeps the mirror flat and simple to read).
  if (path.includes(".")) {
    state[section][path] = value;
  } else {
    state[section][path] = value;
  }
}

function handleMessage(msg) {
  switch (msg.op) {
    case "snapshot":
      applySnapshot(msg.state);
      render();
      break;
    case "patch":
      applyPatch(msg.field, msg.value);
      render();
      break;
    case "port":
      setBanner(msg.state);
      break;
    case "ack": {
      const p = pendingRequests.get(msg.request_id);
      if (p) {
        clearTimeout(p.timeout);
        p.resolve();
        pendingRequests.delete(msg.request_id);
      }
      break;
    }
    case "error": {
      console.warn("set error:", msg);
      const p = pendingRequests.get(msg.request_id);
      if (p) {
        clearTimeout(p.timeout);
        p.reject(new Error(msg.reason || "unknown error"));
        pendingRequests.delete(msg.request_id);
      }
      break;
    }
    default:
      console.warn("unknown op:", msg);
  }
}

function connect() {
  setBanner("connecting");
  const proto = location.protocol === "https:" ? "wss" : "ws";
  ws = new WebSocket(`${proto}://${location.host}/ws`);
  ws.addEventListener("open", () => {
    reconnectDelay = 500;
  });
  ws.addEventListener("message", (ev) => {
    let msg;
    try {
      msg = JSON.parse(ev.data);
    } catch (err) {
      console.error("bad JSON from ws:", err);
      return;
    }
    handleMessage(msg);
  });
  ws.addEventListener("close", () => {
    setBanner("disconnected");
    for (const p of pendingRequests.values()) {
      clearTimeout(p.timeout);
      p.reject(new Error("socket closed"));
    }
    pendingRequests.clear();
    setTimeout(connect, reconnectDelay);
    reconnectDelay = Math.min(RECONNECT_MAX, reconnectDelay * 2);
  });
  ws.addEventListener("error", (ev) => {
    console.warn("ws error:", ev);
  });
}

let nextRequestId = 1;

function sendSet(field, value) {
  if (!ws || ws.readyState !== WebSocket.OPEN) {
    return Promise.reject(new Error("socket not open"));
  }
  const request_id = `r${nextRequestId++}`;
  const msg = { op: "set", field, request_id };
  if (value !== undefined) msg.value = value;
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => {
      pendingRequests.delete(request_id);
      reject(new Error("set timed out"));
    }, 5000);
    pendingRequests.set(request_id, { field, resolve, reject, timeout });
    ws.send(JSON.stringify(msg));
  });
}

// ---- Field binding helpers ----------------------------------------------
//
// Each data-field element binds bidirectionally:
//   * State patches push into the DOM via render().
//   * User input fires sendSet(field, coerced_value).

function getFieldValue(field) {
  let cur = state;
  for (const part of field.split(".")) {
    if (cur === null || cur === undefined || typeof cur !== "object") return undefined;
    cur = cur[part];
  }
  return cur;
}

function coerceFromInput(el) {
  if (el.type === "checkbox") return el.checked;
  // MHz → Hz on the way out for frequency inputs.
  if (el.dataset.coerce === "mhz") {
    const mhz = Number(el.value);
    return Number.isFinite(mhz) ? Math.round(mhz * 1_000_000) : el.value;
  }
  if (el.type === "number" || el.type === "range") {
    const n = Number(el.value);
    return Number.isFinite(n) ? n : el.value;
  }
  // <select> with numeric option values: keep numeric.
  if (el.tagName === "SELECT") {
    const v = el.value;
    const n = Number(v);
    return /^[+-]?\d+(\.\d+)?$/.test(v) && Number.isFinite(n) ? n : v;
  }
  return el.value;
}

function pushIntoElement(el, value) {
  if (value === null || value === undefined) return;
  if (el.type === "checkbox") {
    el.checked = Boolean(value);
    return;
  }
  if (document.activeElement === el) {
    return;  // don't clobber while the user is interacting
  }
  if (el.dataset.coerce === "mhz") {
    el.value = (Number(value) / 1_000_000).toFixed(6);
    return;
  }
  el.value = String(value);
}

function bindDataFieldElements() {
  document.querySelectorAll("[data-field]").forEach((el) => {
    const field = el.dataset.field;
    const eventName =
      el.tagName === "SELECT" || el.type === "checkbox" ? "change" : "input";
    el.addEventListener(eventName, () => {
      const value = coerceFromInput(el);
      sendSet(field, value).catch((err) => {
        console.warn(`set ${field}=${value} failed:`, err.message);
      });
    });
  });

  // Action buttons send a fire-and-forget set with no value (e.g. swap_vfo).
  document.querySelectorAll("[data-action]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const field = btn.dataset.action;
      sendSet(field, undefined).catch((err) => {
        console.warn(`action ${field} failed:`, err.message);
      });
    });
  });
}

function renderDataFieldElements() {
  document.querySelectorAll("[data-field]").forEach((el) => {
    // Some fields are write-only from the UI's perspective (band has no Read);
    // skip echoing state into them entirely.
    if (el.dataset.setOnly === "true") return;
    const value = getFieldValue(el.dataset.field);
    pushIntoElement(el, value);
  });
}

// Scope: keep the ref-level display label in sync with the slider.
function renderScopeRefDisplay() {
  const slider = document.getElementById("scope-ref");
  const display = document.getElementById("scope-ref-display");
  if (slider && display) {
    const v = Number(slider.value);
    display.textContent = `${v >= 0 ? "+" : ""}${v.toFixed(1)} dB`;
  }
}

registerRenderer(renderDataFieldElements);
registerRenderer(renderScopeRefDisplay);

// ---- Boot ----------------------------------------------------------------

window.addEventListener("DOMContentLoaded", () => {
  bindDataFieldElements();
  connect();
});

// Expose hooks for panel modules (Task 37+).
window.ft710 = { state, registerRenderer, sendSet };
