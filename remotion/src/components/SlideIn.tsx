import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";

type SlideInProps = {
  children: React.ReactNode;
  direction?: "left" | "right" | "top" | "bottom";
  duration?: number;
  delay?: number;
};

export const SlideIn: React.FC<SlideInProps> = ({
  children,
  direction = "left",
  duration = 0.8,
  delay = 0,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const startFrame = delay * fps;
  const progress = spring({
    frame: frame - startFrame,
    fps,
    config: { damping: 15, stiffness: 100 },
  });

  const distance = 80;
  let transform = "";

  switch (direction) {
    case "left":
      transform = `translateX(${interpolate(progress, [0, 1], [-distance, 0])}px)`;
      break;
    case "right":
      transform = `translateX(${interpolate(progress, [0, 1], [distance, 0])}px)`;
      break;
    case "top":
      transform = `translateY(${interpolate(progress, [0, 1], [-distance, 0])}px)`;
      break;
    case "bottom":
      transform = `translateY(${interpolate(progress, [0, 1], [distance, 0])}px)`;
      break;
  }

  const opacity = interpolate(progress, [0, 1], [0, 1]);

  return (
    <div style={{ transform, opacity }}>
      {children}
    </div>
  );
};
