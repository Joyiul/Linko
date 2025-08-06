import React from 'react';

const LinkoLogo = ({ height = '40px' }) => {
  return (
    <svg 
      width="160" 
      height="64" 
      viewBox="0 0 160 64" 
      style={{ height: height, width: 'auto' }}
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Handwritten "Linko" text - matching your exact image */}
      <g>
        {/* L - elegant handwritten style with curved bottom */}
        <path 
          d="M8 12 L8 45 Q8 48 12 48 L22 48" 
          stroke="#666666" 
          strokeWidth="4" 
          fill="none" 
          strokeLinecap="round" 
          strokeLinejoin="round"
        />
        
        {/* i with beautiful decorative swirl */}
        <circle cx="32" cy="15" r="2" fill="#666666"/>
        <path 
          d="M32 22 L32 48" 
          stroke="#666666" 
          strokeWidth="4" 
          strokeLinecap="round"
        />
        {/* Elegant green swirl above the i - matching your design */}
        <path 
          d="M25 10 Q28 6 32 10 Q36 14 42 10 Q46 6 50 10" 
          stroke="#A8D8A8" 
          strokeWidth="3" 
          fill="none" 
          strokeLinecap="round"
        />
        
        {/* n - flowing handwritten style */}
        <path 
          d="M45 48 L45 32 Q45 22 55 22 Q65 22 65 32 L65 48" 
          stroke="#666666" 
          strokeWidth="4" 
          fill="none" 
          strokeLinecap="round" 
          strokeLinejoin="round"
        />
        
        {/* k - elegant with flowing strokes */}
        <path 
          d="M75 12 L75 48 M75 32 Q85 22 95 22 M75 32 Q85 42 95 48" 
          stroke="#666666" 
          strokeWidth="4" 
          strokeLinecap="round" 
          strokeLinejoin="round"
        />
        
        {/* o - the adorable earth globe - exactly matching your image */}
        <g transform="translate(105, 22)">
          {/* Earth oval shape - tilted like in your image */}
          <ellipse 
            cx="22" 
            cy="22" 
            rx="20" 
            ry="18" 
            fill="#87CEEB" 
            stroke="#666666" 
            strokeWidth="4"
            transform="rotate(-8 22 22)"
          />
          
          {/* Green landmasses - organic continent shapes exactly like your design */}
          {/* Left continent - larger irregular shape */}
          <path 
            d="M8 16 Q14 12 18 16 Q20 20 18 25 Q16 28 12 27 Q8 25 6 21 Q6 18 8 16" 
            fill="#A8D8A8"
            transform="rotate(-8 22 22)"
          />
          
          {/* Right continent - flowing organic shape */}
          <path 
            d="M28 14 Q34 12 38 16 Q40 20 38 24 Q36 28 32 27 Q28 25 26 21 Q26 17 28 14" 
            fill="#A8D8A8"
            transform="rotate(-8 22 22)"
          />
          
          {/* Bottom landmass - smaller curved shape */}
          <path 
            d="M16 28 Q22 26 28 28 Q32 32 28 36 Q24 38 18 37 Q14 34 14 31 Q14 29 16 28" 
            fill="#A8D8A8"
            transform="rotate(-8 22 22)"
          />
          
          {/* Adorable face - exactly like your image */}
          {/* Eyes - perfectly positioned */}
          <circle cx="17" cy="19" r="1.5" fill="#333333"/>
          <circle cx="27" cy="19" r="1.5" fill="#333333"/>
          
          {/* Sweet heart smile - exactly like your design */}
          <text x="22" y="28" textAnchor="middle" fontSize="6" fill="#333333">♡</text>
        </g>
      </g>
    </svg>
  );
};

export default LinkoLogo;
