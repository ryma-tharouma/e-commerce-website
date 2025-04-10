"use client"
import { useEffect, useState } from "react";
import Link from "next/link";

export default function NavBar() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  return (
    <nav className="bg-gray-800 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link href="/" className="text-2xl font-semibold hover:text-gray-300">Home</Link>
        <div className="space-x-4">
          {isAuthenticated ? (
            <>
              <Link href="/profile" className="hover:text-gray-300">Profile</Link>
              <button
                className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
                onClick={() => localStorage.removeItem("token")}
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link href="/login" className="hover:text-gray-300">Login</Link>
              <Link href="/register" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
