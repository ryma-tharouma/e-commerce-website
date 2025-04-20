"use client";

import { useState, useEffect } from "react";
import Image from "next/image";
import { useParams, useRouter } from "next/navigation";
import axios from "axios";

export default function ProductDetails() {
  const { id } = useParams(); // Retrieve product ID from route
  const router = useRouter();
  const [product, setProduct] = useState(null);
  const [error, setError] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [showPopup, setShowPopup] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);

  // Simulate login state (replace with real auth logic later)
  const isLoggedIn = false; // Change to true to simulate a logged-in user

  useEffect(() => {
    if (!id) return;

    const fetchProduct = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/inventory/api/products/${id}/`
        );
        if (!response.ok) throw new Error("Failed to fetch product data");

        const data = await response.json();
        setProduct(data);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchProduct();
  }, [id]);

  // Function to add to cart
  const API_URL = "http://localhost:8000/api/cart";

  const api = axios.create({
    baseURL: API_URL,
    withCredentials: true,
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  });

  const addToCart = async (productId, quantity) => {
    try {
      console.log("Adding product to cart:", productId, "Quantity:", quantity);
      await api.post(`/add/${productId}/`, { quantity });
      console.log("Product added to cart!");
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000);
    } catch (err) {
      console.error("Error adding to cart:", err.message || err);
      alert("Failed to add product to cart. Please try again.");
    }
  };

  const handleAddToCart = (e) => {
    e.preventDefault();
    setQuantity(1);
    setShowPopup(true);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (product) {
      addToCart(product.id, quantity);
      setQuantity(1);
      setShowPopup(false);
    }
  };

  if (error)
    return (
      <p className="text-center font-[Georgia] text-red-500 m-10">
        Error: {error}
      </p>
    );
  if (!product)
    return (
      <p className="text-center font-[Georgia] text-yellow-500 m-10">
        Loading...
      </p>
    );

  return (
    <div className="mx-auto px-7 py-8 grid grid-cols-12 gap-4 text-gray-700 font-serif">
      {/* Success Message */}
      {showSuccess && (
        <div className="fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-[100]">
          Product added to cart successfully!
        </div>
      )}

      {/* Quantity Selection Popup */}
      {showPopup && (
        <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-[100]">
          <div className="bg-white p-6 rounded-lg shadow-xl w-96">
            <h3 className="text-lg font-semibold mb-4">Select Quantity</h3>
            <form onSubmit={handleSubmit}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Quantity
                </label>
                <input
                  type="number"
                  min="1"
                  max={product.stock}
                  value={quantity}
                  onChange={(e) => setQuantity(Math.max(1, Math.min(product.stock, parseInt(e.target.value) || 1)))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                />
                <p className="text-sm text-gray-500 mt-1">
                  Available: {product.stock}
                </p>
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => {
                    setQuantity(1);
                    setShowPopup(false);
                  }}
                  className="px-4 py-2 text-gray-700 border border-gray-300 rounded-md hover:bg-gray-100"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-[#D4AF37] text-white rounded-md hover:bg-[#B38F2A]"
                >
                  Add to Cart
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Main Image */}
      <div className="col-span-7 flex justify-center items-center bg-gray-200 relative">
        <div className="w-full h-full relative">
          {product.image && (
            <Image
              src={product.image}
              alt="Product"
              fill
              className="object-contain"
            />
          )}
        </div>
      </div>

      {/* Product Details */}
      <div className="px-4 py-20 col-span-5 space-y-4">
        <h1 className="text-2xl font-semibold text-gray-900">{product.name}</h1>
        <p className="text-sm text-gray-700">{product.description}</p>

        <div className="border-t border-b border-gray-400 py-2 text-gray-500 text-sm text-center font-semibold uppercase">
          Price: ${product.price}
        </div>
        <div>
          <div className="text-center text-lg font-bold text-yellow-600">
            In Stock: {product.stock}
          </div>

          <div className="text-center pt-4">
            <button
              onClick={handleAddToCart}
              className="bg-yellow-600 text-white py-3 w-full font-[Georgia] text-sm font-semibold hover:bg-yellow-700"
            >
              Add to Cart
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}