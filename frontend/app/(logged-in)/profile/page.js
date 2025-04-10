import { useEffect, useState } from "react";
import { getUserProfile } from "@/lib/api";

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
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-3xl font-semibold mb-4">Your Profile</h1>
      {profile ? (
        <div className="space-y-4">
          <p className="text-lg">Username: <span className="font-semibold">{profile.username}</span></p>
          <p className="text-lg">Email: <span className="font-semibold">{profile.email}</span></p>
          <p className="text-lg">Role: <span className="font-semibold">{profile.role}</span></p>
        </div>
      ) : (
        <p className="text-red-500">{error ? "Error fetching profile" : "Loading..."}</p>
      )}
    </div>
  );
}
