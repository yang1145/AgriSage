"""
Nuitka 打包配置文件
用于将 Flask 后端 + tkinter 启动器打包为 Windows exe
使用 --standalone 模式（目录模式），避免 --onefile 的 DLL 提取问题
支持一键生成 Inno Setup 安装包
"""

import os
import sys
import shutil

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(PROJECT_ROOT, 'backend')
FRONTEND_DIR = os.path.join(PROJECT_ROOT, 'frontend')
DIST_DIR = os.path.join(PROJECT_ROOT, 'dist')
AGRI_DIST = os.path.join(DIST_DIR, 'AgriSage')  # 最终发布目录名
INSTALLER_DIR = os.path.join(PROJECT_ROOT, 'installer')  # 安装包输出目录

# 移除旧构建
def clean():
    for d in [DIST_DIR]:
        if os.path.exists(d):
            try:
                shutil.rmtree(d)
                print('已清理 dist 目录')
            except PermissionError:
                print(f'警告: 无法删除 {d}（文件被占用，请关闭 AgriSage.exe 后重试）')
                sys.exit(1)

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
        '--windows-console-mode=disable',
        '--enable-plugin=tk-inter',
        '--follow-imports',
        '--include-module=app',
        '--include-module=psutil',
        '--include-package-data=psutil',
        f'--windows-icon-from-ico={os.path.join(BACKEND_DIR, "favicon.ico")}',
    ] + include_data_dirs + [
        '--output-dir=../dist',
        '--output-filename=AgriSage.exe',
        'launcher.py'
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


def build_installer():
    """使用 Inno Setup 生成安装包"""
    iss_file = os.path.join(BACKEND_DIR, 'setup.iss')
    if not os.path.exists(iss_file):
        print('警告: 未找到 setup.iss，跳过安装包生成')
        return

    print('正在生成安装包...')

    # 查找 Inno Setup 编译器 (ISCC)
    iscc_paths = [
        r'C:\Program Files (x86)\Inno Setup 6\ISCC.exe',
        r'C:\Program Files\Inno Setup 6\ISCC.exe',
    ]
    iscc = None
    for p in iscc_paths:
        if os.path.exists(p):
            iscc = p
            break

    if not iscc:
        # 尝试从 PATH 查找
        import shutil as sh
        iscc = sh.which('iscc')

    if not iscc:
        print('警告: 未找到 Inno Setup 编译器 (ISCC.exe)，跳过安装包生成')
        print('请安装 Inno Setup 6: https://jrsoftware.org/isdl.php')
        print(f'或手动编译: iscc "{iss_file}"')
        return

    # 创建安装包输出目录
    os.makedirs(INSTALLER_DIR, exist_ok=True)

    import subprocess
    result = subprocess.run([iscc, iss_file], cwd=PROJECT_ROOT)
    if result.returncode != 0:
        print('Inno Setup 编译失败!')
        sys.exit(1)

    # 列出生成的安装包
    installer_files = list(os.listdir(INSTALLER_DIR))
    if installer_files:
        print(f'安装包已生成:')
        for f in installer_files:
            full_path = os.path.join(INSTALLER_DIR, f)
            size_mb = os.path.getsize(full_path) / (1024 * 1024)
            print(f'  {f} ({size_mb:.1f} MB)')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='AgriSage Nuitka 打包脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python build_exe.py                       # 完整构建（前端 + 后端）
  python build_exe.py --no-clean            # 增量构建，不清理 dist
  python build_exe.py --skip-frontend       # 跳过前端构建，仅打包后端
  python build_exe.py -sf -i                # 跳过前端 + 生成安装包
  python build_exe.py --installer           # 仅在后端打包后生成安装包
        ''')
    parser.add_argument('--skip-frontend', '-sf', dest='skip_frontend',
                        action='store_true', help='跳过前端构建（使用已有的 frontend/dist/）')
    parser.add_argument('--installer', '-i', dest='build_installer_flag',
                        action='store_true', help='同时生成 Inno Setup 安装包')
    parser.add_argument('--no-clean', '-nc', dest='no_clean',
                        action='store_true', help='不清理 dist 目录（增量构建）')
    args = parser.parse_args()

    print('=' * 50)
    print('AgriSage 打包脚本')
    print('=' * 50)

    if not args.no_clean:
        clean()
    else:
        print('跳过清理 dist 目录')

    check_dependencies()

    if not args.skip_frontend:
        build_frontend()
    else:
        print('跳过前端构建')

    build_backend()
    organize_output()

    if args.build_installer_flag:
        build_installer()

    print()
    print('=' * 50)
    print('全部完成!')
    print()
    print(f'  发布目录: {AGRI_DIST}/')
    print(f'  运行方式: 双击 {AGRI_DIST}\\AgriSage.exe')
    print()

    installer_files = os.listdir(INSTALLER_DIR) if os.path.exists(INSTALLER_DIR) else []
    if installer_files:
        print(f'  安装包: {INSTALLER_DIR}/')
        for f in installer_files:
            print(f'           - {f}')

    print('=' * 50)
