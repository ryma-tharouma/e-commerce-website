"use client";

import { useState } from "react";
import Image from "next/image";

const HoverImage = ({ defaultSrc, hoverSrc }) => {
  const [hovered, setHovered] = useState(false);

  return (
    <div
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      className="relative w-full h-48 bg-gray-100 flex items-center justify-center"
    >
      {defaultSrc && (
        <Image
          src={hovered ? hoverSrc : defaultSrc}
          alt="Product Image"
          fill
          className="object-contain p-2"
        />
      )}
    </div>
  );
};

export default HoverImage;
