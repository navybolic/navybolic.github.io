(function () {
  const SYNC_URL_KEY = "capx-sync-url";
  const SYNC_TOKEN = "navybolic-capx";
  const $ = (id) => document.getElementById(id);
  let saveTimer = null;
  function setSyncStatus(msg) {
    const el = $("sync-status");
    if (el) el.textContent = msg;
  }
  async function cloudSave() {
    const url = localStorage.getItem(SYNC_URL_KEY);
    if (!url || typeof state === "undefined") return;
    setSyncStatus("Saving to Drive…");
    try {
      await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "text/plain;charset=utf-8" },
        body: JSON.stringify({ action: "save", token: SYNC_TOKEN, state }),
      });
      setSyncStatus("Saved to Drive");
    } catch (err) {
      setSyncStatus("Drive save failed — kept on this device");
    }
  }
  async function cloudLoad() {
    const url = localStorage.getItem(SYNC_URL_KEY);
    if (!url) {
      setSyncStatus("Drive sync off — this device only");
      return;
    }
    setSyncStatus("Loading from Drive…");
    try {
      const r = await fetch(url + "?action=load&token=" + encodeURIComponent(SYNC_TOKEN));
      const data = await r.json();
      if (data && data.state && typeof state !== "undefined") {
        const incoming = data.state.updatedAt || 0;
        const local = state.updatedAt || 0;
        if (incoming >= local) {
          Object.keys(data.state).forEach((k) => { state[k] = data.state[k]; });
          localStorage.setItem("capx-trainer-v1", JSON.stringify(state));
          setSyncStatus("Loaded from Drive");
          if (typeof renderHome === "function") renderHome();
        } else {
          setSyncStatus("This device is up to date");
        }
      } else {
        setSyncStatus("Drive connected, no saved session yet");
      }
    } catch (err) {
      setSyncStatus("Could not reach Drive — using this device");
    }
  }
  function connectSync(fromId) {
    const box = $(fromId) || $("sync-url") || $("sync-url-home");
    const v = ((box && box.value) || "").trim();
    if (!v) {
      localStorage.removeItem(SYNC_URL_KEY);
      setSyncStatus("Drive sync off — this device only");
      alert("Drive sync is off on this device.");
      return;
    }
    localStorage.setItem(SYNC_URL_KEY, v);
    setSyncStatus("Drive sync connected — talking to Drive…");
    alert("Saved the Drive address on this device. Checking Drive now.");
    cloudLoad().then(cloudSave).then(() => {
      alert(( $("sync-status") && $("sync-status").textContent) || "Finished talking to Drive.");
    });
  }
  function bind() {
    const a = $("sync-save-btn");
    const b = $("sync-save-home-btn");
    if (a) a.onclick = () => connectSync("sync-url");
    if (b) b.onclick = () => connectSync("sync-url-home");
    const saved = localStorage.getItem(SYNC_URL_KEY) || "";
    ["sync-url", "sync-url-home"].forEach((id) => {
      const el = $(id);
      if (el && !el.value) el.value = saved;
    });
    if (localStorage.getItem(SYNC_URL_KEY)) cloudLoad();
    else setSyncStatus("Drive sync off — paste the script URL below");
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", bind);
  else setTimeout(bind, 250);
})();
