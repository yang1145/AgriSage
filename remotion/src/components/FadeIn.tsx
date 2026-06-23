import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";

type FadeInProps = {
  children: React.ReactNode;
  duration?: number;
  delay?: number;
  direction?: "in" | "out" | "in-out";
};

export const FadeIn: React.FC<FadeInProps> = ({
  children,
  duration = 0.8,
  delay = 0,
  direction = "in",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const startFrame = delay * fps;
  const durFrames = duration * fps;

  let opacity: number;
  if (direction === "in") {
    opacity = interpolate(frame, [startFrame, startFrame + durFrames], [0, 1], {
      extrapolateRight: "clamp",
      extrapolateLeft: "clamp",
    });
  } else if (direction === "out") {
    opacity = interpolate(
      frame,
      [startFrame, startFrame + durFrames],
      [1, 0],
      { extrapolateRight: "clamp", extrapolateLeft: "clamp" }
    );
  } else {
    const half = durFrames / 2;
    opacity = interpolate(
      frame,
      [startFrame, startFrame + half, startFrame + durFrames],
      [0, 1, 0],
      { extrapolateRight: "clamp", extrapolateLeft: "clamp" }
    );
  }

  return <div style={{ opacity }}>{children}</div>;
};
