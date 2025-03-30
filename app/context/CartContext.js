"use client";
import { createContext, useContext, useState, useEffect } from "react";

const CartContext = createContext(null);
const API_URL = "http://localhost:8000/api/cart";

export function CartProvider({ children }) {
  const [cart, setCart] = useState([]);
  const [sessionInitialized, setSessionInitialized] = useState(false);

  // Initialise la session au premier rendu
  useEffect(() => {
    const initializeSession = async () => {
      try {
        // Première requête pour établir la session
        await fetch(`${API_URL}/init/`, {
          credentials: "include",
        });
        setSessionInitialized(true);
      } catch (error) {
        console.error("❌ Erreur d'initialisation de session:", error);
      }
    };
    initializeSession();
  }, []);

  // Charge le panier une fois la session initialisée
  useEffect(() => {
    if (sessionInitialized) {
      fetchCart();
    }
  }, [sessionInitialized]);
  // 🔍 Debug: Affiche le contenu du panier à chaque mise à jour
  useEffect(() => {
    console.log("🛒 Cart State:", cart);
  }, [cart]);

  const fetchCart = async () => {
    try {
      const response = await fetch(`${API_URL}/view/`, {
        method: "GET",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok)
        throw new Error(`HTTP error! status: ${response.status}`);

      const data = await response.json();
      setCart(data?.cart || []);
    } catch (error) {
      console.error("❌ Erreur fetchCart:", error);
    }
  };

  const addToCart = async (product) => {
    try {
      const response = await fetch(`${API_URL}/add/${product.id}/`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ quantity: 1 }),
      });

      if (response.ok) {
        // Réutilise les mêmes cookies pour la requête suivante
        await fetchCart();
      }
    } catch (error) {
      console.error("❌ Erreur addToCart:", error);
    }
  };

  // ... (removeFromCart et clearCart restent identiques)

  return (
    <CartContext.Provider value={{ cart, addToCart }}>
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error("useCart must be used within a CartProvider");
  }
  return context;
}
