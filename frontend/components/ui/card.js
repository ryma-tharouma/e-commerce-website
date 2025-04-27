import React from "react";
import { cn } from "/lib/utils";

function Card({ className, ...props }) {
  return (
    <div className={cn("bg-white border border-gray-200 rounded-2xl shadow-sm", className)} {...props} />
  );
}

export { Card };
