import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";

type TypewriterTextProps = {
  text: string;
  speed?: number;
  delay?: number;
  className?: string;
  style?: React.CSSProperties;
  cursor?: boolean;
};

export const TypewriterText: React.FC<TypewriterTextProps> = ({
  text,
  speed = 2,
  delay = 0,
  className,
  style,
  cursor = true,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const startFrame = delay * fps;
  const charsToShow = Math.min(
    Math.floor((frame - startFrame) / speed),
    text.length
  );

  const visibleText = text.slice(0, Math.max(0, charsToShow));
  const isComplete = charsToShow >= text.length;

  // 光标闪烁 (每15帧切换)
  const blinkPhase = Math.floor(frame / 15) % 2;

  return (
    <span className={className} style={style}>
      {visibleText}
      {cursor && !isComplete && (
        <span
          style={{
            display: "inline-block",
            width: 3,
            height: "1em",
            backgroundColor: "#22c55e",
            marginLeft: 2,
            verticalAlign: "text-bottom",
          }}
        />
      )}
      {cursor && isComplete && blinkPhase === 0 && (
        <span
          style={{
            display: "inline-block",
            width: 3,
            height: "1em",
            backgroundColor: "#22c55e",
            marginLeft: 2,
            verticalAlign: "text-bottom",
          }}
        />
      )}
    </span>
  );
};
