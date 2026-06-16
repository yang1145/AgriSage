"""
Nuitka 打包配置文件
用于将 Flask 后端打包为 Windows exe
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

# Nuitka 打包后端
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
        '--windows-console-mode=attach',
        '--enable-console',
        '--follow-imports',
    ] + include_data_dirs + [
        '--output-dir=../dist',
        '--output-filename=AgriSage.exe',
        'app.py'
    ]

    result = os.system(' '.join(nuitka_cmd))
    if result != 0:
        print('Nuitka 打包失败!')
        sys.exit(1)
    print('后端打包完成')

# 复制前端静态资源到 dist
def copy_frontend_static():
    print('复制前端静态资源...')
    dist_fe = os.path.join(DIST_DIR, 'frontend')
    os.makedirs(dist_fe, exist_ok=True)

    # 复制 dist 到 backend 目录下的正确位置
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
    build_frontend()
    copy_frontend_static()
    build_backend()

    print('=' * 50)
    print('打包完成! 输出目录: dist/AgriSage.exe')
    print('=' * 50)
