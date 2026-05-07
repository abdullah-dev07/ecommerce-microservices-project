import { z } from "zod";

export const orderStatusSchema = z.enum(["pending", "confirmed", "cancelled"]);
export type OrderStatus = z.infer<typeof orderStatusSchema>;

export const orderLineSchema = z.object({
  product_id: z.number().int(),
  name: z.string(),
  quantity: z.number().int(),
  unit_price: z.number(),
  line_total: z.number(),
});
export type OrderLine = z.infer<typeof orderLineSchema>;

export const orderOutSchema = z.object({
  id: z.number().int(),
  user_id: z.number().int(),
  items: z.array(orderLineSchema),
  total: z.number(),
  status: orderStatusSchema,
  created_at: z.string(),
});
export type Order = z.infer<typeof orderOutSchema>;

// Coerce the numeric inputs because <input type="number"> hands us strings
// via react-hook-form. See the same pattern in lib/schemas/product.ts.
export const createOrderItemSchema = z.object({
  product_id: z.coerce
    .number({ invalid_type_error: "Pick a product" })
    .int()
    .positive("Pick a product"),
  quantity: z.coerce
    .number({ invalid_type_error: "Quantity must be a number" })
    .int("Quantity must be a whole number")
    .positive("Quantity must be at least 1"),
});
export type CreateOrderItem = z.infer<typeof createOrderItemSchema>;

export const createOrderSchema = z.object({
  user_id: z.coerce
    .number({ invalid_type_error: "Pick a user" })
    .int()
    .positive("Pick a user"),
  items: z.array(createOrderItemSchema).min(1, "Add at least one item"),
});
export type CreateOrderInput = z.infer<typeof createOrderSchema>;
