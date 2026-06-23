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
  27 ~ 42秒 (810 ~ 1260帧)
  视觉：深色背景，2×3 卡片网格，错落排列。
*/

const STEPS = [
  {
    num: "01",
    action: "画地",
    desc: "地图上圈地块，自动算面积",
    example: "东岭地块 → 12.3亩 · 壤土",
    color: "#3b82f6",
  },
  {
    num: "02",
    action: "定品种",
    desc: "从广西主推品种库中选",
    example: "桂糖44号 · 糖分 14.8%",
    color: "#22c55e",
  },
  {
    num: "03",
    action: "记农事",
    desc: "施肥/灌溉/防虫/采收逐笔记录",
    example: "03-15 尿素40kg/亩 → 东岭",
    color: "#f59e0b",
  },
  {
    num: "04",
    action: "看天气",
    desc: "实时气象+灾害预警",
    example: "⚠ 明晨霜冻 · 建议覆盖薄膜",
    color: "#06b6d4",
  },
  {
    num: "05",
    action: "传照片",
    desc: "按生长阶段分期上传影像",
    example: "萌芽期 · 东岭地块 · 3张",
    color: "#ec4899",
  },
  {
    num: "06",
    action: "出报告",
    desc: "Excel汇总 / PDF档案 / 一键备份",
    example: "2024春植季.pdf · 完整记录",
    color: "#8b5cf6",
  },
];

const CARD_OFFSETS = [
  { x: 0, y: 0 },
  { x: 6, y: -4 },
  { x: -3, y: 3 },
  { x: -4, y: 6 },
  { x: 3, y: 2 },
  { x: -2, y: -3 },
];

export const FeaturesScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleOpacity = interpolate(frame, [0, 0.7 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });
  const titleY = interpolate(frame, [0, 0.8 * fps], [20, 0], {
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

    const scale = interpolate(cardProgress, [0, 1], [0.88, 1]);
    const y = interpolate(cardProgress, [0, 1], [24, 0]);
    const opacity = interpolate(cardProgress, [0, 1], [0, 1]);
    const rotate = CARD_OFFSETS[i].y * 0.25;

    return (
      <div
        key={i}
        style={{
          width: 580,
          padding: "32px 30px 28px",
          borderRadius: 16,
          backgroundColor: "rgba(255,255,255,0.04)",
          border: `1.5px solid ${step.color}18`,
          transform: `translate(${CARD_OFFSETS[i].x}px, ${
            CARD_OFFSETS[i].y + y
          }px) scale(${scale}) rotate(${rotate}deg)`,
          opacity,
          display: "flex",
          gap: 22,
          alignItems: "flex-start",
        }}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 12,
            flexShrink: 0,
          }}
        >
          <div
            style={{
              fontSize: 52,
              fontWeight: 900,
              color: `${step.color}50`,
              fontVariantNumeric: "tabular-nums",
              lineHeight: 1,
            }}
          >
            {step.num}
          </div>
          <div
            style={{
              width: 56,
              height: 56,
              borderRadius: 12,
              backgroundColor: `${step.color}10`,
              border: `2px solid ${step.color}25`,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <div
              style={{
                width: 14,
                height: 14,
                borderRadius: "50%",
                backgroundColor: step.color,
              }}
            />
          </div>
        </div>

        <div style={{ flex: 1, minWidth: 0 }}>
          <div
            style={{
              fontSize: 36,
              fontWeight: 800,
              color: "#f0fdf4",
              marginBottom: 8,
            }}
          >
            {step.action}
          </div>

          <div
            style={{
              fontSize: 22,
              color: "#86a88e",
              lineHeight: 1.6,
              marginBottom: 14,
            }}
          >
            {step.desc}
          </div>

          <div
            style={{
              fontSize: 19,
              color: step.color,
              fontFamily: "'Courier New', monospace",
              padding: "7px 16px",
              borderRadius: 6,
              backgroundColor: `${step.color}08`,
              border: `1px solid ${step.color}12`,
              display: "inline-block",
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
        backgroundColor: "#0c1510",
        fontFamily: "'Noto Sans SC', sans-serif",
      }}
    >
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage:
            "radial-gradient(circle at 50% 50%, rgba(34,197,94,0.04) 0%, transparent 50%)",
        }}
      />

      <AbsoluteFill
        style={{
          display: "flex",
          flexDirection: "column",
          padding: "48px 80px 40px",
        }}
      >
        <div
          style={{
            textAlign: "center",
            marginBottom: 32,
            transform: `translateY(${titleY}px)`,
            opacity: titleOpacity,
          }}
        >
          <div
            style={{
              fontSize: 56,
              fontWeight: 900,
              color: "#f0fdf4",
              letterSpacing: 2,
            }}
          >
            从种到收，就{" "}
            <span style={{ color: "#22c55e" }}>六步</span>
          </div>
          <div
            style={{
              fontSize: 24,
              color: "#86a88e",
              marginTop: 10,
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
            gap: 18,
            justifyContent: "center",
          }}
        >
          <div
            style={{
              display: "flex",
              gap: 20,
              justifyContent: "center",
            }}
          >
            {cards.slice(0, 3)}
          </div>
          <div
            style={{
              display: "flex",
              gap: 20,
              justifyContent: "center",
            }}
          >
            {cards.slice(3, 6)}
          </div>
        </div>

        <div
          style={{
            textAlign: "center",
            paddingTop: 18,
            opacity: bottomOpacity,
          }}
        >
          <div
            style={{
              fontSize: 22,
              color: "#5c7c66",
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
