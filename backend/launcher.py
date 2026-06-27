"""
AgriSage 启动器 — 基于 tkinter 的服务管理界面
作为打包 exe 的入口程序，提供服务启停、状态监控、浏览器启动等功能。
"""

import os
import sys

# ═══════════════════════════════════════════════════════
# 早期诊断与路径配置（必须在任何第三方库导入之前）
# ═══════════════════════════════════════════════════════
_is_frozen = getattr(sys, 'frozen', False)

if _is_frozen:
    # PyInstaller: sys.frozen=True, sys._MEIPASS 指向临时解压目录
    # exe 所在目录为 BASE_DIR（数据文件、前端、数据库等在此）
    BASE_DIR = os.path.dirname(sys.executable)

    # 强制 numpy/OpenBLAS 使用通用 CPU 指令集
    # 避免在旧 CPU 上触发 0xC000001D (STATUS_ILLEGAL_INSTRUCTION)
    if 'OPENBLAS_CORETYPE' not in os.environ:
        os.environ['OPENBLAS_CORETYPE'] = 'CORE2'
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CRASH_LOG = os.path.join(BASE_DIR, 'agrisage_crash.log')

# 写入早期诊断日志（Python 已启动的证明）
try:
    with open(CRASH_LOG, 'w', encoding='utf-8') as f:
        f.write(f'AgriSage 早期诊断 - Python 已启动\n')
        f.write(f'BASE_DIR = {BASE_DIR}\n')
        f.write(f'_is_frozen = {_is_frozen}\n')
        f.write(f'sys.executable = {sys.executable}\n')
        f.write(f'sys.version = {sys.version}\n')
        f.write(f'os.getcwd = {os.getcwd()}\n')
except Exception:
    pass

# 数据库路径（运行时自动创建）
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'agrisage.db')
UPLOADS_DIR = os.path.join(BASE_DIR, 'uploads')

# 服务配置
HOST = '0.0.0.0'
PORT = 5000
SERVICE_URL = f'http://localhost:{PORT}'


