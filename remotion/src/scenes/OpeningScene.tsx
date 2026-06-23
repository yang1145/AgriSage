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
  0 ~ 8秒 (0 ~ 240帧)
  视觉：深色背景上，一张手写混乱的记事本从左入场，随后平移到左侧，
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

  // 整体淡入
  const sceneOpacity = interpolate(frame, [0, 0.5 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });

  // 记事本入场
  const notebookProgress = spring({
    frame: frame - 0.2 * fps,
    fps,
    config: { damping: 18, stiffness: 60 },
  });
  const notebookOpacity = interpolate(notebookProgress, [0, 1], [0, 1]);
  const notebookRotate = interpolate(notebookProgress, [0, 1], [-3, 0]);
  const notebookX = interpolate(
    frame,
    [6 * fps, 7.5 * fps],
    [0, -320],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // 高亮标记
  const problemHighlight = interpolate(
    frame,
    [4.5 * fps, 5.5 * fps],
    [0, 1],
    { extrapolateRight: "clamp" }
  );

  // 右侧品牌信息
  const brandProgress = spring({
    frame: frame - 6.2 * fps,
    fps,
    config: { damping: 18, stiffness: 70 },
  });
  const brandX = interpolate(brandProgress, [0, 1], [80, 0]);
  const brandOpacity = interpolate(brandProgress, [0, 1], [0, 1]);

  // 品牌名逐字
  const brandChars = "桂收".split("");
  const brandCharElements = brandChars.map((char, i) => {
    const charProgress = spring({
      frame: frame - (6.8 + i * 0.2) * fps,
      fps,
      config: { damping: 12, stiffness: 160 },
    });
    const charY = interpolate(charProgress, [0, 1], [24, 0]);
    const charOpacity = interpolate(charProgress, [0, 1], [0, 1]);

    return (
      <span
        key={i}
        style={{
          display: "inline-block",
          transform: `translateY(${charY}px)`,
          opacity: charOpacity,
          fontSize: 72,
          fontWeight: 900,
          color: "#f0fdf4",
          letterSpacing: 8,
        }}
      >
        {char}
      </span>
    );
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0c1510",
        fontFamily: "'Noto Sans SC', sans-serif",
        opacity: sceneOpacity,
      }}
    >
      {/* 柔光背景 */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage:
            "radial-gradient(circle at 30% 50%, rgba(34,197,94,0.06) 0%, transparent 45%)",
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
            backgroundColor: "#fffef9",
            borderRadius: 8,
            boxShadow:
              "0 12px 40px rgba(0,0,0,0.25), inset 0 0 60px rgba(0,0,0,0.02)",
            padding: "44px 52px",
            width: 480,
            border: "1px solid rgba(0,0,0,0.06)",
            backgroundImage:
              "repeating-linear-gradient(transparent, transparent 35px, #e8e0d4 35px, #e8e0d4 36px)",
            flexShrink: 0,
          }}
        >
          {/* 高亮标记 */}
          <div
            style={{
              position: "absolute",
              top: 188,
              left: 36,
              right: 36,
              height: 32,
              backgroundColor: `rgba(234,88,12,${problemHighlight * 0.12})`,
              borderRadius: 2,
              transform: `skewX(-10deg)`,
            }}
          />

          <div
            style={{
              fontSize: 14,
              color: "#9ca3af",
              marginBottom: 20,
              paddingBottom: 10,
              borderBottom: "1px dashed #d1ccc0",
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
                  fontSize: line.emphasis ? 20 : 19,
                  color: line.emphasis ? "#c2410c" : "#374151",
                  fontFamily: "'Courier New', monospace",
                  lineHeight: 1.9,
                  fontStyle: line.emphasis ? "italic" : "normal",
                  fontWeight: line.emphasis ? 600 : 400,
                }}
              >
                {line.text}
              </div>
            );
          })}

          <div
            style={{
              marginTop: 20,
              paddingTop: 12,
              borderTop: "1px dashed #fecaca",
              opacity: problemHighlight,
              display: "flex",
              alignItems: "center",
              gap: 8,
            }}
          >
            <span style={{ fontSize: 16, color: "#dc2626" }}>→</span>
            <span
              style={{
                fontSize: 15,
                color: "#dc2626",
                fontWeight: 600,
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
            right: 120,
            top: "50%",
            transform: `translateY(-50%) translateX(${brandX}px)`,
            opacity: brandOpacity,
            textAlign: "left",
            width: 420,
          }}
        >
          <div
            style={{
              fontSize: 16,
              color: "#22c55e",
              fontWeight: 600,
              marginBottom: 10,
              letterSpacing: 2,
            }}
          >
            甘蔗种植管理系统
          </div>

          <div style={{ marginBottom: 12 }}>{brandCharElements}</div>

          <div
            style={{
              fontSize: 22,
              color: "#22c55e",
              fontWeight: 700,
              letterSpacing: 4,
              marginBottom: 22,
            }}
          >
            AGRISAGE CANE
          </div>

          <div
            style={{
              fontSize: 17,
              color: "#86a88e",
              lineHeight: 1.8,
            }}
          >
            给每一块甘蔗地建一份档案
            <br />
            <span style={{ color: "#f0fdf4", fontWeight: 600 }}>
              不需要联网，数据就在你自己手里
            </span>
          </div>
        </div>
      </AbsoluteFill>
      <Audio src={staticFile("[女主播]这是蔗农的种植笔记-1782190026445.mp3")} />
    </AbsoluteFill>
  );
};
