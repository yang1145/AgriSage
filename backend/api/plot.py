from flask import Blueprint, request, jsonify

from extensions import db
from models import Plot, PlantingCycle, PlotImage
from api.auth import token_required, role_required
from utils.area_calc import calculate_area_from_geojson

plot_bp = Blueprint('plot', __name__)


@plot_bp.route('/', methods=['GET'])
@token_required
def list_plots(current_user):
    """获取地块列表。支持按名称、状态、面积范围筛选"""
    if current_user.role == 'owner':
        query = Plot.query.filter_by(user_id=current_user.id)
    elif current_user.role == 'coop_admin':
        from models import User
        member_ids = [u.id for u in User.query.filter_by(cooperative_id=current_user.cooperative_id).all()]
        query = Plot.query.filter(Plot.user_id.in_(member_ids)) if member_ids else Plot.query.filter_by(id=-1)
    elif current_user.role == 'technician':
        query = Plot.query.filter_by(user_id=current_user.id)
    else:
        query = Plot.query.filter_by(user_id=current_user.id)

    # 搜索筛选
    name_kw = request.args.get('name')
    if name_kw:
        query = query.filter(Plot.name.contains(name_kw))

    status_filter = request.args.get('status')
    if status_filter:
        query = query.filter_by(status=status_filter)

    min_area = request.args.get('min_area', type=float)
    if min_area is not None:
        query = query.filter(Plot.area >= min_area)

    max_area = request.args.get('max_area', type=float)
    if max_area is not None:
        query = query.filter(Plot.area <= max_area)

    plots = query.all()

    result = []
    for p in plots:
        plot_data = p.to_dict()
        plot_data['planting_cycle_count'] = p.planting_cycles.count()
        plot_data['image_count'] = p.images.count()
        result.append(plot_data)

    # 状态统计
    status_counts = {}
    for p in plots:
        status = p.status or '未知'
        status_counts[status] = status_counts.get(status, 0) + 1

    return jsonify({'plots': result, 'status_counts': status_counts}), 200


@plot_bp.route('/', methods=['POST'])
@token_required
def create_plot(current_user):
    """创建地块，自动根据GeoJSON计算面积"""
    data = request.get_json()
    if not data:
        return jsonify({'message': '请求数据为空'}), 400

    name = data.get('name')
    if not name:
        return jsonify({'message': '地块名称不能为空'}), 400

    boundary_geojson = data.get('boundary_geojson')

    plot = Plot(
        user_id=current_user.id,
        name=name,
        elevation=data.get('elevation'),
        slope=data.get('slope'),
        slope_aspect=data.get('slope_aspect'),
        soil_type=data.get('soil_type'),
        soil_ph=data.get('soil_ph'),
        organic_matter=data.get('organic_matter'),
        soil_depth=data.get('soil_depth'),
        boundary_geojson=boundary_geojson,
        status=data.get('status', '闲置'),
        township=data.get('township'),
    )

    # 自动计算面积
    if boundary_geojson:
        calculated_area = calculate_area_from_geojson(boundary_geojson)
        if calculated_area > 0:
            plot.area = calculated_area
        elif data.get('area'):
            plot.area = data['area']
    elif data.get('area'):
        plot.area = data['area']

    db.session.add(plot)
    db.session.commit()

    return jsonify({'plot': plot.to_dict(), 'message': '地块创建成功'}), 201


@plot_bp.route('/stats', methods=['GET'])
@token_required
def plot_stats(current_user):
    """获取地块汇总统计：总面积、地块数量、状态分布"""
    if current_user.role == 'owner':
        plots = Plot.query.filter_by(user_id=current_user.id).all()
    elif current_user.role == 'coop_admin':
        from models import User
        member_ids = [u.id for u in User.query.filter_by(cooperative_id=current_user.cooperative_id).all()]
        plots = Plot.query.filter(Plot.user_id.in_(member_ids)).all() if member_ids else []
    else:
        plots = Plot.query.filter_by(user_id=current_user.id).all()

    total_area = sum(p.area or 0 for p in plots)
    plot_count = len(plots)
    status_distribution = {}
    for p in plots:
        status = p.status or '未知'
        status_distribution[status] = status_distribution.get(status, 0) + 1

    return jsonify({
        'total_area': round(total_area, 2),
        'plot_count': plot_count,
        'status_distribution': status_distribution,
    }), 200


@plot_bp.route('/<int:plot_id>', methods=['GET'])
@token_required
def get_plot(current_user, plot_id):
    """获取地块详情，包含种植周期和最新图片"""
    plot = Plot.query.get(plot_id)
    if not plot:
        return jsonify({'message': '地块不存在'}), 404

    plot_data = plot.to_dict()
    plot_data['planting_cycles'] = [c.to_dict() for c in plot.planting_cycles.order_by(PlantingCycle.created_at.desc()).all()]
    plot_data['latest_images'] = [img.to_dict() for img in plot.images.order_by(PlotImage.taken_at.desc()).limit(5).all()]

    return jsonify({'plot': plot_data}), 200


@plot_bp.route('/<int:plot_id>', methods=['PUT'])
@token_required
def update_plot(current_user, plot_id):
    """更新地块信息"""
    plot = Plot.query.get(plot_id)
    if not plot:
        return jsonify({'message': '地块不存在'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': '请求数据为空'}), 400

    for field in ['name', 'elevation', 'slope', 'slope_aspect', 'soil_type',
                  'soil_ph', 'organic_matter', 'soil_depth', 'status', 'township']:
        if field in data:
            setattr(plot, field, data[field])

    if 'boundary_geojson' in data:
        plot.boundary_geojson = data['boundary_geojson']
        calculated_area = calculate_area_from_geojson(data['boundary_geojson'])
        if calculated_area > 0:
            plot.area = calculated_area

    if 'area' in data and not getattr(plot, 'area', None):
        plot.area = data['area']

    db.session.commit()

    return jsonify({'plot': plot.to_dict(), 'message': '地块更新成功'}), 200


@plot_bp.route('/<int:plot_id>', methods=['DELETE'])
@role_required('owner')
def delete_plot(current_user, plot_id):
    """删除地块（仅户主）"""
    plot = Plot.query.get(plot_id)
    if not plot:
        return jsonify({'message': '地块不存在'}), 404

    if plot.user_id != current_user.id:
        return jsonify({'message': '只能删除自己的地块'}), 403

    db.session.delete(plot)
    db.session.commit()

    return jsonify({'message': '地块删除成功'}), 200
