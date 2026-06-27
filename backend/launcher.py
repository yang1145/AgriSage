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
DEFAULT_PORT = 5000


class AgriSageLauncher:
    """AgriSage 服务启动器 — 在线程内运行 Flask 服务，避免子进程依赖问题"""

    def __init__(self):
        self._server_thread = None
        self._server = None
        self.running = False
        self._start_time = None
        self.port = DEFAULT_PORT
        self._build_ui()
        self._start_monitor()

    # 仪表盘配色
    _GAUGE_TRACK = '#2a3a4a'
    _GAUGE_CPU_CLR = '#00f0ff'
    _GAUGE_MEM_CLR = '#39ff14'

    # ── UI 构建 ──────────────────────────────────────

    def _build_ui(self):
        import tkinter as tk
        from tkinter import ttk

        self.root = tk.Tk()
        self.root.title('桂收 · 甘蔗专用版')
        self.root.geometry('520x680')
        self.root.resizable(False, False)
        self.root.configure(bg='#0a0f14')
        self.root.overrideredirect(True)

        # 窗口居中
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - 520) // 2
        y = (sh - 680) // 2
        self.root.geometry(f'520x680+{x}+{y}')

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

        # ===== 自定义标题栏（可拖动 + 关闭按钮） =====
        self._drag_x = 0
        self._drag_y = 0

        titlebar = tk.Frame(self.root, bg='#0a0f14', height=40)
        titlebar.pack(fill='x')
        titlebar.pack_propagate(False)

        # 标题文字
        tk.Label(titlebar, text='桂收 · 甘蔗专用版', bg='#0a0f14',
                 fg='#00f0ff', font=('Microsoft YaHei UI', 10, 'bold')
                 ).pack(side='left', padx=14)

        # 关闭按钮
        close_btn = tk.Label(titlebar, text='✕', bg='#0a0f14', fg='#667788',
                             font=('Consolas', 14), cursor='hand2')
        close_btn.pack(side='right', padx=14)
        close_btn.bind('<Enter>', lambda e: close_btn.config(fg='#ff4444', bg='#3a1515'))
        close_btn.bind('<Leave>', lambda e: close_btn.config(fg='#667788', bg='#0a0f14'))
        close_btn.bind('<Button-1>', lambda e: self._on_close())

        # 标题栏拖动绑定
        titlebar.bind('<Button-1>', self._start_drag)
        titlebar.bind('<B1-Motion>', self._on_drag)
        for child in titlebar.winfo_children():
            if child is not close_btn:
                child.bind('<Button-1>', self._start_drag)
                child.bind('<B1-Motion>', self._on_drag)

        # ===== 标题区 =====
        title_frame = tk.Frame(self.root, bg='#0a0f14')
        title_frame.pack(fill='x', padx=24, pady=(8, 4))
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
        addr_right = tk.Frame(row2, bg='#141c24')
        addr_right.pack(side='right')
        tk.Label(addr_right, text='http://localhost:', bg='#141c24',
                 fg='#00f0ff', font=('Consolas', 10)).pack(side='left')
        self.port_var = tk.StringVar(value=str(self.port))
        self.port_entry = tk.Entry(addr_right, textvariable=self.port_var,
                                    width=6, bg='#1a2430', fg='#00f0ff',
                                    insertbackground='#00f0ff',
                                    font=('Consolas', 10),
                                    relief='flat', bd=0,
                                    disabledbackground='#1a2430',
                                    disabledforeground='#00f0ff')
        self.port_entry.pack(side='left')
        self.port_entry.bind('<Return>', lambda e: self._apply_port())
        self.port_entry.bind('<FocusOut>', lambda e: self._apply_port())

        # 分隔线
        sep = tk.Frame(card, height=1, bg='#2a3a4a')
        sep.pack(fill='x', padx=12, pady=8)

        # 监控信息标题
        tk.Label(card, text='系统监控', bg='#141c24', fg='#00f0ff',
                 font=('Microsoft YaHei UI', 10, 'bold')).pack(
                     anchor='w', padx=12)

        # ===== 仪表盘区域 =====
        gauge_frame = tk.Frame(card, bg='#141c24')
        gauge_frame.pack(fill='x', padx=12, pady=(8, 0))

        # CPU 仪表盘
        cpu_gauge_wrap = tk.Frame(gauge_frame, bg='#141c24')
        cpu_gauge_wrap.pack(side='left', expand=True)
        self.cpu_canvas = tk.Canvas(cpu_gauge_wrap, width=160, height=110,
                                     bg='#141c24', highlightthickness=0)
        self.cpu_canvas.pack()
        self.cpu_pct_label = tk.Label(cpu_gauge_wrap, text='0.0%',
                                       bg='#141c24', fg=self._GAUGE_CPU_CLR,
                                       font=('Consolas', 14, 'bold'))
        self.cpu_pct_label.pack()
        tk.Label(cpu_gauge_wrap, text='CPU 使用率', bg='#141c24',
                 fg='#8899aa', font=('Microsoft YaHei UI', 9)).pack()

        # 内存仪表盘
        mem_gauge_wrap = tk.Frame(gauge_frame, bg='#141c24')
        mem_gauge_wrap.pack(side='left', expand=True)
        self.mem_canvas = tk.Canvas(mem_gauge_wrap, width=160, height=110,
                                     bg='#141c24', highlightthickness=0)
        self.mem_canvas.pack()
        self.mem_pct_label = tk.Label(mem_gauge_wrap, text='0.0%',
                                       bg='#141c24', fg=self._GAUGE_MEM_CLR,
                                       font=('Consolas', 14, 'bold'))
        self.mem_pct_label.pack()
        self.mem_detail_label = tk.Label(mem_gauge_wrap, text='-- MB',
                                          bg='#141c24', fg='#8899aa',
                                          font=('Consolas', 9))
        self.mem_detail_label.pack()

        # 初始绘制仪表盘
        self._draw_gauge(self.cpu_canvas, 0, self._GAUGE_CPU_CLR)
        self._draw_gauge(self.mem_canvas, 0, self._GAUGE_MEM_CLR)

        # 数据库信息 + 运行时间
        info_row = tk.Frame(card, bg='#141c24')
        info_row.pack(fill='x', padx=12, pady=(6, 4))
        self.db_size_label = tk.Label(info_row, text='数据库: --',
                                       bg='#141c24', fg='#e0e8f0',
                                       font=('Consolas', 9))
        self.db_size_label.pack(side='left', expand=True, fill='x')
        self.db_conn_label = tk.Label(info_row, text='状态: 未创建',
                                       bg='#141c24', fg='#e0e8f0',
                                       font=('Consolas', 9))
        self.db_conn_label.pack(side='left', expand=True, fill='x')
        self.runtime_label = tk.Label(info_row, text='运行: --',
                                       bg='#141c24', fg='#8899aa',
                                       font=('Consolas', 9))
        self.runtime_label.pack(side='left', expand=True, fill='x')

        # 卡片底部间距
        tk.Frame(card, height=8, bg='#141c24').pack()

        # ===== 操作按钮区 =====
        btn_frame = tk.Frame(self.root, bg='#0a0f14')
        btn_frame.pack(fill='x', padx=24, pady=(4, 8))

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

        # ===== 底部账号信息卡片 =====
        acct_card = tk.Frame(self.root, bg='#111820',
                              highlightbackground='#2a3a4a',
                              highlightthickness=1)
        acct_card.pack(fill='x', padx=24, pady=(0, 16))

        acct_inner = tk.Frame(acct_card, bg='#111820')
        acct_inner.pack(fill='x', padx=16, pady=10)

        tk.Label(acct_inner, text='默认登录凭据', bg='#111820',
                 fg='#8899aa', font=('Microsoft YaHei UI', 9)).pack(
                     anchor='w')

        cred_row = tk.Frame(acct_inner, bg='#111820')
        cred_row.pack(fill='x', pady=(4, 0))

        # 账号
        user_frame = tk.Frame(cred_row, bg='#1a2430', padx=10, pady=4)
        user_frame.pack(side='left', expand=True, fill='x', padx=(0, 4))
        tk.Label(user_frame, text='账号', bg='#1a2430', fg='#667788',
                 font=('Microsoft YaHei UI', 8)).pack(anchor='w')
        tk.Label(user_frame, text='admin', bg='#1a2430', fg='#e0e8f0',
                 font=('Consolas', 11, 'bold')).pack(anchor='w')

        # 密码
        pwd_frame = tk.Frame(cred_row, bg='#1a2430', padx=10, pady=4)
        pwd_frame.pack(side='left', expand=True, fill='x', padx=(4, 0))
        tk.Label(pwd_frame, text='密码', bg='#1a2430', fg='#667788',
                 font=('Microsoft YaHei UI', 8)).pack(anchor='w')
        tk.Label(pwd_frame, text='admin123', bg='#1a2430', fg='#e0e8f0',
                 font=('Consolas', 11, 'bold')).pack(anchor='w')

    # ── 标题栏拖动 & 关闭 ────────────────────────────

    def _start_drag(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def _on_drag(self, event):
        x = self.root.winfo_x() + event.x - self._drag_x
        y = self.root.winfo_y() + event.y - self._drag_y
        self.root.geometry(f'+{x}+{y}')

    def _on_close(self):
        """关闭窗口前先停止服务"""
        if self.running:
            self.stop_service()
        self.root.destroy()

    # ── 仪表盘绘制 ──────────────────────────────────

    def _arc_points(self, cx, cy, r, start_deg, end_deg, segments=80):
        """生成弧线上的坐标点列表 [x0, y0, x1, y1, ...]"""
        import math
        pts = []
        for i in range(segments + 1):
            angle = math.radians(start_deg + (end_deg - start_deg) * i / segments)
            pts.append(cx + r * math.cos(angle))
            pts.append(cy - r * math.sin(angle))
        return pts

    def _draw_gauge(self, canvas, pct, color):
        """在 Canvas 上绘制半圆弧仪表盘，pct 范围 0~100"""
        import math

        canvas.delete('all')
        w, h = 160, 110
        cx, cy = w / 2, h - 10
        r = 58
        line_w = 10

        # 背景轨道（原点在左侧 180°，满刻度在右侧 0°，经过顶部 90°）
        track_pts = self._arc_points(cx, cy, r, 180, 0)
        canvas.create_line(*track_pts, fill=self._GAUGE_TRACK,
                           width=line_w, capstyle='round', smooth=False)

        # 前景弧（从左侧 180° 开始，顺时针画到对应百分比位置）
        if pct > 0:
            pct = min(pct, 100)
            fg_pts = self._arc_points(cx, cy, r, 180, 180 - pct / 100 * 180)
            canvas.create_line(*fg_pts, fill=color,
                               width=line_w, capstyle='round', smooth=False)

            # 末端小圆点
            end_angle = math.radians(180 - pct / 100 * 180)
            dot_x = cx + r * math.cos(end_angle)
            dot_y = cy - r * math.sin(end_angle)
            canvas.create_oval(dot_x - 5, dot_y - 5,
                               dot_x + 5, dot_y + 5,
                               fill=color, outline='')

        # 刻度标记 (0, 25, 50, 75, 100)
        for tick in [0, 25, 50, 75, 100]:
            tick_angle = math.radians(180 - tick / 100 * 180)
            inner_r = r - line_w / 2 - 4
            outer_r = r - line_w / 2 - 12
            x1 = cx + inner_r * math.cos(tick_angle)
            y1 = cy - inner_r * math.sin(tick_angle)
            x2 = cx + outer_r * math.cos(tick_angle)
            y2 = cy - outer_r * math.sin(tick_angle)
            canvas.create_line(x1, y1, x2, y2, fill='#4a5a6a', width=1)

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
        from waitress import create_server

        with open(os.path.join(BASE_DIR, 'agrisage_startup.log'), 'w', encoding='utf-8') as log:
            log.write(f'launcher BASE_DIR = {BASE_DIR}\n')
            log.write(f'sys.executable = {sys.executable}\n')
            log.write(f'sys.frozen = {getattr(sys, "frozen", None)}\n')

        app = create_app(project_root=BASE_DIR)
        print(f'桂收 · 甘蔗专用版 服务启动中...')
        print(f'访问地址: http://localhost:{self.port}')
        print(f'按「停止服务」按钮停止服务')
        self._server = create_server(app, host=HOST, port=self.port, threads=4)
        self._server.run()

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
            # 关闭 waitress 服务器
            if self._server is not None:
                self._server.close()
                self._server = None

            # 等待服务线程结束
            if self._server_thread is not None and self._server_thread.is_alive():
                self._server_thread.join(timeout=5)
            self._server_thread = None

            self.running = False
            self._start_time = None
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
        webbrowser.open(f'http://localhost:{self.port}')

    # ── 状态更新 ────────────────────────────────────

    def _update_status(self, running):
        if running:
            self.status_label.config(text='运行中', fg='#39ff14')
        else:
            self.status_label.config(text='已停止', fg='#ff6b35')
            self.runtime_label.config(text='运行: --')

    def _set_buttons(self, running):
        if running:
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.restart_btn.config(state='normal')
            self.browser_btn.config(state='normal')
            self.port_entry.config(state='disabled')
        else:
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            self.restart_btn.config(state='disabled')
            self.browser_btn.config(state='disabled')
            self.port_entry.config(state='normal')

    def _apply_port(self):
        """校验并应用端口号"""
        try:
            val = int(self.port_var.get())
            if not (1 <= val <= 65535):
                raise ValueError
            self.port = val
            self.port_var.set(str(val))
        except (ValueError, TypeError):
            self.port_var.set(str(self.port))

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
        self.root.after(0, lambda c=cpu: self._draw_gauge(
            self.cpu_canvas, c, self._GAUGE_CPU_CLR))
        self.root.after(0, lambda c=cpu: self.cpu_pct_label.config(
            text=f'{c:.1f}%'))

        # 内存使用
        mem = psutil.virtual_memory()
        mem_pct = mem.percent
        mem_mb = mem.used // (1024 * 1024)
        self.root.after(0, lambda p=mem_pct: self._draw_gauge(
            self.mem_canvas, p, self._GAUGE_MEM_CLR))
        self.root.after(0, lambda p=mem_pct: self.mem_pct_label.config(
            text=f'{p:.1f}%'))
        self.root.after(0, lambda mb=mem_mb: self.mem_detail_label.config(
            text=f'{mb} MB 已使用'))

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
                                 text=f'数据库: {s}'))
            self.root.after(0, lambda:
                             self.db_conn_label.config(
                                 text='状态: 已连接'))
        else:
            self.root.after(0, lambda:
                             self.db_size_label.config(
                                 text='数据库: --'))
            self.root.after(0, lambda:
                             self.db_conn_label.config(
                                 text='状态: 未创建'))

        # 运行时间
        if self.running and self._start_time:
            elapsed = int(time.time() - self._start_time)
            h, m, s = elapsed // 3600, (elapsed % 3600) // 60, elapsed % 60
            runtime_str = f'运行: {h:02d}:{m:02d}:{s:02d}'
            self.root.after(0, lambda r=runtime_str:
                             self.runtime_label.config(text=r))
        else:
            self.root.after(0, lambda:
                             self.runtime_label.config(text='运行: --'))

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
