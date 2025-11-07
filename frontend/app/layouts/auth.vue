<script lang="ts" setup>
import { useRouter } from "vue-router";
import { useDialog } from "~/composables/base/useDialog";

const isReady = ref(true);
const router = useRouter();
const dialog = useDialog();
const drawer = ref(true);

const menuItems = [
  { title: "Inicio", icon: "mdi-home", to: "/" },
  { title: "Access", icon: "mdi-lock", to: "/access" },
  { title: "Users", icon: "mdi-account", to: "/users" },
  { title: "Umbrales", icon: "mdi-tune", to: "/thresholds" },
];
</script>
<template>
  <div>
    <base-loading v-if="!isReady"></base-loading>
    <div v-else>
      <v-navigation-drawer v-model="drawer" class="position-fixed">
        <template #prepend>
          <v-sheet width="100%" color="transparent" class="d-flex justify-center">
            <base-logo class="pa-4" />
          </v-sheet>
        </template>
        <template #default>
          <v-list nav>
            <v-list-item
             class="rounded-sm px-6"
              v-for="item in menuItems"
              :key="item.to"
              :to="item.to"
              link
              
            >
              <template #prepend>
                <v-icon>{{ item.icon }}</v-icon>
              </template>
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </template>
      </v-navigation-drawer>
      <v-app-bar variant="flat" elevation="0" color="background">
        <template #prepend>
          <v-btn icon @click="drawer = !drawer" color="primary">
            <v-icon>mdi-menu</v-icon>
          </v-btn>
          
        </template>
      </v-app-bar>
      <v-main>
        <v-container>
          <NuxtPage />
        </v-container>
      </v-main>
    </div>
  </div>
</template>
