"use client";
import Link from "next/link";
import Image from "next/image";
import {
  FiPhone,
  FiMail,
  FiHeart,
  FiShoppingBag,
  FiSearch,
} from "react-icons/fi";
import { useCart } from "./CartContext";
import Header from "../../../components/Header";

export default function Cart() {
  const {
    cart,
    addToCart,
    removeFromCart,
    clearCart,
    create_checkout_session,
  } = useCart();
  const total = cart.reduce((sum, item) => sum + item.subtotal, 0);
  //console.log("🛒 Contenu du panier :", cart);
  return (
    <div className="min-h-screen flex flex-col justify-between bg-gray-100 font-serif">
      <Header />
      {/* MAIN CONTENT */}
      <main className="flex-grow px-8 py-12">
        <h1 className="text-2xl font-[Georgia] font-light tracking-wide mb-8 text-gray-800">Shopping Bag</h1>

        {cart.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-12">
            <p className="text-gray-600 text-lg mb-8 font-light">
              Your shopping bag is currently empty.
            </p>
            <Link href="/">
              <button className="px-12 py-5 bg-gray-900 text-white text-lg rounded-sm shadow-sm hover:bg-white hover:text-gray-900 hover:shadow-md transition-all duration-300 cursor-pointer font-light tracking-wide">
                CONTINUE BROWSING
              </button>
            </Link>
          </div>
        ) : (
          <div className="flex flex-col md:flex-row gap-8 w-full items-start">
            <div className="flex flex-col md:flex-row gap-8 w-full items-start">
              {/* Left Column: Cart Items */}
              <div className="w-full md:w-2/3 space-y-6 bg-white p-8 shadow-sm rounded-sm">
                <div>
                  <Link href="/">
                    <button className="text-gray-600 hover:text-gray-900 font-light tracking-wide cursor-pointer transition-colors duration-300">
                      ← Continue Browsing
                    </button>
                  </Link>
                </div>

                {cart.map((item) => (
                  <div
                    key={item.name}
                    className="flex justify-between items-center border-b border-gray-100 py-6"
                  >
                    <div className="flex items-center space-x-6">
                      <Image
                        src={item.image}
                        alt={item.name}
                        width={100}
                        height={100}
                        className="rounded-sm object-cover"
                      />
                      <div>
                        <h2 className="text-lg font-light tracking-wide text-gray-800">{item.name}</h2>
                        <p className="text-gray-600 font-light">${item.price}</p>
                        <p className="text-gray-500 text-sm font-light">x{item.quantity}</p>
                      </div>
                    </div>
                    <div className="flex space-x-3">
                      <button
                        onClick={() => addToCart(item)}
                        className="flex items-center justify-center p-2 bg-gray-50 hover:bg-gray-100 text-gray-600 rounded-sm transition-colors duration-300"
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
                        className="flex items-center justify-center p-2 bg-gray-50 hover:bg-gray-100 text-gray-600 rounded-sm transition-colors duration-300"
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
                <div className="flex justify-center pt-6">
                  <button
                    onClick={() => clearCart()}
                    className="px-6 py-3 bg-gray-50 text-gray-600 rounded-sm shadow-sm hover:bg-gray-100 hover:text-gray-900 border border-gray-200 transition-all duration-300 cursor-pointer font-light tracking-wide"
                  >
                    Clear cart
                  </button>
                </div>
              </div>

              {/* Right Column: Order Summary */}
              <div className="w-full md:w-1/3 bg-white p-8 rounded-sm shadow-sm sticky top-6">
                <h2 className="text-lg font-light tracking-wide mb-6 text-center text-gray-800">
                  ORDER SUMMARY
                </h2>
                <div className="space-y-4 text-sm text-gray-600">
                  <div className="flex justify-between">
                    <span className="font-light">Subtotal</span>
                    <span className="font-light">${total}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="font-light">Shipping & Handling</span>
                    <span className="text-gray-400 font-light">
                      Calculated at checkout
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="font-light">Estimated Tax</span>
                    <span className="text-gray-400 font-light">
                      Calculated at checkout
                    </span>
                  </div>
                  <hr className="my-4 border-gray-100" />
                  <div className="flex justify-between">
                    <span className="font-light">Estimated Total</span>
                    <span className="font-light">${total}</span>
                  </div>
                </div>
                <button
                  onClick={() => create_checkout_session()}
                  className="mt-8 w-full bg-gray-900 hover:bg-gray-800 text-white py-4 rounded-sm text-lg font-light tracking-wide cursor-pointer transition-colors duration-300"
                >
                  CHECKOUT
                </button>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* FOOTER */}
      <footer className="bg-white shadow-sm py-8 text-gray-600">
        <div className="container mx-auto grid grid-cols-2 md:grid-cols-4 gap-8 px-8 text-sm">
          {[
            {
              title: "Shop",
              links: ["Recent Acquisitions", "Antiques", "Jewelry", "Fine Art"],
            },
            {
              title: "Can We Help?",
              links: ["Customer Care", "FAQs", "Design Services", "Contact Us"],
            },
            {
              title: "Our Company",
              links: ["Buy with Confidence", "Events", "Sell to Us", "Careers"],
            },
          ].map((section, index) => (
            <div key={index}>
              <h3 className="font-light tracking-wide mb-4">{section.title}</h3>
              <ul className="space-y-2">
                {section.links.map((link, i) => (
                  <li
                    key={i}
                    className="flex items-center hover:text-gray-900 cursor-pointer transition-colors duration-300 font-light"
                  >
                    {link}
                  </li>
                ))}
              </ul>
            </div>
          ))}

          {/* Newsletter */}
          <div>
            <h3 className="font-light tracking-wide mb-4">Get The Latest</h3>
            <input
              type="email"
              placeholder="Email Address"
              className="border border-gray-200 p-2 w-full rounded-sm hover:border-gray-300 focus:border-gray-400 transition-colors duration-300 font-light"
            />
            <button className="mt-3 px-4 py-2 bg-gray-900 text-white rounded-sm hover:bg-gray-800 w-full cursor-pointer transition-colors duration-300 font-light tracking-wide">
              Join
            </button>
          </div>
        </div>
        <div className="text-center text-xs mt-8 font-light">
          © 2025 M.S. Rau | Privacy | Site Map
        </div>
      </footer>
    </div>
  );
}
