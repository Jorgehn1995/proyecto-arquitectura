<script lang="ts" setup>
import { useTheme } from "vuetify";
const theme = useTheme();
</script>
<template>
  <div>
    <nuxt-link :to="{ name: 'home' }">
      <v-sheet width="100" class="rounded-md px-4 py-2"  color="transparent">
        <v-img src="/umg.png" />
      </v-sheet>
    </nuxt-link>
  </div>
</template>
