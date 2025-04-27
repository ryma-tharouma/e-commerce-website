"use client";

import { useState } from "react";
import Image from "next/image";

const HoverImage = ({ defaultSrc, hoverSrc, className = "" }) => {
  const [hovered, setHovered] = useState(false);

  return (
    <div
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      className={`relative w-full h-full ${className}`}
    >
      {defaultSrc && (
        <Image
          src={hovered ? hoverSrc : defaultSrc}
          alt="Product Image"
          fill
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          className="object-cover transition-transform duration-300 hover:scale-105"
          priority
        />
      )}
    </div>
  );
};

export default HoverImage;
