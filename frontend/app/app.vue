<template>
  <ClientOnly>
    <v-app>
      <!-- Test de Hot Reload - Docker funciona! -->
      <Toaster position="top-right"  rich-colors/>
      <BaseDialog />
      <NuxtLayout>
        <NuxtPage />
      </NuxtLayout>
    </v-app>
  </ClientOnly>
</template>
<script lang="ts" setup>
import { Toaster } from "vue-sonner";
import "vue-sonner/style.css";

import { useTheme } from "vuetify";

const theme = useTheme();

if (process.client) {
  const savedTheme = localStorage.getItem("theme-preference");
  if (savedTheme) {
    theme.change(savedTheme);
  } else {
    const prefersDark =
      window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches;
    theme.change(prefersDark ? "dark" : "light");
  }
}
</script>
