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
  场景3：解决方案 — 桂收是什么
  24 ~ 41秒 (720 ~ 1230帧)
  视觉：浅色背景，左侧简化的软件界面，右侧说明文字。
*/

const MENU_ITEMS = [
  { label: "控制台首页" },
  { label: "地块管理" },
  { label: "农事记录" },
  { label: "数据大屏" },
  { label: "气象数据" },
  { label: "系统设置" },
];

const CONTENT_DATA: Record<number, { title: string; lines: string[] }> = {
  0: {
    title: "今日概览",
    lines: [
      "管理地块: 5 块 · 总面积: 42.8 亩",
      "当前周期: 2024新植蔗 · 已进行 128 天",
      "本周农事: 施肥 1 次 · 灌溉 2 次",
    ],
  },
  1: {
    title: "地块列表",
    lines: [
      "#1 东岭地块  ·  12.3亩  ·  桂糖44号  ·  新植",
      "#2 鱼塘北     ·   8.7亩  ·  桂糖58号  ·  宿根2年",
      "#3 大路东     ·  11.2亩  ·  柳城05136 ·  宿根1年",
      "#4 后山脚     ·   6.4亩  ·  桂糖55号  ·  新植",
      "#5 河滩地     ·   4.2亩  ·  新台糖22号 ·  宿根3年",
    ],
  },
  2: {
    title: "近期农事",
    lines: [
      "[03-15] 东岭地块 · 施肥 · 尿素 40kg/亩",
      "[03-12] 鱼塘北   · 灌溉 · 沟灌 2小时",
      "[03-08] 全部地块 · 防虫 · 吡虫啉喷雾",
      "[03-01] 大路东   · 施肥 · 复合肥 50kg/亩",
    ],
  },
  3: {
    title: "数据统计",
    lines: [
      "本季总投入: ¥12,680  ·  预估产量: 256吨",
      "品种分布: 桂糖系列 62% · 柳城系列 28%",
      "同比去年: 面积 +8% · 投入 +3%",
    ],
  },
  4: {
    title: "天气情况",
    lines: [
      "崇左市江州区 · 今日 26°C · 湿度 78%",
      "未来3日: 多云 → 小雨 → 阴",
      "⚠ 周三可能有霜冻，注意覆盖保温",
    ],
  },
  5: {
    title: "系统状态",
    lines: [
      "版本: v1.0.0  ·  数据库: 正常",
      "离线模式: 已开启  ·  数据备份: 今日已备",
      "用户: admin (户主) · 在线设备: 1",
    ],
  },
};

