import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",

  future: {
    compatibilityVersion: 4,
  },

  devtools: { enabled: true },

  modules: [
    "@pinia/nuxt",
    "@vueuse/nuxt",
    "@nuxt/icon",
    "@nuxt/image",
    "@nuxt/test-utils/module",
  ],

  css: ["~/assets/css/main.css"],

  vite: {
    plugins: [tailwindcss()],
  },

  typescript: {
    strict: true,
    typeCheck: false,
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000",
    },
  },

  icon: {
    serverBundle: "remote",
    clientBundle: {
      scan: true,
    },
  },
});
