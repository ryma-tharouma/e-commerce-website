'use client'

import { useState, useEffect } from "react";
import Image from "next/image";
import { useParams } from "next/navigation";

export default function Sealed_Auction_Item() {
  
  // const images = [
  //   "/imgs/product1.webp",
  //   "/imgs/product2.jpg",
  // ];

  const { id } = useParams();
  const [auction, setAuction] = useState(null);
  const [images, setImages] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null);
  const [timeLeft, setTimeLeft] = useState("");
  const controller = new AbortController();
  const [bidAmount, setBidAmount] = useState("");  
  const [error, setError] = useState(null);


  useEffect(() => {
    if (!id) return; //evite une requet vide 
    fetch(`http://127.0.0.1:8000/Auction_English/auctions/${id}/`)
    .then(response => {
        // console.log("Réponse brute :", response);
        return response.json(); // Convertir la réponse en JSON
      })
      .then(data => {
        console.log("Données reçues :", data);
        setAuction(data);
        if (data.end_time) {
            updateTimeLeft(data.end_time);
            const interval = setInterval(() => updateTimeLeft(data.end_time), 1000);
            return () => clearInterval(interval);  // Nettoyage de l'intervalle
          
      }
    })
      .catch(error => console.error("Erreur lors de la récupération des données :", error));
      return () => controller.abort();
    }, [id]);

    useEffect(() => {
      if (!id) return; // Avoid making an empty request

      const checkImages = async () => {
          const imgList = [];
          for (let i = 1; i <= 10; i++) { // Assume max 10 images
              const imgPath = `/imgs/Auction_English/${id}/image${i}.jpg`;
            
              // const imgPath = `/imgs/Auction_English/${id}/image${i}.jpg`;

              const res = await fetch(imgPath, { method: "HEAD" });

              if (res.ok) imgList.push(imgPath);
              else break; // Stop checking if a file is missing
          }
          setImages(imgList);
          if (imgList.length > 0) setSelectedImage(imgList[0]); // Set first image
      };

      checkImages();
  }, [id]);
    


 function updateTimeLeft(endTime) {
    const endDate = new Date(endTime);
    const now = new Date();
    const diff = endDate - now;

    if (diff <= 0) {
      setTimeLeft("Auction ended");
      return;
    }
    

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);


    setTimeLeft(`Auction ends in: ${days}j ${hours}h ${minutes}m ${seconds}s`);
  }

  
  const handleBid = async () => {
    setError(null); // Réinitialiser les erreurs

    const bidData = {
      user: 1, // Utilisateur statique
      amount: bidAmount, // Convertir l’entrée en nombre
    };

    try {
      const response = await fetch(`http://127.0.0.1:8000/Auction_English/auctions/${id}/bid/`, {

        
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(bidData),
      });
      console.log("Reponse brute:", response);
      if (!response.ok) {
        console.log("Error Details:", errorData); 
        throw new Error("Bid failed! Please enter a valid amount.");
      }

      const data = await response.json();
      // setAuction((prev) => ({ ...prev, current_price: data.new_price }));
      setBidAmount(""); // Réinitialiser le champ
    } catch (error) {
      setError(error.message);
    }
  };
  if (!auction) return <p  className="font-[Georgia]">Loading...</p>;

  return (
    
    <div className=" mx-auto px-7 py-8 grid grid-cols-12 gap-4 text-gray-700 font-serif">
      {/* Left: Image Gallery */}
      <div className="col-span-1 flex flex-col gap-4">
        {images.map((img, index) => (
          
          <div key={index} className="border border-gray-200 p-1 w-40 h-50  ">
            <Image
              src={img}
              alt={`Product image ${index + 1}`}
              width={150}
              height={150}
              className="cursor-pointer object-cover border hover:border-yellow-500"
              onClick={() => setSelectedImage(img)}
            />
          </div>
        ))}
      </div>

      <div className="col-span-1">
      </div>
{/* Center: Main Image */}
<div className="col-span-6 flex justify-center items-center bg-gray-200 relative">
  <div className="w-full h-full relative">
    <Image
      src={selectedImage}
      alt="Selected product"
      fill
      className="object-contain"
    />
  </div>
</div>



      
      {/* Right: Product Details */}
      <div className="px-4 py-20 col-span-4 space-y-4 ">

        <h1 className="text-2xl font-semibold text-gray-900">{auction.title}</h1>
        <p className="text-sm text-gray-700">{auction.description}</p>

        {timeLeft !== "Auction ended" && (
          <div className="border-t border-b border-gray-400 py-2 text-gray-500 text-sm text-center font-semibold uppercase">
        Starting price : ${auction.starting_price}
        </div>)
        }
        {/* a sealed auction doesnt have a current price */}
{/* Timer */}
<div className="text-center text-lg font-bold text-yellow-600">
          {timeLeft}
        </div>
        {timeLeft !== "Auction ended" && (
          <div className=" rounded-lg">
          {/* Bidding Section */}
          
          <button className="mt-4 w-full bg-yellow-600 text-white py-2 text-sm font-semibold font-[Georgia] hover:bg-yellow-700" onClick={handleBid}>
          Place Bid</button>
          <input 
          type="number" className="w-full border p-2 text-sm mt-2 " placeholder="Enter your bid" 
          value={bidAmount}
          onChange={(e) => setBidAmount(e.target.value)}
          />
        </div>)}

      </div>




      

    
    </div>
  );
}
