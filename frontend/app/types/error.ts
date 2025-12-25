import { z } from "zod";

export const errorLogSchema = z.object({
  id: z.number(),
  message: z.string(),
  error_type: z.string().nullable(),
  project: z.string().nullable(),
  git_branch: z.string().nullable(),
  git_commit: z.string().nullable(),
  os: z.string().nullable(),
  language: z.string().nullable(),
  tags: z.array(z.string()).nullable(),
  solution: z.string().nullable(),
  notes: z.string().nullable(),
  time_to_fix_min: z.number().nullable(),
  resolved: z.boolean(),
  created_at: z.string(),
  updated_at: z.string().nullable(),
});

export const errorLogCreateSchema = z.object({
  message: z.string().min(1, "Message is required"),
  error_type: z.string().optional(),
  project: z.string().optional(),
  git_branch: z.string().optional(),
  git_commit: z.string().max(40, "Git commit hash must be 40 characters or less").optional(),
  os: z.string().optional(),
  language: z.string().optional(),
  tags: z.array(z.string()).optional(),
  solution: z.string().optional(),
  notes: z.string().optional(),
  time_to_fix_min: z.number().int().positive().optional(),
  resolved: z.boolean().default(false),
});

export const errorLogUpdateSchema = errorLogCreateSchema.partial();

export type ErrorLog = z.infer<typeof errorLogSchema>;
export type ErrorLogCreate = z.infer<typeof errorLogCreateSchema>;
export type ErrorLogUpdate = z.infer<typeof errorLogUpdateSchema>;

export interface ErrorFilters {
  project?: string;
  tag?: string;
  resolved?: boolean;
  language?: string;
  error_type?: string;
}
