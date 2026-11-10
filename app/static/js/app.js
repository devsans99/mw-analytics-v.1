// Alpine components shared by every page. Loaded (deferred) before Alpine itself.
document.addEventListener("alpine:init", () => {
  Alpine.data("themeToggle", () => ({
    dark: document.documentElement.classList.contains("dark"),
    toggle() {
      this.dark = !this.dark;
      document.documentElement.classList.toggle("dark", this.dark);
      try {
        localStorage.setItem("theme", this.dark ? "dark" : "light");
      } catch (e) {
        /* ignore */
      }
    },
  }));
});
