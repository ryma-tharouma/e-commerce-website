"use client";
import React from "react";
import { cn } from "/lib/utils";

const Button = React.forwardRef(({ className, variant = "default", ...props }, ref) => {
  const base =
    "inline-flex items-center justify-center rounded-2xl text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none";
  const variants = {
    default: "bg-[#D4AF37] text-white hover:bg-[#B59030]",
    outline: "border border-gray-300 text-gray-700 hover:border-[#D4AF37] hover:text-[#D4AF37]",
  };

  return (
    <button
      ref={ref}
      className={cn(base, variants[variant], className, "px-4 py-2")}
      {...props}
    />
  );
});
Button.displayName = "Button";

export { Button };
