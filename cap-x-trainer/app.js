const DOMAIN_NAME = {
  I: "I Business problem framing",
  II: "II Analytics problem framing",
  III: "III Data",
  IV: "IV Methodology selection",
  V: "V Model development",
  VI: "VI Deployment",
  VII: "VII Lifecycle management",
};
const FORM_SIZE = 115;
const TARGETS = { I: 18, II: 20, III: 24, IV: 15, V: 18, VI: 12, VII: 8 };
const STORE = "capx-trainer-v1";

const $ = (id) => document.getElementById(id);
let BANK = null;
let state = loadState();
let tickHandle = null;

function loadState() {
  try {
    return JSON.parse(localStorage.getItem(STORE)) || defaultState();
  } catch {
    return defaultState();
  }
}
function defaultState() {
  return {
    sessionId: null,
    bankSlot: "A",
    formIds: [],
    index: 0,
    answers: {},
    flagged: {},
    timed: false,
    remainingSec: 3 * 60 * 60,
    running: false,
    filterDomain: "ALL",
    tallyResetAt: 0,
    history: [],
  };
}
function saveState() {
  localStorage.setItem(STORE, JSON.stringify(state));
}

function byId(id) {
  return BANK.questions.find((q) => q.question_id === id);
}

function shuffle(arr, seed) {
  const a = arr.slice();
  let s = seed || Date.now() % 2147483647;
  const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rnd() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function buildForm(seed) {
  const eligible = BANK.questions.filter((q) => q.status !== "retired");
  const byD = { I: [], II: [], III: [], IV: [], V: [], VI: [], VII: [] };
  eligible.forEach((q) => byD[q.domain] && byD[q.domain].push(q.question_id));
  Object.keys(byD).forEach((d) => {
    byD[d] = shuffle(byD[d], seed + d.charCodeAt(0));
  });
  const picked = [];
  const used = new Set();
  for (const [d, n] of Object.entries(TARGETS)) {
    const take = byD[d].slice(0, n);
    take.forEach((id) => used.add(id));
    picked.push(...take);
  }
  if (picked.length < FORM_SIZE) {
    const rest = shuffle(
      eligible.map((q) => q.question_id).filter((id) => !used.has(id)),
      seed + 99
    );
    while (picked.length < FORM_SIZE && rest.length) picked.push(rest.shift());
  }
  if (picked.length < FORM_SIZE) {
    const extra = shuffle(eligible.map((q) => q.question_id), seed + 7);
    let i = 0;
    while (picked.length < FORM_SIZE && extra.length) {
      picked.push(extra[i++ % extra.length]);
    }
  }
  return shuffle(picked.slice(0, FORM_SIZE), seed + 3);
}

function currentIds() {
  if (state.filterDomain !== "ALL") {
    return BANK.questions
      .filter((q) => q.domain === state.filterDomain)
      .map((q) => q.question_id);
  }
  return state.formIds;
}

function startNew({ timed, domain, slot }) {
  state.bankSlot = slot || state.bankSlot || "A";
  state.filterDomain = domain || "ALL";
  state.timed = !!timed;
  state.remainingSec = 3 * 60 * 60;
  state.running = true;
  state.sessionId = "S-" + new Date().toISOString().replace(/[:.]/g, "").slice(0, 15) + "-" + state.bankSlot;
  state.formIds = buildForm(Date.now());
  state.index = 0;
  state.answers = {};
  state.flagged = {};
  saveState();
  showQuiz();
}

function continueSession() {
  if (!state.formIds.length) return startNew({ timed: false, domain: "ALL", slot: "A" });
  state.running = true;
  saveState();
  showQuiz();
}

function tally() {
  let right = 0, wrong = 0, blank = 0;
  const ids = currentIds();
  ids.forEach((id) => {
    const q = byId(id);
    const a = state.answers[id];
    if (!a) blank++;
    else if (a === q.correct_key) right++;
    else wrong++;
  });
  return { right, wrong, blank, total: ids.length };
}

function renderHome() {
  $("view-home").classList.remove("hidden");
  $("view-quiz").classList.add("hidden");
  $("pool-count").textContent = BANK.question_count;
  const t = tally();
  $("home-tally").textContent = `Saved session: ${t.right} right / ${t.wrong} wrong / ${t.blank} blank of ${t.total || 0}`;
  $("continue-btn").disabled = !state.formIds.length;
  $("mode").value = state.timed ? "timed" : "untimed";
  $("slot").value = state.bankSlot || "A";
  $("domain").value = state.filterDomain || "ALL";
  paintTimer();
}

function showQuiz() {
  $("view-home").classList.add("hidden");
  $("view-quiz").classList.remove("hidden");
  renderQuestion();
  startClock();
}

function startClock() {
  if (tickHandle) clearInterval(tickHandle);
  tickHandle = setInterval(() => {
    if (!state.timed || !state.running) return;
    state.remainingSec = Math.max(0, state.remainingSec - 1);
    if (state.remainingSec === 0) state.running = false;
    saveState();
    paintTimer();
  }, 1000);
  paintTimer();
}

function paintTimer() {
  const el = $("timer");
  if (!state.timed) {
    el.textContent = "Untimed";
    el.className = "timer";
    return;
  }
  const s = state.remainingSec;
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sec = s % 60;
  el.textContent = `${h}:${String(m).padStart(2, "0")}:${String(sec).padStart(2, "0")}`;
  el.className = "timer" + (s < 300 ? " hot" : s < 900 ? " warn" : "");
}

function renderQuestion() {
  const ids = currentIds();
  if (!ids.length) return;
  if (state.index < 0) state.index = 0;
  if (state.index >= ids.length) state.index = ids.length - 1;
  const id = ids[state.index];
  const q = byId(id);
  const chosen = state.answers[id];
  $("qmeta").textContent = `${DOMAIN_NAME[q.domain]} · ${q.difficulty || ""} · ${q.topic || ""}`;
  $("qpos").textContent = `Question ${state.index + 1} of ${ids.length} · ${id} · Bank ${state.bankSlot}`;
  $("stem").textContent = q.stem;
  const box = $("options");
  box.innerHTML = "";
  q.options.forEach((opt) => {
    const b = document.createElement("button");
    b.className = "opt";
    if (chosen) {
      if (opt.key === q.correct_key) b.classList.add("correct");
      if (opt.key === chosen && chosen !== q.correct_key) b.classList.add("wrong");
    }
    if (chosen === opt.key) b.classList.add("chosen");
    b.innerHTML = `<span class="k">${opt.key}.</span> ${escapeHtml(opt.text)}`;
    b.onclick = () => answer(opt.key);
    box.appendChild(b);
  });
  renderExplain(q, chosen);
  const t = tally();
  $("live-tally").innerHTML = `<b>${t.right}</b> right · <b>${t.wrong}</b> wrong · <b>${t.blank}</b> unanswered`;
  $("flag-btn").textContent = state.flagged[id] ? "Unflag" : "Flag";
  const modeLive = $("mode-live");
  if (modeLive) modeLive.value = state.timed ? "timed" : "untimed";
  paintNav(ids);
  paintTimer();
  saveState();
}

function renderExplain(q, chosen) {
  const el = $("explain");
  if (!chosen) {
    el.classList.add("hidden");
    el.innerHTML = "";
    return;
  }
  el.classList.remove("hidden");
  const ok = chosen === q.correct_key;
  let html = `<p><b>${ok ? "Correct" : "Incorrect"}.</b> You chose ${chosen}. Official key is ${q.correct_key}.</p>`;
  q.options.forEach((opt) => {
    html += `<h3>${opt.key}. ${opt.is_correct ? "Why this is right" : "Why this is wrong"}</h3>`;
    html += `<p>${escapeHtml(opt.rationale || "")}</p>`;
    (opt.citations || []).forEach((c) => {
      const loc = c.locator ? ` — ${escapeHtml(c.locator)}` : "";
      const link = c.url
        ? `<a href="${c.url}" target="_blank" rel="noopener">${escapeHtml(c.source || c.url)}</a>`
        : escapeHtml(c.source || "");
      html += `<p class="cite">${link}${loc}</p>`;
    });
  });
  el.innerHTML = html;
}

function answer(key) {
  const ids = currentIds();
  const id = ids[state.index];
  state.answers[id] = key;
  state.history.push({ at: new Date().toISOString(), id, key, session: state.sessionId });
  saveState();
  renderQuestion();
}

function go(delta) {
  state.index += delta;
  const ids = currentIds();
  state.index = Math.max(0, Math.min(ids.length - 1, state.index));
  renderQuestion();
}

function jumpTo() {
  const map = $("navq");
  const n = parseInt($("jump").value, 10);
  const ids = currentIds();
  if (n >= 1 && n <= ids.length) {
    state.index = n - 1;
    $("jump").value = "";
    renderQuestion();
    map.classList.remove("hidden");
    return;
  }
  map.classList.toggle("hidden");
}

function paintNav(ids) {
  const nav = $("navq");
  if (!nav) return;
  nav.innerHTML = "";
  ids.forEach((id, i) => {
    const q = byId(id);
    const b = document.createElement("button");
    b.type = "button";
    b.textContent = i + 1;
    if (i === state.index) b.classList.add("now");
    const a = state.answers[id];
    if (a && a === q.correct_key) b.classList.add("done");
    else if (a) b.classList.add("miss");
    if (state.flagged[id]) b.classList.add("flag");
    b.onclick = () => {
      state.index = i;
      renderQuestion();
    };
    nav.appendChild(b);
  });
}

function resetTally() {
  if (!confirm("Reset answers and tally for this session? Questions stay the same.")) return;
  state.answers = {};
  state.history = [];
  state.tallyResetAt = Date.now();
  state.index = 0;
  saveState();
  renderQuestion();
}

function restartForm() {
  if (!confirm("Restart this form from question 1 and clear answers?")) return;
  state.answers = {};
  state.index = 0;
  state.remainingSec = state.timed ? 3 * 60 * 60 : state.remainingSec;
  saveState();
  renderQuestion();
}

function shuffleForm() {
  if (!confirm("Shuffle a new 115-question form from the main bank? Current answers on this form will clear.")) return;
  startNew({ timed: state.timed, domain: "ALL", slot: state.bankSlot });
}

function toggleFlag() {
  const id = currentIds()[state.index];
  if (state.flagged[id]) delete state.flagged[id];
  else state.flagged[id] = true;
  renderQuestion();
}

function exportProgress() {
  const blob = new Blob(
    [JSON.stringify({ exported_at: new Date().toISOString(), state, tally: tally() }, null, 2)],
    { type: "application/json" }
  );
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `capx-progress-${state.sessionId || "none"}.json`;
  a.click();
}

function importProgress(file) {
  const reader = new FileReader();
  reader.onload = () => {
    try {
      const data = JSON.parse(reader.result);
      if (data.state) state = data.state;
      saveState();
      showQuiz();
    } catch (e) {
      alert("Could not read that progress file.");
    }
  };
  reader.readAsText(file);
}

function printStudy() {
  const wrap = $("print-root");
  wrap.innerHTML = "";
  currentIds().forEach((id, i) => {
    const q = byId(id);
    const div = document.createElement("section");
    div.className = "card";
    div.style.margin = "12px 0";
    let html = `<p class="pill">${i + 1}. ${id} · ${DOMAIN_NAME[q.domain]}</p><p class="stem">${escapeHtml(q.stem)}</p>`;
    q.options.forEach((opt) => {
      html += `<p><b>${opt.key}.</b> ${escapeHtml(opt.text)} ${opt.is_correct ? "(KEY)" : ""}</p>`;
      html += `<p>${escapeHtml(opt.rationale || "")}</p>`;
      (opt.citations || []).forEach((c) => {
        html += `<p class="cite">${escapeHtml(c.source || "")} — ${escapeHtml(c.locator || "")} ${c.url || ""}</p>`;
      });
    });
    div.innerHTML = html;
    wrap.appendChild(div);
  });
  window.print();
}

function escapeHtml(s) {
  return String(s || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function wire() {
  $("start-btn").onclick = () =>
    startNew({
      timed: $("mode").value === "timed",
      domain: $("domain").value,
      slot: $("slot").value,
    });
  $("continue-btn").onclick = continueSession;
  $("prev-btn").onclick = () => go(-1);
  $("next-btn").onclick = () => go(1);
  $("jump-btn").onclick = jumpTo;
  $("jump").addEventListener("keydown", (e) => {
    if (e.key === "Enter") jumpTo();
  });
  $("reset-btn").onclick = resetTally;
  $("restart-btn").onclick = restartForm;
  $("shuffle-btn").onclick = shuffleForm;
  $("flag-btn").onclick = toggleFlag;
  $("home-btn").onclick = () => {
    state.running = false;
    saveState();
    renderHome();
  };
  $("export-btn").onclick = exportProgress;
  $("import-file").onchange = (e) => e.target.files[0] && importProgress(e.target.files[0]);
  $("print-btn").onclick = printStudy;
  $("mode-live").onchange = () => {
    state.timed = $("mode-live").value === "timed";
    if (state.timed && state.remainingSec <= 0) state.remainingSec = 3 * 60 * 60;
    $("mode").value = state.timed ? "timed" : "untimed";
    saveState();
    paintTimer();
  };
  $("mode").onchange = () => {
    state.timed = $("mode").value === "timed";
    if (state.timed && state.remainingSec <= 0) state.remainingSec = 3 * 60 * 60;
    const live = $("mode-live");
    if (live) live.value = state.timed ? "timed" : "untimed";
    saveState();
    paintTimer();
  };
}

function boot() {
  if (window.CAPX_BANK && window.CAPX_BANK.questions) {
    BANK = window.CAPX_BANK;
    wire();
    renderHome();
    return;
  }
  fetch("data/questions.json")
    .then((r) => r.json())
    .then((data) => {
      BANK = data;
      wire();
      renderHome();
    })
    .catch((err) => {
      document.body.innerHTML =
        "<p style='padding:24px'>Could not load the question bank. Keep index.html, app.js, styles.css, and the data folder together, then double-click index.html again.</p>";
      console.error(err);
    });
}
boot();
