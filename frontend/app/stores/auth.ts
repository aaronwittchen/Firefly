interface User {
  id: number;
  github_id: number;
  github_username: string;
  email: string | null;
  name: string | null;
  avatar_url: string | null;
}

export const useAuthStore = defineStore("auth", () => {
  const config = useRuntimeConfig();
  const apiBase = config.public.apiBase;

  const user = ref<User | null>(null);
  const token = ref<string | null>(null);
  const isLoading = ref(false);

  const isAuthenticated = computed(() => !!token.value && !!user.value);

  async function init() {
    const savedToken = localStorage.getItem("auth_token");
    console.log("Auth init - saved token:", savedToken ? "exists" : "none");
    if (savedToken) {
      token.value = savedToken;
      await fetchUser();
    }
  }

  async function fetchUser() {
    if (!token.value) {
      console.log("fetchUser - no token");
      return;
    }

    isLoading.value = true;
    try {
      console.log("fetchUser - making request with token:", token.value.substring(0, 20) + "...");
      const response = await fetch(`${apiBase}/auth/me`, {
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
      });

      console.log("fetchUser - response status:", response.status);
      if (!response.ok) {
        console.log("fetchUser - not ok, logging out");
        logout();
        return;
      }

      user.value = await response.json();
      console.log("fetchUser - user loaded:", user.value?.github_username);
    } catch (e) {
      console.error("fetchUser - error:", e);
      logout();
    } finally {
      isLoading.value = false;
    }
  }

  function login() {
    localStorage.setItem("auth_return_to", window.location.pathname);
    window.location.href = `${apiBase}/auth/login`;
  }

  function handleCallback(accessToken: string, userData: User) {
    token.value = accessToken;
    user.value = userData;
    localStorage.setItem("auth_token", accessToken);
  }

  function logout() {
    token.value = null;
    user.value = null;
    localStorage.removeItem("auth_token");
  }

  function getAuthHeaders(): Record<string, string> {
    if (!token.value) return {};
    return { Authorization: `Bearer ${token.value}` };
  }

  return {
    user,
    token,
    isLoading,
    isAuthenticated,
    init,
    login,
    logout,
    fetchUser,
    getAuthHeaders,
  };
});
