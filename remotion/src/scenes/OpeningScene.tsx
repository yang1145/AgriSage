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
  场景1：开场
  0 ~ 12秒 (0 ~ 360帧)
  视觉：浅色纸质背景，一本真实手写笔记入场，随后移向左侧，
        右侧浮现品牌信息。
*/

const NOTE_LINES = [
  { text: "3月12日  东边那块地", delay: 0 },
  { text: "施了复合肥，大概...50斤？", delay: 1.2 },
  { text: "哪块来着，靠近鱼塘的那块", delay: 2.8 },
  { text: "还是路边那块...算了记不清了", delay: 4.2, emphasis: true },
];

export const OpeningScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const notebookProgress = spring({
    frame: frame - 0.2 * fps,
    fps,
    config: { damping: 18, stiffness: 60 },
  });
  const notebookOpacity = interpolate(notebookProgress, [0, 1], [0, 1]);
  const notebookRotate = interpolate(notebookProgress, [0, 1], [-4, -1]);
  const notebookX = interpolate(
    frame,
    [6 * fps, 7.5 * fps],
    [0, -360],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const problemHighlight = interpolate(
    frame,
    [4.5 * fps, 5.5 * fps],
    [0, 1],
    { extrapolateRight: "clamp" }
  );

  const brandProgress = spring({
    frame: frame - 6.2 * fps,
    fps,
    config: { damping: 18, stiffness: 70 },
  });
  const brandX = interpolate(brandProgress, [0, 1], [80, 0]);
  const brandOpacity = interpolate(brandProgress, [0, 1], [0, 1]);

  const brandChars = "桂收".split("");
  const brandCharElements = brandChars.map((char, i) => {
    const charProgress = spring({
      frame: frame - (6.8 + i * 0.2) * fps,
      fps,
      config: { damping: 12, stiffness: 160 },
    });
    const charY = interpolate(charProgress, [0, 1], [30, 0]);
    const charOpacity = interpolate(charProgress, [0, 1], [0, 1]);

    return (
      <span
        key={i}
        style={{
          display: "inline-block",
          transform: `translateY(${charY}px)`,
          opacity: charOpacity,
          fontSize: 120,
          fontWeight: 900,
          color: "#2d5a27",
          letterSpacing: 10,
        }}
      >
        {char}
      </span>
    );
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#f4f1ea",
        fontFamily: "'Noto Sans SC', sans-serif",
      }}
    >
      {/* 纸张纹理 */}
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
          padding: 80,
        }}
      >
        {/* 记事本 */}
        <div
          style={{
            transform: `rotate(${notebookRotate}deg) translateX(${notebookX}px)`,
            opacity: notebookOpacity,
            backgroundColor: "#fffdf7",
            borderRadius: 4,
            padding: "52px 60px",
            width: 560,
            border: "1px solid #d9d4c9",
            boxShadow: "4px 4px 0 #d9d4c9",
            flexShrink: 0,
          }}
        >
          {/* 线圈装订效果 */}
          <div
            style={{
              position: "absolute",
              left: 16,
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
              position: "absolute",
              top: 232,
              left: 48,
              right: 48,
              height: 40,
              backgroundColor: `rgba(234,88,12,${problemHighlight * 0.18})`,
              borderRadius: 2,
              transform: `skewX(-8deg) rotate(-1deg)`,
            }}
          />

          <div
            style={{
              fontSize: 16,
              color: "#8c7f6b",
              marginBottom: 24,
              marginLeft: 28,
              paddingBottom: 12,
              borderBottom: "1px dashed #d9d4c9",
            }}
          >
            2024年3月 · 种植笔记
          </div>

          {NOTE_LINES.map((line, i) => {
            const lineOpacity = interpolate(
              frame,
              [(1 + line.delay) * fps, (1.4 + line.delay) * fps],
              [0, 1],
              { extrapolateRight: "clamp", extrapolateLeft: "clamp" }
            );
            const jitterX = Math.sin(frame * 0.3 + i * 2) * (lineOpacity > 0.8 ? 0.5 : 0);

            return (
              <div
                key={i}
                style={{
                  opacity: lineOpacity,
                  transform: `translateX(${jitterX}px)`,
                  fontSize: line.emphasis ? 24 : 22,
                  color: line.emphasis ? "#9c4b1c" : "#3d3a34",
                  fontFamily: "'Courier New', monospace",
                  lineHeight: 2,
                  marginLeft: 28,
                  fontStyle: line.emphasis ? "italic" : "normal",
                  fontWeight: line.emphasis ? 700 : 400,
                }}
              >
                {line.text}
              </div>
            );
          })}

          <div
            style={{
              marginTop: 24,
              marginLeft: 28,
              paddingTop: 14,
              borderTop: "1px dashed #e5a685",
              opacity: problemHighlight,
              display: "flex",
              alignItems: "center",
              gap: 8,
            }}
          >
            <span style={{ fontSize: 18, color: "#9c4b1c" }}>→</span>
            <span
              style={{
                fontSize: 18,
                color: "#9c4b1c",
                fontWeight: 700,
                fontStyle: "italic",
              }}
            >
              这块地多大？今年种的什么品种？
            </span>
          </div>
        </div>

        {/* 右侧品牌区域 */}
        <div
          style={{
            position: "absolute",
            right: 90,
            top: "50%",
            transform: `translateY(-50%) translateX(${brandX}px)`,
            opacity: brandOpacity,
            textAlign: "left",
            width: 500,
          }}
        >
          <div
            style={{
              fontSize: 20,
              color: "#8c6239",
              fontWeight: 800,
              marginBottom: 12,
              letterSpacing: 3,
            }}
          >
            甘蔗种植管理系统
          </div>

          <div style={{ marginBottom: 16 }}>{brandCharElements}</div>

          <div
            style={{
              fontSize: 28,
              color: "#8c6239",
              fontWeight: 800,
              letterSpacing: 5,
              marginBottom: 28,
            }}
          >
            AGRISAGE CANE
          </div>

          <div
            style={{
              fontSize: 24,
              color: "#5c564a",
              lineHeight: 1.9,
            }}
          >
            给每一块甘蔗地建一份档案
            <br />
            <span style={{ color: "#2d5a27", fontWeight: 800 }}>
              不需要联网，数据就在你自己手里
            </span>
          </div>
        </div>
      </AbsoluteFill>
      <Audio src={staticFile("[女主播]这是蔗农的种植笔记-1782190026445.mp3")} />
    </AbsoluteFill>
  );
};
