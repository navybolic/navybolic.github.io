const SHEET_ID = "1iWXpz34IqMSibMMneyII-19VNx2Bq7g4wZZsjpMvJkg";
const TOKEN = "navybolic-capx";

function jsonOut_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
function book_() { return SpreadsheetApp.openById(SHEET_ID); }
function ensureTabs_() {
  const ss = book_();
  if (!ss.getSheetByName("Sessions")) {
    const sh = ss.insertSheet("Sessions");
    sh.appendRow(["session_id", "updated_at", "token_ok", "state_json"]);
  }
  if (!ss.getSheetByName("Progress")) {
    const sh = ss.insertSheet("Progress");
    sh.appendRow(["answered_at", "session_id", "bank_slot", "question_id", "chosen", "correct_key", "is_correct", "timed", "notes"]);
  }
  return ss;
}
function doGet(e) {
  e = e || { parameter: {} };
  if ((e.parameter.token || "") !== TOKEN) return jsonOut_({ ok: false, error: "bad token" });
  const ss = ensureTabs_();
  const sh = ss.getSheetByName("Sessions");
  const last = sh.getLastRow();
  if (last < 2) return jsonOut_({ ok: true, state: null });
  const row = sh.getRange(last, 1, 1, 4).getValues()[0];
  let parsed = null;
  try { parsed = JSON.parse(row[3] || "null"); } catch (err) { parsed = null; }
  return jsonOut_({ ok: true, updated_at: row[1], state: parsed });
}
function doPost(e) {
  let body = {};
  try { body = JSON.parse((e && e.postData && e.postData.contents) || "{}"); } catch (err) { return jsonOut_({ ok: false, error: "bad json" }); }
  if ((body.token || "") !== TOKEN) return jsonOut_({ ok: false, error: "bad token" });
  const st = body.state || {};
  const ss = ensureTabs_();
  ss.getSheetByName("Sessions").appendRow([st.sessionId || "", st.updatedAt || Date.now(), true, JSON.stringify(st)]);
  return jsonOut_({ ok: true });
}
