from api.auth import auth_bp
from api.user import user_bp
from api.plot import plot_bp
from api.planting_cycle import cycle_bp
from api.farming_record import farming_bp
from api.dictionary import dict_bp
from api.image import image_bp
from api.export import export_bp
from api.system import system_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(plot_bp, url_prefix='/api/plots')
    app.register_blueprint(cycle_bp, url_prefix='/api/cycles')
    app.register_blueprint(farming_bp, url_prefix='/api/farming')
    app.register_blueprint(dict_bp, url_prefix='/api/dict')
    app.register_blueprint(image_bp, url_prefix='/api/images')
    app.register_blueprint(export_bp, url_prefix='/api/export')
    app.register_blueprint(system_bp, url_prefix='/api/system')
