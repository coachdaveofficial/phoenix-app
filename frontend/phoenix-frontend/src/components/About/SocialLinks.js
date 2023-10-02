import React from 'react';

export default function SocialLinks() {
  return (
    <div className="flex space-x-4">
      <a
        href="https://www.facebook.com/Phoenixfc.pdx"
        target="_blank"
        rel="noopener noreferrer"
        className="text-blue-600 hover:underline"
      >
        Facebook
      </a>
      <a
        href="https://www.instagram.com/phoenix_fc_pdx/"
        target="_blank"
        rel="noopener noreferrer"
        className="text-purple-600 hover:underline"
      >
        Instagram
      </a>
      <a
        href="https://www.youtube.com/channel/UC4RkQ33coMZkmtCWtGLVJlA"
        target="_blank"
        rel="noopener noreferrer"
        className="text-red-600 hover:underline"
      >
        YouTube
      </a>
      <a
        href="http://gpsdsoccer.com/"
        target="_blank"
        rel="noopener noreferrer"
        className="text-green-600 hover:underline"
      >
        League Website
      </a>
    </div>
  );
};


