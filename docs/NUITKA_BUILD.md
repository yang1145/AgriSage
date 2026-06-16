# Nuitka 打包说明

本项目使用 Nuitka 将 Flask 后端打包为独立的 Windows exe 可执行文件。

## 一、安装打包依赖

### 1. 安装 Nuitka

```powershell
pip install nuitka
```

### 2. 安装 MSVC 编译器（Windows 构建工具）

Nuitka 需要 C 编译器，推荐使用 Microsoft Visual C++。

**方式一：使用 winget（推荐）**
```powershell
winget install Microsoft.VisualStudio.2022.BuildTools
```
安装时选择 "使用 C++ 的桌面开发" 工作负载。

**方式二：使用 Chocolatey**
```powershell
choco install visualstudio2022buildtools
```

### 3. 安装前端构建工具

```powershell
# 在项目根目录
cd frontend
npm install
```

## 二、打包步骤

### 方式一：使用打包脚本（推荐）

```powershell
# 在项目根目录执行
python backend\build_exe.py
```

脚本会自动：
1. 清理旧的 dist 目录
2. 构建前端（npm run build）
3. 复制前端静态资源到 dist
4. 使用 Nuitka 打包后端为单文件 exe

### 方式二：手动打包

```powershell
# 1. 进入后端目录
cd backend

# 2. 构建前端
cd ..\frontend
npm run build
cd ..\backend

# 3. 使用 Nuitka 打包
python -m nuitka ^
    --standalone ^
    --onefile ^
    --windows-console-mode=attach ^
    --enable-console ^
    --follow-imports ^
    --include-data-dir=..\frontend\dist=frontend\dist ^
    --include-data-dir=..\frontend\public\tiles=tiles ^
    --include-data-dir=..\data=data ^
    --include-data-dir=..\uploads=uploads ^
    --output-dir=..\dist ^
    --output-filename=AgriSage.exe ^
    app.py
```

## 三、打包输出

打包完成后，exe 文件位于 `dist/AgriSage.exe`

同时复制到 dist 目录的还有：
- `frontend/dist/` — 前端静态文件
- `tiles/` — 离线地图瓦片（如有）
- `uploads/` — 上传文件目录

> 注意：`data/` 目录不会打包，程序首次运行时会自动创建空数据库文件。

## 四、运行 exe

双击 `AgriSage.exe` 即可启动服务：

```
桂收 · 甘蔗专用版 服务启动中...
访问地址: http://localhost:5000
默认账号: admin / admin123
按 Ctrl+C 停止服务
```

打开浏览器访问 `http://localhost:5000` 即可使用。

## 五、打包选项说明

| 选项 | 说明 |
|------|------|
| `--standalone` | 创建独立部署包，不依赖系统 Python |
| `--onefile` | 打包为单个 exe 文件 |
| `--onefile-windows-console-mode=attach` | 运行时附加到父控制台，避免重复弹窗 |
| `--follow-imports` | 自动包含所有导入的模块 |
| `--include-data-dir` | 包含额外数据目录 |
| `--windows-icon` | 可选：设置 exe 图标 |

## 六、自定义图标（可选）

如果需要自定义 exe 图标：

1. 准备 256x256 的 .ico 文件
2. 添加 `--windows-icon=path/to/icon.ico` 参数

## 七、常见问题

### Q: 打包失败，提示 "No compatible compiler found"

确保已安装 Visual Studio Build Tools 并选择 "使用 C++ 的桌面开发"。

### Q: 打包后运行 exe 报错 "ModuleNotFoundError"

某些动态导入的模块 Nuitka 无法自动发现。可以在命令行添加：
```
--include-module=模块名
```

### Q: 打包时间很长

Nuitka 首次打包需要编译所有 Python 模块，大约需要 5-15 分钟。后续增量打包会快很多。

### Q: exe 文件太大

正常现象。Nuitka 打包包含完整 Python 运行时和所有依赖，单文件模式还会压缩。体积通常在 30-80MB。

## 八、 Nuitka 性能优化（可选）

添加以下选项可以提升运行性能（但会延长编译时间）：

```powershell
--lto=yes           # 链接时优化
--windows-arch=x86_64 # 64位架构（如果不需要32位支持）
```
