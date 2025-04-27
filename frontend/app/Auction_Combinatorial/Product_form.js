"use client";
import { useState } from "react";

export default function CreateProduct() {
  const [formData, setFormData] = useState({
    title: "",
    description: "",
  });
  const [images, setImages] = useState([]);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleImageChange = (e) => {
    setImages([...e.target.files]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const form = new FormData();
    form.append("title", formData.title);
    form.append("description", formData.description);
    images.forEach((image) => form.append("images", image));

    try {
      const response = await fetch("http://127.0.0.1:8000/Auction_Combinatoire/auctions/create_product", {
        method: "POST",
        body: form,
      });

      if (!response.ok) {
        throw new Error("Error creating product");
      }

      alert("Product created successfully!");
      window.location.reload();
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className="min-h-screen p-5 bg-gray-100">
    <div className="max-w-2xl mx-auto p-8 bg-white shadow-lg ">
      {/* Title */}
      <h2 className="text-3xl font-[Georgia] text-center mb-2">Create a Product</h2>
      <div className="w-70 h-0.5 bg-yellow-500 mx-auto mb-6"></div>

      {error && <p className="text-red-500 text-center">{error}</p>}

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        <label className="block text-gray-700 text-sm font-[Georgia] ">Title</label>
          <input type="text" name="title" placeholder="Title*" required className="border w-full p-3 text-sm" onChange={handleChange} />
          
          <label className="block text-gray-700 text-sm font-[Georgia] ">Description</label> 
        <textarea name="description" placeholder="Description*" required className="border w-full p-3 text-sm" onChange={handleChange}></textarea>
        
        {/* Image Upload */}
        <label className="block text-gray-700 text-sm font-[Georgia] font-semibold ">Upload Images</label>
        <input type="file" multiple accept="image/*" className="border w-full p-2" onChange={handleImageChange} />

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

        {/* Submit Button */}
        <button type="submit" className="bg-yellow-600 text-white py-3 w-full font-[Georgia] text-sm font-semibold hover:bg-yellow-700">
          SUBMIT
        </button>
      </form>
    </div>
    </div>
  );
}
