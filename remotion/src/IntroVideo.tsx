import React from "react";
import { AbsoluteFill } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { wipe } from "@remotion/transitions/wipe";
import { OpeningScene } from "./scenes/OpeningScene";
import { PainPointScene } from "./scenes/PainPointScene";
import { SolutionScene } from "./scenes/SolutionScene";
import { FeaturesScene } from "./scenes/FeaturesScene";
import { TechScene } from "./scenes/TechScene";
import { OutroScene } from "./scenes/OutroScene";

/*
  桂收·甘蔗专用版 项目介绍动画
  总时长: 115.5秒 @ 30fps = 3465帧
  每个场景在原配音时长的基础上额外延长了 2~2.5 秒，
  作为转场前的静音缓冲区，避免相邻场景配音重叠。
*/

export const IntroVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#f4f1ea" }}>
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={420}>
          <OpeningScene />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          timing={linearTiming({ durationInFrames: 30 })}
          presentation={fade()}
        />

        <TransitionSeries.Sequence durationInFrames={420}>
          <PainPointScene />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          timing={linearTiming({ durationInFrames: 30 })}
          presentation={wipe({ direction: "from-left" })}
        />

        <TransitionSeries.Sequence durationInFrames={570}>
          <SolutionScene />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          timing={linearTiming({ durationInFrames: 30 })}
          presentation={fade()}
        />

        <TransitionSeries.Sequence durationInFrames={870}>
          <FeaturesScene />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          timing={linearTiming({ durationInFrames: 30 })}
          presentation={wipe({ direction: "from-right" })}
        />

        <TransitionSeries.Sequence durationInFrames={675}>
          <TechScene />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          timing={linearTiming({ durationInFrames: 45 })}
          presentation={fade()}
        />

        <TransitionSeries.Sequence durationInFrames={510}>
          <OutroScene />
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </AbsoluteFill>
  );
};
