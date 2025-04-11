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
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [images, setImages] = useState([]);
  // const images = [
  //   "/imgs/Sealed_Auction/3/image1.jpg",
  //   "/imgs/Sealed_Auction/3/image2.jpg",
  //   "/imgs/Sealed_Auction/3/image3.jpg"
  // ];
  const [selectedImage, setSelectedImage] = useState(images[0]);
   
  useEffect(() => {
    fetch("http://127.0.0.1:8000/Combinatoire_Auction/auctions/")
      .then((response) => response.json())
      .then((data) => {
        setAuctions(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Erreur lors du chargement des enchères :", err);
        setError("Impossible de charger les enchères.");
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    if (!selectedProduct?.id) return; // Avoid unnecessary fetches

    const fetchImages = async () => {
        const imgList = [];
        for (let i = 1; i <= 10; i++) { // Assume max 10 images
            const imgPath = `/imgs/Sealed_Auction/${selectedProduct.id}/image${i}.jpg`;
            const res = await fetch(imgPath, { method: "HEAD" });

            if (res.ok) imgList.push(imgPath);
            else break; // Stop checking if an image is missing
        }
        setImages(imgList);
        if (imgList.length > 0) setSelectedImage(imgList[0]); //default
    };

    fetchImages();
}, [selectedProduct]);


if (loading) return <p className="text-center font-[Georgia] text-yellow-500 m-10">Loading auctions...</p>;
if (error) return <p className="text-center font-[Georgia] text-yellow-500 m-10">{error}</p>;
  return (
    <div className=" mx-auto px-19 py-8">
      {/* the bar thing  */}
      <div className="flex justify-between items-center mb-8">
        <button className="text-sm flex items-center gap-2">
          <span className="font-semibold">FILTER & SORT</span> ⚙️
        </button>
        <div className="flex items-center gap-2">
          <span className="text-sm">ITEMS PER PAGE</span>
          <button className="px-2 py-1 bg-gray-300 hover:text-yellow-500">24</button>
          <button className="px-2 py-1 hover:text-yellow-500">30</button>
          <button className="px-2 py-1 hover:text-yellow-500">36</button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

        {auctions.map((auction) => {
          
          const defaultImg = `/imgs/Sealed_Auction/${auction.id}/image1.jpg`;
          const hoverImg = `/imgs/Sealed_Auction/${auction.id}/image2.jpg`;
          return(
            <div key={auction.id}>

          <div key={auction.id} className="relative block bg-gray-200 overflow-hidden" onClick={() => setSelectedProduct(auction) }>
            <HoverImage defaultSrc={defaultImg} hoverSrc={hoverImg} 
            />
            <div className="mt-2 text-center p-2 bg-white">
              <p className="font-semibold text-gray-900">{auction.title}</p>
              <p className="text-gray-600">{auction.starting_price ? `Start at $${auction.starting_price}` : "Price Upon Request"}</p>
            </div>
          </div>
         

{/* Floating Modal */}
{selectedProduct && (
                
                <div className="fixed inset-0  bg-[rgba(229,231,235,0.55)] flex justify-center items-center">
                    <div className="bg-white p-8 shadow-lg w-[60%] h-[70%] relative overflow-hidden">
                        {/* Close Button */}
                        <button 
                            className="absolute top-4 right-4 text-gray-600 hover:text-gray-900 text-xl"
                            onClick={() => setSelectedProduct(null)}
                        >
                            ✕
                        </button>

                        <div className="grid grid-cols-12 gap-4 text-gray-700 font-serif h-full">
                            {/* Left: Image Gallery */}
                            <div className="col-span-2 flex flex-col gap-4">
                                {images.map((img, index) => (
                                    <div key={index} className="border border-gray-200 p-1 w-24 h-24">
                                        <Image
                                            src={img}
                                            alt={`Product image ${index + 1}`}
                                            width={80}
                                            height={80}
                                            className="cursor-pointer object-cover border hover:border-yellow-500"
                                            onClick={() => setSelectedImage(img)}
                                        />
                                    </div>
                                ))}
                            </div>

                            {/* Center: Main Image */}
                            <div className="col-span-6 flex justify-center items-center bg-gray-200 relative">
                                <div className="w-full h-full relative">
                                    {selectedImage && (
                                        <Image
                                            src={selectedImage}
                                            alt="Selected product"
                                            fill
                                            className="object-contain"
                                        />
                                    )}
                                </div>
                            </div>

                            {/* Right: Product Details */}
                            <div className="col-span-4 px-6 py-10 space-y-4">
                                <h1 className="text-2xl font-semibold text-gray-900">{selectedProduct.title}</h1>
                                <p className="text-sm text-gray-700">{selectedProduct.description}</p>
                            </div>
                        </div>
                    </div>
                </div>
            )}



</div>)
        }
      )
    }
    </div>
    </div>
  );
}
