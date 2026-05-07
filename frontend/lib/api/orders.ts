import { api } from "@/lib/api/client";
import type { CreateOrderInput, Order } from "@/lib/schemas/order";

export const ordersApi = {
  // Note: the gateway exposes orders only by user. There is intentionally no
  // "list all orders" endpoint — we keep that constraint visible in the UI.
  listForUser: (userId: number) =>
    api.get<Order[]>(`/users/${userId}/orders`),
  get: (id: number) => api.get<Order>(`/orders/${id}`),
  create: (input: CreateOrderInput) => api.post<Order>("/orders", input),
  cancel: (id: number) => api.patch<Order>(`/orders/${id}/cancel`),
};