class AgriSageLauncher:
    """AgriSage 服务启动器 — 在线程内运行 Flask 服务，避免子进程依赖问题"""

    def __init__(self):
        self._server_thread = None
        self.running = False
        self._start_time = None
        self._build_ui()
        self._start_monitor()

    # ── UI 构建 ──────────────────────────────────────

    def _build_ui(self):
        import tkinter as tk
        from tkinter import ttk

        self.root = tk.Tk()
        self.root.title('桂收 · 甘蔗专用版')
        self.root.geometry('480x520')
        self.root.resizable(False, False)
        self.root.configure(bg='#0a0f14')

        # 设置窗口图标
        icon_path = os.path.join(BASE_DIR, 'favicon.ico')
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass

        # 样式
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel',
                        background='#0a0f14', foreground='#00f0ff',
                        font=('Microsoft YaHei UI', 18, 'bold'))
        style.configure('Subtitle.TLabel',
                        background='#0a0f14', foreground='#8899aa',
                        font=('Microsoft YaHei UI', 9))
        style.configure('Card.TFrame', background='#141c24')
        style.configure('Action.TButton',
                        font=('Microsoft YaHei UI', 10),
                        padding=(20, 8))

        # ===== 标题区 =====
        title_frame = tk.Frame(self.root, bg='#0a0f14')
        title_frame.pack(fill='x', padx=24, pady=(20, 4))
        ttk.Label(title_frame, text='桂收 · 甘蔗专用版',
                  style='Title.TLabel').pack(anchor='w')
        ttk.Label(title_frame, text='AgriSage Cane Service Manager',
                  style='Subtitle.TLabel').pack(anchor='w')

        # ===== 状态卡片 =====
        card = ttk.Frame(self.root, style='Card.TFrame')
        card.pack(fill='x', padx=24, pady=12)

        # 状态指示
        row1 = tk.Frame(card, bg='#141c24')
        row1.pack(fill='x', padx=12, pady=(12, 4))
        tk.Label(row1, text='● 服务状态', bg='#141c24', fg='#8899aa',
                 font=('Microsoft YaHei UI', 10)).pack(side='left')
        self.status_label = tk.Label(row1, text='未启动', bg='#141c24',
                                      fg='#ff6b35',
                                      font=('Microsoft YaHei UI', 10, 'bold'))
        self.status_label.pack(side='right')

        # 地址信息
        row2 = tk.Frame(card, bg='#141c24')
        row2.pack(fill='x', padx=12, pady=4)
        tk.Label(row2, text='访问地址', bg='#141c24', fg='#8899aa',
                 font=('Microsoft YaHei UI', 10)).pack(side='left')
        tk.Label(row2, text=SERVICE_URL, bg='#141c24', fg='#00f0ff',
                 font=('Consolas', 10)).pack(side='right')

        # 分隔线
        sep = tk.Frame(card, height=1, bg='#2a3a4a')
        sep.pack(fill='x', padx=12, pady=8)

        # 监控信息标题
        tk.Label(card, text='系统监控', bg='#141c24', fg='#00f0ff',
                 font=('Microsoft YaHei UI', 10, 'bold')).pack(
                     anchor='w', padx=12)

        # CPU / 内存
        info_frame = tk.Frame(card, bg='#141c24')
        info_frame.pack(fill='x', padx=12, pady=(8, 4))
        self.cpu_label = tk.Label(info_frame, text='CPU: --%', bg='#141c24',
                                   fg='#e0e8f0', font=('Consolas', 10))
        self.cpu_label.pack(side='left', expand=True, fill='x')
        self.mem_label = tk.Label(info_frame, text='内存: -- MB', bg='#141c24',
                                   fg='#e0e8f0', font=('Consolas', 10))
        self.mem_label.pack(side='left', expand=True, fill='x')

        # 数据库信息
        db_frame = tk.Frame(card, bg='#141c24')
        db_frame.pack(fill='x', padx=12, pady=4)
        self.db_size_label = tk.Label(db_frame, text='数据库大小: --',
                                       bg='#141c24', fg='#e0e8f0',
                                       font=('Consolas', 10))
        self.db_size_label.pack(side='left', expand=True, fill='x')
        self.db_conn_label = tk.Label(db_frame, text='数据库: 未创建',
                                       bg='#141c24', fg='#e0e8f0',
                                       font=('Consolas', 10))
        self.db_conn_label.pack(side='left', expand=True, fill='x')

        # 运行时间
        self.runtime_label = tk.Label(card, text='运行时间: --',
                                       bg='#141c24', fg='#8899aa',
                                       font=('Consolas', 10))
        self.runtime_label.pack(anchor='w', padx=12, pady=(4, 12))

        # ===== 操作按钮区 =====
        btn_frame = tk.Frame(self.root, bg='#0a0f14')
        btn_frame.pack(fill='x', padx=24, pady=(4, 16))

        # 第一行：启动 / 停止 / 重启
        row_btn1 = tk.Frame(btn_frame, bg='#0a0f14')
        row_btn1.pack(fill='x', pady=4)

        self.start_btn = tk.Button(row_btn1, text='▶ 启动服务',
                                    command=self.start_service,
                                    bg='#1a3a2a', fg='#39ff14',
                                    activebackground='#2a5a3a',
                                    activeforeground='#39ff14',
                                    font=('Microsoft YaHei UI', 10, 'bold'),
                                    width=12, relief='flat', cursor='hand2',
                                    bd=0)
        self.start_btn.pack(side='left', expand=True, padx=(0, 4))

        self.stop_btn = tk.Button(row_btn1, text='■ 停止服务',
                                   command=self.stop_service,
                                   bg='#3a2020', fg='#ff6b35',
                                   activebackground='#5a3030',
                                   activeforeground='#ff6b35',
                                   font=('Microsoft YaHei UI', 10, 'bold'),
                                   width=12, relief='flat', cursor='hand2',
                                   bd=0, state='disabled')
        self.stop_btn.pack(side='left', expand=True, padx=4)

        self.restart_btn = tk.Button(row_btn1, text='↻ 重启服务',
                                     command=self.restart_service,
                                     bg='#2a2a3a', fg='#00f0ff',
                                     activebackground='#3a3a5a',
                                     activeforeground='#00f0ff',
                                     font=('Microsoft YaHei UI', 10, 'bold'),
                                     width=12, relief='flat', cursor='hand2',
                                     bd=0, state='disabled')
        self.restart_btn.pack(side='left', expand=True, padx=(4, 0))

        # 第二行：打开浏览器
        self.browser_btn = tk.Button(btn_frame, text='🌐 打开浏览器访问',
                                      command=self.open_browser,
                                      bg='#1a2040', fg='#8090ff',
                                      activebackground='#2a3060',
                                      activeforeground='#8090ff',
                                      font=('Microsoft YaHei UI', 10),
                                      width=40, relief='flat', cursor='hand2',
                                      bd=0, state='disabled')
        self.browser_btn.pack(pady=8)

        # 底部提示
        tip = tk.Label(self.root,
                       text='默认账号: admin  |  密码: admin123',
                       bg='#0a0f14', fg='#556677',
                       font=('Microsoft YaHei UI', 9))
        tip.pack(pady=(0, 12))

    # ── 服务管理（线程内启动，无需子进程） ────────────

    def _run_flask_server(self):
        """在后台线程中启动 Flask waitress 服务器"""
        import threading
        os.environ['AGRISAGE_HOME'] = BASE_DIR

        # 确保 backend 目录在 sys.path 中
        if not _is_frozen:
            backend_dir = os.path.join(BASE_DIR, 'backend')
            if backend_dir not in sys.path:
                sys.path.insert(0, backend_dir)

        # PyInstaller: 数据文件在 sys._MEIPASS 临时目录中
        # 需要告诉 app.py 从 _MEIPASS 查找前端等资源
        if _is_frozen and hasattr(sys, '_MEIPASS'):
            os.environ['AGRISAGE_RESOURCE_DIR'] = sys._MEIPASS

        from app import create_app  # type: ignore[import-not-found]
        from waitress import serve

        with open(os.path.join(BASE_DIR, 'agrisage_startup.log'), 'w', encoding='utf-8') as log:
            log.write(f'launcher BASE_DIR = {BASE_DIR}\n')
            log.write(f'sys.executable = {sys.executable}\n')
            log.write(f'sys.frozen = {getattr(sys, "frozen", None)}\n')

        app = create_app(project_root=BASE_DIR)
        print(f'桂收 · 甘蔗专用版 服务启动中...')
        print(f'访问地址: http://localhost:{PORT}')
        print(f'按「停止服务」按钮停止服务')
        serve(app, host=HOST, port=PORT, threads=4)

    def start_service(self):
        """启动 Flask 服务（在线程中）"""
        import threading
        if self.running:
            return

        try:
            self._server_thread = threading.Thread(
                target=self._run_flask_server,
                daemon=True,
            )
            self._server_thread.start()

            self.running = True
            import time
            self._start_time = time.time()
            self._update_status(True)
            self._set_buttons(running=True)
        except Exception as e:
            self._show_error(f'启动失败: {e}')

    def stop_service(self):
        """停止服务"""
        if not self.running:
            return

        try:
            self.running = False
            self._server_thread = None
            self._update_status(False)
            self._set_buttons(running=False)
        except Exception as e:
            self._show_error(f'停止失败: {e}')

    def restart_service(self):
        """重启服务"""
        import time
        self.stop_service()
        time.sleep(1.5)
        self.start_service()

    def open_browser(self):
        """打开浏览器"""
        import webbrowser
        webbrowser.open(SERVICE_URL)

    # ── 状态更新 ────────────────────────────────────

    def _update_status(self, running):
        if running:
            self.status_label.config(text='运行中', fg='#39ff14')
        else:
            self.status_label.config(text='已停止', fg='#ff6b35')
            self.runtime_label.config(text='运行时间: --')

    def _set_buttons(self, running):
        if running:
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.restart_btn.config(state='normal')
            self.browser_btn.config(state='normal')
        else:
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            self.restart_btn.config(state='disabled')
            self.browser_btn.config(state='disabled')

    def _show_error(self, msg):
        import tkinter.messagebox
        tkinter.messagebox.showerror('错误', msg)

    # ── 监控线程 ────────────────────────────────────

    def _start_monitor(self):
        import threading
        thread = threading.Thread(target=self._monitor_loop, daemon=True)
        thread.start()

    def _monitor_loop(self):
        import time
        while True:
            try:
                self._refresh_info()
            except Exception:
                pass
            time.sleep(2)

    def _refresh_info(self):
        """刷新监控数据"""
        import psutil
        import time

        # CPU 使用率
        cpu = psutil.cpu_percent(interval=None)
        self.root.after(0, lambda: self.cpu_label.config(
            text=f'CPU: {cpu:.1f}%'))

        # 内存使用
        mem = psutil.virtual_memory()
        mem_mb = mem.used // (1024 * 1024)
        mem_pct = mem.percent
        self.root.after(0, lambda: self.mem_label.config(
            text=f'内存: {mem_mb}MB ({mem_pct:.0f}%)'))

        # 数据库信息
        if os.path.exists(DB_PATH):
            size_bytes = os.path.getsize(DB_PATH)
            if size_bytes < 1024 * 1024:
                size_str = f'{size_bytes / 1024:.1f} KB'
            elif size_bytes < 1024 * 1024 * 1024:
                size_str = f'{size_bytes / (1024 * 1024):.1f} MB'
            else:
                size_str = f'{size_bytes / (1024 ** 3):.2f} GB'
            self.root.after(0, lambda s=size_str:
                             self.db_size_label.config(
                                 text=f'数据库大小: {s}'))
            self.root.after(0, lambda:
                             self.db_conn_label.config(
                                 text='数据库: 已连接 (SQLite)'))
        else:
            self.root.after(0, lambda:
                             self.db_size_label.config(
                                 text='数据库大小: --'))
            self.root.after(0, lambda:
                             self.db_conn_label.config(
                                 text='数据库: 未创建'))

        # 运行时间
        if self.running and self._start_time:
            elapsed = int(time.time() - self._start_time)
            h, m, s = elapsed // 3600, (elapsed % 3600) // 60, elapsed % 60
            runtime_str = f'运行时间: {h:02d}:{m:02d}:{s:02d}'
            self.root.after(0, lambda r=runtime_str:
                             self.runtime_label.config(text=r))

    # ── 入口 ────────────────────────────────────────

    def run(self):
        """启动主循环"""
        self.root.mainloop()


