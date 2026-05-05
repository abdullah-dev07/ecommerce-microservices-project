import { api } from "@/lib/api/client";
import type { CreateUserInput, UserOut } from "@/lib/schemas/user";

export const usersApi = {
  list: () => api.get<UserOut[]>("/users"),
  get: (id: number) => api.get<UserOut>(`/users/${id}`),
  create: (input: CreateUserInput) => api.post<UserOut>("/users", input),
};
