import os
import sys
from flask import Flask, send_from_directory, abort
from config import Config, DATA_DIR, UPLOAD_DIR
from extensions import db, cors


def create_app(project_root=None):
    if project_root is None:
        if 'AGRISAGE_HOME' in os.environ:
            project_root = os.environ['AGRISAGE_HOME']
        elif getattr(sys, 'frozen', False):
            project_root = os.path.dirname(sys.executable)
        else:
            project_root = os.path.dirname(os.path.dirname(__file__))

    # PyInstaller: 数据文件（前端、瓦片等）在 _MEIPASS 临时目录
    resource_dir = os.environ.get('AGRISAGE_RESOURCE_DIR', project_root)

    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    cors.init_app(app, origins="*")

    # Ensure data and uploads directories exist
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Register blueprints
    from api import register_blueprints
    register_blueprints(app)

    # Create all database tables
    with app.app_context():
        from models import User, Plot, PlantingCycle, FertilizationRecord, IrrigationRecord, PestDiseaseRecord, HarvestRecord, PlotImage, Variety, SugarFactory, WeatherStation, SoilTemplate  # noqa: F401
        db.create_all()

        if User.query.count() == 0:
            admin = User(name='admin', role='owner', phone='13800000000')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

    # 离线地图瓦片服务
    tiles_dir = os.path.join(resource_dir, 'tiles')

    @app.route('/tiles/<int:z>/<int:x>/<int:y>.png')
    def serve_tile(z, x, y):
        tile_path = os.path.join(tiles_dir, str(z), str(x), f'{y}.png')
        if os.path.exists(tile_path):
            return send_from_directory(os.path.join(tiles_dir, str(z), str(x)), f'{y}.png')
        abort(404)

    # Serve frontend static files in production mode
    frontend_dist = os.path.join(resource_dir, 'frontend', 'dist')

    with open(os.path.join(project_root, 'agrisage_startup.log'), 'a', encoding='utf-8') as log:
        log.write(f'project_root = {project_root}\n')
        log.write(f'frontend_dist = {frontend_dist}\n')
        log.write(f'frontend_dist exists = {os.path.isdir(frontend_dist)}\n')
        if os.path.isdir(frontend_dist):
            log.write(f'frontend_dist contents = {os.listdir(frontend_dist)}\n')

    if os.path.isdir(frontend_dist):

        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def serve_frontend(path):
            # 优先匹配瓦片路由
            if path and os.path.exists(os.path.join(frontend_dist, path)):
                return send_from_directory(frontend_dist, path)
            return send_from_directory(frontend_dist, 'index.html')

    return app


def main():
    """使用 waitress WSGI 服务器启动，适合 Windows 本地/离线部署"""
    from waitress import serve
    app = create_app()
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    print(f'桂收 · 甘蔗专用版 服务启动中...')
    print(f'访问地址: http://localhost:{port}')
    print(f'默认账号: admin / admin123')
    print(f'按 Ctrl+C 停止服务')
    serve(app, host=host, port=port, threads=4)


if __name__ == '__main__':
    main()