def main():
    """入口函数：启动 tkinter GUI 界面"""
    import traceback

    # 逐个导入并记录，定位哪个模块导入失败
    try:
        with open(CRASH_LOG, 'a', encoding='utf-8') as f:
            f.write('\n--- main() 开始执行 ---\n')
    except Exception:
        pass

    try:
        with open(CRASH_LOG, 'a', encoding='utf-8') as f:
            f.write('导入 tkinter...\n')
        import tkinter  # noqa: F401

        with open(CRASH_LOG, 'a', encoding='utf-8') as f:
            f.write('导入 psutil...\n')
        import psutil  # noqa: F401

        with open(CRASH_LOG, 'a', encoding='utf-8') as f:
            f.write('导入完成，创建 UI...\n')

        launcher = AgriSageLauncher()

        with open(CRASH_LOG, 'a', encoding='utf-8') as f:
            f.write('UI 创建成功，进入主循环\n')
        # 清除崩溃日志（启动成功后无意义）
        try:
            os.remove(CRASH_LOG)
        except Exception:
            pass

        launcher.run()

    except Exception as e:
        # 写入崩溃日志
        try:
            with open(CRASH_LOG, 'a', encoding='utf-8') as f:
                f.write(f'\n!!! 启动崩溃 !!!\n')
                f.write(f'{traceback.format_exc()}\n')
        except Exception:
            pass
        # 弹窗提示用户
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror('桂收 · 启动失败',
                                 f'程序启动时发生错误:\n\n{e}\n\n'
                                 f'详细信息已保存到:\n{CRASH_LOG}')
        except Exception:
            pass


if __name__ == '__main__':
    main()
