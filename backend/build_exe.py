"""
AgriSage 打包脚本
使用 PyInstaller 将 Flask 后端 + tkinter 启动器打包为 Windows exe
支持一键生成 Inno Setup 安装包
"""

import os
import sys
import shutil
import subprocess

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(PROJECT_ROOT, 'backend')
FRONTEND_DIR = os.path.join(PROJECT_ROOT, 'frontend')
DIST_DIR = os.path.join(PROJECT_ROOT, 'dist')
AGRI_DIST = os.path.join(DIST_DIR, 'AgriSage')  # 最终发布目录名
INSTALLER_DIR = os.path.join(PROJECT_ROOT, 'installer')  # 安装包输出目录


def clean():
    """移除旧构建"""
    for d in [DIST_DIR]:
        if os.path.exists(d):
            try:
                shutil.rmtree(d)
                print('已清理 dist 目录')
            except PermissionError:
                print(f'警告: 无法删除 {d}（文件被占用，请关闭 AgriSage.exe 后重试）')
                sys.exit(1)


def build_frontend():
    """构建前端"""
    print('正在构建前端...')
    subprocess.run(['npm', 'run', 'build'], cwd=FRONTEND_DIR, check=True)
    print('前端构建完成')


def check_dependencies():
    """检查打包所需的依赖"""
    missing = []
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        missing.append('pyinstaller (pip install pyinstaller)')
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


def build_backend():
    """PyInstaller 打包（入口为 launcher.py）"""
    print('正在打包后端（PyInstaller）...')
    os.chdir(BACKEND_DIR)

    # 构建 --add-data 参数列表
    add_data_args = []

    # 前端构建产物
    frontend_dist = os.path.join(PROJECT_ROOT, 'frontend', 'dist')
    if os.path.isdir(frontend_dist):
        add_data_args.append(f'--add-data={os.path.abspath(frontend_dist)};frontend/dist')

    # 上传目录（空目录占位）
    uploads_dir = os.path.join(PROJECT_ROOT, 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    # 创建一个占位文件确保空目录能被打包
    placeholder = os.path.join(uploads_dir, '.gitkeep')
    if not os.path.exists(placeholder):
        with open(placeholder, 'w') as f:
            pass
    add_data_args.append(f'--add-data={os.path.abspath(uploads_dir)};uploads')

    # tiles 目录（离线地图瓦片，可能不存在）
    tiles_src = os.path.join(PROJECT_ROOT, 'frontend', 'public', 'tiles')
    if os.path.isdir(tiles_src):
        add_data_args.append(f'--add-data={os.path.abspath(tiles_src)};tiles')

    # 图标（必须使用绝对路径，PyInstaller 相对路径基于 workpath 解析）
    icon_path = os.path.abspath(os.path.join(BACKEND_DIR, 'favicon.ico'))
    if not os.path.isfile(icon_path):
        icon_path = None

    # 隐式导入（PyInstaller 无法自动发现的模块）
    hidden_imports = [
        '--hidden-import=app',
        '--hidden-import=api',
        '--hidden-import=api.auth',
        '--hidden-import=api.user',
        '--hidden-import=api.plot',
        '--hidden-import=api.planting_cycle',
        '--hidden-import=api.farming_record',
        '--hidden-import=api.dictionary',
        '--hidden-import=api.image',
        '--hidden-import=api.export',
        '--hidden-import=api.system',
        '--hidden-import=models',
        '--hidden-import=models.user',
        '--hidden-import=models.plot',
        '--hidden-import=models.planting_cycle',
        '--hidden-import=models.farming_record',
        '--hidden-import=models.plot_image',
        '--hidden-import=models.dictionary',
        '--hidden-import=utils',
        '--hidden-import=utils.area_calc',
        '--hidden-import=utils.export_helpers',
        '--hidden-import=seed',
        '--hidden-import=seed.init_db',
        '--hidden-import=seed.soil_templates',
        '--hidden-import=seed.sugar_factories',
        '--hidden-import=seed.varieties',
        '--hidden-import=seed.weather_stations',
        '--hidden-import=psutil',
        '--hidden-import=waitress',
        '--hidden-import=flask',
        '--hidden-import=flask_sqlalchemy',
        '--hidden-import=flask_cors',
        '--hidden-import=openpyxl',
        '--hidden-import=reportlab',
        '--hidden-import=jwt',
        '--hidden-import=numpy',
        '--hidden-import=sqlalchemy.dialects.sqlite',
        '--hidden-import=sqlalchemy.sql.default_comparator',
    ]

    pyinstaller_cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--name=AgriSage',
        '--noconfirm',
        '--windowed',               # 不显示控制台
    ]
    if icon_path:
        pyinstaller_cmd.append(f'--icon={icon_path}')
    pyinstaller_cmd += add_data_args + hidden_imports + [
        'launcher.py'
    ]

    print(f'  命令: {" ".join(pyinstaller_cmd[:6])} ...')
    result = subprocess.run(pyinstaller_cmd)
    if result.returncode != 0:
        print('PyInstaller 打包失败!')
        sys.exit(1)
    print('后端打包完成')


