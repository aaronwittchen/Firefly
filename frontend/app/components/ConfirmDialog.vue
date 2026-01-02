<script setup lang="ts">
import {
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogOverlay,
  DialogPortal,
  DialogRoot,
  DialogTitle,
} from "reka-ui";

defineProps<{
  open: boolean;
  title: string;
  description: string;
  confirmText?: string;
  cancelText?: string;
  destructive?: boolean;
}>();

defineEmits<{
  "update:open": [value: boolean];
  confirm: [];
}>();
</script>

<template>
  <DialogRoot :open="open" @update:open="$emit('update:open', $event)">
    <DialogPortal>
      <DialogOverlay class="fixed inset-0 z-40 bg-black/50" />
      <DialogContent
        class="fixed left-1/2 top-1/2 z-50 w-full max-w-md -translate-x-1/2 -translate-y-1/2 rounded-lg bg-white p-6 shadow-xl dark:bg-gray-800"
      >
        <DialogTitle
          class="text-lg font-semibold text-gray-900 dark:text-gray-100"
        >
          {{ title }}
        </DialogTitle>
        <DialogDescription
          class="mt-2 text-sm text-gray-500 dark:text-gray-400"
        >
          {{ description }}
        </DialogDescription>

        <div class="mt-6 flex justify-end gap-3">
          <DialogClose
            class="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600"
          >
            {{ cancelText || 'Cancel' }}
          </DialogClose>
          <button
            :class="[
              'rounded-md px-4 py-2 text-sm font-medium text-white',
              destructive
                ? 'bg-red-600 hover:bg-red-700'
                : 'bg-primary-600 hover:bg-primary-700',
            ]"
            @click="$emit('confirm')"
          >
            {{ confirmText || 'Confirm' }}
          </button>
        </div>
      </DialogContent>
    </DialogPortal>
  </DialogRoot>
</template>
