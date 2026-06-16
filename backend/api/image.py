import os
from datetime import datetime

from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

from extensions import db
from models import Plot, PlotImage, PlantingCycle
from api.auth import token_required

image_bp = Blueprint('image', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@image_bp.route('/plot/<int:plot_id>', methods=['POST'])
@token_required
def upload_images(current_user, plot_id):
    """上传地块图片，支持多文件上传"""
    plot = Plot.query.get(plot_id)
    if not plot:
        return jsonify({'message': '地块不存在'}), 404

    files = request.files.getlist('files')
    if not files or all(f.filename == '' for f in files):
        return jsonify({'message': '未选择文件'}), 400

    growth_stage = request.form.get('growth_stage')
    cycle_id = request.form.get('cycle_id')
    taken_at_str = request.form.get('taken_at')

    if growth_stage and growth_stage not in PlotImage.VALID_GROWTH_STAGES:
        return jsonify({'message': f'无效生长阶段，有效阶段: {PlotImage.VALID_GROWTH_STAGES}'}), 400

    taken_at = None
    if taken_at_str:
        try:
            taken_at = datetime.fromisoformat(taken_at_str)
        except ValueError:
            return jsonify({'message': '拍摄时间格式无效'}), 400

    upload_folder = current_app.config['UPLOAD_FOLDER']
    plot_dir = os.path.join(upload_folder, f'plot_{plot_id}')
    os.makedirs(plot_dir, exist_ok=True)

    created_images = []
    for f in files:
        if f.filename == '' or not allowed_file(f.filename):
            continue

        filename = secure_filename(f.filename)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_name = f'{timestamp}_{filename}'
        file_path = os.path.join(plot_dir, unique_name)
        f.save(file_path)

        relative_path = os.path.join(f'plot_{plot_id}', unique_name)

        image = PlotImage(
            plot_id=plot_id,
            cycle_id=int(cycle_id) if cycle_id else None,
            growth_stage=growth_stage,
            file_path=relative_path,
            taken_at=taken_at,
        )

        db.session.add(image)
        created_images.append(image)

    if not created_images:
        return jsonify({'message': '没有有效的图片文件'}), 400

    db.session.commit()

    return jsonify({
        'images': [img.to_dict() for img in created_images],
        'message': f'成功上传 {len(created_images)} 张图片',
    }), 201


@image_bp.route('/plot/<int:plot_id>', methods=['GET'])
@token_required
def list_images(current_user, plot_id):
    """获取地块图片列表，按生长阶段分组"""
    plot = Plot.query.get(plot_id)
    if not plot:
        return jsonify({'message': '地块不存在'}), 404

    images = PlotImage.query.filter_by(plot_id=plot_id).order_by(PlotImage.taken_at.desc()).all()

    grouped = {}
    for img in images:
        stage = img.growth_stage or '未分类'
        if stage not in grouped:
            grouped[stage] = []
        grouped[stage].append(img.to_dict())

    return jsonify({'images': grouped, 'total': len(images)}), 200


@image_bp.route('/<int:image_id>', methods=['PUT'])
@token_required
def update_image(current_user, image_id):
    """更新图片标注信息"""
    image = PlotImage.query.get(image_id)
    if not image:
        return jsonify({'message': '图片不存在'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': '请求数据为空'}), 400

    if 'annotations' in data:
        image.annotations = data['annotations']

    if 'growth_stage' in data:
        if data['growth_stage'] not in PlotImage.VALID_GROWTH_STAGES:
            return jsonify({'message': f'无效生长阶段，有效阶段: {PlotImage.VALID_GROWTH_STAGES}'}), 400
        image.growth_stage = data['growth_stage']

    if 'cycle_id' in data:
        image.cycle_id = data['cycle_id']

    if 'taken_at' in data and data['taken_at']:
        try:
            image.taken_at = datetime.fromisoformat(data['taken_at'])
        except ValueError:
            return jsonify({'message': '拍摄时间格式无效'}), 400

    db.session.commit()

    return jsonify({'image': image.to_dict(), 'message': '图片更新成功'}), 200


@image_bp.route('/<int:image_id>', methods=['DELETE'])
@token_required
def delete_image(current_user, image_id):
    """删除图片记录及文件"""
    image = PlotImage.query.get(image_id)
    if not image:
        return jsonify({'message': '图片不存在'}), 404

    # 删除实际文件
    if image.file_path:
        full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image.file_path)
        if os.path.exists(full_path):
            os.remove(full_path)

    db.session.delete(image)
    db.session.commit()

    return jsonify({'message': '图片删除成功'}), 200
