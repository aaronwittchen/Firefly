<script setup lang="ts">
import { useDebounceFn } from "@vueuse/core";
import type { ErrorFilters } from "~/types/error";

const props = defineProps<{
  modelValue: ErrorFilters;
}>();

const emit = defineEmits<{
  "update:modelValue": [value: ErrorFilters];
  search: [];
}>();

const filters = computed({
  get: () => props.modelValue,
  set: (value) => emit("update:modelValue", value),
});

const resolvedOptions = [
  { value: undefined, label: "All" },
  { value: false, label: "Open" },
  { value: true, label: "Resolved" },
] as const;

const debouncedSearch = useDebounceFn(() => {
  emit("search");
}, 300);

function handleInput() {
  debouncedSearch();
}

function handleStatusChange() {
  emit("search");
}

function clearFilters() {
  emit("update:modelValue", {});
  emit("search");
}
</script>

<template>
  <div
    class="rounded-lg border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-700 dark:bg-gray-800"
  >
    <div class="flex flex-wrap items-end gap-4">
      <div class="min-w-[150px] flex-1">
        <label
          for="filter-project"
          class="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Project</label
        >
        <input
          id="filter-project"
          v-model="filters.project"
          type="text"
          class="mt-1 block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100"
          placeholder="Filter by project"
          @input="handleInput"
        />
      </div>

      <div class="min-w-[150px] flex-1">
        <label
          for="filter-tag"
          class="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Tag</label
        >
        <input
          id="filter-tag"
          v-model="filters.tag"
          type="text"
          class="mt-1 block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100"
          placeholder="Filter by tag"
          @input="handleInput"
        />
      </div>

      <div class="min-w-[150px] flex-1">
        <label
          for="filter-language"
          class="block text-sm font-medium text-gray-700 dark:text-gray-300"
        >
          Language
        </label>
        <input
          id="filter-language"
          v-model="filters.language"
          type="text"
          class="mt-1 block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100"
          placeholder="Filter by language"
          @input="handleInput"
        />
      </div>

      <div class="min-w-[120px]">
        <label
          for="filter-status"
          class="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Status</label
        >
        <select
          id="filter-status"
          v-model="filters.resolved"
          class="mt-1 block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100"
          @change="handleStatusChange"
        >
          <option
            v-for="option in resolvedOptions"
            :key="String(option.value)"
            :value="option.value"
          >
            {{ option.label }}
          </option>
        </select>
      </div>

      <div>
        <button
          class="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600"
          @click="clearFilters"
        >
          Clear
        </button>
      </div>
    </div>
  </div>
</template>
