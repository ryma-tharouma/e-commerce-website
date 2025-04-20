// Supprimez 'use client' et laissez Next.js gérer cela comme un Server Component
import { CartProvider } from "./CartContext";
import "../../globals.css";

export const metadata = {
  title: "Votre Panier",
  description: "Gérez vos articles",
};

export default function CartLayout({ children }) {
  return (
    <CartProvider>
      {children}
    </CartProvider>
  );
}