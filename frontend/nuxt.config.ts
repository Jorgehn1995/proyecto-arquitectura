// https://nuxt.com/docs/api/configuration/nuxt-config
import vuetify, { transformAssetUrls } from "vite-plugin-vuetify";
export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  
  // Runtime config for API URL
  runtimeConfig: {
    public: {
      apiUrl: 'http://localhost:8000',
      apiUrlClient: 'http://localhost:8000',
    },
  },
  app: {
    head: {
      title: "UMG - Arquitectura - Proyecto",
      link: [
        {
          rel: "stylesheet",
          href: "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@100..900&display=swap",
        },
        {
          rel: "stylesheet",
          href: "https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap",
        },
      ],
    },
  },
  build: {
    transpile: ["vuetify"],
  },
  css: ["@/assets/css/main.css"],
  modules: [
    "@pinia/nuxt",
    "vue-sonner/nuxt",
    
    (_options, nuxt) => {
      nuxt.hooks.hook("vite:extendConfig", (config) => {
        // @ts-expect-error
        config.plugins.push(vuetify({ autoImport: true }));
      });
    },
    //...
  ],
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          // Opciones de Sass
          quietDeps: true, // Silencia advertencias de dependencias
          silenceDeprecations: ["import"], // Silencia específicamente la deprecación de @import
        },
      },
    },
    vue: {
      template: {
        transformAssetUrls,
      },
    },
  },
});
