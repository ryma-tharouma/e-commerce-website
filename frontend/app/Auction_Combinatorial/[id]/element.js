'use client'
import { useState, useEffect } from "react";
import Image from "next/image";
import { useParams } from "next/navigation";


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

export default function ProductGrid() {
    const { id } = useParams();
  
  const [products, setproducts] = useState([]);
  const [auction, setauction] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [images, setImages] = useState([]);
  const [timeLeft, setTimeLeft] = useState("");
  const [isAuctionEnded, setIsAuctionEnded] = useState(false);
  const [bidAmount, setBidAmount] = useState(0);  


  const [selectedImage, setSelectedImage] = useState(images[0]);
   //fetch auction 
  useEffect(() => {
    fetch(`http://127.0.0.1:8000/Auction_Combinatoire/auctions/${id}/`)  
      .then((response) => response.json())
      .then((data) => {
        setauction(data);
        setLoading(false);
        if (data.end_time) {
          updateTimeLeft(data.end_time);
          const interval = setInterval(() => updateTimeLeft(data.end_time), 1000);
          return () => clearInterval(interval);}
      })
      .catch((err) => {
        console.error("Erreur lors du chargement des enchères :", err);
        setError("Impossible de charger les enchères.");
        setLoading(false);
      });
  }, []);
 
//fetching its products 
  useEffect(() => {
    if (!id) return; 
    fetch(`http://127.0.0.1:8000/Auction_Combinatoire/auctions/${id}/products`)  
      .then((response) => response.json())
      .then((data) => {
        setproducts(data.products);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Erreur lors du chargement des enchères :", err);
        setError("Impossible de charger les enchères.");
        setLoading(false);
      });
  }, []);
  
  // fetching imgs 
  useEffect(() => {
    if (!selectedProduct?.id) return; // Avoid unnecessary fetches

    const fetchImages = async () => {
        const imgList = [];
        for (let i = 1; i <= 10; i++) { // Assume max 10 images
            const imgPath = `/imgs/Auction_Combinatoire/Products/${selectedProduct.id}/image${i}.jpg`;
            const res = await fetch(imgPath, { method: "HEAD" });

            if (res.ok) imgList.push(imgPath);
            else break; // Stop checking if an image is missing
        }
        setImages(imgList);
        if (imgList.length > 0) setSelectedImage(imgList[0]); //default
    };

    fetchImages();
}, [selectedProduct]);

function updateTimeLeft(endTime) {
  const endDate = new Date(endTime);
  const now = new Date();
  const diff = endDate - now;

  if (diff <= 0) {
    setTimeLeft("Auction ended");
    setIsAuctionEnded(true);

    return;
  }

  const days = Math.floor(diff / (1000 * 60 * 60 * 24));
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((diff % (1000 * 60)) / 1000);

  setTimeLeft(`Auction ends in: ${days}j ${hours}h ${minutes}m ${seconds}s`);
}

const [isSubmitting, setIsSubmitting] = useState(false);

const handleBid = async () => {
  setError(null); // Reset errors

  const bidData = {
    user: 1, // Static user
    amount: bidAmount,
    products: selectedProducts,
  };

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/Auction_Combinatoire/auctions/${id}/bid/`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(bidData),
      }
    );

    console.log("Raw response:", response);

    if (!response.ok) {
      const errorDetails = await response.json();
      console.log("Error Details:", errorDetails);
      alert(errorDetails.error || "Failed to place bid");
    } else {
      setBidAmount(0); // Reset bid input on success
      alert("Bid placed successfully!");
    }
  } catch (error) {
    setError(error.message);
    alert("Network error: " + error.message);
  }
};




const [selectedProducts, setSelectedProducts] = useState([]);

const handleSelection = (product) => {
  console.log("Handling Selection for:", product);
  
  setSelectedProducts((prevSelected) => {
    console.log("Previous Selected Products:", prevSelected);
    
    if (prevSelected.some((p) => p.id === product.id)) {
      console.log("Removing Product:", product.id);
      return prevSelected.filter((p) => p.id !== product.id);
    } else {
      console.log("Adding Product:", product.id);
      return [...prevSelected, product];
    }
  });
};


  if (loading) return <p className="text-center text-gray-700">Loading products...</p>;


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
{/* auction title  */}
      <h2 className="text-3xl font-[Georgia] text-center mb-2">{auction.title}</h2>
      <div className="w-70 h-0.5 bg-yellow-500 mx-auto mb-2"></div>

      <p className="text-sm text-gray-700 text-center p-5 ">{auction.description}</p>

{/* Timer */}
<div className="text-center text-lg font-bold text-yellow-600 mb-6">
          {isAuctionEnded && (
            <h1 className="text-3xl font-[Georgia] text-center m-5 mb-4"><p>
              This Auction Has Ended, No bids can be made.
              </p>
            We Invite You To Check The Products In The Auction </h1>)}
        {!isAuctionEnded && (
          <div>

            {timeLeft} 
          </div>
          )}
        </div>

        {!isAuctionEnded && (


      <h1 className="text-3xl font-[Georgia] text-center m-5">Featured Products in the Bid </h1>
        )}
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

        {products.map((product) => {
          
          const defaultImg = `/imgs/Auction_Combinatoire/Products/${product.id}/image1.jpg`;
          const hoverImg = `/imgs/Auction_Combinatoire/Products/${product.id}/image2.jpg`;
          return(
            <div key={product.id}>
          <div key={product.id} className="relative block bg-gray-200 overflow-hidden" 
          
          onClick={() => {
            setSelectedProduct(null); // Reset first to clear the old selection
            
            setTimeout(() => {}, 0); 
            setSelectedProduct(product); 
          }}
          >
            <HoverImage defaultSrc={defaultImg} hoverSrc={hoverImg} 
            />
            <div className=" text-center p-4 bg-white">
              <p className="font-semibold text-gray-900">{product.name}</p>
            </div>
          </div>
         

{/* Floating Modal */}
{selectedProduct && (
                
                <div className="fixed inset-0  bg-[rgba(229,231,235,0.55)] flex justify-center items-center">
                    <div className="bg-white p-8 shadow-lg w-[60%] h-[70%] relative overflow-hidden">
                        {/* Close Button */}
                        <button 
                            className="absolute top-4 right-4 text-gray-600 hover:text-gray-900 text-xl"
                            onClick={() =>{ setSelectedProduct(null);setSelectedImage(null);
                            console.log("Selected Products:", selectedProducts);// Set new selection after a short delay

                            }}
                        >
                            ✕
                        </button>

                        <div className="grid grid-cols-12 gap-4 text-gray-700 font-[Georgia] h-full">
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
                                <h1 className="text-2xl font-semibold text-gray-900">{selectedProduct.name}</h1>
                                <p className="text-sm text-gray-700">{selectedProduct.description}</p>
                                {!isAuctionEnded && (
        <div >
        {/* Selection */}
          
          <button className="mt-4 w-full bg-yellow-600 text-white py-2 text-sm   hover:bg-yellow-700" onClick={() => {handleSelection(selectedProduct); }} >
          {selectedProducts.some((p) => p.id === selectedProduct.id)
        ? "Remove From My Selection" // If already selected
        : "Add To My Selection" // If not selected
      }
      
      </button>
          
        </div>)}
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


    {!isAuctionEnded && (
        <div className="mt-9">
          {/* Bidding Section */}
          
    {selectedProducts && selectedProducts.length > 0 && (
      <div className="mt-8 p-4 border border-gray-300  bg-gray-100">

    <h2 className="text-3xl font-[Georgia] text-center mb-2">Your Selection</h2>
  <div className="w-70 h-0.5 bg-yellow-500 mx-auto mb-2"></div>
  
    <ul className="flex flex-wrap gap-4 mb-10">
      {selectedProducts.map((product) => (
        <li key={product.id} className="p-2 bg-white shadow-md">
          <p className="text-gray-700">{product.name}</p>
        </li>
      ))}
    </ul>
          <div className="flex flex-col items-center gap-4 w-full">
  {/* Button */}
  <button 
    className="w-[40%] bg-yellow-600 text-white py-2 mt-4 text-sm font-[Georgia] font-semibold hover:bg-yellow-700"
    onClick={handleBid}
  >
    Place Bid
  </button>

  {/* Input */}
  <input 
    type="number" 
    className="w-[40%] border p-2 text-sm text-center"
    placeholder="Enter your bid"
    value={bidAmount}
    onChange={(e) => setBidAmount(e.target.value)}
  />
</div>
  </div>
)}
          

          
        </div>)}
    </div>
  );
}
