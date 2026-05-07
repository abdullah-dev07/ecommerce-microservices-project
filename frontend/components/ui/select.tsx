import * as React from "react";

import { cn } from "@/lib/utils";

export type SelectProps = React.SelectHTMLAttributes<HTMLSelectElement>;

// Plain styled native <select>. Keeps keyboard / a11y behaviour for free; we
// can swap in a fancier popover-based select later if/when we need search,
// multi-select, or rich item rendering.
export const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ className, children, ...props }, ref) => (
    <select
      ref={ref}
      className={cn(
        "flex h-9 w-full rounded-md border border-input bg-background px-2 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary disabled:cursor-not-allowed disabled:opacity-50",
        className,
      )}
      {...props}
    >
      {children}
    </select>
  ),
);
Select.displayName = "Select";
