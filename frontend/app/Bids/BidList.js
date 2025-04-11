// app/auction/[id]/page.jsx

"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";

export default function Bids({ params }) {
  const { id } = params;
  const router = useRouter();
  const [bids, setBids] = useState({
    english_bids: [],
    sealed_bids: [],
    combinatorial_bids: [],
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchBids() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/Bids/1`);

        // Check if the response is in JSON format
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        setBids(data);
        console.log(data);  // log the actual data, not the response
      } catch (error) {
        console.error("Error fetching bids:", error);
        setError("Impossible de charger les enchères.");
        setLoading(false);
      } finally {
        setLoading(false);
      }
    }

    fetchBids();
  }, [id]);

  async function handlePayment() {
    try {
      await axios.post(`/api/auction/${id}/pay`);
      router.push("/success");
    } catch (error) {
      console.error("Payment failed:", error);
    }
  }

  if (loading) return <p className="text-center text-yellow-700 m-10">Loading Bids...</p>;
  if (error) return <p className="text-center text-yellow-700 m-10">An Error Has Occured </p>;
  if (bids.length==0) return <p className="text-center text-yellow-700 m-10">You Have Made No Bids </p>;

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl text-center text-yellow-700 font-semibold font-[Georgia] mb-4">Bids</h1>
      <div className="w-40 h-0.5 bg-yellow-700 mx-auto mb-2"></div>
      
      {/* English Bids */}
      {bids.english_bids.length > 0 && (
        <div className="p-6 mx-auto">
          <h2 className="text-xl font-semibold font-[Georgia] text-yellow-700  mb-2">English Bids</h2>
          {bids.english_bids.map((bid) => (
            <div
              key={bid.id}
              className="flex items-center justify-between p-4 bg-gray-200  shadow-sm mb-4"
            >
              <div className="text-lg font-medium">{bid.auction_title}</div>
              <div className="text-lg font-semibold">${bid.amount}</div>
            </div>
          ))}
        </div>
      )}

      {/* Sealed Bids */}
      {bids.sealed_bids.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold mb-2">Sealed Bids</h2>
          {bids.sealed_bids.map((bid) => (
            <div
              key={bid.id}
              className="flex items-center justify-between p-4 border  shadow-sm mb-2"
            >
              <div className="text-lg font-medium">{bid.auction.title}</div>
              <div className="text-lg font-semibold">${bid.amount}</div>
            </div>
          ))}
        </div>
      )}

      {/* Combinatorial Bids */}
      {bids.combinatorial_bids.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold mb-2">Combinatorial Bids</h2>
          {bids.combinatorial_bids.map((bid) => (
            <div
              key={bid.id}
              className="flex items-center justify-between p-4 border  shadow-sm mb-2"
            >
              <div className="text-lg font-medium">{bid.auction.title}</div>
              <div className="text-lg font-semibold">${bid.amount}</div>
            </div>
          ))}
        </div>
      )}

      {/* Payment Button */}
      <button
        onClick={handlePayment}
        className="mt-6 w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4  shadow-md"
      >
        Pay
      </button>
 
    </div>
  );
}
