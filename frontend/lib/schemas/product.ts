import { z } from "zod";

export const productOutSchema = z.object({
  id: z.number().int(),
  name: z.string(),
  description: z.string(),
  price: z.number(),
  stock: z.number().int(),
  created_at: z.string(),
});
export type Product = z.infer<typeof productOutSchema>;

// `coerce` because <input type="number"> still gives us strings via
// react-hook-form unless we set valueAsNumber on every register() call.
// Coercing in the schema keeps the form code simple and consistent.
export const createProductSchema = z.object({
  name: z.string().min(1, "Name is required").max(200),
  description: z.string().max(2000).default(""),
  price: z.coerce
    .number({ invalid_type_error: "Price must be a number" })
    .positive("Price must be greater than 0"),
  stock: z.coerce
    .number({ invalid_type_error: "Stock must be a number" })
    .int("Stock must be a whole number")
    .nonnegative("Stock cannot be negative")
    .default(0),
});
export type CreateProductInput = z.infer<typeof createProductSchema>;
