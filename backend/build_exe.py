"""
Nuitka 打包配置文件
用于将 Flask 后端 + tkinter 启动器打包为 Windows exe
"""

import os
import sys
import shutil

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(PROJECT_ROOT, 'backend')
FRONTEND_DIR = os.path.join(PROJECT_ROOT, 'frontend')
DIST_DIR = os.path.join(PROJECT_ROOT, 'dist')

# 移除旧构建
def clean():
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
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
        '--onefile',
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

# 复制前端静态资源到 dist
def copy_frontend_static():
    print('复制前端静态资源...')

    # 复制 dist 到 backend 目录下的正确位置
    dist_fe = os.path.join(DIST_DIR, 'frontend')
    os.makedirs(dist_fe, exist_ok=True)

    src_dist = os.path.join(FRONTEND_DIR, 'dist')
    if os.path.exists(src_dist):
        for item in os.listdir(src_dist):
            src = os.path.join(src_dist, item)
            dst = os.path.join(dist_fe, item)
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)

    # 复制 tiles
    src_tiles = os.path.join(FRONTEND_DIR, 'public', 'tiles')
    dst_tiles = os.path.join(DIST_DIR, 'tiles')
    if os.path.exists(src_tiles):
        if os.path.exists(dst_tiles):
            shutil.rmtree(dst_tiles)
        shutil.copytree(src_tiles, dst_tiles)

    # 复制 uploads 目录
    src_uploads = os.path.join(PROJECT_ROOT, 'uploads')
    dst_uploads = os.path.join(DIST_DIR, 'uploads')
    if os.path.exists(src_uploads):
        if os.path.exists(dst_uploads):
            shutil.rmtree(dst_uploads)
        shutil.copytree(src_uploads, dst_uploads)

    print('前端静态资源复制完成')

if __name__ == '__main__':
    print('=' * 50)
    print('AgriSage Nuitka 打包脚本')
    print('=' * 50)

    clean()
    check_dependencies()
    build_frontend()
    copy_frontend_static()
    build_backend()

    print('=' * 50)
    print('打包完成! 输出目录: dist/AgriSage.exe')
    print('=' * 50)
