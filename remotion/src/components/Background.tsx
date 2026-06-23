import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";

type BackgroundProps = {
  variant?: "dark" | "gradient-green" | "gradient-blue" | "grid";
};

export const Background: React.FC<BackgroundProps> = ({ variant = "dark" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const bgStyle: Record<string, React.CSSProperties> = {
    dark: { backgroundColor: "#0a0f1a" },
    "gradient-green": {
      background: `
        radial-gradient(ellipse at 20% 50%, rgba(34,197,94,0.12) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 50%, rgba(16,185,129,0.08) 0%, transparent 60%),
        linear-gradient(180deg, #0a0f1a 0%, #0c1825 50%, #0a1520 100%)
      `,
    },
    "gradient-blue": {
      background: `
        radial-gradient(ellipse at 50% 0%, rgba(59,130,246,0.10) 0%, transparent 50%),
        linear-gradient(180deg, #0a0f1a 0%, #0f172a 100%)
      `,
    },
    grid: {
      background: `
        linear-gradient(rgba(34,197,94,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(34,197,94,0.03) 1px, transparent 1px),
        linear-gradient(180deg, #0a0f1a 0%, #0c1220 100%)
      `,
      backgroundSize: "60px 60px, 60px 60px, 100% 100%",
    },
  };

  const offset = interpolate(frame, [0, 10 * fps], [0, 60], {
    extrapolateRight: "extend",
  });

  return (
    <AbsoluteFill
      style={{
        ...bgStyle[variant],
        backgroundPosition: variant === "grid"
          ? `${offset}px ${offset}px, ${offset}px ${offset}px, center`
          : undefined,
      }}
    />
  );
};
