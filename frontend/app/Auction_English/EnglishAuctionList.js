'use client'
import { useState, useEffect } from "react";
import Image from "next/image";
import Link from "next/link";

const HoverImage = ({ defaultSrc, hoverSrc }) => {
  const [hovered, setHovered] = useState(false);

  return (
    <div
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      className="relative w-full h-64 bg-gray-200"
    >
      {defaultSrc && (
        <Image
          src={hovered ? hoverSrc : defaultSrc}
          alt="Product Image"
          fill
          objectFit="contain"

          className="object-cover"
        />
      )}
    </div>
  );
};

export default function AuctionGrid() {
  const [auctions, setAuctions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/Auction_English/auctions/")
      .then((response) => response.json())
      .then((data) => {
        setAuctions(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Erreur lors du chargement des enchères :", err);
        setError("Erreur: Impossible de charger les enchères.");
        setLoading(false);
      });
  }, []);

  if (loading) return <p className="text-center font-[Georgia] text-yellow-500 m-10">Loading auctions...</p>;
  if (error) return <p className="text-center font-[Georgia] text-yellow-500 m-10">{error}</p>;

  return (
    <div className=" mx-auto px-19 py-8">
      {/* the bar thing  */}
      <div className="flex justify-between items-center mb-8">
        <button className="text-sm flex items-center gap-2">
          <span className="font-[Georgia] font-semibold">FILTER & SORT</span> ⚙️
        </button>
        <div className="flex items-center gap-2">
          <span className="text-sm">ITEMS PER PAGE</span>
          <button className="px-2 py-1 bg-gray-300 hover:text-yellow-500">24</button>
          <button className="px-2 py-1 hover:text-yellow-500">30</button>
          <button className="px-2 py-1 hover:text-yellow-500">36</button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {auctions.map((auction) => 
        {
          const basePath = `/imgs/Auction_English/${auction.id}/image1.jpg`;
          const hoverBasePath = `/imgs/Auction_English/${auction.id}/image2.jpg`;

          return(
          <Link key={auction.id} href={`Auction_English/${auction.id}`} className="relative block bg-gray-200 overflow-hidden">
            <HoverImage 
            defaultSrc={basePath} 
            hoverSrc={hoverBasePath}  />
            <div className="mt-2 text-center p-2 bg-white">
              <p className="font-semibold text-gray-900">{auction.title}</p>
              <p className="text-gray-600">{auction.current_price ? `$${auction.current_price}` : "Price Upon Request"}</p>
            </div>
          </Link>
        )})}
      </div>
    </div>
  );
}
