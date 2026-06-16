from datetime import date

from flask import Blueprint, request, jsonify

from extensions import db
from models import (
    PlantingCycle, FertilizationRecord, IrrigationRecord,
    PestDiseaseRecord, HarvestRecord,
)
from api.auth import token_required

farming_bp = Blueprint('farming', __name__)

RECORD_MODELS = {
    'fertilization': FertilizationRecord,
    'irrigation': IrrigationRecord,
    'pest_disease': PestDiseaseRecord,
    'harvest': HarvestRecord,
}


@farming_bp.route('/cycle/<int:cycle_id>', methods=['GET'])
@token_required
def list_records(current_user, cycle_id):
    """获取指定周期的所有农事记录，按类型分组"""
    cycle = PlantingCycle.query.get(cycle_id)
    if not cycle:
        return jsonify({'message': '种植周期不存在'}), 404

    result = {
        'fertilization': [r.to_dict() for r in cycle.farming_records_fertilization.order_by(FertilizationRecord.date.desc()).all()],
        'irrigation': [r.to_dict() for r in cycle.farming_records_irrigation.order_by(IrrigationRecord.date.desc()).all()],
        'pest_disease': [r.to_dict() for r in cycle.farming_records_pest.order_by(PestDiseaseRecord.discovery_date.desc()).all()],
        'harvest': [r.to_dict() for r in cycle.farming_records_harvest.order_by(HarvestRecord.actual_date.desc()).all()],
    }

    return jsonify({'records': result}), 200


