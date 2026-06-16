import os

from flask import Blueprint, jsonify, current_app

from extensions import db
from models import Plot, PlantingCycle, User, Variety, SugarFactory
from api.auth import token_required, role_required

system_bp = Blueprint('system', __name__)


@system_bp.route('/stats', methods=['GET'])
@token_required
def get_system_stats(current_user):
    """获取系统数据量统计"""
    plot_count = Plot.query.filter_by(user_id=current_user.id).count() if current_user.role == 'owner' else Plot.query.count()
    cycle_count = PlantingCycle.query.count()
    user_count = User.query.count()
    variety_count = Variety.query.count()
    factory_count = SugarFactory.query.count()

    # 数据库文件信息
    db_uri = current_app.config['SQLALCHEMY_DATABASE_URI']
    db_size = 0
    if db_uri.startswith('sqlite:///'):
        db_path = db_uri.replace('sqlite:///', '')
        if not os.path.isabs(db_path):
            db_path = os.path.join(current_app.root_path, '..', db_path)
        if os.path.exists(db_path):
            db_size = os.path.getsize(db_path)

    return jsonify({
        'plot_count': plot_count,
        'cycle_count': cycle_count,
        'user_count': user_count,
        'variety_count': variety_count,
        'factory_count': factory_count,
        'db_size': db_size,
        'db_size_mb': round(db_size / (1024 * 1024), 2) if db_size else 0,
    }), 200


@system_bp.route('/seed', methods=['POST'])
@role_required('owner')
def reload_seed_data(current_user):
    """重新加载预置种子数据（仅户主）"""
    try:
        from seed.init_db import seed_varieties, seed_sugar_factories, seed_weather_stations, seed_soil_templates
        seed_varieties()
        seed_sugar_factories()
        seed_weather_stations()
        seed_soil_templates()
        return jsonify({'message': '预置数据更新成功'}), 200
    except Exception as e:
        return jsonify({'message': f'预置数据更新失败: {str(e)}'}), 500