export const SolutionScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleOpacity = interpolate(frame, [0, 0.7 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });
  const titleY = interpolate(frame, [0, 0.8 * fps], [24, 0], {
    extrapolateRight: "clamp",
  });

  const windowProgress = spring({
    frame: frame - 0.3 * fps,
    fps,
    config: { damping: 18, stiffness: 60 },
  });
  const windowY = interpolate(windowProgress, [0, 1], [40, 0]);
  const windowOpacity = interpolate(windowProgress, [0, 1], [0, 1]);

  const contentPhase = Math.min(
    Math.floor((frame - 2 * fps) / (1.2 * fps)),
    MENU_ITEMS.length - 1
  );

  const currentContent = CONTENT_DATA[contentPhase] || CONTENT_DATA[0];
  const contentStartFrame = (2 + contentPhase * 1.2 + 0.3) * fps;

  const descOpacity = interpolate(frame, [1.5 * fps, 2.5 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });

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
          padding: "52px 72px 44px",
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
              color: "#1c1917",
              letterSpacing: 1,
            }}
          >
            桂收能做什么？
          </div>
          <div
            style={{
              fontSize: 24,
              color: "#5c564a",
              marginTop: 10,
            }}
          >
            打开浏览器就能用，离线也能跑
          </div>
        </div>

        <div
          style={{
            flex: 1,
            display: "flex",
            gap: 44,
            alignItems: "center",
          }}
        >
          {/* 左侧：简化界面 */}
          <div
            style={{
              flex: 1,
              height: "100%",
              maxWidth: 960,
              borderRadius: 4,
              backgroundColor: "#fffdf7",
              border: "2px solid #d9d4c9",
              overflow: "hidden",
              transform: `translateY(${windowY}px)`,
              opacity: windowOpacity,
              display: "flex",
              flexDirection: "column",
              boxShadow: "4px 4px 0 #d9d4c9",
            }}
          >
            {/* 标签栏 */}
            <div
              style={{
                height: 48,
                backgroundColor: "#f4f1ea",
                display: "flex",
                alignItems: "center",
                padding: "0 18px",
                gap: 10,
                borderBottom: "2px solid #d9d4c9",
              }}
            >
              <div
                style={{
                  width: 12,
                  height: 12,
                  borderRadius: "50%",
                  backgroundColor: "#d9d4c9",
                }}
              />
              <div
                style={{
                  width: 12,
                  height: 12,
                  borderRadius: "50%",
                  backgroundColor: "#d9d4c9",
                }}
              />
              <div
                style={{
                  width: 12,
                  height: 12,
                  borderRadius: "50%",
                  backgroundColor: "#d9d4c9",
                }}
              />
              <div
                style={{
                  marginLeft: 14,
                  fontSize: 14,
                  color: "#8c7f6b",
                }}
              >
                桂收 · 甘蔗专用版
              </div>
            </div>

            {/* 主体 */}
            <div style={{ flex: 1, display: "flex", minHeight: 0 }}>
              {/* 侧边栏 */}
              <div
                style={{
                  width: 200,
                  backgroundColor: "#faf8f2",
                  borderRight: "2px solid #d9d4c9",
                  padding: "18px 12px",
                  display: "flex",
                  flexDirection: "column",
                  gap: 4,
                }}
              >
                <div
                  style={{
                    fontSize: 22,
                    fontWeight: 900,
                    color: "#2d5a27",
                    marginBottom: 18,
                    paddingLeft: 8,
                    letterSpacing: 3,
                  }}
                >
                  桂收
                </div>
                {MENU_ITEMS.map((item, i) => {
                  const isActive = i === contentPhase;
                  const isVisited = frame > (2 + i * 1.2) * fps && !isActive;

                  return (
                    <div
                      key={i}
                      style={{
                        padding: "11px 14px",
                        borderRadius: 2,
                        backgroundColor: isActive
                          ? "#2d5a27"
                          : isVisited
                            ? "#e8e4da"
                            : "transparent",
                        color: isActive ? "#fffdf7" : isVisited ? "#2d5a27" : "#5c564a",
                        fontSize: 16,
                        fontWeight: isActive ? 800 : 500,
                      }}
                    >
                      {item.label}
                    </div>
                  );
                })}
              </div>

              {/* 内容区 */}
              <div style={{ flex: 1, padding: "26px 32px", position: "relative" }}>
                <div
                  style={{
                    fontSize: 26,
                    fontWeight: 900,
                    color: "#1c1917",
                    marginBottom: 22,
                    paddingBottom: 14,
                    borderBottom: "2px solid #d9d4c9",
                  }}
                >
                  {currentContent.title}
                </div>

                <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
                  {currentContent.lines.map((line, i) => {
                    const lineOpacity = interpolate(
                      frame,
                      [
                        contentStartFrame + i * 0.35 * fps,
                        contentStartFrame + (i + 0.5) * 0.35 * fps,
                      ],
                      [0, 1],
                      { extrapolateRight: "clamp", extrapolateLeft: "clamp" }
                    );

                    return (
                      <div
                        key={i}
                        style={{
                          fontSize: 19,
                          color: "#5c564a",
                          lineHeight: 1.8,
                          opacity: lineOpacity,
                          display: "flex",
                          alignItems: "center",
                          gap: 12,
                        }}
                      >
                        <span
                          style={{
                            color: "#2d5a27",
                            fontSize: 14,
                            flexShrink: 0,
                            fontWeight: 800,
                          }}
                        >
                          —
                        </span>
                        {line}
                      </div>
                    );
                  })}
                </div>

                {/* 状态栏 */}
                <div
                  style={{
                    position: "absolute",
                    bottom: 0,
                    left: 0,
                    right: 0,
                    height: 36,
                    backgroundColor: "#f4f1ea",
                    borderTop: "2px solid #d9d4c9",
                    display: "flex",
                    alignItems: "center",
                    padding: "0 20px",
                    gap: 16,
                  }}
                >
                  <span
                    style={{
                      fontSize: 14,
                      color: "#2d5a27",
                      display: "flex",
                      alignItems: "center",
                      gap: 6,
                      fontWeight: 800,
                    }}
                  >
                    <span
                      style={{
                        width: 7,
                        height: 7,
                        borderRadius: "50%",
                        backgroundColor: "#2d5a27",
                      }}
                    />
                    离线模式运行中
                  </span>
                  <span style={{ fontSize: 14, color: "#8c7f6b" }}>|</span>
                  <span style={{ fontSize: 14, color: "#8c7f6b" }}>
                    SQLite 本地数据库
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* 右侧：说明 */}
          <div
            style={{
              width: 620,
              flexShrink: 0,
              opacity: descOpacity,
            }}
          >
            <div
              style={{
                fontSize: 18,
                color: "#8c6239",
                fontWeight: 900,
                marginBottom: 20,
                letterSpacing: 3,
              }}
            >
              一句话
            </div>
            <div
              style={{
                fontSize: 48,
                fontWeight: 900,
                color: "#1c1917",
                lineHeight: 1.45,
                marginBottom: 32,
              }}
            >
              它是专门为你家甘蔗地
              <br />
              做的电子账本
            </div>
            <div
              style={{
                fontSize: 26,
                color: "#5c564a",
                lineHeight: 2,
              }}
            >
              地块、农事、天气、数据，一个页面全管完。
              <br />
              <br />
              不需要安装，不需要联网，数据就存在你自己的电脑上。
            </div>
          </div>
        </div>
      </AbsoluteFill>
      <Audio src={staticFile("[女主播]桂收能做什么打开浏-1782190046161.mp3")} />
    </AbsoluteFill>
  );
};
