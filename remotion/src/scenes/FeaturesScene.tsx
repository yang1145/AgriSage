import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Audio,
  staticFile,
} from "remotion";

/*
  场景4：核心功能 — 从种到收六步
  41 ~ 68秒 (1230 ~ 2040帧)
  视觉：浅色背景，6 张步骤卡片像桌面上的卡片一样铺开。
*/

const STEPS = [
  {
    num: "01",
    action: "画地",
    desc: "地图上圈地块，自动算面积",
    example: "东岭地块 → 12.3亩 · 壤土",
    color: "#4a6fa5",
  },
  {
    num: "02",
    action: "定品种",
    desc: "从广西主推品种库中选",
    example: "桂糖44号 · 糖分 14.8%",
    color: "#3d7a3a",
  },
  {
    num: "03",
    action: "记农事",
    desc: "施肥/灌溉/防虫/采收逐笔记录",
    example: "03-15 尿素40kg/亩 → 东岭",
    color: "#b86d29",
  },
  {
    num: "04",
    action: "看天气",
    desc: "实时气象+灾害预警",
    example: "⚠ 明晨霜冻 · 建议覆盖薄膜",
    color: "#2d8a9c",
  },
  {
    num: "05",
    action: "传照片",
    desc: "按生长阶段分期上传影像",
    example: "萌芽期 · 东岭地块 · 3张",
    color: "#9c4b8c",
  },
  {
    num: "06",
    action: "出报告",
    desc: "Excel汇总 / PDF档案 / 一键备份",
    example: "2024春植季.pdf · 完整记录",
    color: "#6b5b95",
  },
];

const ROTATIONS = [-1.2, 0.8, -0.6, 1, -0.9, 0.5];

export const FeaturesScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleOpacity = interpolate(frame, [0, 0.7 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });
  const titleY = interpolate(frame, [0, 0.8 * fps], [24, 0], {
    extrapolateRight: "clamp",
  });

  const subtitleOpacity = interpolate(
    frame,
    [0.4 * fps, 1.2 * fps],
    [0, 1],
    { extrapolateRight: "clamp" }
  );

  const cards = STEPS.map((step, i) => {
    const row = Math.floor(i / 3);
    const col = i % 3;
    const delay = 1.0 + row * 0.5 + col * 0.3;

    const cardProgress = spring({
      frame: frame - delay * fps,
      fps,
      config: { damping: 16, stiffness: 80 },
    });

    const y = interpolate(cardProgress, [0, 1], [30, 0]);
    const opacity = interpolate(cardProgress, [0, 1], [0, 1]);

    return (
      <div
        key={i}
        style={{
          width: 580,
          padding: "32px 30px 28px",
          borderRadius: 2,
          backgroundColor: "#fffdf7",
          border: "1px solid #d9d4c9",
          boxShadow: "3px 3px 0 #d9d4c9",
          transform: `translateY(${y}px) rotate(${ROTATIONS[i]}deg)`,
          opacity,
          display: "flex",
          gap: 22,
          alignItems: "flex-start",
          position: "relative",
        }}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 10,
            flexShrink: 0,
          }}
        >
          <div
            style={{
              fontSize: 56,
              fontWeight: 900,
              color: step.color,
              fontVariantNumeric: "tabular-nums",
              lineHeight: 1,
            }}
          >
            {step.num}
          </div>
        </div>

        <div style={{ flex: 1, minWidth: 0 }}>
          <div
            style={{
              fontSize: 38,
              fontWeight: 900,
              color: "#1c1917",
              marginBottom: 8,
            }}
          >
            {step.action}
          </div>

          <div
            style={{
              fontSize: 23,
              color: "#5c564a",
              lineHeight: 1.65,
              marginBottom: 14,
            }}
          >
            {step.desc}
          </div>

          <div
            style={{
              fontSize: 18,
              color: step.color,
              fontFamily: "'Courier New', monospace",
              padding: "7px 16px",
              borderRadius: 2,
              backgroundColor: "#f4f1ea",
              border: "1px solid #d9d4c9",
              display: "inline-block",
              fontWeight: 800,
            }}
          >
            {step.example}
          </div>
        </div>
      </div>
    );
  });

  const bottomOpacity = interpolate(
    frame,
    [6.5 * fps, 7.5 * fps],
    [0, 1],
    { extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#f4f1ea",
        fontFamily: "'Noto Sans SC', sans-serif",
      }}
    >
      <div
        style={{
          position: "absolute",
          inset: 0,
          opacity: 0.25,
          backgroundImage:
            "url(\"data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E\")",
        }}
      />

      <AbsoluteFill
        style={{
          display: "flex",
          flexDirection: "column",
          padding: "52px 80px 44px",
        }}
      >
        <div
          style={{
            textAlign: "center",
            marginBottom: 36,
            transform: `translateY(${titleY}px)`,
            opacity: titleOpacity,
          }}
        >
          <div
            style={{
              fontSize: 64,
              fontWeight: 900,
              color: "#1c1917",
              letterSpacing: 2,
            }}
          >
            从种到收，就{" "}
            <span style={{ color: "#2d5a27" }}>六步</span>
          </div>
          <div
            style={{
              fontSize: 26,
              color: "#5c564a",
              marginTop: 12,
              opacity: subtitleOpacity,
            }}
          >
            不复杂、不花哨，就是你平时干的事 —— 只不过现在有地方记了
          </div>
        </div>

        <div
          style={{
            flex: 1,
            display: "flex",
            flexDirection: "column",
            gap: 20,
            justifyContent: "center",
          }}
        >
          <div
            style={{
              display: "flex",
              gap: 22,
              justifyContent: "center",
            }}
          >
            {cards.slice(0, 3)}
          </div>
          <div
            style={{
              display: "flex",
              gap: 22,
              justifyContent: "center",
            }}
          >
            {cards.slice(3, 6)}
          </div>
        </div>

        <div
          style={{
            textAlign: "center",
            paddingTop: 22,
            opacity: bottomOpacity,
          }}
        >
          <div
            style={{
              fontSize: 24,
              color: "#8c7f6b",
            }}
          >
            全程离线可用 · 数据不出村 · SQLite 本地存储
          </div>
        </div>
      </AbsoluteFill>
      <Audio src={staticFile("[女主播]从种到收就 六步-1782190085977.mp3")} />
    </AbsoluteFill>
  );
};
