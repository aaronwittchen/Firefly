<script setup lang="ts">
definePageMeta({
  layout: "blank",
});

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

onMounted(async () => {
  console.log("Callback - query params:", route.query);
  const tokenParam = route.query.token as string | undefined;
  const error = route.query.error as string | undefined;
  const returnTo = localStorage.getItem("auth_return_to") || "/";
  localStorage.removeItem("auth_return_to");

  console.log("Callback - tokenParam:", tokenParam ? "exists" : "none");
  console.log("Callback - returnTo:", returnTo);

  if (error) {
    console.error("Auth error:", error);
    router.push(returnTo);
    return;
  }

  if (tokenParam) {
    const token = decodeURIComponent(tokenParam);
    console.log("Callback - saving token:", token.substring(0, 20) + "...");
    localStorage.setItem("auth_token", token);
    await authStore.init();
    console.log("Callback - auth init complete, isAuthenticated:", authStore.isAuthenticated);
  }

  router.push(returnTo);
});
</script>

<template>
  <div class="flex min-h-screen items-center justify-center bg-gray-50 dark:bg-gray-900">
    <div class="text-center">
      <Icon name="lucide:loader-2" class="mx-auto h-8 w-8 animate-spin text-primary-500" />
      <p class="mt-4 text-gray-600 dark:text-gray-400">Completing login...</p>
    </div>
  </div>
</template>
