"use client";

import { AlertCircle, Loader2 } from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useCancelOrder, useUserOrders } from "@/hooks/use-orders";
import { ApiError } from "@/lib/api/client";
import type { Order, OrderStatus } from "@/lib/schemas/order";
import { cn, formatCurrency, formatDate } from "@/lib/utils";

const STATUS_STYLES: Record<OrderStatus, string> = {
  pending: "bg-amber-100 text-amber-900",
  confirmed: "bg-emerald-100 text-emerald-900",
  cancelled: "bg-zinc-200 text-zinc-700",
};

function StatusBadge({ status }: { status: OrderStatus }) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium capitalize",
        STATUS_STYLES[status],
      )}
    >
      {status}
    </span>
  );
}

function OrderItemsSummary({ order }: { order: Order }) {
  if (order.items.length === 0) return null;
  return (
    <ul className="mt-1 space-y-0.5 text-xs text-muted-foreground">
      {order.items.map((item) => (
        <li key={item.product_id}>
          {item.quantity} × {item.name}{" "}
          <span className="opacity-70">
            ({formatCurrency(item.unit_price)} ea)
          </span>
        </li>
      ))}
    </ul>
  );
}

type OrdersTableProps = {
  userId: number | null;
};

export function OrdersTable({ userId }: OrdersTableProps) {
  const { data, isLoading, error, refetch, isRefetching } = useUserOrders(userId);
  const cancelOrder = useCancelOrder();

  if (userId === null) {
    return (
      <p className="text-sm text-muted-foreground">
        Select a customer above to view their orders.
      </p>
    );
  }

  if (isLoading) {
    return (
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <Loader2 className="h-4 w-4 animate-spin" />
        Loading orders…
      </div>
    );
  }

  if (error) {
    const detail =
      error instanceof ApiError ? error.detail : (error as Error).message;
    return (
      <div className="flex items-start gap-2 rounded-md border border-destructive/30 bg-destructive/5 p-3 text-sm text-destructive">
        <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
        <div className="flex-1">
          <p className="font-medium">Could not load orders</p>
          <p className="text-xs opacity-80">{detail}</p>
          <button
            type="button"
            onClick={() => refetch()}
            className="mt-2 text-xs font-medium underline"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <p className="text-sm text-muted-foreground">
        This customer has no orders yet.
      </p>
    );
  }

  const handleCancel = async (orderId: number) => {
    try {
      await cancelOrder.mutateAsync(orderId);
      toast.success(`Order #${orderId} cancelled`);
    } catch (err) {
      const detail =
        err instanceof ApiError ? err.detail : (err as Error).message;
      toast.error(detail || "Failed to cancel order");
    }
  };

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-16">ID</TableHead>
            <TableHead>Items</TableHead>
            <TableHead className="text-right">Total</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Created</TableHead>
            <TableHead className="w-20" />
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((order) => (
            <TableRow key={order.id}>
              <TableCell className="font-mono text-xs text-muted-foreground align-top">
                #{order.id}
              </TableCell>
              <TableCell className="align-top">
                <div className="font-medium">
                  {order.items.length} item{order.items.length === 1 ? "" : "s"}
                </div>
                <OrderItemsSummary order={order} />
              </TableCell>
              <TableCell className="text-right tabular-nums align-top">
                {formatCurrency(order.total)}
              </TableCell>
              <TableCell className="align-top">
                <StatusBadge status={order.status} />
              </TableCell>
              <TableCell className="text-muted-foreground align-top">
                {formatDate(order.created_at)}
              </TableCell>
              <TableCell className="align-top">
                {order.status !== "cancelled" && (
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={() => handleCancel(order.id)}
                    disabled={
                      cancelOrder.isPending &&
                      cancelOrder.variables === order.id
                    }
                  >
                    {cancelOrder.isPending && cancelOrder.variables === order.id
                      ? "Cancelling…"
                      : "Cancel"}
                  </Button>
                )}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      {isRefetching && (
        <p className="border-t px-3 py-2 text-xs text-muted-foreground">
          Refreshing…
        </p>
      )}
    </div>
  );
}
