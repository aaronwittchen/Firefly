<script setup lang="ts">
import type { ErrorLog } from "~/types/error";

defineProps<{
  errors: ErrorLog[];
  isLoading: boolean;
}>();

defineEmits<{
  edit: [error: ErrorLog];
  delete: [id: number];
  view: [error: ErrorLog];
}>();

const { formatRelative } = useDayjs();
</script>

<template>
  <div
    class="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm dark:border-gray-700 dark:bg-gray-800"
  >
    <div v-if="isLoading" class="flex items-center justify-center p-8">
      <Icon
        name="lucide:loader-2"
        class="h-6 w-6 animate-spin text-primary-500"
      />
      <span class="ml-2 text-gray-500 dark:text-gray-400"
        >Loading errors...</span
      >
    </div>

    <div
      v-else-if="errors.length === 0"
      class="p-8 text-center text-gray-500 dark:text-gray-400"
    >
      <Icon
        name="lucide:inbox"
        class="mx-auto h-12 w-12 text-gray-300 dark:text-gray-600"
      />
      <p class="mt-2">No errors found</p>
    </div>

    <table
      v-else
      class="min-w-full divide-y divide-gray-200 dark:divide-gray-700"
    >
      <thead class="bg-gray-50 dark:bg-gray-900">
        <tr>
          <th
            class="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400"
          >
            Message
          </th>
          <th
            class="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400"
          >
            Project
          </th>
          <th
            class="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400"
          >
            Type
          </th>
          <th
            class="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400"
          >
            Status
          </th>
          <th
            class="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400"
          >
            Created
          </th>
          <th
            class="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400"
          >
            Actions
          </th>
        </tr>
      </thead>
      <tbody
        class="divide-y divide-gray-200 bg-white dark:divide-gray-700 dark:bg-gray-800"
      >
        <tr
          v-for="error in errors"
          :key="error.id"
          class="cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-700"
          @click="$emit('view', error)"
        >
          <td
            class="max-w-xs truncate px-4 py-3 text-sm text-gray-900 dark:text-gray-100"
          >
            {{ error.message }}
          </td>
          <td class="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">
            {{ error.project || '-' }}
          </td>
          <td class="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">
            {{ error.error_type || '-' }}
          </td>
          <td class="px-4 py-3">
            <span
              :class="[
                'inline-flex rounded-full px-2 text-xs font-semibold leading-5',
                error.resolved
                  ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                  : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
              ]"
            >
              {{ error.resolved ? 'Resolved' : 'Open' }}
            </span>
          </td>
          <td class="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">
            {{ formatRelative(error.created_at) }}
          </td>
          <td class="px-4 py-3 text-right text-sm" @click.stop>
            <button
              class="mr-2 text-primary-600 hover:text-primary-900 dark:text-primary-400 dark:hover:text-primary-300"
              @click="$emit('edit', error)"
            >
              <Icon name="lucide:pencil" class="h-4 w-4" />
            </button>
            <button
              class="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300"
              @click="$emit('delete', error.id)"
            >
              <Icon name="lucide:trash-2" class="h-4 w-4" />
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
