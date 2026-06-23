import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";

type FeatureCardProps = {
  icon: React.ReactNode;
  title: string;
  description: string;
  color: string;
  index: number;
  cardWidth?: number;
  cardHeight?: number;
};

export const FeatureCard: React.FC<FeatureCardProps> = ({
  icon,
  title,
  description,
  color,
  index,
  cardWidth = 280,
  cardHeight = 220,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const delay = index * 0.25;

  const scaleProgress = spring({
    frame: frame - delay * fps,
    fps,
    config: { damping: 12, stiffness: 80 },
  });

  const yProgress = spring({
    frame: frame - delay * fps,
    fps,
    config: { damping: 20, stiffness: 60 },
  });

  const scale = interpolate(scaleProgress, [0, 1], [0.6, 1]);
  const translateY = interpolate(yProgress, [0, 1], [60, 0]);
  const opacity = interpolate(scaleProgress, [0, 1], [0, 1]);

  return (
    <div
      style={{
        width: cardWidth,
        height: cardHeight,
        backgroundColor: "rgba(15, 23, 42, 0.85)",
        borderRadius: 16,
        border: `1.5px solid ${color}33`,
        padding: 24,
        display: "flex",
        flexDirection: "column",
        gap: 12,
        transform: `scale(${scale}) translateY(${translateY}px)`,
        opacity,
        backdropFilter: "blur(10px)",
        boxShadow: `0 8px 32px ${color}15`,
      }}
    >
      <div
        style={{
          width: 48,
          height: 48,
          borderRadius: 12,
          backgroundColor: `${color}18`,
          border: `1.5px solid ${color}40`,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: color,
          fontSize: 24,
          flexShrink: 0,
        }}
      >
        {icon}
      </div>

      <div
        style={{
          fontSize: 20,
          fontWeight: 700,
          color: "#f1f5f9",
          lineHeight: 1.3,
        }}
      >
        {title}
      </div>

      <div
        style={{
          fontSize: 14,
          color: "#94a3b8",
          lineHeight: 1.6,
          flex: 1,
        }}
      >
        {description}
      </div>

      <div
        style={{
          height: 3,
          width: interpolate(scaleProgress, [0, 1], [0, 60]),
          borderRadius: 2,
          backgroundColor: color,
          marginTop: "auto",
        }}
      />
    </div>
  );
};
