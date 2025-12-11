export default function Logo({ className = "", size = "default" }: { className?: string; size?: "small" | "default" | "large" }) {
  const sizes = {
    small: { width: 120, height: 32 },
    default: { width: 180, height: 48 },
    large: { width: 240, height: 64 },
  };

  const { width, height } = sizes[size];

  return (
    <svg
      width={width}
      height={height}
      viewBox="0 0 180 48"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* Icon - Abstract bandage/healing symbol */}
      <g>
        {/* Outer rounded rectangle (bandage shape) */}
        <rect
          x="4"
          y="12"
          width="40"
          height="24"
          rx="12"
          fill="#0066CC"
        />
        {/* Inner healing cross/plus */}
        <rect
          x="21"
          y="17"
          width="6"
          height="14"
          rx="2"
          fill="white"
        />
        <rect
          x="15"
          y="21"
          width="18"
          height="6"
          rx="2"
          fill="white"
        />
        {/* Connection dots */}
        <circle cx="10" cy="24" r="2" fill="white" opacity="0.6" />
        <circle cx="38" cy="24" r="2" fill="white" opacity="0.6" />
      </g>

      {/* Text - STITCHLESS */}
      <text
        x="52"
        y="32"
        fontFamily="system-ui, -apple-system, sans-serif"
        fontWeight="700"
        fontSize="20"
        fill="#1a1a1a"
      >
        STITCHLESS
      </text>

      {/* Trademark symbol */}
      <text
        x="168"
        y="22"
        fontFamily="system-ui, -apple-system, sans-serif"
        fontWeight="500"
        fontSize="8"
        fill="#666666"
      >
        ™
      </text>
    </svg>
  );
}
