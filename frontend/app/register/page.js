"use client"
import { useState } from "react";
import { registerUser } from "@/lib/api";

export default function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const userData = { username, email, password };
      await registerUser(userData);
      setSuccess(true);
      setError(null);
    } catch (err) {
      setError(err);
      setSuccess(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-6">
      <h1 className="text-3xl font-semibold mb-4">Register</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full p-3 border border-gray-300 rounded"
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full p-3 border border-gray-300 rounded"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-3 border border-gray-300 rounded"
        />
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-3 rounded hover:bg-blue-600"
        >
          Register
        </button>
      </form>

      {success && <p className="text-green-500 mt-4">Registration successful!</p>}
      {error && <p className="text-red-500 mt-4">{error}</p>}
    </div>
  );
}
