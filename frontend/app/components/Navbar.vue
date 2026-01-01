<script setup lang="ts">
import { DropdownMenuContent, DropdownMenuItem, DropdownMenuPortal, DropdownMenuRoot, DropdownMenuTrigger } from "reka-ui";

const route = useRoute();
const authStore = useAuthStore();
const { user, isAuthenticated } = storeToRefs(authStore);
const { isDark, toggle } = useDarkMode();

const navLinks = [
  { name: "Handbook", path: "/handbook" },
  { name: "Logs", path: "/logs" },
];
</script>

<template>
  <nav class="border-b border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-800">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="flex h-16 items-center justify-between">
        <div class="flex items-center gap-8">
          <NuxtLink to="/" class="text-xl font-bold text-gray-900 dark:text-white">
            Firefly
          </NuxtLink>
          <div class="flex items-center gap-1">
            <NuxtLink
              v-for="link in navLinks"
              :key="link.path"
              :to="link.path"
              :class="[
                'rounded-md px-3 py-2 text-sm font-medium transition-colors',
                route.path === link.path
                  ? 'bg-gray-100 text-gray-900 dark:bg-gray-700 dark:text-white'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900 dark:text-gray-300 dark:hover:bg-gray-700 dark:hover:text-white',
              ]"
            >
              {{ link.name }}
            </NuxtLink>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <button
            class="rounded-md p-2 text-gray-500 hover:bg-gray-100 hover:text-gray-900 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white"
            @click="toggle"
          >
            <Icon v-if="isDark" name="lucide:sun" class="h-5 w-5" />
            <Icon v-else name="lucide:moon" class="h-5 w-5" />
          </button>
          <button
            v-if="!isAuthenticated"
            class="inline-flex items-center gap-2 rounded-md bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800 dark:bg-white dark:text-gray-900 dark:hover:bg-gray-100"
            @click="authStore.login"
          >
            <Icon name="lucide:github" class="h-4 w-4" />
            Login
          </button>
          <DropdownMenuRoot v-else>
            <DropdownMenuTrigger class="cursor-pointer outline-none">
              <img
                v-if="user?.avatar_url"
                :src="user.avatar_url"
                :alt="user.name || user.github_username"
                class="h-8 w-8 rounded-full ring-2 ring-gray-200 transition-all hover:ring-primary-500 dark:ring-gray-700"
              />
            </DropdownMenuTrigger>
            <DropdownMenuPortal>
              <DropdownMenuContent
                align="end"
                :side-offset="8"
                class="z-50 min-w-48 rounded-lg border border-gray-200 bg-white p-1 shadow-lg dark:border-gray-700 dark:bg-gray-800"
              >
                <div class="border-b border-gray-200 px-3 py-2 dark:border-gray-700">
                  <p class="text-sm font-medium text-gray-900 dark:text-white">
                    {{ user?.name || user?.github_username }}
                  </p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">
                    @{{ user?.github_username }}
                  </p>
                </div>
                <DropdownMenuItem
                  class="mt-1 flex cursor-pointer items-center gap-2 rounded-md px-3 py-2 text-sm text-red-600 outline-none hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/20"
                  @click="authStore.logout"
                >
                  <Icon name="lucide:log-out" class="h-4 w-4" />
                  Logout
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenuPortal>
          </DropdownMenuRoot>
        </div>
      </div>
    </div>
  </nav>
</template>
