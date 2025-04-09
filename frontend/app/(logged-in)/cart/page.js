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

export default function Cart() {
  const { cart, addToCart,removeFromCart,clearCart } = useCart();
  //console.log("🛒 Contenu du panier :", cart);
  return (
    <div className="min-h-screen flex flex-col justify-between bg-gray-100">
      {/* HEADER */}
      <header className="bg-white shadow-md py-2">
        {/* Top Bar */}
        <div className="container mx-auto flex justify-between items-center px-6 text-sm text-gray-700">
          <div className="flex space-x-4">
            <span className="flex items-center">
              <FiPhone className="mr-1 text-[#D4AF37]" /> 1-888-557-2406
            </span>
            <span className="flex items-center">
              <FiMail className="mr-1 text-[#D4AF37]" /> Sign up for the Latest
            </span>
          </div>
          <div className="flex space-x-4">
            <Link
              href="/wishlist"
              className="flex items-center hover:text-[#D4AF37]"
            >
              Create Wishlist <FiHeart className="ml-1" />
            </Link>
            <Link href="/signin" className="hover:text-[#D4AF37]">
              Sign in &gt;
            </Link>
            <Link
              href="/cart"
              className="flex items-center hover:text-[#D4AF37]"
            >
              Shopping Bag <FiShoppingBag className="ml-1" />
            </Link>
          </div>
        </div>

        {/* Main Header */}
        <div className="container mx-auto flex justify-between items-center px-6 py-3">
          {/* Logo */}
          <div className="flex-1 flex justify-center">
            <Image src="/FNRK.png" alt="Logo" width={120} height={100} />
          </div>
        </div>

        {/* Navigation */}
        <div className="container mx-auto flex justify-between items-center">
          <nav className="container mx-auto flex justify-center space-x-6 font-semibold py-2">
            {[
              "recent",
              "fineart",
              "antiques",
              "jewelry",
              "library",
              "about",
            ].map((item) => (
              <Link
                key={item}
                href={`/${item}`}
                className="text-xs font-[Georgia] hover:text-[#D4AF37]"
              >
                {item.toUpperCase().replace("_", " ")}
              </Link>
            ))}
          </nav>

          {/* Search Bar */}
          <div className="container mx-auto flex justify-end px-6 py-2">
            <div className="relative">
              <input
                type="text"
                placeholder="Search"
                className="border-b border-gray-400 p-2 pl-4 pr-10 text-gray-500 text-sm focus:outline-none"
              />
              <FiSearch className="absolute right-2 top-3 text-[#D4AF37]" />
            </div>
          </div>
        </div>
      </header>

      {/* MAIN CONTENT */}
      <main className="flex flex-col items-center justify-center flex-grow min-h-[50vh] py-10">
        {/* Ajouter un produit test */}
        <button
          onClick={() =>
            addToCart({
              product_id : 1,
              name: "vase",
              price: 150,
              image: "/vase1.jpg",
            })
          }
          className="mt-4 px-6 py-2 bg-green-600 text-white rounded-md shadow-md hover:bg-green-700"
        >
          Ajouter un produit test
        </button>

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
          <div className="w-full max-w-4xl bg-white p-6 shadow-md rounded-lg">
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
                  </div>
                </div>
                <button
                  onClick={() => addToCart(item)}
                  className="text-red-500 hover:underline"
                >
                  Add
                </button>
                <button
                  onClick={() => removeFromCart(item)}
                  className="text-red-500 hover:underline"
                >
                  Remove
                </button>
              </div>
              
            ))}
            <button 
                onClick={()=> clearCart()}
                className="px-12 py-5 bg-gray-900 text-white text-lg rounded-md shadow-md hover:bg-white hover:text-gray-900 hover:shadow-lg cursor-pointer ">
                Clear cart
              </button>
          </div>
        )}
      </main>

      {/* FOOTER */}
      <footer className="bg-white shadow-md py-6 text-gray-700">
        <div className="container mx-auto grid grid-cols-2 md:grid-cols-4 gap-6 px-6 text-sm">
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
              <h3 className="font-semibold">{section.title}</h3>
              <ul>
                {section.links.map((link, i) => (
                  <li
                    key={i}
                    className="flex items-center hover:text-[#D4AF37] cursor-pointer"
                  >
                    {link}
                  </li>
                ))}
              </ul>
            </div>
          ))}

          {/* Newsletter */}
          <div>
            <h3 className="font-semibold">Get The Latest</h3>
            <input
              type="email"
              placeholder="Email Address"
              className="border p-1 w-full rounded hover:border-[#D4AF37]"
            />
            <button className="mt-2 px-4 py-1 bg-gray-900 text-white rounded hover:bg-[#D4AF37] w-full cursor-pointer">
              Join
            </button>
          </div>
        </div>
        <div className="text-center text-xs mt-6">
          © 2025 M.S. Rau | Privacy | Site Map
        </div>
      </footer>
    </div>
  );
}
