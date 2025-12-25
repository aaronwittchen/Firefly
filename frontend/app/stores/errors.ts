import type { ErrorFilters, ErrorLog, ErrorLogCreate, ErrorLogUpdate } from "~/types/error";

export const useErrorsStore = defineStore("errors", () => {
  const config = useRuntimeConfig();
  const apiBase = config.public.apiBase;

  const errors = ref<ErrorLog[]>([]);
  const currentError = ref<ErrorLog | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  async function fetchErrors(filters: ErrorFilters = {}) {
    isLoading.value = true;
    error.value = null;

    try {
      const params = new URLSearchParams();
      if (filters.project) params.append("project", filters.project);
      if (filters.tag) params.append("tag", filters.tag);
      if (filters.resolved !== undefined) params.append("resolved", String(filters.resolved));
      if (filters.language) params.append("language", filters.language);
      if (filters.error_type) params.append("error_type", filters.error_type);

      const queryString = params.toString();
      const url = `${apiBase}/errors/${queryString ? `?${queryString}` : ""}`;

      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Failed to fetch errors: ${response.statusText}`);
      }

      errors.value = await response.json();
    } catch (e) {
      error.value = e instanceof Error ? e.message : "An error occurred";
      throw e;
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchError(id: number) {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch(`${apiBase}/errors/${id}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch error: ${response.statusText}`);
      }

      currentError.value = await response.json();
      return currentError.value;
    } catch (e) {
      error.value = e instanceof Error ? e.message : "An error occurred";
      throw e;
    } finally {
      isLoading.value = false;
    }
  }

  async function createError(data: ErrorLogCreate) {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch(`${apiBase}/errors/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`Failed to create error: ${response.statusText}`);
      }

      const newError: ErrorLog = await response.json();
      errors.value.unshift(newError);
      return newError;
    } catch (e) {
      error.value = e instanceof Error ? e.message : "An error occurred";
      throw e;
    } finally {
      isLoading.value = false;
    }
  }

  async function updateError(id: number, data: ErrorLogUpdate) {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch(`${apiBase}/errors/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`Failed to update error: ${response.statusText}`);
      }

      const updatedError: ErrorLog = await response.json();
      const index = errors.value.findIndex((e) => e.id === id);
      if (index !== -1) {
        errors.value[index] = updatedError;
      }
      if (currentError.value?.id === id) {
        currentError.value = updatedError;
      }
      return updatedError;
    } catch (e) {
      error.value = e instanceof Error ? e.message : "An error occurred";
      throw e;
    } finally {
      isLoading.value = false;
    }
  }

  async function deleteError(id: number) {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch(`${apiBase}/errors/${id}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error(`Failed to delete error: ${response.statusText}`);
      }

      errors.value = errors.value.filter((e) => e.id !== id);
      if (currentError.value?.id === id) {
        currentError.value = null;
      }
    } catch (e) {
      error.value = e instanceof Error ? e.message : "An error occurred";
      throw e;
    } finally {
      isLoading.value = false;
    }
  }

  return {
    errors,
    currentError,
    isLoading,
    error,
    fetchErrors,
    fetchError,
    createError,
    updateError,
    deleteError,
  };
});
