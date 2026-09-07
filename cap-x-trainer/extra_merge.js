(function () {
  var B = window.CAPX_BANK;
  if (!B) return;
  var have = {};
  B.questions.forEach(function (q) { have[q.question_id] = true; });
  [window.CAPX_EXTRA_1, window.CAPX_EXTRA_2, window.CAPX_EXTRA_3, window.CAPX_EXTRA_4, window.CAPX_EXTRA].forEach(function (E) {
    if (!E || !E.questions) return;
    E.questions.forEach(function (q) {
      if (!have[q.question_id]) { B.questions.push(q); have[q.question_id] = true; }
    });
    if (E.bank_forms) B.bank_forms = E.bank_forms;
  });
  B.question_count = B.questions.length;
})();
