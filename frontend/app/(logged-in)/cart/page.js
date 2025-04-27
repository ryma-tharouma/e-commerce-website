"use client";
import Link from "next/link";
import Image from "next/image";
import Header from "../../../components/Header";
import Footer from "../../../components/Footer";

import {
  FiPhone,
  FiMail,
  FiHeart,
  FiShoppingBag,
  FiSearch,
} from "react-icons/fi";
import { useCart } from "./CartContext";
import { useState } from "react";

export default function Cart() {
  const {
    cart,
    addToCart,
    removeFromCart,
    clearCart,
    create_checkout_session,
  } = useCart();
  const total = cart.reduce((sum, item) => sum + item.subtotal, 0);
  const [paymentMethod, setPaymentMethod] = useState("stripe");

  //console.log("🛒 Contenu du panier :", cart);
  return (
    <div className="min-h-screen flex flex-col justify-between bg-gray-100">
      {/* HEADER */}
      <Header/>

      {/* MAIN CONTENT */}
      <main className="flex flex-col items-center justify-center flex-grow min-h-[50vh] py-10">
        {/* Ajouter un produit test */}
         {/* <button
          onClick={() =>
            addToCart({
              product_id: 1,
              name: "vase",
              price: 10,
              image: "/vase1.jpg",
            })
          }
          className="mt-4 px-6 py-2 bg-green-600 text-white rounded-md shadow-md hover:bg-green-700"
        >
          Ajouter un produit test
        </button>
        <button
          onClick={() =>
            addToCart({
              product_id: 2,
              name: "lampe",
              price: 30,
              image: "/lampe.jpg",
            })
          }
          className="mt-4 px-6 py-2 bg-green-600 text-white rounded-md shadow-md hover:bg-green-700"
        >
          Ajouter un produit test 2
        </button>  */}

        <h1 className="text-4xl font-[Georgia] font-bold mb-6">Shopping Bag</h1>

        {cart.length === 0 ? (
          <>
            <p className="text-gray-600 text-lg mb-8">
              Your shopping bag is currently empty.
            </p>
            <Link href="/">
              <button className="px-12 py-5 bg-gray-900 text-white text-lg rounded-md shadow-md hover:bg-white hover:text-gray-900 hover:shadow-lg cursor-pointer">
                CONTINUE BROWSING
              </button>
            </Link>
          </>
        ) : (
          <div className="flex flex-col md:flex-row gap-6 w-full items-start px-4 sm:px-6">
            <div className="flex flex-col md:flex-row gap-6 w-full items-start">
              {/* Colonne gauche : Panier */}
              <div className="w-full md:w-2/3 space-y-6 bg-white p-6 shadow-md rounded-lg">
                <div>
                  <Link href="/">
                    <button className="text-yellow-600 hover:underline font-medium cursor-pointer">
                      ← Continue Browsing
                    </button>
                  </Link>
                </div>

                <div className="w-full bg-white p-6 shadow-md rounded-lg">
                  {cart.map((item) => (
                    <div
                      key={item.name}
                      className="flex justify-between items-center border-b py-4"
                    >
                      <div className="flex items-center space-x-4">
                        <Image
                          src={item.image}
                          alt={item.name}
                          width={80}
                          height={80}
                          className="rounded"
                        />
                        <div>
                          <h2 className="text-lg font-semibold">{item.name}</h2>
                          <p className="text-gray-600">${item.price}</p>
                          <p className="text-gray-600">x{item.quantity}</p>
                        </div>
                      </div>
                      <div className="flex flex-col space-y-2 items-end">
                        <button
                          onClick={() => addToCart(item)}
                          className="flex items-center justify-center p-2 bg-green-100 hover:bg-green-200 text-green-800 rounded-full transition-colors"
                          aria-label="Add to cart"
                        >
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            className="h-5 w-5"
                            viewBox="0 0 20 20"
                            fill="currentColor"
                          >
                            <path
                              fillRule="evenodd"
                              d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
                              clipRule="evenodd"
                            />
                          </svg>
                        </button>

                        <button
                          onClick={() => removeFromCart(item)}
                          className="flex items-center justify-center p-2 bg-red-100 hover:bg-red-200 text-red-800 rounded-full transition-colors"
                          aria-label="Remove from cart"
                        >
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            className="h-5 w-5"
                            viewBox="0 0 20 20"
                            fill="currentColor"
                          >
                            <path
                              fillRule="evenodd"
                              d="M5 10a1 1 0 011-1h8a1 1 0 110 2H6a1 1 0 01-1-1z"
                              clipRule="evenodd"
                            />
                          </svg>
                        </button>
                      </div>
                    </div>
                  ))}
                  <div className="flex justify-center">
                    <button
                      onClick={() => clearCart()}
                      className="mt-6 px-6 py-3 bg-gray-900 text-white rounded-md shadow hover:bg-white hover:text-gray-900 border border-gray-900 transition cursor-pointer"
                    >
                      Clear cart
                    </button>
                  </div>
                </div>
              </div>

              {/* Colonne droite : Résumé commande */}
              <div className="w-full md:w-1/3 bg-gray-100 p-6 rounded-lg shadow-md sticky top-6">
                <h2 className="text-lg font-semibold mb-4 text-center">
                  ORDER SUMMARY
                </h2>
                <div className="space-y-2 text-sm text-gray-800">
                  <div className="flex justify-between">
                    <span>Subtotal</span>
                    <span>${total}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Shipping & Handling</span>
                    <span className="text-gray-500">
                      Calculated at checkout
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>Estimated Tax</span>
                    <span className="text-gray-500">
                      Calculated at checkout
                    </span>
                  </div>
                  <hr className="my-3" />
                  <div className="flex justify-between font-bold">
                    <span>Estimated Total</span>
                    <span>${total}</span>
                  </div>
                <div className="grid grid-cols-2 gap-4">
                  <button
                    onClick={() => setPaymentMethod("stripe")}
                    className={`border rounded-md px-4 py-2 text-sm font-medium transition ${
                      paymentMethod === "stripe"
                        ? "border-yellow-600 bg-yellow-100 text-yellow-800"
                        : "border-gray-300 bg-white text-gray-700 hover:bg-gray-50"
                    }`}
                  >
                    💳 Stripe
                  </button>
                  <button
                    onClick={() => setPaymentMethod("edahabia")}
                    className={`border rounded-md px-4 py-2 text-sm font-medium transition ${
                      paymentMethod === "edahabia"
                        ? "border-yellow-600 bg-yellow-100 text-yellow-800"
                        : "border-gray-300 bg-white text-gray-700 hover:bg-gray-50"
                    }`}
                  >
                    🧾 Edahabia
                  </button>
                </div>
              </div>

              {/* Bouton checkout */}
              <button
                onClick={() => create_checkout_session(paymentMethod)}
                className="mt-6 w-full bg-yellow-600 hover:bg-yellow-700 text-white py-3 rounded-md text-lg font-medium cursor-pointer"
              >
                CHECKOUT
              </button>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* FOOTER */}
      <Footer/>
    </div>
  );
}