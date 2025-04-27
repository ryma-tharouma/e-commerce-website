'use client';

import Header from "../../components/Header";
import Footer from "../../components/Footer";

export default function AboutPage() {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-grow">
        <div className="max-w-4xl mx-auto px-4 py-12">
          <h1 className="text-4xl font-bold text-center mb-8 font-[Georgia] text-[#D4AF37]">
            About Us
          </h1>
          
          <div className="space-y-8">
            <section className="bg-white p-8 rounded-lg shadow-sm">
              <h2 className="text-2xl font-semibold mb-4 font-[Georgia] text-gray-800">Our Story</h2>
              <p className="text-gray-600 leading-relaxed font-[Georgia]">
                Founded with a passion for bringing unique and high-quality products to discerning customers, 
                our e-commerce platform has grown into a trusted destination for those seeking exceptional items. 
                We pride ourselves on curating a collection that combines timeless elegance with modern functionality.
              </p>
            </section>

            <section className="bg-white p-8 rounded-lg shadow-sm">
              <h2 className="text-2xl font-semibold mb-4 font-[Georgia] text-gray-800">Our Mission</h2>
              <p className="text-gray-600 leading-relaxed font-[Georgia]">
                Our mission is to provide an exceptional shopping experience by offering carefully selected products 
                that meet the highest standards of quality and craftsmanship. We are committed to customer satisfaction 
                and strive to build lasting relationships with our clients through transparency, reliability, and 
                outstanding service.
              </p>
            </section>

            <section className="bg-white p-8 rounded-lg shadow-sm">
              <h2 className="text-2xl font-semibold mb-4 font-[Georgia] text-gray-800">Our Values</h2>
              <ul className="list-disc list-inside space-y-2 text-gray-600 font-[Georgia]">
                <li>Quality: We source only the finest products from trusted suppliers</li>
                <li>Customer Service: Your satisfaction is our top priority</li>
                <li>Integrity: We conduct business with honesty and transparency</li>
                <li>Innovation: We continuously seek to improve and enhance your shopping experience</li>
              </ul>
            </section>

            <section className="bg-white p-8 rounded-lg shadow-sm">
              <h2 className="text-2xl font-semibold mb-4 font-[Georgia] text-gray-800">Contact Us</h2>
              <div className="space-y-4 text-gray-600 font-[Georgia]">
                <p>Email: info@example.com</p>
                <p>Phone: (123) 456-7890</p>
                <p>Address: 123 Commerce Street, Business City, BC 12345</p>
              </div>
            </section>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
} 