'use client';

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import Header from "../../components/Header";
import Footer from "../../components/Footer";
import ProductList from "../../components/ProductList";

export default function ProductsPage() {
  const searchParams = useSearchParams();
  const category = searchParams.get('category');

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-grow">
        <ProductList category={category} />
      </main>
      <Footer />
    </div>
  );
} 