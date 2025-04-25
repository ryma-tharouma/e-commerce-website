export default function Footer() {
    return (
      <footer className="bg-white shadow-md py-6 text-gray-700">
        <div className="container mx-auto grid grid-cols-2 md:grid-cols-4 gap-6 px-6 text-sm">
          <div>
            <h3 className="font-semibold">Shop</h3>
            <ul>
              <li className="hover:text-[#D4AF37] cursor-pointer">Recent Acquisitions</li>
              <li className="hover:text-[#D4AF37] cursor-pointer">Antiques</li>
              <li className="hover:text-[#D4AF37] cursor-pointer">Jewelry</li>
              <li className="hover:text-[#D4AF37] cursor-pointer">Fine Art</li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold">Can We Help?</h3>
            <ul>
              <li className="hover:text-[#D4AF37] cursor-pointer">Customer Care</li>
              <li className="hover:text-[#D4AF37] cursor-pointer">FAQs</li>
              <li className="hover:text-[#D4AF37] cursor-pointer">Design Services</li>
              <li className="hover:text-[#D4AF37] cursor-pointer">Contact Us</li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold">Our Company</h3>
            <ul>
              <li className="hover:text-[#D4AF37] cursor-pointer">Buy with Confidence</li>
              <li className="hover:text-[#D4AF37] cursor-pointer">Events</li>
              <li className="hover:text-[#D4AF37] cursor-pointer">Sell to Us</li>
              <li className="hover:text-[#D4AF37] cursor-pointer">Careers</li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold">Get The Latest</h3>
            <input
              type="email"
              placeholder="Email Address"
              className="border p-1 w-full rounded hover:border-[#D4AF37]"
            />
            <button className="mt-2 px-4 py-1 bg-gray-900 text-white rounded hover:bg-[#D4AF37] w-full cursor-pointer">
              Join
            </button>
          </div>
        </div>
        <div className="text-center text-xs mt-6">
          © 2025 FNRK | Privacy | Site Map
        </div>
      </footer>
    );
  }
  