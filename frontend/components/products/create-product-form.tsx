"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useCreateProduct } from "@/hooks/use-products";
import { ApiError } from "@/lib/api/client";
import {
  createProductSchema,
  type CreateProductInput,
} from "@/lib/schemas/product";

export function CreateProductForm() {
  const createProduct = useCreateProduct();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<CreateProductInput>({
    resolver: zodResolver(createProductSchema),
    defaultValues: { name: "", description: "", price: 0, stock: 0 },
  });

  const onSubmit = handleSubmit(async (values) => {
    try {
      const product = await createProduct.mutateAsync(values);
      toast.success(`Created product #${product.id}: ${product.name}`);
      reset();
    } catch (err) {
      const detail =
        err instanceof ApiError ? err.detail : (err as Error).message;
      toast.error(detail || "Failed to create product");
    }
  });

  return (
    <form onSubmit={onSubmit} className="space-y-4">
      <div className="grid gap-2">
        <Label htmlFor="name">Name</Label>
        <Input id="name" placeholder="Wireless mouse" {...register("name")} />
        {errors.name && (
          <p className="text-xs text-destructive">{errors.name.message}</p>
        )}
      </div>

      <div className="grid gap-2">
        <Label htmlFor="description">Description</Label>
        <Input
          id="description"
          placeholder="Optional"
          {...register("description")}
        />
        {errors.description && (
          <p className="text-xs text-destructive">
            {errors.description.message}
          </p>
        )}
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="grid gap-2">
          <Label htmlFor="price">Price (USD)</Label>
          <Input
            id="price"
            type="number"
            step="0.01"
            min="0"
            placeholder="19.99"
            {...register("price")}
          />
          {errors.price && (
            <p className="text-xs text-destructive">{errors.price.message}</p>
          )}
        </div>

        <div className="grid gap-2">
          <Label htmlFor="stock">Stock</Label>
          <Input
            id="stock"
            type="number"
            step="1"
            min="0"
            placeholder="0"
            {...register("stock")}
          />
          {errors.stock && (
            <p className="text-xs text-destructive">{errors.stock.message}</p>
          )}
        </div>
      </div>

      <Button type="submit" disabled={isSubmitting || createProduct.isPending}>
        {createProduct.isPending ? "Creating…" : "Create product"}
      </Button>
    </form>
  );
}
