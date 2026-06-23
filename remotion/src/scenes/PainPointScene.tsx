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
  场景2：痛点
  8 ~ 17秒 (240 ~ 510帧)
  视觉：深色背景，2×2 四宫格卡片，每张卡片一个人物故事。
*/

const PAINS = [
  {
    who: "李叔",
    initial: "李",
    words: "我家一共5块地，你说哪块施了多少肥...",
    fact: "全村 86 户蔗农 · 平均每户 3.2 块地",
    result: "靠脑子记，年底一问三不知",
    color: "#d97706",
  },
  {
    who: "张大姐",
    initial: "张",
    words: "糖厂打电话问产量，我翻了一下午本子",
    fact: "上级要数据 → 翻票据 → 算计算器 → 加班填表",
    result: "每年报数据至少折腾 3 天",
    color: "#3b82f6",
  },
  {
    who: "王技术员",
    initial: "王",
    words: "村里信号时有时无，那个App根本打不开",
    fact: "广西山区蔗地网络覆盖率不足 40%",
    result: "市面上的农场软件基本等于摆设",
    color: "#16a34a",
  },
  {
    who: "陈社长",
    initial: "陈",
    words: "去年虫害没及时治，那一季减产了两成",
    fact: "没有记录就没有预警机制",
    result: "病虫害 / 天气 / 农事 全凭经验和运气",
    color: "#ef4444",
  },
];

const CARD_CONFIG = [
  { delay: 0.5, fromX: -40, fromY: 30 },
  { delay: 1.0, fromX: 40, fromY: 30 },
  { delay: 1.5, fromX: -40, fromY: -30 },
  { delay: 2.0, fromX: 40, fromY: -30 },
];

export const PainPointScene: React.FC = () => {
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

  const cards = PAINS.map((pain, i) => {
    const cfg = CARD_CONFIG[i];
    const progress = spring({
      frame: frame - cfg.delay * fps,
      fps,
      config: { damping: 16, stiffness: 80 },
    });

    const x = interpolate(progress, [0, 1], [cfg.fromX, 0]);
    const y = interpolate(progress, [0, 1], [cfg.fromY, 0]);
    const opacity = interpolate(progress, [0, 1], [0, 1]);
    const scale = interpolate(progress, [0, 1], [0.9, 1]);

    return (
      <div
        key={i}
        style={{
          flex: 1,
          padding: 32,
          borderRadius: 16,
          backgroundColor: "rgba(255,255,255,0.04)",
          border: `1.5px solid ${pain.color}20`,
          transform: `translate(${x}px, ${y}px) scale(${scale})`,
          opacity,
          display: "flex",
          flexDirection: "column",
          gap: 18,
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 16,
          }}
        >
          <div
            style={{
              width: 56,
              height: 56,
              borderRadius: "50%",
              backgroundColor: `${pain.color}12`,
              border: `2px solid ${pain.color}35`,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 24,
              fontWeight: 800,
              color: pain.color,
              flexShrink: 0,
            }}
          >
            {pain.initial}
          </div>
          <span
            style={{
              fontSize: 24,
              fontWeight: 700,
              color: "#f0fdf4",
            }}
          >
            {pain.who}
          </span>
        </div>

        <div
          style={{
            fontSize: 24,
            fontWeight: 700,
            color: "#f0fdf4",
            lineHeight: 1.55,
            borderLeft: `3px solid ${pain.color}`,
            paddingLeft: 16,
          }}
        >
          "{pain.words}"
        </div>

        <div
          style={{
            fontSize: 20,
            color: "#86a88e",
            lineHeight: 1.7,
          }}
        >
          {pain.fact}
        </div>

        <div
          style={{
            fontSize: 18,
            fontWeight: 600,
            color: pain.color,
            marginTop: "auto",
            display: "flex",
            alignItems: "center",
            gap: 8,
          }}
        >
          <span>→</span>
          {pain.result}
        </div>
      </div>
    );
  });

  const turnOpacity = interpolate(
    frame,
    [5.5 * fps, 6.8 * fps],
    [0, 1],
    { extrapolateRight: "clamp" }
  );
  const turnY = interpolate(
    frame,
    [5.5 * fps, 6.3 * fps],
    [16, 0],
    { extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill
      style={{ backgroundColor: "#0c1510", fontFamily: "'Noto Sans SC', sans-serif" }}
    >
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage:
            "radial-gradient(circle at 70% 30%, rgba(217,119,6,0.05) 0%, transparent 40%)",
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
              fontSize: 52,
              fontWeight: 900,
              color: "#f0fdf4",
              letterSpacing: 1,
            }}
          >
            广西蔗农的真实日常
          </div>
          <div
            style={{
              fontSize: 22,
              color: "#86a88e",
              marginTop: 8,
              opacity: subtitleOpacity,
            }}
          >
            走访了崇左、来宾、百色的几十户蔗农，听到了这些声音
          </div>
        </div>

        <div
          style={{
            flex: 1,
            display: "flex",
            flexDirection: "column",
            gap: 18,
          }}
        >
          <div style={{ display: "flex", gap: 18, flex: 1 }}>
            {cards.slice(0, 2)}
          </div>
          <div style={{ display: "flex", gap: 18, flex: 1 }}>
            {cards.slice(2, 4)}
          </div>
        </div>

        <div
          style={{
            textAlign: "center",
            paddingTop: 28,
            opacity: turnOpacity,
            transform: `translateY(${turnY}px)`,
          }}
        >
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 12,
              padding: "12px 28px",
              borderRadius: 999,
              backgroundColor: "rgba(34,197,94,0.08)",
              border: "1.5px solid rgba(34,197,94,0.25)",
            }}
          >
            <span style={{ fontSize: 22, color: "#22c55e", fontWeight: 700 }}>
              所以我们做了桂收
            </span>
            <span style={{ fontSize: 24, color: "#22c55e", fontWeight: 900 }}>→</span>
          </div>
        </div>
      </AbsoluteFill>
      <Audio src={staticFile("[女主播]李叔家5块地年底一-1782190036937.mp3")} />
    </AbsoluteFill>
  );
};
