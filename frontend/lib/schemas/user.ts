import { z } from "zod";

export const userOutSchema = z.object({
  id: z.number().int(),
  name: z.string(),
  email: z.string().email(),
  created_at: z.string(),
});
export type UserOut = z.infer<typeof userOutSchema>;

export const createUserSchema = z.object({
  name: z.string().min(1, "Name is required").max(100),
  email: z.string().email("Enter a valid email"),
  password: z.string().min(8, "Password must be at least 8 characters").max(128),
});
export type CreateUserInput = z.infer<typeof createUserSchema>;
