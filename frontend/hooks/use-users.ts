"use client";

import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import { usersApi } from "@/lib/api/users";
import type { CreateUserInput, UserOut } from "@/lib/schemas/user";

export const usersKeys = {
  all: ["users"] as const,
  list: () => [...usersKeys.all, "list"] as const,
  detail: (id: number) => [...usersKeys.all, "detail", id] as const,
};

export function useUsers() {
  return useQuery<UserOut[]>({
    queryKey: usersKeys.list(),
    queryFn: usersApi.list,
  });
}

export function useUser(id: number) {
  return useQuery<UserOut>({
    queryKey: usersKeys.detail(id),
    queryFn: () => usersApi.get(id),
    enabled: Number.isFinite(id),
  });
}

export function useCreateUser() {
  const qc = useQueryClient();
  return useMutation<UserOut, Error, CreateUserInput>({
    mutationFn: usersApi.create,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: usersKeys.list() });
    },
  });
}
