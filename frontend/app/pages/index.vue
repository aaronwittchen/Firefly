<script setup lang="ts">
import type { ErrorFilters, ErrorLog, ErrorLogCreate } from "~/types/error";

const errorsStore = useErrorsStore();
const { errors, isLoading, error: storeError } = storeToRefs(errorsStore);
const { isDark, toggle, init } = useDarkMode();

const filters = ref<ErrorFilters>({});
const isFormOpen = ref(false);
const isDetailOpen = ref(false);
const isDeleteDialogOpen = ref(false);
const selectedError = ref<ErrorLog | null>(null);
const errorToDelete = ref<number | null>(null);

async function loadErrors() {
  try {
    await errorsStore.fetchErrors(filters.value);
  } catch {
    // Error is handled in store
  }
}

function handleCreate() {
  selectedError.value = null;
  isFormOpen.value = true;
}

function handleEdit(error: ErrorLog) {
  selectedError.value = error;
  isDetailOpen.value = false;
  isFormOpen.value = true;
}

function handleView(error: ErrorLog) {
  selectedError.value = error;
  isDetailOpen.value = true;
}

function handleDeleteClick(id: number) {
  errorToDelete.value = id;
  isDeleteDialogOpen.value = true;
}

async function handleDelete() {
  if (errorToDelete.value === null) return;

  try {
    await errorsStore.deleteError(errorToDelete.value);
    isDeleteDialogOpen.value = false;
    errorToDelete.value = null;
  } catch {
    // Error is handled in store
  }
}

async function handleSave(data: ErrorLogCreate) {
  try {
    if (selectedError.value) {
      await errorsStore.updateError(selectedError.value.id, data);
    } else {
      await errorsStore.createError(data);
    }
    isFormOpen.value = false;
    selectedError.value = null;
  } catch {
    // Error is handled in store
  }
}

onMounted(() => {
  init();
  loadErrors();
});
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <div class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <div class="mb-8 flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">Error Tracker</h1>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Track and manage your development errors</p>
        </div>
        <div class="flex items-center gap-3">
          <button
            class="rounded-md border border-gray-300 bg-white p-2 text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
            @click="toggle"
          >
            <Icon v-if="isDark" name="lucide:sun" class="h-5 w-5" />
            <Icon v-else name="lucide:moon" class="h-5 w-5" />
          </button>
          <button
            class="inline-flex items-center rounded-md bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700"
            @click="handleCreate"
          >
            <Icon name="lucide:plus" class="mr-2 h-4 w-4" />
            New Error
          </button>
        </div>
      </div>

      <div v-if="storeError" class="mb-4 rounded-md bg-red-50 p-4 dark:bg-red-900/20">
        <div class="flex">
          <Icon name="lucide:alert-circle" class="h-5 w-5 text-red-400" />
          <div class="ml-3">
            <p class="text-sm text-red-700 dark:text-red-400">{{ storeError }}</p>
          </div>
        </div>
      </div>

      <div class="mb-6">
        <ErrorFilters v-model="filters" @search="loadErrors" />
      </div>

      <ErrorList
        :errors="errors"
        :is-loading="isLoading"
        @edit="handleEdit"
        @delete="handleDeleteClick"
        @view="handleView"
      />

      <ErrorForm
        v-model:open="isFormOpen"
        :error="selectedError"
        @save="handleSave"
      />

      <ErrorDetail
        v-model:open="isDetailOpen"
        :error="selectedError"
        @edit="handleEdit"
      />

      <ConfirmDialog
        v-model:open="isDeleteDialogOpen"
        title="Delete Error"
        description="Are you sure you want to delete this error? This action cannot be undone."
        confirm-text="Delete"
        :destructive="true"
        @confirm="handleDelete"
      />
    </div>
  </div>
</template>
