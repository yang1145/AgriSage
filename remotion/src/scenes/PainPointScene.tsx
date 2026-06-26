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
  12 ~ 24秒 (360 ~ 720帧)
  视觉：浅色背景，四张像贴在木板/墙上的便签，每张一个人物故事。
*/

const PAINS = [
  {
    who: "李叔",
    words: "我家一共5块地，你说哪块施了多少肥...",
    fact: "全村 86 户蔗农 · 平均每户 3.2 块地",
    result: "靠脑子记，年底一问三不知",
    color: "#b86d29",
  },
  {
    who: "张大姐",
    words: "糖厂打电话问产量，我翻了一下午本子",
    fact: "上级要数据 → 翻票据 → 算计算器 → 加班填表",
    result: "每年报数据至少折腾 3 天",
    color: "#4a6fa5",
  },
  {
    who: "王技术员",
    words: "村里信号时有时无，那个App根本打不开",
    fact: "广西山区蔗地网络覆盖率不足 40%",
    result: "市面上的农场软件基本等于摆设",
    color: "#3d7a3a",
  },
  {
    who: "陈社长",
    words: "去年虫害没及时治，那一季减产了两成",
    fact: "没有记录就没有预警机制",
    result: "病虫害 / 天气 / 农事 全凭经验和运气",
    color: "#b04444",
  },
];

export const PainPointScene: React.FC = () => {
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

  const cards = PAINS.map((pain, i) => {
    const row = Math.floor(i / 2);
    const col = i % 2;
    const delay = 0.6 + row * 0.6 + col * 0.3;

    const progress = spring({
      frame: frame - delay * fps,
      fps,
      config: { damping: 16, stiffness: 80 },
    });

    const y = interpolate(progress, [0, 1], [40, 0]);
    const opacity = interpolate(progress, [0, 1], [0, 1]);
    const rotate = [-1.5, 1, -0.8, 1.2][i];

    return (
      <div
        key={i}
        style={{
          flex: 1,
          padding: 36,
          borderRadius: 2,
          backgroundColor: "#fffdf7",
          border: "1px solid #d9d4c9",
          boxShadow: "3px 3px 0 #d9d4c9",
          transform: `translateY(${y}px) rotate(${rotate}deg)`,
          opacity,
          display: "flex",
          flexDirection: "column",
          gap: 18,
          position: "relative",
        }}
      >
        {/* 图钉 */}
        <div
          style={{
            position: "absolute",
            top: 14,
            right: 18,
            width: 16,
            height: 16,
            borderRadius: "50%",
            backgroundColor: pain.color,
            boxShadow: "1px 1px 2px rgba(0,0,0,0.2)",
          }}
        />

        <div
          style={{
            fontSize: 26,
            fontWeight: 900,
            color: pain.color,
          }}
        >
          {pain.who}
        </div>

        <div
          style={{
            fontSize: 26,
            fontWeight: 800,
            color: "#1c1917",
            lineHeight: 1.55,
            borderLeft: `4px solid ${pain.color}`,
            paddingLeft: 16,
          }}
        >
          "{pain.words}"
        </div>

        <div
          style={{
            fontSize: 20,
            color: "#5c564a",
            lineHeight: 1.7,
          }}
        >
          {pain.fact}
        </div>

        <div
          style={{
            fontSize: 18,
            fontWeight: 800,
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
    [18, 0],
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
          padding: "56px 80px 44px",
        }}
      >
        <div
          style={{
            textAlign: "center",
            marginBottom: 40,
            transform: `translateY(${titleY}px)`,
            opacity: titleOpacity,
          }}
        >
          <div
            style={{
              fontSize: 64,
              fontWeight: 900,
              color: "#1c1917",
              letterSpacing: 1,
            }}
          >
            广西蔗农的真实日常
          </div>
          <div
            style={{
              fontSize: 26,
              color: "#5c564a",
              marginTop: 10,
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
            gap: 22,
          }}
        >
          <div style={{ display: "flex", gap: 22, flex: 1 }}>
            {cards.slice(0, 2)}
          </div>
          <div style={{ display: "flex", gap: 22, flex: 1 }}>
            {cards.slice(2, 4)}
          </div>
        </div>

        <div
          style={{
            textAlign: "center",
            paddingTop: 32,
            opacity: turnOpacity,
            transform: `translateY(${turnY}px)`,
          }}
        >
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 14,
              padding: "14px 32px",
              backgroundColor: "#2d5a27",
              color: "#fffdf7",
              fontSize: 24,
              fontWeight: 800,
              boxShadow: "3px 3px 0 #1a3a17",
            }}
          >
            所以我们做了桂收 →
          </div>
        </div>
      </AbsoluteFill>
      <Audio src={staticFile("[女主播]李叔家5块地年底一-1782190036937.mp3")} />
    </AbsoluteFill>
  );
};