@farming_bp.route('/cycle/<int:cycle_id>/fertilization', methods=['POST'])
@token_required
def create_fertilization(current_user, cycle_id):
    """创建施肥记录"""
    cycle = PlantingCycle.query.get(cycle_id)
    if not cycle:
        return jsonify({'message': '种植周期不存在'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': '请求数据为空'}), 400

    if not data.get('date'):
        return jsonify({'message': '施肥日期不能为空'}), 400

    record = FertilizationRecord(
        cycle_id=cycle_id,
        date=date.fromisoformat(data['date']),
        fertilizer_type=data.get('fertilizer_type'),
        fertilizer_name=data.get('fertilizer_name'),
        npk_content=data.get('npk_content'),
        amount=data.get('amount'),
        method=data.get('method'),
        related_plots=data.get('related_plots'),
    )

    db.session.add(record)
    db.session.commit()

    return jsonify({'record': record.to_dict(), 'message': '施肥记录创建成功'}), 201


@farming_bp.route('/cycle/<int:cycle_id>/irrigation', methods=['POST'])
@token_required
def create_irrigation(current_user, cycle_id):
    """创建灌溉记录"""
    cycle = PlantingCycle.query.get(cycle_id)
    if not cycle:
        return jsonify({'message': '种植周期不存在'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': '请求数据为空'}), 400

    if not data.get('date'):
        return jsonify({'message': '灌溉日期不能为空'}), 400

    record = IrrigationRecord(
        cycle_id=cycle_id,
        date=date.fromisoformat(data['date']),
        method=data.get('method'),
        water_amount=data.get('water_amount'),
        water_source=data.get('water_source'),
    )

    db.session.add(record)
    db.session.commit()

    return jsonify({'record': record.to_dict(), 'message': '灌溉记录创建成功'}), 201


@farming_bp.route('/cycle/<int:cycle_id>/pest-disease', methods=['POST'])
@token_required
def create_pest_disease(current_user, cycle_id):
    """创建病虫害记录"""
    cycle = PlantingCycle.query.get(cycle_id)
    if not cycle:
        return jsonify({'message': '种植周期不存在'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': '请求数据为空'}), 400

    if not data.get('discovery_date'):
        return jsonify({'message': '发现日期不能为空'}), 400

    record = PestDiseaseRecord(
        cycle_id=cycle_id,
        discovery_date=date.fromisoformat(data['discovery_date']),
        pest_type=data.get('pest_type'),
        affected_part=data.get('affected_part'),
        severity=data.get('severity'),
        control_date=date.fromisoformat(data['control_date']) if data.get('control_date') else None,
        pesticide_name=data.get('pesticide_name'),
        dosage=data.get('dosage'),
        effect=data.get('effect'),
    )

    db.session.add(record)
    db.session.commit()

    return jsonify({'record': record.to_dict(), 'message': '病虫害记录创建成功'}), 201


@farming_bp.route('/cycle/<int:cycle_id>/harvest', methods=['POST'])
@token_required
def create_harvest(current_user, cycle_id):
    """创建收获记录"""
    cycle = PlantingCycle.query.get(cycle_id)
    if not cycle:
        return jsonify({'message': '种植周期不存在'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': '请求数据为空'}), 400

    record = HarvestRecord(
        cycle_id=cycle_id,
        planned_date=date.fromisoformat(data['planned_date']) if data.get('planned_date') else None,
        actual_date=date.fromisoformat(data['actual_date']) if data.get('actual_date') else None,
        harvest_area=data.get('harvest_area'),
        yield_tons=data.get('yield_tons'),
        brix_percent=data.get('brix_percent'),
        sugar_percent=data.get('sugar_percent'),
        unit_price=data.get('unit_price'),
        sugar_factory=data.get('sugar_factory'),
        transport_cost=data.get('transport_cost'),
    )

    db.session.add(record)

    # 如果有实际收获日期，更新周期状态
    if data.get('actual_date'):
        cycle.status = '收获完毕'

    db.session.commit()

    return jsonify({'record': record.to_dict(), 'message': '收获记录创建成功'}), 201


@farming_bp.route('/<record_type>/<int:record_id>', methods=['PUT'])
@token_required
def update_record(current_user, record_type, record_id):
    """更新农事记录"""
    model = RECORD_MODELS.get(record_type)
    if not model:
        return jsonify({'message': f'无效记录类型，有效类型: {list(RECORD_MODELS.keys())}'}), 400

    record = model.query.get(record_id)
    if not record:
        return jsonify({'message': '记录不存在'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': '请求数据为空'}), 400

    if record_type == 'fertilization':
        if 'date' in data and data['date']:
            record.date = date.fromisoformat(data['date'])
        for field in ['fertilizer_type', 'fertilizer_name', 'npk_content', 'amount', 'method']:
            if field in data:
                setattr(record, field, data[field])
        if 'related_plots' in data:
            record.related_plots = data['related_plots']

    elif record_type == 'irrigation':
        if 'date' in data and data['date']:
            record.date = date.fromisoformat(data['date'])
        for field in ['method', 'water_amount', 'water_source']:
            if field in data:
                setattr(record, field, data[field])

    elif record_type == 'pest_disease':
        if 'discovery_date' in data and data['discovery_date']:
            record.discovery_date = date.fromisoformat(data['discovery_date'])
        if 'control_date' in data:
            record.control_date = date.fromisoformat(data['control_date']) if data['control_date'] else None
        for field in ['pest_type', 'affected_part', 'severity', 'pesticide_name', 'dosage', 'effect']:
            if field in data:
                setattr(record, field, data[field])

    elif record_type == 'harvest':
        if 'planned_date' in data:
            record.planned_date = date.fromisoformat(data['planned_date']) if data['planned_date'] else None
        if 'actual_date' in data:
            record.actual_date = date.fromisoformat(data['actual_date']) if data['actual_date'] else None
        for field in ['harvest_area', 'yield_tons', 'brix_percent', 'sugar_percent',
                      'unit_price', 'sugar_factory', 'transport_cost']:
            if field in data:
                setattr(record, field, data[field])

    db.session.commit()

    return jsonify({'record': record.to_dict(), 'message': '记录更新成功'}), 200


@farming_bp.route('/<record_type>/<int:record_id>', methods=['DELETE'])
@token_required
def delete_record(current_user, record_type, record_id):
    """删除农事记录"""
    model = RECORD_MODELS.get(record_type)
    if not model:
        return jsonify({'message': f'无效记录类型，有效类型: {list(RECORD_MODELS.keys())}'}), 400

    record = model.query.get(record_id)
    if not record:
        return jsonify({'message': '记录不存在'}), 404

    db.session.delete(record)
    db.session.commit()

    return jsonify({'message': '记录删除成功'}), 200
