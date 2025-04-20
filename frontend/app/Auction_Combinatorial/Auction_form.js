"use client";
import { useState, useEffect  } from "react";
import Image from "next/image";

export default function CreateAuction() {
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    starting_price: "",
    start_time: "",
    end_time: "",
    products: [],
  });
  
  const [images, setImages] = useState([]);
  const [error, setError] = useState("");
  const [products, setProducts] = useState([]); // Products from backend
  const [selectedProducts, setSelectedProducts] = useState([]); // Chosen products
  const [showModal, setShowModal] = useState(false); // Modal visibility


  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  useEffect(() => {
    fetch("http://127.0.0.1:8000/Auction_Combinatoire/get_products")
      .then((res) => res.json())
      .then((data) => setProducts(data))
      .catch((err) => console.error("Error fetching products:", err));
  }, []);


  const toggleProductSelection = (productId) => {
    setSelectedProducts((prevSelected) =>
      prevSelected.includes(productId)
        ? prevSelected.filter((id) => id !== productId) // Remove if already selected
        : [...prevSelected, productId] // Add if not selected
    );
  };



  const handleSubmit = async (e) => {
    e.preventDefault();
    if (selectedProducts.length === 0) {
      setError("Please select at least one product.");
      return;
    }
    
    const form = new FormData();
    Object.entries(formData).forEach(([key, value]) => form.append(key, value));
    form.append("products", JSON.stringify(selectedProducts));

    try {
      const response = await fetch("http://127.0.0.1:8000/Auction_Combinatoire/auctions/create_auction", {
        method: "POST",
        body: form,
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error);
      }

      alert("Auction created successfully!");
    } catch (error) {
      setError(error.message);
      alert(error.message);

    }
  };

  return (
    <div className="min-h-screen p-5 bg-gray-100">
    <div className="max-w-2xl mx-auto p-8 bg-white shadow-lg ">
      {/* Title */}
      <h2 className="text-3xl font-[Georgia] text-center mb-2">Create an Auction</h2>
      <div className="w-70 h-0.5 bg-yellow-500 mx-auto mb-6"></div>

      {error && <p className="text-red-500 text-center">{error}</p>}

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        <label className="block text-gray-700 text-sm font-[Georgia] ">Title</label>
          <input type="text" name="title" placeholder="Title*" required className="border w-full p-3 text-sm" onChange={handleChange} />
        
        <textarea name="description" placeholder="Description*" required className="border w-full p-3 text-sm" onChange={handleChange}></textarea>
        
        <label className="block text-gray-700 text-sm font-[Georgia] ">Starting Time</label>
        <input type="datetime-local" name="start_time" required className="border w-full p-3 text-sm" onChange={handleChange} />

        <label className="block text-gray-700 text-sm font-[Georgia] ">Ending Time</label>
        <input type="datetime-local" name="end_time" required className="border w-full p-3 text-sm" onChange={handleChange} />


        {/* Checkboxes */}
        {/* <div className="flex space-x-4">
          <label className="flex items-center space-x-2">
            <input type="checkbox" className="w-4 h-4" />
            <span className="text-sm">Feature this auction</span>
          </label>
          <label className="flex items-center space-x-2">
            <input type="checkbox" className="w-4 h-4" />
            <span className="text-sm">Enable auto-extension</span>
          </label>
        </div> */}

{/* Select Products Button */}
<button button type="button"  onClick={() => setShowModal(true)} className="bg-gray-100 border border-yellow-600 text-yellow-600 py-2 px-4 w-full">
          Select Products
        </button>


                {/* Floating Modal */}
                {showModal && (
                  <div className="fixed inset-0 flex items-center h-[100%] justify-center bg-[rgba(229,231,235,0.7)]">
                    <div className="bg-white p-6 w-[80%] max-w-5xl relative shadow-lg overflow-hidden">
                      
                      {/* Close Button */}
                      <button 
                        className="absolute top-4 right-4 text-gray-600 hover:text-black text-2xl"
                        onClick={() => setShowModal(false)}
                      >
                        &times;
                      </button>

                      {/* Title */}
                      <h3 className="text-lg font-semibold mb-4 text-center">Select Products</h3>

                      {/* Product Grid */}
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 overflow-y-auto px-2">
                        {products.map((product) => {
                          const defaultImg = `/imgs/Combinatorial_Auction/Products/${product.id}/image1.jpg`;
                          const isSelected = selectedProducts.includes(product.id);

                          return (
                            <div
                              key={product.id}
                              className={`relative block bg-gray-100 overflow-hidden cursor-pointer shadow-md ${isSelected ? "border-4 border-yellow-500" : ""}`}
                              onClick={() => toggleProductSelection(product.id)}
                            >
                              {/* Image Container */}
                              <div className="relative w-full h-40">
                                <Image
                                  src={defaultImg}
                                  alt="Product Image"
                                  fill
                                  objectFit="contain"
                                  className="object-cover"
                                />
                              </div>

                              {/* Product Info */}
                              <div className="p-3 bg-white text-center">
                                <p className="font-semibold text-gray-900">{product.name}</p>
                              </div>
                            </div>
                          );
                        })}
                      </div>

              <div className="py-2"></div>
              <button onClick={() => setShowModal(false)} className="bg-gray-100 border border-yellow-600 text-yellow-60 mt-4 w-full py-2">
                Close
              </button>
                    </div>
                  </div>

                )}


            {/* </div>
          </div> */}
        
        
        

        {/* Submit Button */}
        <button type="submit" className="bg-yellow-600 text-white py-3 w-full font-[Georgia] text-sm font-semibold hover:bg-yellow-700">
          SUBMIT
        </button>
      </form>
    </div>
    </div>
  );
}
