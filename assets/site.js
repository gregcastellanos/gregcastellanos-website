/* Gregory Castellanos — site behavior. Progressive enhancement, no dependencies. */
(function () {
  "use strict";

  /* ---- Theme toggle (light / dark) ------------------------------------- */
  var root = document.documentElement;
  var STORE = "gc-theme";
  function systemDark() {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  }
  function currentTheme() {
    return root.getAttribute("data-theme") || (systemDark() ? "dark" : "light");
  }
  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    document.querySelectorAll(".theme-toggle").forEach(function (btn) {
      btn.setAttribute("aria-label", theme === "dark" ? "Switch to light theme" : "Switch to dark theme");
      btn.setAttribute("aria-pressed", String(theme === "dark"));
    });
  }
  document.querySelectorAll(".theme-toggle").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      try { localStorage.setItem(STORE, next); } catch (e) {}
      applyTheme(next);
    });
  });
  // Sync label on load (theme itself is set by the inline no-flash script)
  applyTheme(currentTheme());

  /* ---- Mobile navigation ------------------------------------------------ */
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.querySelector(".site-nav");
  if (toggle && nav) {
    var closeNav = function () {
      nav.classList.remove("is-open");
      document.body.classList.remove("nav-open");
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Open navigation");
    };
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
      document.body.classList.toggle("nav-open", open);
    });
    nav.querySelectorAll("a").forEach(function (link) { link.addEventListener("click", closeNav); });
    window.addEventListener("keydown", function (e) { if (e.key === "Escape") closeNav(); });
  }

  /* ---- Reveal on scroll ------------------------------------------------- */
  var reveals = document.querySelectorAll(".reveal");
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reveals.length && "IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add("is-in"); io.unobserve(entry.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ---- Work filter ------------------------------------------------------ */
  var filters = document.querySelectorAll(".filter");
  if (filters.length) {
    filters.forEach(function (button) {
      button.addEventListener("click", function () {
        var filter = button.dataset.filter;
        filters.forEach(function (b) { b.classList.toggle("is-active", b === button); });
        document.querySelectorAll(".case-card").forEach(function (item) {
          var areas = (item.dataset.areas || "").split(" ");
          item.hidden = !(filter === "all" || areas.indexOf(filter) !== -1);
        });
      });
    });
  }

  /* ---- Contact form (builds a mailto draft) ----------------------------- */
  var startedAt = document.querySelector("#startedAt");
  if (startedAt) startedAt.value = String(Date.now());
  var form = document.querySelector("#contact-form");
  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var data = new FormData(form);
      var note = document.querySelector("#form-note");
      var elapsed = Date.now() - Number(data.get("startedAt") || 0);
      if (data.get("website") || elapsed < 2000) {
        note.textContent = "Thanks. Please try again in a moment.";
        return;
      }
      var required = ["name", "email", "area", "message"];
      var missing = required.filter(function (k) { return !String(data.get(k) || "").trim(); });
      if (missing.length) {
        note.textContent = "Please complete the required fields before preparing the inquiry.";
        return;
      }
      var subject = encodeURIComponent("Inquiry (" + data.get("area") + ") — " + data.get("name"));
      var body = encodeURIComponent([
        "Name: " + data.get("name"),
        "Email: " + data.get("email"),
        "Organization: " + (data.get("organization") || ""),
        "Area: " + data.get("area"),
        "Timing: " + (data.get("timing") || ""),
        "How they heard: " + (data.get("referral") || ""),
        "", String(data.get("message") || "")
      ].join("\n"));
      note.innerHTML = 'Your inquiry is ready. <a href="mailto:gregcastellanoswork@gmail.com?subject=' +
        subject + '&body=' + body + '">Open your email draft</a> to send it.';
    });
  }

  /* ---- Footer year ------------------------------------------------------ */
  var yr = document.querySelector("#year");
  if (yr) yr.textContent = String(new Date().getFullYear());
})();
