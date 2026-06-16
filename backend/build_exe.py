"""
Nuitka 打包配置文件
用于将 Flask 后端 + tkinter 启动器打包为 Windows exe
使用 --standalone 模式（目录模式），避免 --onefile 的 DLL 提取问题
"""

import os
import sys
import shutil
import glob as glob_mod

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(PROJECT_ROOT, 'backend')
FRONTEND_DIR = os.path.join(PROJECT_ROOT, 'frontend')
DIST_DIR = os.path.join(PROJECT_ROOT, 'dist')
AGRI_DIST = os.path.join(DIST_DIR, 'AgriSage')  # 最终发布目录名

# 移除旧构建
def clean():
    for d in [DIST_DIR]:
        if os.path.exists(d):
            shutil.rmtree(d)
    print('已清理 dist 目录')

# 构建前端
def build_frontend():
    print('正在构建前端...')
    os.chdir(FRONTEND_DIR)
    os.system('npm run build')
    print('前端构建完成')

# 检查依赖
def check_dependencies():
    """检查打包所需的额外依赖"""
    missing = []
    try:
        import nuitka  # noqa: F401
    except ImportError:
        missing.append('nuitka (pip install nuitka)')
    try:
        import psutil  # noqa: F401
    except ImportError:
        missing.append('psutil (pip install psutil)')
    if missing:
        print('缺少以下依赖:')
        for dep in missing:
            print(f'  - {dep}')
        print('\n请先安装后重试')
        sys.exit(1)

# Nuitka 打包（入口为 launcher.py）
def build_backend():
    print('正在打包后端...')
    os.chdir(BACKEND_DIR)

    # 构建 include-data-dir 参数列表（只包含存在的目录）
    include_data_dirs = [
        '--include-data-dir=../frontend/dist=frontend/dist',
        '--include-data-dir=../uploads=uploads',
    ]

    # tiles 目录存在时才添加
    tiles_src = os.path.join(PROJECT_ROOT, 'frontend', 'public', 'tiles')
    if os.path.exists(tiles_src):
        include_data_dirs.append('--include-data-dir=../frontend/public/tiles=tiles')

    nuitka_cmd = [
        sys.executable, '-m', 'nuitka',
        '--standalone',
        # 注意：去掉 --onefile，改用目录模式，避免 DLL 提取失败
        '--windows-console-mode=disable',   # tkinter GUI 不需要控制台窗口
        '--enable-plugin=tk-inter',          # 启用 tkinter 插件
        '--follow-imports',                  # 跟踪所有导入
        '--include-module=psutil',           # 显式包含 psutil
        '--include-package-data=psutil',     # 包含 psutil 数据文件
        f'--windows-icon-from-ico={os.path.join(BACKEND_DIR, "favicon.ico")}',  # 应用图标
    ] + include_data_dirs + [
        '--output-dir=../dist',
        '--output-filename=AgriSage.exe',
        'launcher.py'                        # 入口改为 launcher.py
    ]

    result = os.system(' '.join(nuitka_cmd))
    if result != 0:
        print('Nuitka 打包失败!')
        sys.exit(1)
    print('后端打包完成')

# 整理输出目录：把 Nuitka 生成的 .dist 目录内容整理为 AgriSage/
def organize_output():
    """将 Nuitka 输出整理为最终的发布目录结构"""
    print('正在整理输出目录...')

    # Nuitka --standalone 会生成 launcher.dist/ 目录
    nuitka_dist = None
    for item in os.listdir(DIST_DIR):
        item_path = os.path.join(DIST_DIR, item)
        if os.path.isdir(item_path) and item.endswith('.dist'):
            nuitka_dist = item_path
            break

    if not nuitka_dist:
        print(f'错误: 未找到 Nuitka 输出目录 ({DIST_DIR} 中没有 *.dist 文件夹)')
        sys.exit(1)

    # 创建最终发布目录
    if os.path.exists(AGRI_DIST):
        shutil.rmtree(AGRI_DIST)

    # 将 .dist 内容移动到 AgriSage/
    shutil.copytree(nuitka_dist, AGRI_DIST)

    # 删除原始的 .dist 和 .build 目录（Nuitka 构建中间产物）
    for item in os.listdir(DIST_DIR):
        item_path = os.path.join(DIST_DIR, item)
        if os.path.isdir(item_path) and (item.endswith('.dist') or item.endswith('.build')):
            shutil.rmtree(item_path)
        elif os.path.isfile(item_path) and item.endswith('.exe') and item != 'AgriSage.exe':
            try:
                os.remove(item_path)
            except Exception:
                pass

    print(f'发布目录: {AGRI_DIST}/')
    print('输出整理完成')

if __name__ == '__main__':
    print('=' * 50)
    print('AgriSage Nuitka 打包脚本')
    print('=' * 50)

    clean()
    check_dependencies()
    build_frontend()
    build_backend()
    organize_output()

    print('=' * 50)
    print(f'打包完成! 发布目录: {AGRI_DIST}/')
    print(f'运行方式: 双击 {AGRI_DIST}\\AgriSage.exe')
    print('=' * 50)
