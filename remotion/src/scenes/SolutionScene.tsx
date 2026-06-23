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
  17 ~ 27秒 (510 ~ 810帧)
  视觉：左侧模拟软件界面，右侧说明文字，整体深色统一背景。
*/

const MENU_ITEMS = [
  { label: "控制台首页", icon: "▣" },
  { label: "地块管理", icon: "◧" },
  { label: "农事记录", icon: "✎" },
  { label: "数据大屏", icon: "◫" },
  { label: "气象数据", icon: "☁" },
  { label: "系统设置", icon: "☰" },
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
  const titleY = interpolate(frame, [0, 0.8 * fps], [20, 0], {
    extrapolateRight: "clamp",
  });

  // 窗口入场
  const windowProgress = spring({
    frame: frame - 0.3 * fps,
    fps,
    config: { damping: 18, stiffness: 60 },
  });
  const windowY = interpolate(windowProgress, [0, 1], [40, 0]);
  const windowOpacity = interpolate(windowProgress, [0, 1], [0, 1]);

  // 菜单高亮
  const contentPhase = Math.min(
    Math.floor((frame - 2 * fps) / (1.2 * fps)),
    MENU_ITEMS.length - 1
  );

  const currentContent = CONTENT_DATA[contentPhase] || CONTENT_DATA[0];
  const contentStartFrame = (2 + contentPhase * 1.2 + 0.3) * fps;

  // 解说文字
  const descOpacity = interpolate(frame, [1.5 * fps, 2.5 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });

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
            "radial-gradient(circle at 20% 70%, rgba(59,130,246,0.04) 0%, transparent 40%)",
        }}
      />

      <AbsoluteFill
        style={{
          display: "flex",
          flexDirection: "column",
          padding: "44px 72px 40px",
        }}
      >
        <div
          style={{
            textAlign: "center",
            marginBottom: 28,
            transform: `translateY(${titleY}px)`,
            opacity: titleOpacity,
          }}
        >
          <div
            style={{
              fontSize: 44,
              fontWeight: 900,
              color: "#f0fdf4",
              letterSpacing: 1,
            }}
          >
            桂收能做什么？
          </div>
          <div
            style={{
              fontSize: 17,
              color: "#86a88e",
              marginTop: 8,
            }}
          >
            打开浏览器就能用，离线也能跑
          </div>
        </div>

        <div
          style={{
            flex: 1,
            display: "flex",
            gap: 36,
            alignItems: "center",
          }}
        >
          {/* 左侧：模拟界面 */}
          <div
            style={{
              flex: 1,
              height: "100%",
              maxWidth: 920,
              borderRadius: 16,
              backgroundColor: "rgba(255,255,255,0.03)",
              border: "1px solid rgba(255,255,255,0.08)",
              overflow: "hidden",
              transform: `translateY(${windowY}px)`,
              opacity: windowOpacity,
              display: "flex",
              flexDirection: "column",
            }}
          >
            {/* 标签栏 */}
            <div
              style={{
                height: 44,
                backgroundColor: "rgba(255,255,255,0.04)",
                display: "flex",
                alignItems: "center",
                padding: "0 18px",
                gap: 10,
                borderBottom: "1px solid rgba(255,255,255,0.06)",
              }}
            >
              <div
                style={{
                  width: 12,
                  height: 12,
                  borderRadius: "50%",
                  backgroundColor: "#ef4444",
                }}
              />
              <div
                style={{
                  width: 12,
                  height: 12,
                  borderRadius: "50%",
                  backgroundColor: "#f59e0b",
                }}
              />
              <div
                style={{
                  width: 12,
                  height: 12,
                  borderRadius: "50%",
                  backgroundColor: "#22c55e",
                }}
              />
              <div
                style={{
                  marginLeft: 14,
                  fontSize: 13,
                  color: "#5c7c66",
                }}
              >
                桂收 · 甘蔗专用版 — localhost:5000
              </div>
            </div>

            {/* 主体 */}
            <div style={{ flex: 1, display: "flex", minHeight: 0 }}>
              {/* 侧边栏 */}
              <div
                style={{
                  width: 200,
                  backgroundColor: "rgba(255,255,255,0.02)",
                  borderRight: "1px solid rgba(255,255,255,0.06)",
                  padding: "16px 12px",
                  display: "flex",
                  flexDirection: "column",
                  gap: 4,
                }}
              >
                <div
                  style={{
                    fontSize: 18,
                    fontWeight: 800,
                    color: "#22c55e",
                    marginBottom: 16,
                    paddingLeft: 8,
                    letterSpacing: 2,
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
                        display: "flex",
                        alignItems: "center",
                        gap: 12,
                        padding: "10px 14px",
                        borderRadius: 8,
                        backgroundColor: isActive
                          ? "#22c55e"
                          : isVisited
                            ? "rgba(34,197,94,0.08)"
                            : "transparent",
                        color: isActive ? "#0c1510" : isVisited ? "#22c55e" : "#5c7c66",
                        fontSize: 15,
                        fontWeight: isActive ? 700 : 400,
                      }}
                    >
                      <span style={{ fontSize: 15, width: 20, textAlign: "center" }}>
                        {item.icon}
                      </span>
                      {item.label}
                    </div>
                  );
                })}
              </div>

              {/* 内容区 */}
              <div style={{ flex: 1, padding: "22px 28px", position: "relative" }}>
                <div
                  style={{
                    fontSize: 20,
                    fontWeight: 700,
                    color: "#f0fdf4",
                    marginBottom: 18,
                    paddingBottom: 12,
                    borderBottom: "1px solid rgba(255,255,255,0.06)",
                  }}
                >
                  {currentContent.title}
                </div>

                <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
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
                          fontSize: 15,
                          color: "#86a88e",
                          lineHeight: 1.7,
                          opacity: lineOpacity,
                          display: "flex",
                          alignItems: "center",
                          gap: 10,
                        }}
                      >
                        <span
                          style={{
                            color: "#22c55e40",
                            fontSize: 12,
                            flexShrink: 0,
                          }}
                        >
                          {"//"}
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
                    height: 34,
                    backgroundColor: "rgba(0,0,0,0.15)",
                    borderTop: "1px solid rgba(255,255,255,0.05)",
                    display: "flex",
                    alignItems: "center",
                    padding: "0 20px",
                    gap: 16,
                  }}
                >
                  <span
                    style={{
                      fontSize: 12,
                      color: "#22c55e",
                      display: "flex",
                      alignItems: "center",
                      gap: 6,
                    }}
                  >
                    <span
                      style={{
                        width: 6,
                        height: 6,
                        borderRadius: "50%",
                        backgroundColor: "#22c55e",
                      }}
                    />
                    离线模式运行中
                  </span>
                  <span style={{ fontSize: 12, color: "#5c7c66" }}>|</span>
                  <span style={{ fontSize: 12, color: "#5c7c66" }}>
                    SQLite 本地数据库
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* 右侧：说明 */}
          <div
            style={{
              width: 560,
              flexShrink: 0,
              opacity: descOpacity,
            }}
          >
            <div
              style={{
                fontSize: 18,
                color: "#22c55e",
                fontWeight: 700,
                marginBottom: 20,
                letterSpacing: 2,
              }}
            >
              一句话
            </div>
            <div
              style={{
                fontSize: 36,
                fontWeight: 800,
                color: "#f0fdf4",
                lineHeight: 1.5,
                marginBottom: 28,
              }}
            >
              它是专门为你家甘蔗地
              <br />
              做的电子账本
            </div>
            <div
              style={{
                fontSize: 22,
                color: "#86a88e",
                lineHeight: 2.1,
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
