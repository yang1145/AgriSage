# Nuitka 打包说明

本项目使用 Nuitka 将 Flask 后端 + tkinter 启动器打包为独立的 Windows exe 可执行文件。

## 一、安装打包依赖

### 1. 安装 Nuitka

```powershell
pip install nuitka
```

### 2. 安装 psutil（系统监控）

```powershell
pip install psutil
```

### 3. 安装 MSVC 编译器（Windows 构建工具）

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

### 4. 安装前端构建工具

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
2. 检查依赖是否完整
3. 构建前端（npm run build）
4. 复制前端静态资源到 dist
5. 使用 Nuitka 以 launcher.py 为入口打包为单文件 exe

### 方式二：手动打包

```powershell
# 1. 进入后端目录
cd backend

# 2. 构建前端
cd ..\frontend
npm run build
cd ..\backend

# 3. 使用 Nuitka 打包（入口为 launcher.py）
python -m nuitka ^
    --standalone ^
    --onefile ^
    --windows-console-mode=disable ^
    --enable-plugin=tk-inter ^
    --follow-imports ^
    --include-module=psutil ^
    --include-package-data=psutil ^
    --include-data-dir=..\frontend\dist=frontend\dist ^
    --include-data-dir=..\uploads=uploads ^
    --output-dir=..\dist ^
    --output-filename=AgriSage.exe ^
    launcher.py
```

## 三、打包输出

打包完成后，exe 文件位于 `dist/AgriSage.exe`

同时复制到 dist 目录的还有：
- `frontend/dist/` — 前端静态文件
- `tiles/` — 离线地图瓦片（如有）
- `uploads/` — 上传文件目录

> 注意：`data/` 目录不会打包，程序首次运行时会自动创建空数据库文件。

## 四、运行 exe

双击 `AgriSage.exe` 后会弹出 **tkinter 服务管理界面**：

| 功能 | 说明 |
|------|------|
| **服务状态** | 显示当前运行/停止状态 |
| **访问地址** | http://localhost:5000 |
| **CPU / 内存** | 实时显示系统资源占用（每 2 秒刷新） |
| **数据库信息** | 数据库大小与连接状态 |
| **运行时间** | 服务启动后的运行时长 |
| **启动/停止/重启** | 控制 Flask 服务生命周期 |
| **打开浏览器** | 一键在浏览器中打开系统 |

### 启动流程

1. 双击 `AgriSage.exe` → 弹出 tkinter 管理界面
2. 点击「启动服务」→ 启动 Flask 后端服务
3. 点击「打开浏览器访问」→ 自动打开浏览器进入系统
4. 默认账号: `admin` / `admin123`
5. 关闭窗口或点击「停止服务」→ 停止后端进程

## 五、打包选项说明

| 选项 | 说明 |
|------|------|
| `--standalone` | 创建独立部署包，不依赖系统 Python |
| `--onefile` | 打包为单个 exe 文件 |
| `--windows-console-mode=disable` | GUI 模式，不弹出控制台窗口 |
| `--enable-plugin=tk-inter` | 启用 tkinter 插件支持 |
| `--follow-imports` | 自动包含所有导入的模块 |
| `--include-module=psutil` | 显式包含 psutil 监控模块 |
| `--include-data-dir` | 包含额外数据目录 |
| `--windows-icon` | 可选：设置 exe 图标 |

## 六、自定义图标（可选）

如果需要自定义 exe 图标：

1. 准备 256x256 的 .ico 文件
2. 在 [build_exe.py](../backend/build_exe.py) 的 nuitka_cmd 中添加：
```
--windows-icon=path/to/icon.ico
```

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

正常现象。Nuitka 打包包含完整 Python 运行时、Flask、tkinter、psutil 和所有依赖，单文件模式还会压缩。体积通常在 40-100MB。

### Q: tkinter 窗口无法显示

确保 Windows 系统中已安装 tcl/tk（Python 自带）。如果使用精简版 Python，需要重新安装完整版。

### Q: CPU/内存数据不更新

psutil 需要在 Nuitka 中显式包含。确认 `build_exe.py` 中有 `--include-module=psutil` 参数。

## 八、Nuitka 性能优化（可选）

添加以下选项可以提升运行性能（但会延长编译时间）：

```powershell
--lto=yes           # 链接时优化
--windows-arch=x86_64 # 64位架构（如果不需要32位支持）
```
