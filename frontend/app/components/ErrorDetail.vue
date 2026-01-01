<script setup lang="ts">
import { DialogClose, DialogContent, DialogOverlay, DialogPortal, DialogRoot, DialogTitle } from "reka-ui";
import type { ErrorLog } from "~/types/error";

defineProps<{
  open: boolean;
  error: ErrorLog | null;
}>();

defineEmits<{
  "update:open": [value: boolean];
  edit: [error: ErrorLog];
}>();

const { formatDateTime } = useDayjs();
</script>

<template>
  <DialogRoot :open="open" @update:open="$emit('update:open', $event)">
    <DialogPortal>
      <DialogOverlay class="fixed inset-0 z-40 bg-black/50" />
      <DialogContent
        class="fixed left-1/2 top-1/2 z-50 max-h-[85vh] w-full max-w-2xl -translate-x-1/2 -translate-y-1/2 overflow-y-auto rounded-lg bg-white p-6 shadow-xl dark:bg-gray-800"
      >
        <div v-if="error" class="space-y-4">
          <div class="flex items-start justify-between">
            <DialogTitle class="max-w-md truncate text-lg font-semibold text-gray-900 dark:text-gray-100">
              {{ error.message }}
            </DialogTitle>
            <span
              :class="[
                'rounded-full px-2.5 py-0.5 text-xs font-medium',
                error.resolved
                  ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                  : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
              ]"
            >
              {{ error.resolved ? "Resolved" : "Open" }}
            </span>
          </div>

          <div class="rounded-md bg-gray-50 p-4 dark:bg-gray-900">
            <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400">Message</h4>
            <p class="mt-1 whitespace-pre-wrap text-sm text-gray-900 dark:text-gray-100">{{ error.message }}</p>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400">Project</h4>
              <p class="mt-1 text-sm text-gray-900 dark:text-gray-100">{{ error.project || "-" }}</p>
            </div>
            <div>
              <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400">Error Type</h4>
              <p class="mt-1 text-sm text-gray-900 dark:text-gray-100">{{ error.error_type || "-" }}</p>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400">Language</h4>
              <p class="mt-1 text-sm text-gray-900 dark:text-gray-100">{{ error.language || "-" }}</p>
            </div>
            <div>
              <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400">OS</h4>
              <p class="mt-1 text-sm text-gray-900 dark:text-gray-100">{{ error.os || "-" }}</p>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400">Git Branch</h4>
              <p class="mt-1 text-sm text-gray-900 dark:text-gray-100">{{ error.git_branch || "-" }}</p>
            </div>
            <div>
              <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400">Git Commit</h4>
              <p class="mt-1 font-mono text-sm text-gray-900 dark:text-gray-100">{{ error.git_commit || "-" }}</p>
            </div>
          </div>

          <div v-if="error.tags && error.tags.length > 0">
            <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400">Tags</h4>
            <div class="mt-1 flex flex-wrap gap-1">
              <span
                v-for="tag in error.tags"
                :key="tag"
                class="rounded-md bg-primary-100 px-2 py-0.5 text-xs font-medium text-primary-700 dark:bg-primary-900/30 dark:text-primary-400"
              >
                {{ tag }}
              </span>
            </div>
          </div>

          <div v-if="error.solution">
            <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400">Solution</h4>
            <p class="mt-1 whitespace-pre-wrap text-sm text-gray-900 dark:text-gray-100">{{ error.solution }}</p>
          </div>

          <div v-if="error.notes">
            <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400">Notes</h4>
            <p class="mt-1 whitespace-pre-wrap text-sm text-gray-900 dark:text-gray-100">{{ error.notes }}</p>
          </div>

          <div class="grid grid-cols-3 gap-4 border-t border-gray-200 pt-4 dark:border-gray-700">
            <div>
              <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400">Time to Fix</h4>
              <p class="mt-1 text-sm text-gray-900 dark:text-gray-100">
                {{ error.time_to_fix_min ? `${error.time_to_fix_min} min` : "-" }}
              </p>
            </div>
            <div>
              <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400">Created</h4>
              <p class="mt-1 text-sm text-gray-900 dark:text-gray-100">{{ formatDateTime(error.created_at) }}</p>
            </div>
            <div>
              <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400">Updated</h4>
              <p class="mt-1 text-sm text-gray-900 dark:text-gray-100">{{ formatDateTime(error.updated_at) }}</p>
            </div>
          </div>

          <div class="flex justify-end gap-3 pt-4">
            <DialogClose
              class="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600"
            >
              Close
            </DialogClose>
            <button
              class="rounded-md bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700"
              @click="$emit('edit', error)"
            >
              Edit
            </button>
          </div>
        </div>
      </DialogContent>
    </DialogPortal>
  </DialogRoot>
</template>
