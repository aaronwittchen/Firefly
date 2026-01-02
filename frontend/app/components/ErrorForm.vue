<script setup lang="ts">
import {
  DialogClose,
  DialogContent,
  DialogOverlay,
  DialogPortal,
  DialogRoot,
  DialogTitle,
} from "reka-ui";
import type { ErrorLog, ErrorLogCreate } from "~/types/error";
import { errorLogCreateSchema } from "~/types/error";

const props = defineProps<{
  open: boolean;
  error?: ErrorLog | null;
}>();

const emit = defineEmits<{
  "update:open": [value: boolean];
  save: [data: ErrorLogCreate];
}>();

const isEditing = computed(() => !!props.error);

const form = reactive<ErrorLogCreate>({
  message: "",
  error_type: "",
  project: "",
  git_branch: "",
  git_commit: "",
  os: "",
  language: "",
  tags: [],
  solution: "",
  notes: "",
  time_to_fix_min: undefined,
  resolved: false,
});

const tagsInput = ref("");
const validationErrors = ref<Record<string, string>>({});

watch(
  () => props.error,
  (error) => {
    if (error) {
      form.message = error.message;
      form.error_type = error.error_type ?? "";
      form.project = error.project ?? "";
      form.git_branch = error.git_branch ?? "";
      form.git_commit = error.git_commit ?? "";
      form.os = error.os ?? "";
      form.language = error.language ?? "";
      form.tags = error.tags ?? [];
      form.solution = error.solution ?? "";
      form.notes = error.notes ?? "";
      form.time_to_fix_min = error.time_to_fix_min ?? undefined;
      form.resolved = error.resolved;
      tagsInput.value = (error.tags ?? []).join(", ");
    } else {
      resetForm();
    }
  },
  { immediate: true }
);

function resetForm() {
  form.message = "";
  form.error_type = "";
  form.project = "";
  form.git_branch = "";
  form.git_commit = "";
  form.os = "";
  form.language = "";
  form.tags = [];
  form.solution = "";
  form.notes = "";
  form.time_to_fix_min = undefined;
  form.resolved = false;
  tagsInput.value = "";
  validationErrors.value = {};
}

function handleTagsChange(value: string) {
  tagsInput.value = value;
  form.tags = value
    .split(",")
    .map((tag) => tag.trim())
    .filter((tag) => tag.length > 0);
}

function handleSubmit() {
  validationErrors.value = {};

  const result = errorLogCreateSchema.safeParse(form);
  if (!result.success) {
    for (const error of result.error.errors) {
      const path = error.path[0];
      if (typeof path === "string") {
        validationErrors.value[path] = error.message;
      }
    }
    return;
  }

  emit("save", result.data);
  emit("update:open", false);
  resetForm();
}

function handleClose() {
  emit("update:open", false);
  resetForm();
}

const inputClass =
  "mt-1 block w-full rounded-md border border-gray-300 bg-white px-3 py-2 shadow-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100";
const labelClass = "block text-sm font-medium text-gray-700 dark:text-gray-300";
</script>

<template>
  <DialogRoot :open="open" @update:open="$emit('update:open', $event)">
    <DialogPortal>
      <DialogOverlay class="fixed inset-0 z-40 bg-black/50" />
      <DialogContent
        class="fixed left-1/2 top-1/2 z-50 max-h-[85vh] w-full max-w-2xl -translate-x-1/2 -translate-y-1/2 overflow-y-auto rounded-lg bg-white p-6 shadow-xl dark:bg-gray-800"
      >
        <DialogTitle
          class="mb-4 text-lg font-semibold text-gray-900 dark:text-gray-100"
        >
          {{ isEditing ? 'Edit Error' : 'New Error' }}
        </DialogTitle>

        <form class="space-y-4" @submit.prevent="handleSubmit">
          <div>
            <label for="message" :class="labelClass">
              Message <span class="text-red-500">*</span>
            </label>
            <textarea
              id="message"
              v-model="form.message"
              rows="3"
              :class="inputClass"
              placeholder="Error message..."
            />
            <p
              v-if="validationErrors.message"
              class="mt-1 text-sm text-red-600 dark:text-red-400"
            >
              {{ validationErrors.message }}
            </p>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label for="project" :class="labelClass">Project</label>
              <input
                id="project"
                v-model="form.project"
                type="text"
                :class="inputClass"
                placeholder="Project name"
              />
            </div>
            <div>
              <label for="error_type" :class="labelClass"> Error Type </label>
              <input
                id="error_type"
                v-model="form.error_type"
                type="text"
                :class="inputClass"
                placeholder="TypeError, SyntaxError..."
              />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label for="language" :class="labelClass">Language</label>
              <input
                id="language"
                v-model="form.language"
                type="text"
                :class="inputClass"
                placeholder="Python, JavaScript..."
              />
            </div>
            <div>
              <label for="os" :class="labelClass">OS</label>
              <input
                id="os"
                v-model="form.os"
                type="text"
                :class="inputClass"
                placeholder="Windows, macOS, Linux..."
              />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label for="git_branch" :class="labelClass"> Git Branch </label>
              <input
                id="git_branch"
                v-model="form.git_branch"
                type="text"
                :class="inputClass"
                placeholder="main, feature/..."
              />
            </div>
            <div>
              <label for="git_commit" :class="labelClass"> Git Commit </label>
              <input
                id="git_commit"
                v-model="form.git_commit"
                type="text"
                :class="inputClass"
                placeholder="abc123..."
              />
            </div>
          </div>

          <div>
            <label for="tags" :class="labelClass">
              Tags (comma separated)
            </label>
            <input
              id="tags"
              :value="tagsInput"
              type="text"
              :class="inputClass"
              placeholder="frontend, api, database..."
              @input="
                handleTagsChange(($event.target as HTMLInputElement).value)
              "
            />
          </div>

          <div>
            <label for="solution" :class="labelClass">Solution</label>
            <textarea
              id="solution"
              v-model="form.solution"
              rows="3"
              :class="inputClass"
              placeholder="How was this error resolved?"
            />
          </div>

          <div>
            <label for="notes" :class="labelClass">Notes</label>
            <textarea
              id="notes"
              v-model="form.notes"
              rows="2"
              :class="inputClass"
              placeholder="Additional notes..."
            />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label for="time_to_fix" :class="labelClass">
                Time to Fix (minutes)
              </label>
              <input
                id="time_to_fix"
                v-model.number="form.time_to_fix_min"
                type="number"
                min="0"
                :class="inputClass"
                placeholder="15"
              />
            </div>
            <div class="flex items-center pt-6">
              <input
                id="resolved"
                v-model="form.resolved"
                type="checkbox"
                class="h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700"
              />
              <label
                for="resolved"
                class="ml-2 block text-sm text-gray-700 dark:text-gray-300"
                >Resolved</label
              >
            </div>
          </div>

          <div class="flex justify-end gap-3 pt-4">
            <DialogClose
              class="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600"
              @click="handleClose"
            >
              Cancel
            </DialogClose>
            <button
              type="submit"
              class="rounded-md bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700"
            >
              {{ isEditing ? 'Update' : 'Create' }}
            </button>
          </div>
        </form>
      </DialogContent>
    </DialogPortal>
  </DialogRoot>
</template>
