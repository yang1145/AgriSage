"""
AgriSage 启动器 — 基于 tkinter 的服务管理界面
作为打包 exe 的入口程序，提供服务启停、状态监控、浏览器启动等功能。
"""

import os
import sys
import time
import subprocess
import threading
import webbrowser
import psutil

# 确保项目路径正确
if getattr(sys, 'frozen', False):
    # Nuitka 打包后的路径
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # 开发环境：launcher.py 位于 backend/，BASE_DIR 为项目根目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 数据库路径（运行时自动创建）
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'agrisage.db')
UPLOADS_DIR = os.path.join(BASE_DIR, 'uploads')

# 服务配置
HOST = '0.0.0.0'
PORT = 5000
SERVICE_URL = f'http://localhost:{PORT}'


class AgriSageLauncher:
    """AgriSage 服务启动器"""

    def __init__(self):
        self.process: subprocess.Popen | None = None  # noqa: UP007
        self.running = False
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
        icon_path = os.path.join(BASE_DIR, 'backend', 'favicon.ico')
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass  # 部分系统不支持，忽略错误

        # 样式
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel',
                        background='#0a0f14', foreground='#00f0ff',
                        font=('Microsoft YaHei UI', 18, 'bold'))
        style.configure('Subtitle.TLabel',
                        background='#0a0f14', foreground='#8899aa',
                        font=('Microsoft YaHei UI', 9))
        style.configure('Info.TLabel',
                        background='#141c24', foreground='#e0e8f0',
                        font=('Consolas', 10), padding=6)
        style.configure('Value.TLabel',
                        background='#141c24', foreground='#00f0ff',
                        font=('Consolas', 11, 'bold'), padding=6)
        style.configure('Status.TLabel',
                        background='#0a0f14', foreground='#39ff14',
                        font=('Microsoft YaHei UI', 11, 'bold'))
        style.configure('StatusOff.TLabel',
                        background='#0a0f14', foreground='#ff6b35',
                        font=('Microsoft YaHei UI', 11, 'bold'))
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

        # 记录启动时间
        self._start_time: float | None = None  # noqa: UP007

    # ── 服务管理 ────────────────────────────────────

    def start_service(self):
        """启动 Flask 服务"""
        if self.running:
            return

        try:
            if getattr(sys, 'frozen', False):
                # 打包模式：直接以当前 exe 作为服务进程启动
                cmd = [sys.executable, '--service-mode']
                self.process = subprocess.Popen(cmd,
                                                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)  # type: ignore[attr-defined]
            else:
                # 开发模式：用 python 运行 app.py
                app_py = os.path.join(BASE_DIR, 'backend', 'app.py')
                cmd = [sys.executable, app_py]
                self.process = subprocess.Popen(cmd,
                                                cwd=os.path.dirname(app_py))  # noqa: S603

            self.running = True
            self._start_time = time.time()
            self._update_status(True)
            self._set_buttons(running=True)
        except Exception as e:
            self._show_error(f'启动失败: {e}')

    def stop_service(self):
        """停止服务"""
        if not self.running or not self.process:
            return

        try:
            # Windows 下终止进程树
            if sys.platform == 'win32':
                self.process.terminate()  # type: ignore[union-attr]
                try:
                    self.process.wait(timeout=5)  # type: ignore[union-attr]
                except subprocess.TimeoutExpired:
                    self.process.kill()  # type: ignore[union-attr]
            else:
                self.process.terminate()  # type: ignore[union-attr]
                self.process.wait()  # type: ignore[union-attr]

            self.running = False
            self.process = None
            self._update_status(False)
            self._set_buttons(running=False)
        except Exception as e:
            self._show_error(f'停止失败: {e}')

    def restart_service(self):
        """重启服务"""
        self.stop_service()
        time.sleep(1)
        self.start_service()

    def open_browser(self):
        """打开浏览器"""
        webbrowser.open(SERVICE_URL)

    # ── 状态更新 ────────────────────────────────────

    def _update_status(self, running: bool):
        if running:
            self.status_label.config(text='运行中', fg='#39ff14')
        else:
            self.status_label.config(text='已停止', fg='#ff6b35')
            self.runtime_label.config(text='运行时间: --')

    def _set_buttons(self, running: bool):
        state_normal = 'normal'
        state_disabled = 'disabled'

        if running:
            self.start_btn.config(state=state_disabled)
            self.stop_btn.config(state=state_normal)
            self.restart_btn.config(state=state_normal)
            self.browser_btn.config(state=state_normal)
        else:
            self.start_btn.config(state=state_normal)
            self.stop_btn.config(state=state_disabled)
            self.restart_btn.config(state=state_disabled)
            self.browser_btn.config(state=state_disabled)

    def _show_error(self, msg: str):
        import tkinter.messagebox
        tkinter.messagebox.showerror('错误', msg)

    # ── 监控线程 ────────────────────────────────────

    def _start_monitor(self):
        """启动后台监控线程，每 2 秒刷新一次数据"""
        thread = threading.Thread(target=self._monitor_loop, daemon=True)
        thread.start()

    def _monitor_loop(self):
        """监控循环"""
        while True:
            try:
                self._refresh_info()
            except Exception:
                pass
            time.sleep(2)

    def _refresh_info(self):
        """刷新监控数据"""
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

        # 检测进程是否意外退出
        if self.running and self.process:
            ret = self.process.poll()  # type: ignore[union-attr]
            if ret is not None:
                self.running = False
                self.process = None
                self.root.after(0, lambda: self._update_status(False))
                self.root.after(0, lambda: self._set_buttons(False))

    # ── 入口 ────────────────────────────────────────

    def run(self):
        """启动主循环"""
        self.root.mainloop()


def main():
    """入口函数：判断是启动 GUI 还是作为服务模式运行"""

    # 如果带 --service-mode 参数，则进入 Flask 服务模式
    if '--service-mode' in sys.argv:
        # 导入并启动 Flask 应用
        app_dir = os.path.join(BASE_DIR, 'backend')
        if app_dir not in sys.path:
            sys.path.insert(0, app_dir)
        from app import main as run_flask  # type: ignore[import-not-found]
        run_flask()
        return

    # 否则启动 tkinter GUI
    launcher = AgriSageLauncher()
    launcher.run()


if __name__ == '__main__':
    main()
