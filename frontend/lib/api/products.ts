import { api } from "@/lib/api/client";
import type { CreateProductInput, Product } from "@/lib/schemas/product";

export const productsApi = {
  list: () => api.get<Product[]>("/products"),
  get: (id: number) => api.get<Product>(`/products/${id}`),
  create: (input: CreateProductInput) => api.post<Product>("/products", input),
};
