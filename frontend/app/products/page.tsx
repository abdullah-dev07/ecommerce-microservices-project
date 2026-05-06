import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { CreateProductForm } from "@/components/products/create-product-form";
import { ProductsTable } from "@/components/products/products-table";

export default function ProductsPage() {
  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Products</h2>
        <p className="text-sm text-muted-foreground">
          Create products and view existing ones. Calls the gateway at{" "}
          <code className="rounded bg-muted px-1 py-0.5 text-xs">
            /products
          </code>
          .
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-[minmax(0,360px)_1fr]">
        <Card>
          <CardHeader>
            <CardTitle>New product</CardTitle>
            <CardDescription>
              Stock changes after this go through the order saga, not this form.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <CreateProductForm />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>All products</CardTitle>
            <CardDescription>
              Pulled live from the product service.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ProductsTable />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
