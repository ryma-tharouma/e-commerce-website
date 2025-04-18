"use client";

import { useState, useEffect } from "react";
import Image from "next/image";
import { useParams, useRouter } from "next/navigation";

export default function ProductDetails() {
  const { id } = useParams(); // Retrieve product ID from route
  const router = useRouter();
  const [product, setProduct] = useState(null);
  const [error, setError] = useState(null);

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

  const handleAddToCart = async () => {
    if (!isLoggedIn) {
      router.push("/auth/login"); // Redirect to login page (set your actual route)
      return;
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/cart/add/${product.id}/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            // Add auth header here when ready (e.g. Authorization: `Bearer ${token}`)
          },
        }
      );

      if (!response.ok) throw new Error("Failed to add to cart");
      alert("Product added to cart!");
    } catch (err) {
      console.error(err);
      alert("Something went wrong. Please try again.");
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
