"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { Plus, Trash2 } from "lucide-react";
import { useFieldArray, useForm } from "react-hook-form";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import { useCreateOrder } from "@/hooks/use-orders";
import { useProducts } from "@/hooks/use-products";
import { useUsers } from "@/hooks/use-users";
import { ApiError } from "@/lib/api/client";
import {
  createOrderSchema,
  type CreateOrderInput,
} from "@/lib/schemas/order";
import { formatCurrency } from "@/lib/utils";

type CreateOrderFormProps = {
  defaultUserId?: number | null;
};

export function CreateOrderForm({ defaultUserId }: CreateOrderFormProps) {
  const usersQuery = useUsers();
  const productsQuery = useProducts();
  const createOrder = useCreateOrder();

  const {
    register,
    handleSubmit,
    control,
    watch,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<CreateOrderInput>({
    resolver: zodResolver(createOrderSchema),
    defaultValues: {
      user_id: defaultUserId ?? 0,
      items: [{ product_id: 0, quantity: 1 }],
    },
  });

  const { fields, append, remove } = useFieldArray({ control, name: "items" });

  // Live preview total. Backend recomputes authoritatively; this is just for UX.
  const watchedItems = watch("items");
  const previewTotal = (watchedItems ?? []).reduce((sum, row) => {
    const product = productsQuery.data?.find((p) => p.id === Number(row.product_id));
    if (!product) return sum;
    const qty = Number(row.quantity) || 0;
    return sum + product.price * qty;
  }, 0);

  const onSubmit = handleSubmit(async (values) => {
    try {
      const order = await createOrder.mutateAsync(values);
      toast.success(
        `Created order #${order.id} for $${order.total.toFixed(2)}`,
      );
      reset({
        user_id: values.user_id,
        items: [{ product_id: 0, quantity: 1 }],
      });
    } catch (err) {
      const detail =
        err instanceof ApiError ? err.detail : (err as Error).message;
      toast.error(detail || "Failed to create order");
    }
  });

  return (
    <form onSubmit={onSubmit} className="space-y-4">
      <div className="grid gap-2">
        <Label htmlFor="user_id">Customer</Label>
        <Select id="user_id" {...register("user_id")} disabled={usersQuery.isLoading}>
          <option value={0}>
            {usersQuery.isLoading ? "Loading users…" : "Select a user"}
          </option>
          {usersQuery.data?.map((u) => (
            <option key={u.id} value={u.id}>
              #{u.id} — {u.name} ({u.email})
            </option>
          ))}
        </Select>
        {errors.user_id && (
          <p className="text-xs text-destructive">{errors.user_id.message}</p>
        )}
      </div>

      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <Label>Items</Label>
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => append({ product_id: 0, quantity: 1 })}
          >
            <Plus className="h-3 w-3" />
            Add item
          </Button>
        </div>

        <div className="space-y-2">
          {fields.map((field, index) => (
            <div
              key={field.id}
              className="grid grid-cols-[1fr_80px_auto] items-start gap-2"
            >
              <div>
                <Select
                  {...register(`items.${index}.product_id`)}
                  disabled={productsQuery.isLoading}
                >
                  <option value={0}>
                    {productsQuery.isLoading
                      ? "Loading products…"
                      : "Select a product"}
                  </option>
                  {productsQuery.data?.map((p) => (
                    <option key={p.id} value={p.id}>
                      #{p.id} — {p.name} ({formatCurrency(p.price)}, stock {p.stock})
                    </option>
                  ))}
                </Select>
                {errors.items?.[index]?.product_id && (
                  <p className="mt-1 text-xs text-destructive">
                    {errors.items[index]?.product_id?.message}
                  </p>
                )}
              </div>

              <div>
                <Input
                  type="number"
                  step="1"
                  min="1"
                  placeholder="Qty"
                  {...register(`items.${index}.quantity`)}
                />
                {errors.items?.[index]?.quantity && (
                  <p className="mt-1 text-xs text-destructive">
                    {errors.items[index]?.quantity?.message}
                  </p>
                )}
              </div>

              <Button
                type="button"
                variant="ghost"
                size="sm"
                onClick={() => remove(index)}
                disabled={fields.length === 1}
                aria-label="Remove item"
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          ))}
        </div>

        {errors.items?.message && (
          <p className="text-xs text-destructive">{errors.items.message}</p>
        )}
      </div>

      <div className="flex items-center justify-between rounded-md bg-muted/50 px-3 py-2 text-sm">
        <span className="text-muted-foreground">Estimated total</span>
        <span className="font-medium tabular-nums">
          {formatCurrency(previewTotal)}
        </span>
      </div>

      <Button type="submit" disabled={isSubmitting || createOrder.isPending}>
        {createOrder.isPending ? "Placing…" : "Place order"}
      </Button>
    </form>
  );
}
