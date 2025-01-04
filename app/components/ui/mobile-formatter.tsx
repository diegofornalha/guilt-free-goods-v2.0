'use client';

import React, { useState, useEffect } from 'react';

interface MobileFormatterProps {
  title: string;
  description: string;
  maxTitleLength?: number;
  maxDescriptionLength?: number;
  className?: string;
}

export const MobileFormatter: React.FC<MobileFormatterProps> = ({
  title,
  description,
  maxTitleLength = 80,
  maxDescriptionLength = 300,
  className = '',
}) => {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth <= 768);
    };

    // Initial check
    checkMobile();

    // Add resize listener
    window.addEventListener('resize', checkMobile);

    // Cleanup
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const formatTitle = (title: string): string => {
    if (!isMobile) return title;
    return title.length > maxTitleLength
      ? `${title.substring(0, maxTitleLength - 3)}...`
      : title;
  };

  const formatDescription = (description: string): string => {
    if (!isMobile) return description;
    return description.length > maxDescriptionLength
      ? `${description.substring(0, maxDescriptionLength - 3)}...`
      : description;
  };

  return (
    <div className={`listing-content ${className}`}>
      <h2 className="listing-title text-lg md:text-xl font-semibold mb-2">
        {formatTitle(title)}
      </h2>
      <p className="listing-description text-sm md:text-base">
        {formatDescription(description)}
      </p>
    </div>
  );
};

export const formatListingForMobile = (
  title: string,
  description: string,
  maxTitleLength = 80,
  maxDescriptionLength = 300
): { title: string; description: string } => {
  return {
    title: title.length > maxTitleLength
      ? `${title.substring(0, maxTitleLength - 3)}...`
      : title,
    description: description.length > maxDescriptionLength
      ? `${description.substring(0, maxDescriptionLength - 3)}...`
      : description,
  };
};
