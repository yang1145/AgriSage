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
  场景6：结尾
  52 ~ 60秒 (1560 ~ 1800帧)
  视觉：深色背景，左侧干净记事本呼应开场，右侧品牌收尾。
*/

const CLEAN_LINES = [
  { text: "东岭地块 (12.3亩)", delay: 0, highlight: false },
  { text: "品种: 桂糖44号 · 新植蔗", delay: 0.6, highlight: false },
  { text: "03-15 施肥: 尿素 40kg/亩", delay: 1.2, highlight: false },
  { text: "03-12 灌溉: 沟灌 2小时", delay: 1.7, highlight: false },
  { text: "当前阶段: 分蘖期 · 第45天", delay: 2.3, highlight: true },
];

export const OutroScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const notebookProgress = spring({
    frame: frame - 0.3 * fps,
    fps,
    config: { damping: 18, stiffness: 60 },
  });
  const notebookY = interpolate(notebookProgress, [0, 1], [30, 0]);
  const notebookOpacity = interpolate(notebookProgress, [0, 1], [0, 1]);

  const brandOpacity = interpolate(
    frame,
    [3.2 * fps, 4.5 * fps],
    [0, 1],
    { extrapolateRight: "clamp" }
  );

  const endingOpacity = interpolate(
    frame,
    [4.8 * fps, 6 * fps],
    [0, 1],
    { extrapolateRight: "clamp" }
  );

  const footerOpacity = interpolate(
    frame,
    [6 * fps, 7 * fps],
    [0, 1],
    { extrapolateRight: "clamp" }
  );

  const lineWidth = interpolate(
    frame,
    [3.8 * fps, 5 * fps],
    [0, 140],
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
            "radial-gradient(circle at 70% 50%, rgba(34,197,94,0.06) 0%, transparent 45%)",
        }}
      />

      <AbsoluteFill
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 80,
          padding: 100,
        }}
      >
        {/* 左侧：干净的记事本 */}
        <div
          style={{
            transform: `translateY(${notebookY}px)`,
            opacity: notebookOpacity,
            backgroundColor: "#fffef9",
            borderRadius: 8,
            boxShadow: "0 12px 40px rgba(0,0,0,0.25)",
            padding: "40px 48px",
            width: 440,
            border: "1px solid rgba(0,0,0,0.05)",
            backgroundImage:
              "repeating-linear-gradient(transparent, transparent 35px, #e8e0d4 35px, #e8e0d4 36px)",
            flexShrink: 0,
          }}
        >
          <div
            style={{
              fontSize: 14,
              color: "#9ca3af",
              marginBottom: 18,
              paddingBottom: 10,
              borderBottom: "1px dashed #d1ccc0",
            }}
          >
            2024年3月 · 东岭地块档案
          </div>

          {CLEAN_LINES.map((line, i) => {
            const lineOpacity = interpolate(
              frame,
              [(1 + line.delay) * fps, (1.4 + line.delay) * fps],
              [0, 1],
              { extrapolateRight: "clamp", extrapolateLeft: "clamp" }
            );

            return (
              <div
                key={i}
                style={{
                  opacity: lineOpacity,
                  fontSize: line.highlight ? 20 : 18,
                  color: line.highlight ? "#16a34a" : "#374151",
                  fontFamily: "'Courier New', monospace",
                  lineHeight: 1.9,
                  fontWeight: line.highlight ? 700 : 400,
                }}
              >
                {line.text}
              </div>
            );
          })}

          <div
            style={{
              marginTop: 18,
              paddingTop: 12,
              borderTop: "1px dashed #bbf7d0",
              opacity: endingOpacity,
              display: "flex",
              alignItems: "center",
              gap: 8,
            }}
          >
            <span style={{ fontSize: 18, color: "#16a34a", fontWeight: 900 }}>✓</span>
            <span
              style={{
                fontSize: 15,
                color: "#16a34a",
                fontWeight: 600,
              }}
            >
              清清楚楚，明明白白
            </span>
          </div>
        </div>

        {/* 右侧：品牌与收尾 */}
        <div
          style={{
            opacity: brandOpacity,
            width: 420,
          }}
        >
          <div
            style={{
              fontSize: 60,
              fontWeight: 900,
              color: "#f0fdf4",
              letterSpacing: 6,
              marginBottom: 8,
            }}
          >
            桂收
          </div>

          <div
            style={{
              width: lineWidth,
              height: 3,
              borderRadius: 2,
              backgroundColor: "#22c55e",
              marginBottom: 20,
            }}
          />

          <div
            style={{
              fontSize: 20,
              color: "#22c55e",
              fontWeight: 700,
              letterSpacing: 3,
              marginBottom: 24,
            }}
          >
            AGRISAGE CANE
          </div>

          <div
            style={{
              fontSize: 17,
              color: "#86a88e",
              lineHeight: 1.9,
              opacity: endingOpacity,
            }}
          >
            种甘蔗这件事本身已经够忙了
            <br />
            记录的事情交给我们
            <br />
            <br />
            <span style={{ color: "#f0fdf4", fontWeight: 600 }}>
              离线、免费、数据在你自己手里
            </span>
          </div>
        </div>
      </AbsoluteFill>

      {/* 底部版权 */}
      <div
        style={{
          position: "absolute",
          bottom: 32,
          left: 0,
          right: 0,
          textAlign: "center",
          opacity: footerOpacity,
        }}
      >
        <div
          style={{
            fontSize: 13,
            color: "#5c7c66",
          }}
        >
          © 2024-2026 桂收·甘蔗专用版 AgriSage Cane · 本地离线 · 数据不出村
        </div>
      </div>
      <Audio src={staticFile("[女主播]东岭地块123亩-1782190099891.mp3")} />
    </AbsoluteFill>
  );
};
