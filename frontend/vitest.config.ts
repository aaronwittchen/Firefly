import { defineVitestConfig } from "@nuxt/test-utils/config";

export default defineVitestConfig({
  test: {
    environment: "happy-dom",
    include: ["**/*.{test,spec}.{js,ts,vue}"],
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      exclude: ["node_modules", ".nuxt", ".output"],
    },
  },
});
