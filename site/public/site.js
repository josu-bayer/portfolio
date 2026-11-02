(function () {
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* entrance for the parts of every section, staggered */
  var rv = $$(".rv");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
    rv.forEach(function (el, i) {
      var sib = $$(".rv", el.parentNode);
      el.style.setProperty("--d", (sib.indexOf(el) % 4) * 80 + "ms");
      io.observe(el);
    });
  } else {
    rv.forEach(function (el) { el.classList.add("in"); });
  }

  /* slow drift on the picture bands: the picture slides inside its frame */
  var bands = $$("[data-drift] img");
  if (bands.length && !reduce) {
    var tick = false;
    var drift = function () {
      tick = false;
      var vh = window.innerHeight;
      bands.forEach(function (img) {
        var r = img.parentNode.getBoundingClientRect();
        if (r.bottom < 0 || r.top > vh) return;
        var p = (r.top + r.height / 2 - vh / 2) / vh;
        var base = parseFloat(img.getAttribute("data-oy") || "50");
        img.style.setProperty("--oy", Math.max(0, Math.min(100, base - p * 36)).toFixed(1) + "%");
      });
    };
    window.addEventListener("scroll", function () { if (!tick) { tick = true; requestAnimationFrame(drift); } }, { passive: true });
    window.addEventListener("resize", drift);
    drift();
  }

  /* work ledger: filter by track, preview the row in focus */
  var rows = $$(".row");
  var peek = $(".peek-in");
  var pf = $(".pf"), pc = $(".pc"), pn = $(".pn");
  var cur = rows[0];
  function show(row) {
    if (!row || !peek) return;
    cur = row;
    rows.forEach(function (r) { r.classList.toggle("on", r === row); });
    peek.classList.add("sw");
    setTimeout(function () {
      pf.textContent = row.getAttribute("data-fig");
      pc.textContent = row.getAttribute("data-cap");
      pn.textContent = row.getAttribute("data-name");
      peek.classList.remove("sw");
    }, reduce ? 0 : 130);
  }
  rows.forEach(function (r) {
    var t = r.firstElementChild;
    r.addEventListener("mouseenter", function () { show(r); });
    t.addEventListener("focus", function () { show(r); });
  });
  if (rows[0]) rows[0].classList.add("on");

  $$(".chip").forEach(function (c) {
    c.addEventListener("click", function () {
      var f = c.getAttribute("data-f");
      $$(".chip").forEach(function (x) { x.setAttribute("aria-pressed", x === c ? "true" : "false"); });
      var first = null;
      rows.forEach(function (r) {
        var ok = f === "all" || r.getAttribute("data-t") === f;
        r.hidden = !ok;
        if (ok && !first) first = r;
      });
      if (first) show(first);
    });
  });

  /* footer wordmark: fit the word to the full width */
  function fit() {
    var t = $(".word text"), s = $(".word");
    if (!t || !t.getBBox) return;
    try {
      var b = t.getBBox();
      if (b.width > 0) {
        var pad = b.width * 0.012;
        s.setAttribute("viewBox", [b.x - pad, b.y, b.width + pad * 2, b.height].join(" "));
      }
    } catch (e) {}
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit); else window.addEventListener("load", fit);
})();
