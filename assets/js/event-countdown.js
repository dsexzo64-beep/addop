(function () {
  var STORAGE_KEY = "petsEventCountdownEnd";
  var DURATION_MS = 2 * 24 * 60 * 60 * 1000 + 5 * 60 * 60 * 1000;
  var intervalId = null;

  function pad(n) {
    return n < 10 ? "0" + n : String(n);
  }

  function getEndTime() {
    try {
      var stored = sessionStorage.getItem(STORAGE_KEY);
      var end = stored ? parseInt(stored, 10) : NaN;
      if (!Number.isFinite(end) || end <= Date.now()) {
        end = Date.now() + DURATION_MS;
        sessionStorage.setItem(STORAGE_KEY, String(end));
      }
      return end;
    } catch (e) {
      return Date.now() + DURATION_MS;
    }
  }

  function formatCountdown(el, end) {
    var left = end - Date.now();
    if (left <= 0) {
      el.textContent = "0d 00h 00m 00s";
      return false;
    }
    var totalSec = Math.floor(left / 1000);
    var s = totalSec % 60;
    var m = Math.floor(totalSec / 60) % 60;
    var h = Math.floor(totalSec / 3600) % 24;
    var d = Math.floor(totalSec / (24 * 3600));
    el.textContent = d + "d " + pad(h) + "h " + pad(m) + "m " + pad(s) + "s";
    return true;
  }

  function start() {
    var el = document.getElementById("petsEventCountdown");
    if (!el) return;

    if (intervalId) {
      clearInterval(intervalId);
      intervalId = null;
    }

    var end = getEndTime();

    function tick() {
      if (!formatCountdown(el, end)) {
        clearInterval(intervalId);
        intervalId = null;
      }
    }

    tick();
    intervalId = setInterval(tick, 1000);
  }

  start();

  window.addEventListener("pageshow", function (ev) {
    var el = document.getElementById("petsEventCountdown");
    if (!el) return;
    var empty = !el.textContent || !String(el.textContent).trim();
    if (ev.persisted || empty) {
      start();
    }
  });
})();
