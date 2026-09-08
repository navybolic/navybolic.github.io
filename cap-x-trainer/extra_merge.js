(function () {
  var B = window.CAPX_BANK;
  if (!B) return;
  var PDF = {
    CH1: ["CH1 Introduction PDF", "https://drive.google.com/file/d/1xpZ78WiaYsZ4F6J44ahMoqrmN2RYGV3x/view"],
    CH2: ["CH2 Getting Started PDF", "https://drive.google.com/file/d/1W1eIPDgroLTY9bZJ3N0O3_3V5LHkhxT2/view"],
    CH3: ["CH3 Data PDF", "https://drive.google.com/file/d/1AAad156Wsd8KdrscDpzxkyJSZ4zDvhC9/view"],
    CH4: ["CH4 Getting to Know Your Data PDF", "https://drive.google.com/file/d/1EJ0ItOQSJ821dy9bZl8ERiAb-X9M6-Sq/view"],
    CH5: ["CH5 Solution methodologies PDF", "https://drive.google.com/file/d/1yyHXRUacIUJdwY3fbykUB-e_DtAAlezt/view"],
    CH6: ["CH6 Modeling PDF", "https://drive.google.com/file/d/1YLpRg9RUE-tha3Jkxu8U2qFRXCD07Gew/view"],
    CH7: ["CH7 Visualization PDF", "https://drive.google.com/file/d/1y67xnqWTD_-xHW1t_AneCyFB8mzDkWDG/view"],
    CH8: ["CH8 Deployment and life cycle PDF", "https://drive.google.com/file/d/13v4WCaewlo67GWw0uyajVfCm7Nk2BmhG/view"],
    CH9: ["CH9 Analytics Leadership PDF", "https://drive.google.com/file/d/1_BPls98zR2U5Zqn29N_ehiIq4ZPH_u3M/view"],
    APP: ["CH Appendix PDF", "https://drive.google.com/file/d/1FrFXNTJZ66-yQeXY3bpGIhz5Tm9zPo2l/view"]
  };
  var STUDY = ["CAP Study Guide PDF (your Drive books folder)", "https://drive.google.com/file/d/1Njz-m1ADgmxm-UZila2kLxYxbMSQwZrj/view"];
  var have = {};
  B.questions.forEach(function (q) { have[q.question_id] = true; });
  function cite(ch, loc, correct) {
    var p = PDF[ch] || PDF.CH8;
    var list = [{ source: p[0], url: p[1], locator: loc || "" }];
    if (correct) list.push({ source: STUDY[0], url: STUDY[1], locator: "CAP-X domain tasks matching this item" });
    return list;
  }
  function addRow(row) {
    var id = row[0];
    if (have[id]) return;
    var opts = row[5].map(function (o) {
      return { key: o[0], text: o[1], is_correct: o[0] === row[4], rationale: o[2], citations: cite(o[3], o[4], o[0] === row[4]) };
    });
    B.questions.push({ question_id: id, revision: 1, status: "eligible", domain: row[1], objectives: ["CAP-X"], topic: row[2], section: "", difficulty: "moderate", stem: row[3], correct_key: row[4], options: opts });
    have[id] = true;
  }
  [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19].forEach(function (i) {
    var pack = window["CAPX_COMPACT_" + i];
    if (!pack) return;
    (pack.rows || []).forEach(addRow);
    if (pack.forms) B.bank_forms = pack.forms;
  });
  B.question_count = B.questions.length;
})();
