# 桂收 · 甘蔗专用版 — 项目启动说明书

## 一、项目概述

| 项目 | 说明 |
|---|---|
| 名称 | 桂收 · 甘蔗专用版（AgriSage Cane） |
| 架构 | 前后端分离 |
| 后端 | Python 3.11+ / Flask / SQLAlchemy / SQLite |
| 前端 | Vue 3 / Vite / Element Plus / ECharts / Leaflet |
| 默认账号 | `admin` / `admin123` |

---

## 二、环境要求

### 2.1 必须安装

- **Python** 3.11 或更高版本
- **Node.js** 18 或更高版本（推荐 LTS 版本）
- **Git**（用于克隆代码）

### 2.2 可选（离线部署）

如需离线使用地图瓦片，需提前下载瓦片文件至 `frontend/public/tiles/` 目录。

---

## 三、项目结构

```
AgriSage/
├── backend/                  # Flask 后端
│   ├── app.py                # 应用入口，创建 Flask 实例
│   ├── config.py             # 配置（数据库、JWT、上传）
│   ├── extensions.py         # 扩展注册（db, cors）
│   ├── requirements.txt      # Python 依赖
│   ├── api/                  # API 路由模块
│   │   ├── __init__.py       # 蓝图注册
│   │   ├── auth.py           # 登录/注册（仅户主可注册）
│   │   ├── user.py           # 用户管理 CRUD
│   │   ├── plot.py           # 地块管理
│   │   ├── planting_cycle.py # 种植周期
│   │   ├── farming_record.py # 农事记录
│   │   ├── dictionary.py     # 字典数据 + 天气 API
│   │   ├── image.py          # 图片管理
│   │   ├── export.py         # 数据导出
│   │   └── system.py         # 系统设置
│   ├── models/               # SQLAlchemy 数据模型
│   │   ├── user.py           # 用户模型
│   │   ├── plot.py           # 地块模型
│   │   ├── planting_cycle.py # 种植周期模型
│   │   ├── farming_record.py # 农事记录模型
│   │   ├── plot_image.py     # 地块图片模型
│   │   └── dictionary.py     # 字典数据模型
│   ├── data/                 # SQLite 数据库自动生成在此处
│   └── uploads/              # 上传文件存储目录
├── frontend/                 # Vue 3 前端
│   ├── package.json          # Node 依赖与脚本
│   ├── vite.config.js        # Vite 配置（代理端口等）
│   ├── public/
│   │   ├── tiles/            # 离线地图瓦片（可选）
│   │   └── login_29/         # 登录页静态资源
│   └── src/
│       ├── main.js           # 入口文件
│       ├── App.vue           # 根组件
│       ├── router/index.js   # 路由配置
│       ├── api/              # Axios 接口封装
│       ├── stores/           # Pinia 状态管理
│       ├── composables/      # 组合式函数
│       ├── components/       # 公共组件
│       ├── views/            # 页面组件
│       └── styles/           # 全局样式变量
```

---

## 四、快速启动

### 第一步：克隆项目

```bash
git clone <仓库地址> AgriSage
cd AgriSage
```

### 第二步：启动后端

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装 Python 依赖
pip install -r requirements.txt

# 启动后端服务（默认 http://localhost:5000）
python app.py
```

看到以下输出说明启动成功：

```
桂收 · 甘蔗专用版 服务启动中...
访问地址: http://localhost:5000
默认账号: admin / admin123
按 Ctrl+C 停止服务
```

### 第三步：启动前端（新终端）

```bash
# 进入前端目录
cd frontend

# 安装 Node 依赖（首次需要）
npm install

# 启动开发服务器（默认 http://localhost:3000）
npm run dev
```

访问 `http://localhost:3000` 即可进入系统。

---

## 五、开发模式 vs 生产模式

### 5.1 开发模式（日常开发）

前后端分别启动，Vite 提供热更新，API 通过代理转发到后端：

```bash
# 终端 1 — 后端
cd backend && python app.py

# 终端 2 — 前端
cd frontend && npm run dev
```

**端口说明：**

| 服务 | 地址 | 说明 |
|---|---|---|
| 前端 | `http://localhost:3000` | Vite 开发服务器 |
| 后端 API | `http://localhost:5000/api/*` | Flask REST API |
| 上传文件 | `http://localhost:5000/uploads/*` | 静态文件服务 |
| 地图瓦片 | `http://localhost:5000/tiles/*` | 离线瓦片服务 |

**代理配置（vite.config.js）：**
- `/api` → 转发到 `http://localhost:5000`
- `/uploads` → 转发到 `http://localhost:5000`

### 5.2 生产模式（打包部署）

```bash
# 1. 构建前端
cd frontend
npm run build

# 构建产物输出到 frontend/dist/

# 2. 启动后端（自动托管前端静态文件）
cd backend
python app.py
```

Flask 会检测到 `frontend/dist/` 目录存在，自动将所有路由指向前端入口（SPA 模式），无需额外配置 Nginx。

---

## 六、配置说明

### 6.1 后端配置（config.py）

所有配置均支持环境变量覆盖：

| 配置项 | 环境变量 | 默认值 | 说明 |
|---|---|---|---|
| `SECRET_KEY` | `SECRET_KEY` | `agrisage-cane-2024-secret-key` | Flask 密钥 |
| `SQLALCHEMY_DATABASE_URI` | `DATABASE_URL` | `sqlite:///data/agrisage.db` | 数据库连接 |
| `JWT_SECRET_KEY` | `JWT_SECRET_KEY` | `agrisage-jwt-secret-2024` | JWT 签名密钥 |
| `JWT_EXPIRATION_HOURS` | — | `720`（30天） | Token 有效期 |
| `UPLOAD_FOLDER` | — | `backend/uploads/` | 文件上传目录 |
| `MAX_CONTENT_LENGTH` | — | `16MB` | 最大上传大小 |

