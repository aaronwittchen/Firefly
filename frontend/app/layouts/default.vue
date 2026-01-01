<script setup lang="ts">
const authStore = useAuthStore();
const { isLoading } = storeToRefs(authStore);
const { init: initDarkMode } = useDarkMode();

const isReady = ref(false);

onMounted(async () => {
  initDarkMode();
  await authStore.init();
  isReady.value = true;
});
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <Navbar />
    <main>
      <div v-if="!isReady" class="flex items-center justify-center py-16">
        <Icon name="lucide:loader-2" class="h-6 w-6 animate-spin text-primary-500" />
      </div>
      <slot v-else />
    </main>
  </div>
</template>
