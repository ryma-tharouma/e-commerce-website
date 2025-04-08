"use client";
import { createContext, useContext, useState, useEffect } from "react";
import axios from "axios";

const CartContext = createContext();
const API_URL = "http://localhost:8000/api/cart";

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    "Accept": "application/json",
    "Content-Type": "application/json",
  },
});

export function CartProvider({ children }) {
  const [cart, setCart] = useState([]);

  const fetchCart = async () => {
    try {
      const { data } = await api.get("/view/");
      console.log("🛒 Réponse API:", data);
      setCart(data?.items || data?.cart || []);
    } catch (error) {
      console.error("❌ Erreur fetchCart:", error.response?.data || error.message);
    }
  };

// Dans CartContext.js (frontend)
useEffect(() => {
    const initializeCart = async () => {
      // 1. Initialise la session
      await axios.get('http://localhost:8000/api/cart/init/', { 
        withCredentials: true 
      });
      
      // 2. Charge le panier
      await fetchCart();
    };
    initializeCart();
  }, []);

  const addToCart = async (productId) => {
    await api.post(`/add/${productId}/`);
    await fetchCart();
  };

  return (
    <CartContext.Provider value={{ cart, addToCart, fetchCart }}>
      {children}
    </CartContext.Provider>
  );
}

// ⚠️ Ceci est la partie manquante ⚠️
export function useCart() {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
}