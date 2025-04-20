"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import HoverImage from "./HoverImage";
import axios from "axios";

export default function ProductList({ category }) {
  const [products, setProducts] = useState([]); // State to store products
  const [loading, setLoading] = useState(true); // State for loading status
  const [error, setError] = useState(null); // State for error handling
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [showSuccess, setShowSuccess] = useState(false);

  // Cart API setup
  const API_URL = "http://localhost:8000/api/cart";
  const api = axios.create({
    baseURL: API_URL,
    withCredentials: true,
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  });

  // Function to add to cart
  const addToCart = async (productId, quantity) => {
    try {
      console.log("Adding product to cart:", productId, "Quantity:", quantity);
      await api.post(`/add/${productId}/`, { quantity });
      console.log("Product added to cart!");
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000); // Hide success message after 3 seconds
    } catch (err) {
      console.error("Error adding to cart:", err.message || err);
      alert("Failed to add product to cart. Please try again.");
    }
  };

  const handleAddToCart = (e, product) => {
    e.preventDefault();
    setSelectedProduct(product);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (selectedProduct) {
      addToCart(selectedProduct.id, quantity);
      setSelectedProduct(null);
      setQuantity(1);
    }
  };

  // Fetch products from the backend
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const url = category 
          ? `http://127.0.0.1:8000/inventory/api/products/?category=${category}`
          : 'http://127.0.0.1:8000/inventory/api/products/';
        
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error('Failed to fetch products');
        }
        const data = await response.json();
        setProducts(data); // Update the products state
      } catch (err) {
        console.error("Error loading products:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, [category]);

  // Handle loading state
  if (loading)
    return (
      <p className="text-center font-[Georgia] text-yellow-500 m-10">
        Loading products...
      </p>
    );

  // Handle error state
  if (error)
    return (
      <p className="text-center font-[Georgia] text-red-500 m-10">{error}</p>
    );

  // Handle empty products list
  if (products.length === 0) {
    return (
      <div className="text-center font-[Georgia] text-yellow-500 m-10">
        No products available in this category.
      </div>
    );
  }

  return (
    <div className="mx-auto px-8 py-12">
      {/* Success Message */}
      {showSuccess && (
        <div className="fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-[100]">
          Product added to cart successfully!
        </div>
      )}

      {/* Quantity Selection Popup */}
      {selectedProduct && (
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
                  max={selectedProduct.stock}
                  value={quantity}
                  onChange={(e) => setQuantity(Math.max(1, Math.min(selectedProduct.stock, parseInt(e.target.value) || 1)))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                />
                <p className="text-sm text-gray-500 mt-1">
                  Available: {selectedProduct.stock}
                </p>
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => {
                    setSelectedProduct(null);
                    setQuantity(1);
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

      {/* Product Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
        {products.map((product) => (
          <Link
            key={product.id}
            href={`/products/${product.id}`}
            className="relative block bg-gray-100 overflow-hidden rounded-lg shadow-sm hover:shadow-md transition-shadow h-[380px] flex flex-col"
          >
            {/* Hover Image */}
            <div className="relative w-full h-[240px]">
              <HoverImage 
                defaultSrc={product.images?.find(img => img.is_primary)?.image || product.image} 
                hoverSrc={product.images?.find(img => img.is_primary)?.image || product.image} 
                className="w-full h-full object-cover"
              />
            </div>
            <div className="mt-2 text-center p-3 bg-white flex-grow flex flex-col">
              <p className="font-semibold text-gray-900 text-sm mb-1 line-clamp-1">{product.name}</p>
              <div className="flex justify-center items-center gap-2 mb-1">
                <p className="text-[#D4AF37] text-base font-bold">
                  {product.price ? `$${product.price}` : "Price Upon Request"}
                </p>
                <span className="text-gray-400">|</span>
                <p className="text-xs text-gray-500">Stock: {product.stock}</p>
              </div>
              <p className="text-xs text-gray-700 mb-2 line-clamp-2 flex-grow">
                {product.description || "No description available"}
              </p>
              <button 
                className="w-full py-1 bg-[#D4AF37] text-white font-semibold rounded hover:bg-[#B38F2A] transition-colors text-xs"
                onClick={(e) => handleAddToCart(e, product)}
              >
                Add to Cart
              </button>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
