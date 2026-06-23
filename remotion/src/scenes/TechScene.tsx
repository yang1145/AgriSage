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
  场景5：技术栈
  42 ~ 52秒 (1260 ~ 1560帧)
  视觉：深色背景，前端/后端双栏架构图，底部关键数据。
*/

const FRONTEND_TECH = [
  { name: "Vue 3.4", note: "渐进式框架，组合式API" },
  { name: "Vite 5.1", note: "极速构建，HMR毫秒级响应" },
  { name: "Element Plus", note: "70+组件，桌面端UI库" },
  { name: "ECharts 5.5", note: "仪表盘图表与数据可视化" },
  { name: "Leaflet 1.9", note: "在线/离线双模式地图引擎" },
];

const BACKEND_TECH = [
  { name: "Flask 3.0", note: "Python轻量级Web框架" },
  { name: "SQLAlchemy", note: "ORM数据库抽象层" },
  { name: "SQLite", note: "单文件嵌入式，零配置离线" },
  { name: "JWT认证", note: "无状态Token，多角色权限" },
  { name: "openpyxl+reportlab", note: "Excel/PDF导出能力" },
];

export const TechScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleOpacity = interpolate(frame, [0, 0.7 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });
  const titleY = interpolate(frame, [0, 0.8 * fps], [20, 0], {
    extrapolateRight: "clamp",
  });

  const frontItems = FRONTEND_TECH.map((tech, i) => {
    const delay = 1 + i * 0.3;
    const progress = spring({
      frame: frame - delay * fps,
      fps,
      config: { damping: 18, stiffness: 90 },
    });
    const x = interpolate(progress, [0, 1], [-30, 0]);
    const opacity = interpolate(progress, [0, 1], [0, 1]);

    return (
      <div
        key={i}
        style={{
          padding: "14px 20px",
          borderRadius: 12,
          backgroundColor: "rgba(59,130,246,0.06)",
          border: "1px solid rgba(59,130,246,0.12)",
          transform: `translateX(${x}px)`,
          opacity,
        }}
      >
        <div
          style={{
            fontSize: 17,
            fontWeight: 700,
            color: "#f0fdf4",
            marginBottom: 3,
          }}
        >
          {tech.name}
        </div>
        <div style={{ fontSize: 14, color: "#86a88e" }}>{tech.note}</div>
      </div>
    );
  });

  const backItems = BACKEND_TECH.map((tech, i) => {
    const delay = 1.2 + i * 0.3;
    const progress = spring({
      frame: frame - delay * fps,
      fps,
      config: { damping: 18, stiffness: 90 },
    });
    const x = interpolate(progress, [0, 1], [30, 0]);
    const opacity = interpolate(progress, [0, 1], [0, 1]);

    return (
      <div
        key={i}
        style={{
          padding: "14px 20px",
          borderRadius: 12,
          backgroundColor: "rgba(34,197,94,0.06)",
          border: "1px solid rgba(34,197,94,0.12)",
          transform: `translateX(${x}px)`,
          opacity,
        }}
      >
        <div
          style={{
            fontSize: 17,
            fontWeight: 700,
            color: "#f0fdf4",
            marginBottom: 3,
          }}
        >
          {tech.name}
        </div>
        <div style={{ fontSize: 14, color: "#86a88e" }}>{tech.note}</div>
      </div>
    );
  });

  const connectorOpacity = interpolate(
    frame,
    [2.5 * fps, 3.5 * fps],
    [0, 1],
    { extrapolateRight: "clamp" }
  );

  const stats = [
    { label: "代码行数", value: "~15,000", sub: "前后端合计" },
    { label: "依赖数量", value: "0", sub: "无需安装额外运行时" },
    { label: "部署方式", value: "双击启动", sub: "Windows可执行程序" },
  ];

  const statElements = stats.map((stat, i) => {
    const delay = 4.5 + i * 0.4;
    const statProgress = spring({
      frame: frame - delay * fps,
      fps,
      config: { damping: 18, stiffness: 120 },
    });
    const statY = interpolate(statProgress, [0, 1], [16, 0]);
    const statOpacity = interpolate(statProgress, [0, 1], [0, 1]);

    return (
      <div
        key={i}
        style={{
          textAlign: "center",
          transform: `translateY(${statY}px)`,
          opacity: statOpacity,
        }}
      >
        <div
          style={{
            fontSize: 30,
            fontWeight: 900,
            color: "#f0fdf4",
          }}
        >
          {stat.value}
        </div>
        <div
          style={{
            fontSize: 15,
            color: "#22c55e",
            fontWeight: 700,
            marginTop: 4,
          }}
        >
          {stat.label}
        </div>
        <div
          style={{
            fontSize: 13,
            color: "#5c7c66",
            marginTop: 2,
          }}
        >
          {stat.sub}
        </div>
      </div>
    );
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
            "radial-gradient(circle at 80% 20%, rgba(59,130,246,0.04) 0%, transparent 40%)",
        }}
      />

      <AbsoluteFill
        style={{
          display: "flex",
          flexDirection: "column",
          padding: "48px 100px 40px",
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
              fontSize: 44,
              fontWeight: 900,
              color: "#f0fdf4",
            }}
          >
            技术选型：轻量、稳定、够用就好
          </div>
          <div
            style={{
              fontSize: 17,
              color: "#86a88e",
              marginTop: 8,
            }}
          >
            不追求最新最潮，只选最适合广西农村实际环境的方案
          </div>
        </div>

        <div
          style={{
            flex: 1,
            display: "flex",
            gap: 0,
            alignItems: "stretch",
            maxWidth: 1100,
            margin: "0 auto",
            width: "100%",
          }}
        >
          <div
            style={{
              flex: 1,
              display: "flex",
              flexDirection: "column",
              gap: 12,
              paddingRight: 24,
            }}
          >
            <div
              style={{
                fontSize: 15,
                color: "#3b82f6",
                fontWeight: 700,
                letterSpacing: 2,
                marginBottom: 8,
                textAlign: "center",
              }}
            >
              前端 Vue 3 + Vite
            </div>
            {frontItems}
          </div>

          <div
            style={{
              width: 80,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              opacity: connectorOpacity,
            }}
          >
            <div
              style={{
                width: 2,
                height: 180,
                background:
                  "linear-gradient(to bottom, rgba(59,130,246,0.6), rgba(34,197,94,0.6))",
                borderRadius: 1,
                position: "relative",
              }}
            >
              <div
                style={{
                  position: "absolute",
                  top: `${interpolate(
                    Math.sin((frame / fps) * 3),
                    [-1, 1],
                    [20, 160]
                  )}px`,
                  left: -4,
                  width: 10,
                  height: 10,
                  borderRadius: "50%",
                  backgroundColor: "#f0fdf4",
                  boxShadow: "0 0 10px rgba(255,255,255,0.4)",
                }}
              />
            </div>
            <span
              style={{
                fontSize: 12,
                color: "#5c7c66",
                marginTop: 10,
                writingMode: "vertical-rl",
              }}
            >
              REST API
            </span>
          </div>

          <div
            style={{
              flex: 1,
              display: "flex",
              flexDirection: "column",
              gap: 12,
              paddingLeft: 24,
            }}
          >
            <div
              style={{
                fontSize: 15,
                color: "#22c55e",
                fontWeight: 700,
                letterSpacing: 2,
                marginBottom: 8,
                textAlign: "center",
              }}
            >
              后端 Flask + SQLite
            </div>
            {backItems}
          </div>
        </div>

        <div
          style={{
            display: "flex",
            justifyContent: "center",
            gap: 100,
            marginTop: 40,
            paddingTop: 28,
            borderTop: "1px solid rgba(255,255,255,0.06)",
          }}
        >
          {statElements}
        </div>
      </AbsoluteFill>
      <Audio src={staticFile("[女主播]技术选型六个字 轻-1782190944599.mp3")} />
    </AbsoluteFill>
  );
};
