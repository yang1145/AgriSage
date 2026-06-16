from flask import Blueprint, request, jsonify

from extensions import db
from models import User
from api.auth import token_required, role_required

user_bp = Blueprint('user', __name__)


@user_bp.route('/', methods=['GET'])
@role_required('owner')
def list_users(current_user):
    """获取所有用户列表（仅户主）"""
    users = User.query.all()
    return jsonify({'users': [u.to_dict() for u in users]}), 200


@user_bp.route('/', methods=['POST'])
@role_required('owner')
def create_user(current_user):
    """创建新用户（仅户主）"""
    data = request.get_json()
    if not data:
        return jsonify({'message': '请求数据为空'}), 400

    name = data.get('name')
    role = data.get('role')
    phone = data.get('phone')
    password = data.get('password')

    if not name or not role or not password:
        return jsonify({'message': '用户名、角色和密码不能为空'}), 400

    if role not in User.VALID_ROLES:
        return jsonify({'message': f'无效角色，有效角色: {User.VALID_ROLES}'}), 400

    if User.query.filter_by(name=name).first():
        return jsonify({'message': '用户名已存在'}), 400

    user = User(
        name=name,
        role=role,
        phone=phone,
    )
    user.set_password(password)
    if data.get('cooperative_id'):
        user.cooperative_id = data['cooperative_id']

    db.session.add(user)
    db.session.commit()

    return jsonify({'user': user.to_dict(), 'message': '用户创建成功'}), 201


@user_bp.route('/<int:user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    """更新用户信息。普通用户只能修改自己；户主可修改任意用户"""
    if current_user.role != 'owner' and current_user.id != user_id:
        return jsonify({'message': '无权修改其他用户信息'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': '用户不存在'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': '请求数据为空'}), 400

    if 'name' in data:
        existing = User.query.filter(User.name == data['name'], User.id != user_id).first()
        if existing:
            return jsonify({'message': '用户名已存在'}), 400
        user.name = data['name']

    if 'role' in data:
        if current_user.role != 'owner':
            return jsonify({'message': '仅户主可修改角色'}), 403
        if data['role'] not in User.VALID_ROLES:
            return jsonify({'message': f'无效角色，有效角色: {User.VALID_ROLES}'}), 400
        user.role = data['role']

    if 'phone' in data:
        user.phone = data['phone']

    if 'cooperative_id' in data:
        user.cooperative_id = data['cooperative_id']

    if 'password' in data and data['password']:
        user.set_password(data['password'])

    db.session.commit()

    return jsonify({'user': user.to_dict(), 'message': '用户更新成功'}), 200


@user_bp.route('/<int:user_id>', methods=['DELETE'])
@role_required('owner')
def delete_user(current_user, user_id):
    """删除用户（仅户主，不能删除自己）"""
    if current_user.id == user_id:
        return jsonify({'message': '不能删除自己的账户'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': '用户不存在'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': '用户删除成功'}), 200
