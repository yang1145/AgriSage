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
  88 ~ 103秒 (2640 ~ 3090帧)
  视觉：浅色背景，左侧干净记事本呼应开场，右侧品牌收尾。
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
    [0, 180],
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
          alignItems: "center",
          justifyContent: "center",
          gap: 90,
          padding: 100,
        }}
      >
        {/* 左侧：干净的记事本 */}
        <div
          style={{
            transform: `translateY(${notebookY}px)`,
            opacity: notebookOpacity,
            backgroundColor: "#fffdf7",
            borderRadius: 4,
            padding: "48px 56px 48px 84px",
            width: 500,
            border: "1px solid #d9d4c9",
            boxShadow: "4px 4px 0 #d9d4c9",
            flexShrink: 0,
            position: "relative",
          }}
        >
          {/* 线圈装订 */}
          <div
            style={{
              position: "absolute",
              left: 18,
              top: 40,
              bottom: 40,
              width: 30,
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
            }}
          >
            {Array.from({ length: 8 }).map((_, i) => (
              <div
                key={i}
                style={{
                  width: 14,
                  height: 14,
                  borderRadius: "50%",
                  backgroundColor: "#c4c0b5",
                  border: "1px solid #a8a49a",
                }}
              />
            ))}
          </div>

          <div
            style={{
              fontSize: 16,
              color: "#8c7f6b",
              marginBottom: 22,
              paddingBottom: 12,
              borderBottom: "1px dashed #d9d4c9",
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
                  fontSize: line.highlight ? 22 : 20,
                  color: line.highlight ? "#2d5a27" : "#3d3a34",
                  fontFamily: "'Courier New', monospace",
                  lineHeight: 1.95,
                  fontWeight: line.highlight ? 900 : 500,
                }}
              >
                {line.text}
              </div>
            );
          })}

          <div
            style={{
              marginTop: 22,
              paddingTop: 14,
              borderTop: "1px dashed #a8c9a0",
              opacity: endingOpacity,
              display: "flex",
              alignItems: "center",
              gap: 8,
            }}
          >
            <span style={{ fontSize: 20, color: "#2d5a27", fontWeight: 900 }}>✓</span>
            <span
              style={{
                fontSize: 18,
                color: "#2d5a27",
                fontWeight: 900,
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
            width: 480,
          }}
        >
          <div
            style={{
              fontSize: 100,
              fontWeight: 900,
              color: "#2d5a27",
              letterSpacing: 8,
              marginBottom: 10,
            }}
          >
            桂收
          </div>

          <div
            style={{
              width: lineWidth,
              height: 4,
              borderRadius: 2,
              backgroundColor: "#2d5a27",
              marginBottom: 24,
            }}
          />

          <div
            style={{
              fontSize: 26,
              color: "#8c6239",
              fontWeight: 900,
              letterSpacing: 4,
              marginBottom: 28,
            }}
          >
            AGRISAGE CANE
          </div>

          <div
            style={{
              fontSize: 22,
              color: "#5c564a",
              lineHeight: 2,
              opacity: endingOpacity,
            }}
          >
            种甘蔗这件事本身已经够忙了
            <br />
            记录的事情交给我们
            <br />
            <br />
            <span style={{ color: "#1c1917", fontWeight: 900 }}>
              离线、免费、数据在你自己手里
            </span>
          </div>
        </div>
      </AbsoluteFill>

      {/* 底部版权 */}
      <div
        style={{
          position: "absolute",
          bottom: 36,
          left: 0,
          right: 0,
          textAlign: "center",
          opacity: footerOpacity,
        }}
      >
        <div
          style={{
            fontSize: 15,
            color: "#8c7f6b",
          }}
        >
          © 2024-2026 桂收·甘蔗专用版 AgriSage Cane · 本地离线 · 数据不出村
        </div>
      </div>
      <Audio src={staticFile("[女主播]东岭地块123亩-1782190099891.mp3")} />
    </AbsoluteFill>
  );
};
