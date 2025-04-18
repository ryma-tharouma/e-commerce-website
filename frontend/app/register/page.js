"use client"
import { useState } from "react"
import axios from "axios"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { UserRound, Mail, Lock } from "lucide-react" // Importing the icons

const registerUser = async (userData) => {
  try {
    const response = await axios.post(
      `${process.env.NEXT_PUBLIC_API_URL}/users/register/`,
      userData
    )
    return response.data
  } catch (err) {
    throw new Error("Error registering user")
  }
}

export default function Register() {
  const [username, setUsername] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const userData = { username, email, password }
      const { access } = await registerUser(userData)
      localStorage.setItem("token", access)
      setSuccess(true)
      setError(null)
    } catch (err) {
      setError(err)
      setSuccess(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-12">
      <Card className="w-full max-w-xl p-10 space-y-6 shadow-lg">
        <h1 className="text-3xl text-center text-gray-800 font-[Georgia]">
          Create your Account
        </h1>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Username Input */}
          <div className="relative">
            <UserRound className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full pl-10 p-3 border border-gray-300 rounded-lg bg-white"
              required
            />
          </div>

          {/* Email Input */}
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full pl-10 p-3 border border-gray-300 rounded-lg bg-white"
              required
            />
          </div>

          {/* Password Input */}
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full pl-10 p-3 border border-gray-300 rounded-lg bg-white"
              required
            />
          </div>

          {/* Register Button */}
          <Button
            type="submit"
            className="w-full bg-[#D4AF37] hover:bg-[#B59030] text-white py-3 text-base"
          >
            Register
          </Button>
        </form>

        {/* Success and Error Messages */}
        {success && (
          <p className="text-green-600 text-center">
            Registration successful!
          </p>
        )}
        {error && (
          <p className="text-red-600 text-center">
            {error.message || "An error occurred"}
          </p>
        )}
      </Card>
    </div>
  )
}
