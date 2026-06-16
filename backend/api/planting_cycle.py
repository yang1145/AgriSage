from datetime import date

from flask import Blueprint, request, jsonify

from extensions import db
from models import PlantingCycle, Plot, FertilizationRecord, IrrigationRecord, PestDiseaseRecord, HarvestRecord
from api.auth import token_required

cycle_bp = Blueprint('cycle', __name__)


@cycle_bp.route('/plot/<int:plot_id>', methods=['GET'])
@token_required
def list_cycles(current_user, plot_id):
    """获取指定地块的种植周期列表"""
    plot = Plot.query.get(plot_id)
    if not plot:
        return jsonify({'message': '地块不存在'}), 404

    cycles = PlantingCycle.query.filter_by(plot_id=plot_id).order_by(PlantingCycle.created_at.desc()).all()
    return jsonify({'cycles': [c.to_dict() for c in cycles]}), 200


@cycle_bp.route('/plot/<int:plot_id>', methods=['POST'])
@token_required
def create_cycle(current_user, plot_id):
    """创建种植周期。宿根类型自动继承同地块最近周期的品种信息"""
    plot = Plot.query.get(plot_id)
    if not plot:
        return jsonify({'message': '地块不存在'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': '请求数据为空'}), 400

    cycle_type = data.get('cycle_type')
    if not cycle_type:
        return jsonify({'message': '轮作类型不能为空'}), 400

    if cycle_type not in PlantingCycle.VALID_CYCLE_TYPES:
        return jsonify({'message': f'无效轮作类型，有效类型: {PlantingCycle.VALID_CYCLE_TYPES}'}), 400

    cycle = PlantingCycle(
        plot_id=plot_id,
        cycle_type=cycle_type,
        variety_id=data.get('variety_id'),
        plant_date=date.fromisoformat(data['plant_date']) if data.get('plant_date') else None,
        seed_source=data.get('seed_source'),
        seed_amount=data.get('seed_amount'),
        row_spacing=data.get('row_spacing'),
        mulch=data.get('mulch', False),
        status=data.get('status', '种植中'),
    )

    # 宿根类型：自动继承同地块最近周期的品种和地块信息
    if '宿根' in cycle_type:
        latest_cycle = PlantingCycle.query.filter_by(plot_id=plot_id).order_by(PlantingCycle.created_at.desc()).first()
        if latest_cycle:
            cycle.parent_cycle_id = latest_cycle.id
            if not cycle.variety_id and latest_cycle.variety_id:
                cycle.variety_id = latest_cycle.variety_id

    db.session.add(cycle)

    # 更新地块状态为种植中
    plot.status = '种植中'

    db.session.commit()

    return jsonify({'cycle': cycle.to_dict(), 'message': '种植周期创建成功'}), 201


@cycle_bp.route('/<int:cycle_id>', methods=['GET'])
@token_required
def get_cycle(current_user, cycle_id):
    """获取种植周期详情，包含农事记录"""
    cycle = PlantingCycle.query.get(cycle_id)
    if not cycle:
        return jsonify({'message': '种植周期不存在'}), 404

    cycle_data = cycle.to_dict()
    cycle_data['fertilization_records'] = [r.to_dict() for r in cycle.farming_records_fertilization.order_by(FertilizationRecord.date.desc()).all()]
    cycle_data['irrigation_records'] = [r.to_dict() for r in cycle.farming_records_irrigation.order_by(IrrigationRecord.date.desc()).all()]
    cycle_data['pest_disease_records'] = [r.to_dict() for r in cycle.farming_records_pest.order_by(PestDiseaseRecord.discovery_date.desc()).all()]
    cycle_data['harvest_records'] = [r.to_dict() for r in cycle.farming_records_harvest.order_by(HarvestRecord.actual_date.desc()).all()]

    return jsonify({'cycle': cycle_data}), 200


@cycle_bp.route('/<int:cycle_id>', methods=['PUT'])
@token_required
def update_cycle(current_user, cycle_id):
    """更新种植周期信息"""
    cycle = PlantingCycle.query.get(cycle_id)
    if not cycle:
        return jsonify({'message': '种植周期不存在'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': '请求数据为空'}), 400

    if 'cycle_type' in data:
        if data['cycle_type'] not in PlantingCycle.VALID_CYCLE_TYPES:
            return jsonify({'message': f'无效轮作类型，有效类型: {PlantingCycle.VALID_CYCLE_TYPES}'}), 400
        cycle.cycle_type = data['cycle_type']

    if 'variety_id' in data:
        cycle.variety_id = data['variety_id']

    if 'plant_date' in data and data['plant_date']:
        cycle.plant_date = date.fromisoformat(data['plant_date'])

    for field in ['seed_source', 'seed_amount', 'row_spacing', 'mulch', 'status']:
        if field in data:
            setattr(cycle, field, data[field])

    db.session.commit()

    return jsonify({'cycle': cycle.to_dict(), 'message': '种植周期更新成功'}), 200


@cycle_bp.route('/<int:cycle_id>/timeline', methods=['GET'])
@token_required
def cycle_timeline(current_user, cycle_id):
    """获取种植周期时间线数据：周期信息 + 所有农事记录按日期排序"""
    cycle = PlantingCycle.query.get(cycle_id)
    if not cycle:
        return jsonify({'message': '种植周期不存在'}), 404

    timeline = []

    # 种植事件
    if cycle.plant_date:
        timeline.append({
            'type': '种植',
            'date': cycle.plant_date.isoformat(),
            'data': {'cycle_type': cycle.cycle_type},
        })

    # 施肥记录
    for r in cycle.farming_records_fertilization.all():
        timeline.append({
            'type': '施肥',
            'date': r.date.isoformat() if r.date else None,
            'data': r.to_dict(),
        })

    # 灌溉记录
    for r in cycle.farming_records_irrigation.all():
        timeline.append({
            'type': '灌溉',
            'date': r.date.isoformat() if r.date else None,
            'data': r.to_dict(),
        })

    # 病虫害记录
    for r in cycle.farming_records_pest.all():
        timeline.append({
            'type': '病虫害',
            'date': r.discovery_date.isoformat() if r.discovery_date else None,
            'data': r.to_dict(),
        })

    # 收获记录
    for r in cycle.farming_records_harvest.all():
        timeline.append({
            'type': '收获',
            'date': (r.actual_date or r.planned_date).isoformat() if (r.actual_date or r.planned_date) else None,
            'data': r.to_dict(),
        })

    # 按日期排序
    timeline.sort(key=lambda x: x['date'] or '')

    return jsonify({'cycle': cycle.to_dict(), 'timeline': timeline}), 200


@cycle_bp.route('/<int:cycle_id>', methods=['DELETE'])
@token_required
def delete_cycle(current_user, cycle_id):
    """删除种植周期（仅户主可删除自己地块的周期）"""
    cycle = PlantingCycle.query.get(cycle_id)
    if not cycle:
        return jsonify({'message': '种植周期不存在'}), 404

    plot = Plot.query.get(cycle.plot_id)
    if not plot:
        return jsonify({'message': '关联地块不存在'}), 404

    if current_user.role != 'owner' or plot.user_id != current_user.id:
        return jsonify({'message': '仅户主可删除自己地块的种植周期'}), 403

    db.session.delete(cycle)
    db.session.commit()

    return jsonify({'message': '种植周期删除成功'}), 200
