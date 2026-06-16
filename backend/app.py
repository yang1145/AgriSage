import os
from flask import Flask, send_from_directory, abort
from config import Config, DATA_DIR, UPLOAD_DIR
from extensions import db, cors


def create_app():
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

    # 离线地图瓦片服务
    tiles_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'public', 'tiles')

    @app.route('/tiles/<int:z>/<int:x>/<int:y>.png')
    def serve_tile(z, x, y):
        tile_path = os.path.join(tiles_dir, str(z), str(x), f'{y}.png')
        if os.path.exists(tile_path):
            return send_from_directory(os.path.join(tiles_dir, str(z), str(x)), f'{y}.png')
        abort(404)

    # Serve frontend static files in production mode
    frontend_dist = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'dist')
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