def organize_output():
    """整理 PyInstaller 输出为最终发布目录"""
    print('正在整理输出目录...')

    # PyInstaller 默认输出在 backend/dist/AgriSage/
    pyinstaller_dist = os.path.join(BACKEND_DIR, 'dist', 'AgriSage')
    if not os.path.isdir(pyinstaller_dist):
        print(f'错误: 未找到 PyInstaller 输出目录 {pyinstaller_dist}')
        sys.exit(1)

    # 复制到项目根目录的 dist/AgriSage/
    if os.path.exists(AGRI_DIST):
        shutil.rmtree(AGRI_DIST)
    os.makedirs(os.path.dirname(AGRI_DIST), exist_ok=True)
    shutil.copytree(pyinstaller_dist, AGRI_DIST)

    # 补充 VC++ 运行时 DLL（PyInstaller 可能遗漏）
    _patch_missing_vcruntime()

    # 复制调试启动脚本
    debug_cmd = os.path.join(BACKEND_DIR, 'debug_launch.cmd')
    if os.path.isfile(debug_cmd):
        shutil.copy2(debug_cmd, os.path.join(AGRI_DIST, 'debug_launch.cmd'))

    # 复制 favicon.ico 到根目录（launcher 引用）
    icon_src = os.path.join(BACKEND_DIR, 'favicon.ico')
    if os.path.isfile(icon_src):
        shutil.copy2(icon_src, os.path.join(AGRI_DIST, 'favicon.ico'))

    # 清理 PyInstaller 构建中间产物（backend/dist/ 和 backend/build/）
    for cleanup in [
        os.path.join(BACKEND_DIR, 'dist'),
        os.path.join(BACKEND_DIR, 'build'),
        os.path.join(BACKEND_DIR, 'AgriSage.spec'),
    ]:
        if os.path.isdir(cleanup):
            shutil.rmtree(cleanup)
        elif os.path.isfile(cleanup):
            os.remove(cleanup)

    print(f'发布目录: {AGRI_DIST}/')
    print('输出整理完成')


def _patch_missing_vcruntime():
    """检查并补充 VC++ 运行时 DLL（msvcp140.dll 等）"""
    required_dlls = ['msvcp140.dll', 'vcruntime140.dll', 'vcruntime140_1.dll']
    missing = [d for d in required_dlls if not os.path.isfile(os.path.join(AGRI_DIST, d))]

    if not missing:
        return

    # 从 numpy.libs 子目录中查找带 hash 后缀的同名 DLL
    numpy_libs = os.path.join(AGRI_DIST, 'numpy.libs')
    for dll_name in list(missing):
        if os.path.isdir(numpy_libs):
            for f in os.listdir(numpy_libs):
                base = dll_name.replace('.dll', '')
                if f.startswith(base + '-') and f.endswith('.dll'):
                    src = os.path.join(numpy_libs, f)
                    dst = os.path.join(AGRI_DIST, dll_name)
                    shutil.copy2(src, dst)
                    print(f'  已补充: {dll_name} (来源: numpy.libs/{f})')
                    missing.remove(dll_name)
                    break

    # 仍缺失的 DLL，从系统目录复制
    if missing:
        sys_dir = os.path.join(os.environ.get('SystemRoot', r'C:\Windows'), 'System32')
        for dll_name in missing:
            sys_dll = os.path.join(sys_dir, dll_name)
            if os.path.isfile(sys_dll):
                dst = os.path.join(AGRI_DIST, dll_name)
                shutil.copy2(sys_dll, dst)
                print(f'  已补充: {dll_name} (来源: System32)')
            else:
                print(f'  警告: 未找到 {dll_name}，目标机器可能需要安装 VC++ 运行时')


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
        iscc = shutil.which('iscc')

    if not iscc:
        print('警告: 未找到 Inno Setup 编译器 (ISCC.exe)，跳过安装包生成')
        print('请安装 Inno Setup 6: https://jrsoftware.org/isdl.php')
        print(f'或手动编译: iscc "{iss_file}"')
        return

    os.makedirs(INSTALLER_DIR, exist_ok=True)

    result = subprocess.run([iscc, iss_file], cwd=PROJECT_ROOT)
    if result.returncode != 0:
        print('Inno Setup 编译失败!')
        sys.exit(1)

    installer_files = list(os.listdir(INSTALLER_DIR))
    if installer_files:
        print('安装包已生成:')
        for f in installer_files:
            full_path = os.path.join(INSTALLER_DIR, f)
            size_mb = os.path.getsize(full_path) / (1024 * 1024)
            print(f'  {f} ({size_mb:.1f} MB)')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='AgriSage PyInstaller 打包脚本',
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
    print('AgriSage 打包脚本 (PyInstaller)')
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
