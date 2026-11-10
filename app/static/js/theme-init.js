// Runs before first paint: applies the saved theme, or the system preference, to <html>.
(function () {
  try {
    var stored = localStorage.getItem("theme");
    var dark = stored
      ? stored === "dark"
      : window.matchMedia("(prefers-color-scheme: dark)").matches;
    document.documentElement.classList.toggle("dark", dark);
  } catch (e) {
    /* storage unavailable: keep default (light) */
  }
})();
