"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import HoverImage from "./HoverImage";

const ProductList = () => {
  const [products, setProducts] = useState([]); // State to store products
  const [loading, setLoading] = useState(true); // State for loading status
  const [error, setError] = useState(null); // State for error handling

  // Fetch products from the backend
  useEffect(() => {
    fetch("http://127.0.0.1:8000/inventory/api/products/")
      .then((response) => response.json())
      .then((data) => {
        setProducts(data); // Update the products state
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error loading products:", err);
        setError("Failed to load products. Please try again later.");
        setLoading(false);
      });
  }, []);

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
        No products available at the moment.
      </div>
    );
  }

  return (
    <div className="mx-auto px-19 py-8">
      {/* Product Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {products.map((product) => (
          <Link
            key={product.id}
            href={`/products/${product.id}`}
            className="relative block bg-gray-200 overflow-hidden"
          >
            {/* Hover Image */}
            <HoverImage defaultSrc={product.image} hoverSrc={product.image} />
            <div className="mt-2 text-center p-2 bg-white">
              <p className="font-semibold text-gray-900">{product.name}</p>
              <p className="text-gray-600">
                {product.price ? `$${product.price}` : "Price Upon Request"}
              </p>
              <p className="text-sm text-gray-500">Stock: {product.stock}</p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default ProductList;
