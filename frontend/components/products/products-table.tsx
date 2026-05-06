"use client";

import { AlertCircle, Loader2 } from "lucide-react";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useProducts } from "@/hooks/use-products";
import { ApiError } from "@/lib/api/client";
import { formatCurrency, formatDate } from "@/lib/utils";

export function ProductsTable() {
  const { data, isLoading, error, refetch, isRefetching } = useProducts();

  if (isLoading) {
    return (
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <Loader2 className="h-4 w-4 animate-spin" />
        Loading products…
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
          <p className="font-medium">Could not load products</p>
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
        No products yet. Create one using the form on the left.
      </p>
    );
  }

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-16">ID</TableHead>
            <TableHead>Name</TableHead>
            <TableHead className="text-right">Price</TableHead>
            <TableHead className="text-right">Stock</TableHead>
            <TableHead>Created</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((product) => (
            <TableRow key={product.id}>
              <TableCell className="font-mono text-xs text-muted-foreground">
                #{product.id}
              </TableCell>
              <TableCell className="font-medium">
                <div>{product.name}</div>
                {product.description && (
                  <div className="text-xs text-muted-foreground">
                    {product.description}
                  </div>
                )}
              </TableCell>
              <TableCell className="text-right tabular-nums">
                {formatCurrency(product.price)}
              </TableCell>
              <TableCell className="text-right tabular-nums">
                {product.stock}
              </TableCell>
              <TableCell className="text-muted-foreground">
                {formatDate(product.created_at)}
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
