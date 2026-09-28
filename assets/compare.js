/* Before/after video comparison (StudioLab).
   Two muted clips of the same moment, frame-aligned offline: the processed one underneath, the raw scan on
   top, clipped at the divider. A transparent range input covers the stage, so mouse, touch and keyboard all
   move the divider. Clips load only when the player scrolls into view and pause when it leaves; the raw clip
   is re-synced to the processed one whenever they drift. prefers-reduced-motion: no autoplay, tap to play. */
(function () {
  "use strict";
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  function setup(fig) {
    var stage = fig.querySelector(".cmp-stage"), after = fig.querySelector(".cmp-after"),
        before = fig.querySelector(".cmp-before"), range = fig.querySelector(".cmp-range"), loaded = false;
    function pos(v) { stage.style.setProperty("--pos", v + "%"); }
    range.addEventListener("input", function () { pos(range.value); });
    pos(range.value);

    function load() {
      if (loaded) return; loaded = true;
      [after, before].forEach(function (v) { v.src = v.getAttribute("data-src"); v.load(); });
    }
    function play() {
      load();
      var p = after.play(); if (p && p.catch) p.catch(function () {});
      var q = before.play(); if (q && q.catch) q.catch(function () {});
    }
    function pause() { after.pause(); before.pause(); }
    function sync() {
      if (Math.abs(before.currentTime - after.currentTime) > 0.08) before.currentTime = after.currentTime;
      if (after.paused !== before.paused) { if (after.paused) before.pause(); else before.play().catch(function () {}); }
    }
    after.addEventListener("timeupdate", sync);
    after.addEventListener("seeked", sync);
    after.addEventListener("playing", sync);

    // Tap/click on the stage (not a drag) toggles play — needed for reduced-motion users and handy for all.
    var downX = null;
    range.addEventListener("pointerdown", function (e) { downX = e.clientX; });
    range.addEventListener("pointerup", function (e) {
      if (downX !== null && Math.abs(e.clientX - downX) < 4 && reduce) { if (after.paused) play(); else pause(); }
      downX = null;
    });

    // One gentle sweep the first time the player is seen, so visitors understand the bar can move.
    var hinted = false;
    function hint() {
      if (hinted || reduce) return; hinted = true;
      var t0 = null;
      function step(ts) {
        if (t0 === null) t0 = ts;
        var t = (ts - t0) / 1800; if (t > 1) { pos(50); range.value = 50; return; }
        var v = 50 + 22 * Math.sin(t * Math.PI * 2); pos(v); range.value = v;
        requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }

    var inView = false;
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          inView = e.isIntersecting;
          if (inView) { load(); if (!reduce) { play(); hint(); } }
          else pause();
        });
      }, { rootMargin: "120px 0px", threshold: 0.25 }).observe(fig);
    } else { load(); }
    // A page opened in a background tab can't start video; start it when the tab comes to the front.
    document.addEventListener("visibilitychange", function () {
      if (document.visibilityState === "visible" && inView && !reduce && after.paused) play();
    });
  }

  function init() { [].forEach.call(document.querySelectorAll(".cmp"), setup); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
