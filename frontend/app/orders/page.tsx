"use client";

import { useState } from "react";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import { CreateOrderForm } from "@/components/orders/create-order-form";
import { OrdersTable } from "@/components/orders/orders-table";
import { useUsers } from "@/hooks/use-users";

export default function OrdersPage() {
  const usersQuery = useUsers();
  const [selectedUserId, setSelectedUserId] = useState<number | null>(null);

  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Orders</h2>
        <p className="text-sm text-muted-foreground">
          Place orders and view existing ones. Calls the gateway at{" "}
          <code className="rounded bg-muted px-1 py-0.5 text-xs">/orders</code>{" "}
          and{" "}
          <code className="rounded bg-muted px-1 py-0.5 text-xs">
            /users/{`{id}`}/orders
          </code>
          .
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Customer</CardTitle>
          <CardDescription>
            The gateway only lists orders by user, so pick one to view their
            orders below.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid max-w-sm gap-2">
            <Label htmlFor="customer">Selected customer</Label>
            <Select
              id="customer"
              value={selectedUserId ?? 0}
              onChange={(e) => {
                const v = Number(e.target.value);
                setSelectedUserId(v > 0 ? v : null);
              }}
              disabled={usersQuery.isLoading}
            >
              <option value={0}>
                {usersQuery.isLoading ? "Loading users…" : "Select a user"}
              </option>
              {usersQuery.data?.map((u) => (
                <option key={u.id} value={u.id}>
                  #{u.id} — {u.name} ({u.email})
                </option>
              ))}
            </Select>
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-6 md:grid-cols-[minmax(0,420px)_1fr]">
        <Card>
          <CardHeader>
            <CardTitle>New order</CardTitle>
            <CardDescription>
              Runs the saga: verifies the user, deducts stock, then writes the
              order. Stock is rolled back on failure.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <CreateOrderForm defaultUserId={selectedUserId} />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Customer orders</CardTitle>
            <CardDescription>
              Cancelling restores stock to the product service.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <OrdersTable userId={selectedUserId} />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
