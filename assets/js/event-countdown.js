(function () {
  var el = document.getElementById("petsEventCountdown");
  if (!el) return;

  var durationMs = 2 * 24 * 60 * 60 * 1000 + 5 * 60 * 60 * 1000;
  var end = Date.now() + durationMs;

  function pad(n) {
    return n < 10 ? "0" + n : String(n);
  }

  function tick() {
    var left = end - Date.now();
    if (left <= 0) {
      el.textContent = "0д 00ч 00м 00с";
      return;
    }
    var totalSec = Math.floor(left / 1000);
    var s = totalSec % 60;
    var m = Math.floor(totalSec / 60) % 60;
    var h = Math.floor(totalSec / 3600) % 24;
    var d = Math.floor(totalSec / (24 * 3600));
    el.textContent = d + "д " + pad(h) + "ч " + pad(m) + "м " + pad(s) + "с";
  }

  tick();
  setInterval(tick, 1000);
})();
