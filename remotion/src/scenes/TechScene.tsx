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
  68 ~ 88秒 (2040 ~ 2640帧)
  视觉：浅色背景，前后端两栏技术清单，底部关键数据。
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
  const titleY = interpolate(frame, [0, 0.8 * fps], [24, 0], {
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
          padding: "18px 24px",
          borderRadius: 2,
          backgroundColor: "#fffdf7",
          border: "1px solid #d9d4c9",
          boxShadow: "2px 2px 0 #d9d4c9",
          transform: `translateX(${x}px)`,
          opacity,
          display: "flex",
          alignItems: "center",
          gap: 16,
        }}
      >
        <div
          style={{
            width: 8,
            height: 8,
            borderRadius: "50%",
            backgroundColor: "#4a6fa5",
            flexShrink: 0,
          }}
        />
        <div>
          <div
            style={{
              fontSize: 22,
              fontWeight: 900,
              color: "#1c1917",
              marginBottom: 3,
            }}
          >
            {tech.name}
          </div>
          <div style={{ fontSize: 17, color: "#5c564a" }}>{tech.note}</div>
        </div>
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
          padding: "18px 24px",
          borderRadius: 2,
          backgroundColor: "#fffdf7",
          border: "1px solid #d9d4c9",
          boxShadow: "2px 2px 0 #d9d4c9",
          transform: `translateX(${x}px)`,
          opacity,
          display: "flex",
          alignItems: "center",
          gap: 16,
        }}
      >
        <div
          style={{
            width: 8,
            height: 8,
            borderRadius: "50%",
            backgroundColor: "#3d7a3a",
            flexShrink: 0,
          }}
        />
        <div>
          <div
            style={{
              fontSize: 22,
              fontWeight: 900,
              color: "#1c1917",
              marginBottom: 3,
            }}
          >
            {tech.name}
          </div>
          <div style={{ fontSize: 17, color: "#5c564a" }}>{tech.note}</div>
        </div>
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
            fontSize: 40,
            fontWeight: 900,
            color: "#1c1917",
          }}
        >
          {stat.value}
        </div>
        <div
          style={{
            fontSize: 18,
            color: "#2d5a27",
            fontWeight: 900,
            marginTop: 6,
          }}
        >
          {stat.label}
        </div>
        <div
          style={{
            fontSize: 15,
            color: "#8c7f6b",
            marginTop: 3,
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
          padding: "52px 100px 44px",
        }}
      >
        <div
          style={{
            textAlign: "center",
            marginBottom: 44,
            transform: `translateY(${titleY}px)`,
            opacity: titleOpacity,
          }}
        >
          <div
            style={{
              fontSize: 56,
              fontWeight: 900,
              color: "#1c1917",
            }}
          >
            技术选型：轻量、稳定、够用就好
          </div>
          <div
            style={{
              fontSize: 24,
              color: "#5c564a",
              marginTop: 10,
            }}
          >
            不追求最新最潮，只选最适合广西农村实际环境的方案
          </div>
        </div>

        <div
          style={{
            flex: 1,
            display: "flex",
            gap: 60,
            alignItems: "stretch",
            maxWidth: 1200,
            margin: "0 auto",
            width: "100%",
          }}
        >
          <div
            style={{
              flex: 1,
              display: "flex",
              flexDirection: "column",
              gap: 14,
            }}
          >
            <div
              style={{
                fontSize: 20,
                color: "#4a6fa5",
                fontWeight: 900,
                letterSpacing: 2,
                marginBottom: 8,
                textAlign: "center",
                paddingBottom: 12,
                borderBottom: "2px solid #d9d4c9",
              }}
            >
              前端 Vue 3 + Vite
            </div>
            {frontItems}
          </div>

          <div
            style={{
              width: 60,
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
                backgroundColor: "#d9d4c9",
                borderRadius: 1,
              }}
            />
            <span
              style={{
                fontSize: 14,
                color: "#8c7f6b",
                marginTop: 12,
                writingMode: "vertical-rl",
                fontWeight: 900,
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
              gap: 14,
            }}
          >
            <div
              style={{
                fontSize: 20,
                color: "#3d7a3a",
                fontWeight: 900,
                letterSpacing: 2,
                marginBottom: 8,
                textAlign: "center",
                paddingBottom: 12,
                borderBottom: "2px solid #d9d4c9",
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
            gap: 120,
            marginTop: 44,
            paddingTop: 32,
            borderTop: "2px solid #d9d4c9",
          }}
        >
          {statElements}
        </div>
      </AbsoluteFill>
      <Audio src={staticFile("[女主播]技术选型六个字 轻-1782190944599.mp3")} />
    </AbsoluteFill>
  );
};
