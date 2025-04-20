'use client'

import { FiPhone, FiMail, FiHeart, FiShoppingBag, FiSearch } from "react-icons/fi";
import "flowbite";
import Link from "next/link";
import Image from "next/image";
import { useState } from "react";

export default function Header() {
  
  return (
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
          <Link href="/wishlist" className="flex items-center hover:text-[#D4AF37]">
            Create Wishlist <FiHeart className="ml-1" />
          </Link>
          <Link href="/signin" className="hover:text-[#D4AF37]">
            Sign in &gt;
          </Link>
          <Link href="/cart" className="flex items-center hover:text-[#D4AF37]">
            Shopping Bag <FiShoppingBag className="ml-1" />
          </Link>
        </div>
      </div>

      {/* Main Header */}
      <div className="container mx-auto flex justify-between items-center px-6 py-3">
        <div className="flex-1 flex justify-center">
          <Image src="/FNRK.png" alt="logo" width={120} height={100} />
        </div>
      </div>

      {/* Navigation & Search Bar */}
      <div className="container mx-auto flex justify-between items-center px-6">
        <nav className="flex justify-center space-x-6 font-semibold py-2 px-50">
          {/* Home Link */}
          <Link href="/" className="text-xs py-5 font-[Georgia] hover:text-[#D4AF37]">
            HOME
          </Link>

          {/* Categories Dropdown */}
          <div className="group relative py-5">
            <div>
              <p className="menu-hover text-xs font-[Georgia] hover:text-gray-500">
                CATEGORIES
              </p>
            </div>

            {/* Categories Dropdown */}
            <div className="invisible absolute flex w-full flex-col text-gray-500 group-hover:visible bg-gray-100 shadow-md mt-5 min-w-[200px] z-10 left-1/2 transform -translate-x-1/2">
              <Link href="/products?category=FURNITURE_DECO" className="px-6 py-3 text-[#00060b] hover:text-[#D4AF37] text-xs font-[Georgia] hover:bg-gray-50">
                Furniture & Decor
              </Link>
              <Link href="/products?category=JEWELRY" className="px-6 py-3 text-[#00060b] hover:text-[#D4AF37] text-xs font-[Georgia] hover:bg-gray-50">
                Jewelry
              </Link>
              <Link href="/products?category=FINE_ART" className="px-6 py-3 text-[#00060b] hover:text-[#D4AF37] text-xs font-[Georgia] hover:bg-gray-50">
                Fine Art
              </Link>
            </div>
          </div>

          {/* Auctions Dropdown */}
          <div className="group relative py-5">
            <div>
              <p className="menu-hover text-xs font-[Georgia] hover:text-gray-500">
                AUCTIONS
              </p>
            </div>

            {/* Auctions Dropdown */}
            <div className="invisible absolute flex w-full flex-row text-gray-500 group-hover:visible bg-gray-100 shadow-md mt-5 min-w-[900px] z-10 left-1/2 transform -translate-x-1/2">
              {/* Image Column - Full Height Featured Image */}
              <div className="w-1/4 pr-4">
                <div className="relative h-full min-h-[250px]">
                  <Image 
                    src="/dropdown.jpg" 
                    alt="Featured Artwork"
                    fill
                    className="object-cover"
                  />
                </div>
              </div>
              
              {/* First Column - English Auctions */}
              <div className="px-10 flex flex-col w-1/4 py-8 font-[Georgia]">
                <p className="py-2 font-semibold text-sm text-gray-500 mb-2">English Auctions</p>
                <Link href="/Auction_English/form_page" className="py-2 text-[#00060b] hover:text-[#D4AF37] text-xs">
                  Create an English Auction
                </Link>
                <Link href="/Auction_English" className="py-2 text-[#00060b] hover:text-[#D4AF37] text-xs">
                  View All English Auctions
                </Link>
              </div>

              {/* Second Column - Sealed Auctions */}
              <div className="py-8 flex flex-col w-1/4 font-[Georgia]">
                <p className="py-2 font-semibold text-sm text-gray-500 mb-4">Sealed Auctions</p>
                <Link href="/Auction_Sealed/form_page" className="py-2 text-[#00060b] hover:text-[#D4AF37] text-xs">
                  Create a Sealed Auction
                </Link>
                <Link href="/Auction_Sealed" className="py-2 text-[#00060b] hover:text-[#D4AF37] text-xs">
                  View All Sealed Auctions
                </Link>
              </div>

              {/* Third Column - Combinatorial Auctions */}
              <div className="py-8 flex flex-col w-1/4 font-[Georgia]">
                <p className="py-2 font-semibold text-sm text-gray-500 mb-4">Combinatorial Auctions</p>
                <Link href="/Auction_Combinatorial/form_page" className="py-2 text-[#00060b] hover:text-[#D4AF37] text-xs">
                  Create a Combinatorial Auction
                </Link>
                <Link href="/Auction_Combinatorial" className="py-2 text-[#00060b] hover:text-[#D4AF37] text-xs">
                  View All Combinatorial Auctions
                </Link>
              </div>
            </div>
          </div>

          {/* About Us Link */}
          <Link href="/about" className="text-xs py-5 font-[Georgia] hover:text-[#D4AF37]">
            ABOUT US
          </Link>
        </nav>

        {/* Search Bar */}
        <div className="relative">
          <input
            type="text"
            placeholder="Search"
            className="border-b border-gray-400 p-2 pl-4 pr-10 text-gray-500 text-sm focus:outline-none"
          />
          <FiSearch className="absolute right-2 top-3 text-[#D4AF37]" />
        </div>
      </div>
    </header>
  );
}
