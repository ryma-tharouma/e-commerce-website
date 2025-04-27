"use client";
import { createContext, useContext, useState, useEffect } from "react";
import axios from "axios";

const CartContext = createContext();
const API_URL = "http://localhost:8000/api/cart";

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
});

export function CartProvider({ children }) {
  const [cart, setCart] = useState([]);

  const fetchCart = async () => {
    try {
      const { data } = await api.get("/view/");
      console.log("🛒 Réponse API:", data);
      setCart(data);
    } catch (error) {
      console.error(
        "❌ Erreur fetchCart:",
        error.response?.data || error.message
      );
    }
  };

  // Dans CartContext.js (frontend)
  useEffect(() => {
    const initializeCart = async () => {
      // 1. Initialise la session
      await axios.get("http://localhost:8000/api/cart/init/", {
        withCredentials: true,
      });

      // 2. Charge le panier
      await fetchCart();
    };
    initializeCart();
  }, []);

  const addToCart = async (productId) => {
    console.log("test", productId.product_id);
    await api.post(`/add/${productId.product_id}/`);
    console.log("tst", await fetchCart());
  };

  const removeFromCart = async (productId) => {
    console.log("tst", productId);
    await api.post(`/remove/${productId.product_id}/`);
    console.log("tst", await fetchCart());
  };
  const clearCart = async () => {
    await api.post(`/clear/`);
    console.log("tst", await fetchCart());
  };
  
  
  const create_checkout_session = async (paymentMethod) => {
    try {
      let url = '';
  
      if (paymentMethod === 'stripe') {
        const response = await axios.get('http://localhost:8000/api/cart/api/checkout-session/', {
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
          },
          withCredentials: true,
        });
  
        if (!response.data || !response.data.url) {
          throw new Error('Invalid response from server.');
        }
  
        url = response.data.url;
  
      } else if (paymentMethod === 'edahabia') {
        url = 'http://localhost:8000/payment/checkout/';
      } else {
        throw new Error('Unsupported payment method selected.');
      }
  
      window.location.href = url;
  
    } catch (error) {
      console.error("Checkout error:", error.response ? error.response.data : error.message);
      alert(error.response ? error.response.data.error : 'An unexpected error occurred');
    }
  };
  
  
  // Helper function to get cookies
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }
  
  

  return (
    <CartContext.Provider value={{ cart, addToCart, fetchCart,removeFromCart,clearCart,create_checkout_session }}>
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
