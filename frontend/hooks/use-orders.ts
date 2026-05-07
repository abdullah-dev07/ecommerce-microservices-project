"use client";

import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import { ordersApi } from "@/lib/api/orders";
import type { CreateOrderInput, Order } from "@/lib/schemas/order";

export const ordersKeys = {
  all: ["orders"] as const,
  forUser: (userId: number) => [...ordersKeys.all, "user", userId] as const,
  detail: (id: number) => [...ordersKeys.all, "detail", id] as const,
};

export function useUserOrders(userId: number | null) {
  return useQuery<Order[]>({
    queryKey: ordersKeys.forUser(userId ?? -1),
    queryFn: () => ordersApi.listForUser(userId as number),
    enabled: typeof userId === "number" && Number.isFinite(userId),
  });
}

export function useOrder(id: number) {
  return useQuery<Order>({
    queryKey: ordersKeys.detail(id),
    queryFn: () => ordersApi.get(id),
    enabled: Number.isFinite(id),
  });
}

export function useCreateOrder() {
  const qc = useQueryClient();
  return useMutation<Order, Error, CreateOrderInput>({
    mutationFn: ordersApi.create,
    onSuccess: (order) => {
      // Refresh that user's order list and any product caches (stock changed).
      qc.invalidateQueries({ queryKey: ordersKeys.forUser(order.user_id) });
      qc.invalidateQueries({ queryKey: ["products"] });
    },
  });
}

export function useCancelOrder() {
  const qc = useQueryClient();
  return useMutation<Order, Error, number>({
    mutationFn: (id) => ordersApi.cancel(id),
    onSuccess: (order) => {
      qc.invalidateQueries({ queryKey: ordersKeys.forUser(order.user_id) });
      qc.invalidateQueries({ queryKey: ordersKeys.detail(order.id) });
      // Cancelling restores stock, so refresh product caches.
      qc.invalidateQueries({ queryKey: ["products"] });
    },
  });
}
