"use client"
import { useState } from "react"
import {useRouter} from "next/navigation"
import axios from "axios"
import { Card } from "/components/ui/card"
import { Button } from "/components/ui/button"
import { Lock, UserRound } from "lucide-react"


const loginUser = async (credentials) => {
  try {
    const response = await axios.post(
      `${process.env.NEXT_PUBLIC_API_URL}/users/login/`,
      credentials
    )
    return response.data
  } catch (err) {
    throw new Error("Invalid credentials")
  }
}

export default function Login() {
  const router = useRouter();
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
    

      const credentials = { username, password }
      const { access } = await loginUser(credentials)
      localStorage.setItem("token", access)
      setSuccess(true)
      
      setError(null)
      router.push('/')
    } catch (err) {
      setError(err)
      setSuccess(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-12">
      <Card className="w-full max-w-xl p-10 space-y-6 shadow-lg">

        <h1 className="text-3xl  text-center text-gray-800 font-[Georgia] ">
          Login to your Account
        </h1>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="flex items-center border border-gray-300 rounded-lg p-3 bg-white">
            <UserRound className="text-gray-400 w-5 h-5 mr-3" />
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full outline-none bg-transparent"
              required
            />
          </div>
          <div className="flex items-center border border-gray-300 rounded-lg p-3 bg-white">
            <Lock className="text-gray-400 w-5 h-5 mr-3" />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full outline-none bg-transparent"
              required
            />
          </div>
          <Button
            type="submit"
            className="w-full bg-[#D4AF37] hover:bg-[#B59030] text-white py-3 text-base"
          >
            Login
          </Button>
        </form>

        {success && (
          <p className="text-green-600 text-center">Login successful!</p>
        )}
        {error && (
          <p className="text-red-600 text-center">
            {error.message || "Login failed"}
          </p>
        )}
              <div className="text-center text-sm text-gray-600">
        Don't have an account?{" "}
  <span
    className="text-[#D4AF37] cursor-pointer hover:underline"
    onClick={() => router.push('/register')}
  >
    Register now!
  </span>
</div>
      </Card>

    </div>
  )
}
