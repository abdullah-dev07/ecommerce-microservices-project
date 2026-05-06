"use client";

import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import { productsApi } from "@/lib/api/products";
import type { CreateProductInput, Product } from "@/lib/schemas/product";

export const productsKeys = {
  all: ["products"] as const,
  list: () => [...productsKeys.all, "list"] as const,
  detail: (id: number) => [...productsKeys.all, "detail", id] as const,
};

export function useProducts() {
  return useQuery<Product[]>({
    queryKey: productsKeys.list(),
    queryFn: productsApi.list,
  });
}

export function useProduct(id: number) {
  return useQuery<Product>({
    queryKey: productsKeys.detail(id),
    queryFn: () => productsApi.get(id),
    enabled: Number.isFinite(id),
  });
}

export function useCreateProduct() {
  const qc = useQueryClient();
  return useMutation<Product, Error, CreateProductInput>({
    mutationFn: productsApi.create,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: productsKeys.list() });
    },
  });
}
