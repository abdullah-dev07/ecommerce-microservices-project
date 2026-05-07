import Link from "next/link";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const SECTIONS = [
  {
    href: "/users",
    title: "Users",
    description: "Create and view registered users.",
    available: true,
  },
  {
    href: "/products",
    title: "Products",
    description: "Manage the product catalog and view stock.",
    available: true,
  },
  {
    href: "/orders",
    title: "Orders",
    description: "Place orders, view and cancel them per customer.",
    available: true,
  },
];

export default function DashboardPage() {
  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Dashboard</h2>
        <p className="text-sm text-muted-foreground">
          Frontend connects to the gateway at{" "}
          <code className="rounded bg-muted px-1 py-0.5 text-xs">
            NEXT_PUBLIC_API_BASE_URL
          </code>
          .
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        {SECTIONS.map((section) => (
          <Card key={section.href} className={section.available ? "" : "opacity-60"}>
            <CardHeader>
              <CardTitle>{section.title}</CardTitle>
              <CardDescription>{section.description}</CardDescription>
            </CardHeader>
            <CardContent>
              {section.available ? (
                <Link
                  href={section.href}
                  className="text-sm font-medium text-primary hover:underline"
                >
                  Open →
                </Link>
              ) : (
                <span className="text-sm text-muted-foreground">Not yet implemented</span>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
