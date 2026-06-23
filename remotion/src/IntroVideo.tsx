import React from "react";
import {
  AbsoluteFill,
  Series,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
} from "remotion";
import { OpeningScene } from "./scenes/OpeningScene";
import { PainPointScene } from "./scenes/PainPointScene";
import { SolutionScene } from "./scenes/SolutionScene";
import { FeaturesScene } from "./scenes/FeaturesScene";
import { TechScene } from "./scenes/TechScene";
import { OutroScene } from "./scenes/OutroScene";

/*
  桂收·甘蔗专用版 项目介绍动画
  总时长: 103秒 @ 30fps = 3090帧 (匹配配音音频)
*/

// 每个场景切换时淡入，配合统一的深色背景，消除硬切感
const FadeIn: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const opacity = interpolate(frame, [0, 0.4 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });

  return <div style={{ width: "100%", height: "100%", opacity }}>{children}</div>;
};

export const IntroVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#0c1510" }}>
      <Series>
        <Series.Sequence durationInFrames={360}>
          <FadeIn>
            <OpeningScene />
          </FadeIn>
        </Series.Sequence>

        <Series.Sequence durationInFrames={360}>
          <FadeIn>
            <PainPointScene />
          </FadeIn>
        </Series.Sequence>

        <Series.Sequence durationInFrames={510}>
          <FadeIn>
            <SolutionScene />
          </FadeIn>
        </Series.Sequence>

        <Series.Sequence durationInFrames={810}>
          <FadeIn>
            <FeaturesScene />
          </FadeIn>
        </Series.Sequence>

        <Series.Sequence durationInFrames={600}>
          <FadeIn>
            <TechScene />
          </FadeIn>
        </Series.Sequence>

        <Series.Sequence durationInFrames={450}>
          <FadeIn>
            <OutroScene />
          </FadeIn>
        </Series.Sequence>
      </Series>
    </AbsoluteFill>
  );
};
