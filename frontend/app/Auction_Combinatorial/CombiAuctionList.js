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
  const [filteredAuctions, setFilteredAuctions] = useState([]);
    
  const [showModal, setShowModal] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/Auction_Combinatoire/auctions/")
      .then((response) => response.json())
      .then((data) => {
      setAuctions(data);
        setFilteredAuctions(data);
          setLoading(false);
      })
      .catch((err) => {
        console.error("Erreur lors du chargement des enchères :", err);
        setError("Impossible de charger les enchères.");
        setLoading(false);
      });
  }, []);

  const handleSearch = () => {
    let filtered = auctions.filter(auction =>
      auction.title.toLowerCase().includes(searchQuery.toLowerCase())
    );

    if (minPrice) {
      filtered = filtered.filter(auction => auction.starting_price >= parseFloat(minPrice));
    }

    if (maxPrice) {
      filtered = filtered.filter(auction => auction.starting_price <= parseFloat(maxPrice));
    }

    if (startDate) {
      filtered = filtered.filter(auction => new Date(auction.start_date) >= new Date(startDate));
    }

    if (endDate) {
      filtered = filtered.filter(auction => new Date(auction.end_date) <= new Date(endDate));
    }

    setFilteredAuctions(filtered);
    setShowModal(false);
  };

  if (loading) return <p className="text-center font-[Georgia] text-yellow-500 m-10">Loading auctions...</p>;
  if (error) return <p className="text-center font-[Georgia] text-yellow-500 m-10">{error}</p>;
  
  // check for empty auctions
  if (auctions.length === 0) {
    return (
      <div className="text-center font-[Georgia] text-yellow-500 m-10">
        No auctions available at the moment.
      </div>
    );
  }


  return (
<div className="font-[Georgia]  relative mx-auto px-19 py-8">
      {/* the bar thing  */}
      <div className="flex justify-between items-center mb-8">
      <button
          className="text-sm flex items-center gap-2 bg-gray-200 px-4 py-2 rounded hover:text-yellow-500"
          onClick={() => setShowModal(true)}
        >
          <span className="font-semibold">FILTER & SORT</span> ⚙️
        </button>
        {/* <div className="flex items-center gap-2">
          <span className="text-sm">ITEMS PER PAGE</span>
          <button className="px-2 py-1 bg-gray-300 hover:text-yellow-500">24</button>
          <button className="px-2 py-1 hover:text-yellow-500">30</button>
          <button className="px-2 py-1 hover:text-yellow-500">36</button>
        </div> */}
      </div>

      {showModal && (
        <div className="absolute top-0 left-0 w-full h-full z-50 bg-[rgba(229,231,235,0.55)]">

          {/* Modal */}
          <div className="absolute top-0 left-0 p-4 ">
            <div className="bg-white p-6 shadow-lg w-96 border border-gray-300 rounded-none">
              <h2 className="text-xl font-bold mb-4">Filter Auctions</h2>

              <div className="mb-2 flex items-center">
                <label className="w-40 text-sm font-medium">Title:</label>
                <input
                  type="text"
                  placeholder="Search by title..."
                  className="w-full border px-3 py-2"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>

              <div className="mb-2 flex items-center">
                <label className="w-40 text-sm font-medium">Min Price:</label>
                <input
                  type="number"
                  className="w-full border px-3 py-2"
                  value={minPrice}
                  onChange={(e) => setMinPrice(e.target.value)}
                />
              </div>

              <div className="mb-2 flex items-center">
                <label className="w-40 text-sm font-medium">Max Price:</label>
                <input
                  type="number"
                  className="w-full border px-3 py-2"
                  value={maxPrice}
                  onChange={(e) => setMaxPrice(e.target.value)}
                />
              </div>

              <div className="mb-2 flex items-center">
                <label className="w-40 text-sm font-medium">Start Date:</label>
                <input
                  type="date"
                  className="w-full border px-3 py-2"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                />
              </div>

              <div className="mb-4 flex items-center">
                <label className="w-40 text-sm font-medium">End Date:</label>
                <input
                  type="date"
                  className="w-full border px-3 py-2"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                />
              </div>

              <div className="flex justify-end gap-2">
                <button onClick={() => setShowModal(false)} className="px-4 py-2 bg-gray-300 hover:bg-gray-400">Cancel</button>
                <button onClick={handleSearch} className="px-4 py-2 bg-yellow-500 text-white hover:bg-yellow-600">Apply</button>
              </div>
            </div>
          </div>
        </div>
      )}

{filteredAuctions.length===0 &&(<div> <p className="text-center text-yellow-700 m-10">No Available Auctions</p></div>)}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredAuctions.map((auction) => (
          
          <Link key={auction.id} href={`Auction_Combinatorial/${auction.id}`} className="relative block bg-gray-200 overflow-hidden">
            <HoverImage defaultSrc={`/imgs/Auction_Combinatoire/${auction.id}/image1.jpg`} hoverSrc={`/imgs/Auction_Combinatoire/${auction.id}/image2.jpg`} />
            <div className="mt-2 text-center p-2 bg-white">
              <p className="font-semibold text-gray-900">{auction.title}</p>
              <p className="text-gray-600">{auction.current_price ? `$${auction.current_price}` : "Price Upon Request"}</p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
