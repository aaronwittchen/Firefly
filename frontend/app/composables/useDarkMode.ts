export function useDarkMode() {
  const colorMode = useState<"light" | "dark">("colorMode", () => "light");

  const isDark = computed(() => colorMode.value === "dark");

  function toggle() {
    colorMode.value = colorMode.value === "light" ? "dark" : "light";
    updateClass();
    localStorage.setItem("colorMode", colorMode.value);
  }

  function updateClass() {
    if (import.meta.client) {
      if (colorMode.value === "dark") {
        document.documentElement.classList.add("dark");
      } else {
        document.documentElement.classList.remove("dark");
      }
    }
  }

  function init() {
    if (import.meta.client) {
      const stored = localStorage.getItem("colorMode") as "light" | "dark" | null;
      const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

      colorMode.value = stored ?? (prefersDark ? "dark" : "light");
      updateClass();
    }
  }

  return {
    colorMode,
    isDark,
    toggle,
    init,
  };
}
