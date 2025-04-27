"use client"
import { useEffect, useState } from "react";
import axios from "axios";
import { Card } from "/components/ui/card";
import { Separator } from "/components/ui/separator";
import { Button } from "/components/ui/button";
import { UserRound, Mail, Shield, Edit, Settings } from "lucide-react";

const getUserProfile = async (token) => {
  try {
    const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/users/profile/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (err) {
    console.log("err ::: ", err);
    throw new Error("Error fetching profile");
  }
};

export default function Profile() {
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      getUserProfile(token)
        .then((data) => setProfile(data))
        .catch((err) => setError(err));
    }
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto p-6 space-y-8">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-[Georgia] text-gray-800">My Account</h1>
          <Button variant="outline" className="hover:text-[#D4AF37] hover:border-[#D4AF37]">
            <Settings className="w-4 h-4 mr-2 " />
            Account Settings
          </Button>
        </div>

        {profile ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Profile Overview Card */}
            <Card className="col-span-1 p-6 space-y-6">
              <div className="flex justify-center">
                <div className="w-32 h-32 rounded-full bg-gray-200 flex items-center justify-center">
                  <UserRound className="w-16 h-16 text-gray-400" />
                </div>
              </div>
              <div className="text-center">
                <h2 className="text-xl font-semibold text-gray-800">{profile.username}</h2>
                <p className="text-sm text-gray-500">{profile.role}</p>
              </div>
              <Button className="w-full bg-[#D4AF37] hover:bg-[#B59030] text-white">
                <Edit className="w-4 h-4 mr-2" />
                Edit Profile
              </Button>
            </Card>

            {/* Profile Details Card */}
            <Card className="col-span-1 md:col-span-2 p-6">
              <h2 className="text-xl font-[Georgia] text-gray-800 mb-6">Profile Details</h2>
              <div className="space-y-4">
                <div className="flex items-center space-x-4 p-3 hover:bg-gray-50 rounded-lg transition-colors">
                  <UserRound className="w-5 h-5 text-[#D4AF37]" />
                  <div>
                    <p className="text-sm text-gray-500">Username</p>
                    <p className="font-medium">{profile.username}</p>
                  </div>
                </div>
                
                <Separator />
                
                <div className="flex items-center space-x-4 p-3 hover:bg-gray-50 rounded-lg transition-colors">
                  <Mail className="w-5 h-5 text-[#D4AF37]" />
                  <div>
                    <p className="text-sm text-gray-500">Email</p>
                    <p className="font-medium">{profile.email}</p>
                  </div>
                </div>
                
                <Separator />
                
                <div className="flex items-center space-x-4 p-3 hover:bg-gray-50 rounded-lg transition-colors">
                  <Shield className="w-5 h-5 text-[#D4AF37]" />
                  <div>
                    <p className="text-sm text-gray-500">Role</p>
                    <p className="font-medium">{profile.role}</p>
                  </div>
                </div>
              </div>
            </Card>

            {/* Quick Actions Card */}
            <Card className="col-span-1 md:col-span-3 p-6">
              <h2 className="text-xl font-[Georgia] text-gray-800 mb-6">Quick Actions</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Button variant="outline" className="justify-start hover:text-[#D4AF37] hover:border-[#D4AF37]">
                  View My Bids
                </Button>
                <Button variant="outline" className="justify-start hover:text-[#D4AF37] hover:border-[#D4AF37]">
                  Wishlist
                </Button>
                <Button variant="outline" className="justify-start hover:text-[#D4AF37] hover:border-[#D4AF37]">
                  Purchase History
                </Button>
              </div>
            </Card>
          </div>
        ) : (
          <Card className="p-6">
            <div className="text-center">
              {error ? (
                <p className="text-red-500">Error fetching profile data. Please try again later.</p>
              ) : (
                <div className="flex justify-center items-center space-x-2">
                  <div className="w-6 h-6 border-2 border-[#D4AF37] border-t-transparent rounded-full animate-spin"></div>
                  <p className="text-gray-500">Loading your profile...</p>
                </div>
              )}
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}