**修改示例（Windows PowerShell）：**

```powershell
$env:SECRET_KEY = "your-custom-secret-key"
$env:JWT_SECRET_KEY = "your-jwt-secret"
python app.py
```

### 6.2 前端配置（vite.config.js）

| 配置项 | 默认值 | 说明 |
|---|---|---|
| 开发服务器端口 | `3000` | 可在 `server.port` 中修改 |
| API 代理目标 | `http://localhost:5000` | 对应后端地址 |
| 路径别名 `@` | `src/` | 导入路径简写 |

---

## 七、数据库

### 7.1 默认数据库

首次启动时自动创建 SQLite 数据库文件：`backend/data/agrisage.db`

无需手动初始化数据库，`app.py` 中已包含 `db.create_all()` 调用。

### 7.2 数据表

| 表名 | 模型 | 说明 |
|---|---|---|
| users | User | 用户账户（含角色权限） |
| plots | Plot | 地块信息（含 GeoJSON 边界） |
| planting_cycles | PlantingCycle | 种植周期 |
| fertilization_records | FertilizationRecord | 施肥记录 |
| irrigation_records | IrrigationRecord | 灌溉记录 |
| pest_disease_records | PestDiseaseRecord | 病虫害记录 |
| harvest_records | HarvestRecord | 收割记录 |
| plot_images | PlotImage | 地块图片 |
| varieties | Variety | 品种图鉴 |
| sugar_factories | SugarFactory | 糖厂通讯录 |
| weather_stations | WeatherStation | 气象站 |
| soil_templates | SoilTemplate | 土壤模板 |

### 7.3 切换为 MySQL/PostgreSQL

修改环境变量即可切换数据库，例如 MySQL：

```powershell
$env:DATABASE_URL = "mysql+pymysql://user:pass@localhost:3306/agrisage"
python app.py
```

需要先安装对应驱动：`pip install pymysql` 或 `pip install psycopg2-binary`

---

## 八、用户角色与权限

| 角色 | 权限范围 |
|---|---|
| owner（户主） | 全部功能 + 用户管理 + 系统设置 |
| family（家庭成员） | 地块管理 + 农事记录 + 数据查看 |
| coop_admin（合作社管理员） | 地块管理 + 农事记录 + 数据导出 |
| technician（农技员） | 数据查看 + 农事记录录入 |

**注意：** 注册接口已关闭，新用户只能由户主通过「用户管理」页面添加。

---

## 九、天气功能

系统集成了**中国气象局公开 API**（weather.cma.cn），提供：

- 当前实时气象（温度/湿度/气压/风向/风速/降雨量/体感温度）
- 未来多日天气预报
- 气象预警信息
- 城市监测站搜索

**前提条件：** 后端服务器需能访问外网。纯离线环境下天气页面会显示错误提示。

---

## 十、地图功能

### 在线模式（默认）

优先加载高德卫星图（国内 CDN），失败时自动回退到本地离线瓦片。

### 离线模式

将瓦片文件放入 `frontend/public/tiles/{z}/{x}/{y}.png` 格式目录即可。

可使用项目中自带的 `backend/download_tiles.py` 工具下载指定区域的瓦片。

---

## 十一、常见问题

### Q: 前端启动报错 `npm install` 失败

确认 Node.js 版本 >= 18，尝试删除 `node_modules` 和 `package-lock.json` 后重新安装：
```bash
rm -rf node_modules package-lock.json
npm install
```

### Q: 后端启动报 `ModuleNotFoundError`

确保已在虚拟环境中执行了 `pip install -r requirements.txt`。

### Q: 前端页面空白，控制台报 CORS 错误

确认后端服务已启动且运行在 `http://localhost:5000`。

### Q: 登录后刷新页面丢失登录状态

正常现象。系统会在页面加载时自动从 localStorage 读取 token 并恢复用户信息。

### Q: 天气数据显示 502 错误

确认后端服务器能访问外网（中国气象局 API 需要 `User-Agent` 请求头）。

### Q: 地图不显示瓦片

检查网络连接。在线瓦片不可用时，确保 `frontend/public/tiles/` 下有离线瓦片文件。

---

## 十二、技术栈清单

### 后端

| 技术 | 用途 |
|---|---|
| Flask 3.0 | Web 框架 |
| Flask-SQLAlchemy 3.1 | ORM |
| Flask-CORS 4.0 | 跨域支持 |
| PyJWT 2.8 | JWT 身份认证 |
| requests 2.31 | HTTP 客户端（天气 API） |
| openpyxl 3.1 | Excel 导出 |
| reportlab 4.0 | PDF 导出 |
| waitress 3.0 | WSGI 生产服务器 |
| SQLite | 数据库（默认） |

### 前端

| 技术 | 用途 |
|---|---|
| Vue 3.4 | 渐进式框架 |
| Vite 5.1 | 构建工具 |
| Element Plus 2.5 | UI 组件库 |
| Pinia 2.1 | 状态管理 |
| Vue Router 4.3 | 路由 |
| ECharts 5.5 | 图表可视化 |
| Leaflet 1.9 | 地图引擎 |
| Axios 1.6 | HTTP 请求 |
| dayjs 1.11 | 日期处理 |
| SCSS | 样式预处理器 |
