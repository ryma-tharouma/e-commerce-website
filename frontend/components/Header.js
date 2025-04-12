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

          <Link href="/jewelry" className="text-xs font-[Georgia] hover:text-[#D4AF37]">JEWELRY</Link>
          <Link href="/library" className="text-xs font-[Georgia] hover:text-[#D4AF37]">LIBRARY</Link>
          <Link href="/about" className="text-xs font-[Georgia] hover:text-[#D4AF37]">ABOUT US</Link>

{/* Dropdown Group */}
<div className="flex items-center justify-center ">
  <div className="group relative py-5">
    <div className="">
      <p className="menu-hover text-xs font-[Georgia] hover:text-gray-500">
        AUCTIONS
      </p>
    </div>

    {/* Dropdown */}
    <div className="invisible absolute  flex w-full flex-row text-gray-500 group-hover:visible bg-gray-100 shadow-md mt-5 min-w-[900px] z-10 left-1/2 transform -translate-x-1/2">
{/* Image Column - Full Height Featured Image */}
<div className="w-1/4 pr-4">
    <div className="relative h-full min-h-[250px]">
      <Image 
        src="/dropdown.jpg" 
        alt="Featured Artwork"
        fill
        className="object-cover"
      />
      {/* <div className="absolute bottom-0 left-0 right-0 bg-black bg-opacity-50 p-3 text-white">
      </div> */}
    </div>
  </div>
      {/* First Column - English Auctions */}
      
      <div className="px-10 py-2 flex flex-col w-1/4">
        <p className="py-2 font-semibold text-sm text-gray-500">English Auctions</p>
        <Link href="/Auction_English/form_page" className="py-2  text-[#00060b] hover:text-[#D4AF37] text-xs font-[Georgia]">
          Add Auction
        </Link>
        <Link href="/Auction_English" className="py-2  text-[#00060b] hover:text-[#D4AF37] text-xs font-[Georgia]">
          See Auctions
        </Link>
      </div>


      {/* Second Column - Sealed Auctions */}
      <div className="py-2 flex flex-col w-1/4">
        <p className="py-2 font-semibold text-sm text-gray-500">Sealed Auctions</p>
        <Link href="/Auction_Sealed/form_page" className="py-2 text-[#00060b] hover:text-[#D4AF37] text-xs font-[Georgia]">
          Create Sealed Auction
        </Link>
        <Link href="/Auction_Sealed" className="py-2 text-[#00060b] hover:text-[#D4AF37] text-xs font-[Georgia]">
          View Sealed Auctions
        </Link>
      </div>

      {/* Third Column - Combinatorial Auctions */}
      <div className=" py-2 flex flex-col w-1/4">
        <p className="py-2 font-semibold text-sm text-gray-500">Combinatorial Auctions</p>
        <Link href="/Auction_Combinatorial/form_page" className="py-2 text-[#00060b] hover:text-[#D4AF37] text-xs font-[Georgia]">
          Start Combinatorial Auction
        </Link>
        <Link href="/Auction_Combinatorial" className="py-2 text-[#00060b] hover:text-[#D4AF37] text-xs font-[Georgia]">
          Browse Combinatorial Auctions
        </Link>
      </div>

      {/* Final Column - My Bids */}
      <div className="px-2 py-2 flex flex-col w-1/4">
        <p className="py-2 font-semibold text-sm text-gray-500">My Bids</p>
        <Link href="/My_Bids/active" className="py-2 text-[#00060b] hover:text-[#D4AF37] text-xs font-[Georgia]">
          Active Bids
        </Link>

        <Link href="/My_Bids" className="py-2 text-[#00060b] hover:text-[#D4AF37] text-xs font-[Georgia]">
          View My Bids
        </Link>
      </div>

    </div>
  </div>
</div>

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
