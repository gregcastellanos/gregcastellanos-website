const themeToggle = document.querySelector(".theme-toggle");
const applyTheme = (theme) => {
  document.documentElement.dataset.theme = theme;
if (themeToggle) {
    const dark = theme === "dark";
    themeToggle.setAttribute("aria-pressed", String(dark));
    themeToggle.setAttribute("aria-label", dark ? "Switch to light theme" : "Switch to dark theme");
    const label = themeToggle.querySelector(".theme-label");
    if (label) label.textContent = dark ? "Light" : "Dark";
  }
};
try {
  const stored = localStorage.getItem("greg-theme");
  const systemDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  applyTheme(stored || (systemDark ? "dark" : "light"));
} catch {
  applyTheme(document.documentElement.dataset.theme || "light");
}
if (themeToggle) {
  themeToggle.addEventListener("click", () => {
    const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    applyTheme(next);
    try { localStorage.setItem("greg-theme", next); } catch {}
  });
}

const toggle = document.querySelector(".menu-toggle");
const nav = document.querySelector(".site-nav");
if (toggle && nav) {
  const closeNav = () => {
    nav.classList.remove("is-open");
    document.body.classList.remove("nav-open");
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "Open navigation");
  };
  toggle.addEventListener("click", () => {
    const open = nav.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
    document.body.classList.toggle("nav-open", open);
  });
  nav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", closeNav);
  });
  window.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeNav();
  });
}

window.gregAnalytics = {
  track(name, detail = {}) {
    window.dispatchEvent(new CustomEvent("greg:analytics", { detail: { name, ...detail } }));
  }
};

document.querySelectorAll(".filter").forEach((button) => {
  button.addEventListener("click", () => {
    const filter = button.dataset.filter;
    document.querySelectorAll(".filter").forEach((item) => item.classList.toggle("is-active", item === button));
    document.querySelectorAll(".work-item, .directory-row").forEach((item) => {
      const visible = filter === "all" || item.dataset.areas?.split(" ").includes(filter);
      item.hidden = !visible;
    });
    window.gregAnalytics.track("work_filter", { filter });
  });
});

const startedAt = document.querySelector("#startedAt");
if (startedAt) startedAt.value = String(Date.now());

const form = document.querySelector("#contact-form");
if (form) {
  const params = new URLSearchParams(window.location.search);
  const area = params.get("area");
  if (area) {
    const select = form.querySelector('select[name="area"]');
    if (select && [...select.options].some((option) => option.value === area || option.textContent === area)) select.value = area;
  }
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const note = document.querySelector("#form-note");
    const submit = form.querySelector('button[type="submit"]');
    const elapsed = Date.now() - Number(data.get("startedAt") || 0);
    if (data.get("website") || elapsed < 2500) {
      note.textContent = "Thanks. Please try again in a moment.";
      return;
    }
    const required = ["name", "email", "area", "message"];
    const missing = required.filter((key) => !String(data.get(key) || "").trim());
    if (missing.length) {
      note.textContent = "Please complete the required fields before sending the inquiry.";
      return;
    }
    // Keep the delivered email clean; spam checks above already used these.
    data.delete("website");
    data.delete("startedAt");
    const endpoint = form.dataset.endpoint || form.getAttribute("action") || "";
    if (endpoint) {
      try {
        if (submit) {
          submit.disabled = true;
          submit.setAttribute("aria-busy", "true");
          submit.textContent = "Sending";
        }
        note.textContent = "Sending your inquiry...";
        const payload = Object.fromEntries(data.entries());
        const response = await fetch(endpoint, {
          method: "POST",
          body: JSON.stringify(payload),
          headers: { "Content-Type": "application/json", Accept: "application/json" },
        });
        let result = {};
        try {
          result = await response.json();
        } catch {}
        if (!response.ok || result.success === false) throw new Error(result.message || "Form submission failed");
        form.reset();
        if (startedAt) startedAt.value = String(Date.now());
        note.textContent = "Thanks. Your inquiry has been sent.";
        window.gregAnalytics.track("contact_submit", { area: data.get("area") });
        return;
      } catch {
        note.textContent = "The form could not send. Please email Greg directly at gregcastellanoswork@gmail.com.";
      } finally {
        if (submit) {
          submit.disabled = false;
          submit.removeAttribute("aria-busy");
          submit.textContent = "Send inquiry";
        }
      }
      return;
    }
    const subject = encodeURIComponent("Gregory Castellanos inquiry: " + data.get("area"));
    const body = encodeURIComponent([
      "Name: " + data.get("name"),
      "Email: " + data.get("email"),
      "Organization: " + (data.get("organization") || ""),
      "Area: " + data.get("area"),
      "Timing: " + (data.get("timing") || ""),
      "",
      String(data.get("message") || "")
    ].join("\n"));
    note.innerHTML = 'Email draft ready: <a href="mailto:gregcastellanoswork@gmail.com?subject=' + subject + '&body=' + body + '">open email draft</a>.';
    window.gregAnalytics.track("contact_prepare", { area: data.get("area") });
  });
}
// Background video: never animate for reduced-motion visitors (poster remains via CSS).
const bgVideo = document.querySelector(".site-backdrop video");
if (bgVideo && window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  bgVideo.pause();
  bgVideo.removeAttribute("autoplay");
}
