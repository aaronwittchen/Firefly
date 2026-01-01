<script setup lang="ts">
import type { ErrorFilters, ErrorLog, ErrorLogCreate } from "~/types/error";

const errorsStore = useErrorsStore();
const authStore = useAuthStore();
const { errors, isLoading, error: storeError } = storeToRefs(errorsStore);
const { isAuthenticated } = storeToRefs(authStore);

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
  if (authStore.isAuthenticated) {
    loadErrors();
  }
});

watch(isAuthenticated, (authenticated) => {
  if (authenticated) {
    loadErrors();
  }
});
</script>

<template>
  <div class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
    <div class="mb-8 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">Logs</h1>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Track and manage your development logs</p>
      </div>
      <button
        v-if="isAuthenticated"
        class="inline-flex items-center rounded-md bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700"
        @click="handleCreate"
      >
        <Icon name="lucide:plus" class="mr-2 h-4 w-4" />
        New Log
      </button>
    </div>

    <div v-if="!isAuthenticated" class="flex flex-col items-center justify-center py-16">
      <Icon name="lucide:lock" class="h-16 w-16 text-gray-300 dark:text-gray-600" />
      <h2 class="mt-4 text-xl font-semibold text-gray-900 dark:text-gray-100">Login to continue</h2>
      <p class="mt-2 text-gray-500 dark:text-gray-400">Sign in with GitHub to view your logs</p>
    </div>

    <template v-else>
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
    </template>

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
      title="Delete Log"
      description="Are you sure you want to delete this log? This action cannot be undone."
      confirm-text="Delete"
      :destructive="true"
      @confirm="handleDelete"
    />
  </div>
</template>
