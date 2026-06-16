import jwt
from datetime import datetime, timedelta
from functools import wraps

from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db
from models import User

auth_bp = Blueprint('auth', __name__)


def token_required(f):
    """装饰器：验证JWT令牌，将当前用户注入路由"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]

        if not token:
            return jsonify({'message': '缺少认证令牌'}), 401

        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(payload['user_id'])
            if not current_user:
                return jsonify({'message': '用户不存在'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': '令牌已过期，请重新登录'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': '无效令牌'}), 401

        return f(current_user, *args, **kwargs)
    return decorated


def role_required(*roles):
    """装饰器：检查当前用户角色是否在允许列表中"""
    def decorator(f):
        @wraps(f)
        @token_required
        def decorated(current_user, *args, **kwargs):
            if current_user.role not in roles:
                return jsonify({'message': '权限不足'}), 403
            return f(current_user, *args, **kwargs)
        return decorated
    return decorator


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录，返回JWT令牌和用户信息"""
    data = request.get_json()
    if not data:
        return jsonify({'message': '请求数据为空'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': '用户名和密码不能为空'}), 400

    user = User.query.filter_by(name=username).first()
    if not user or not user.check_password(password):
        return jsonify({'message': '用户名或密码错误'}), 401

    expiration = datetime.utcnow() + timedelta(hours=current_app.config.get('JWT_EXPIRATION_HOURS', 720))
    token = jwt.encode(
        {'user_id': user.id, 'exp': expiration},
        current_app.config['JWT_SECRET_KEY'],
        algorithm='HS256'
    )

    return jsonify({
        'token': token,
        'user': user.to_dict(),
    }), 200


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_me(current_user):
    """获取当前登录用户信息"""
    return jsonify({'user': current_user.to_dict()}), 200


@auth_bp.route('/register', methods=['POST'])
@role_required('owner')
def register(current_user):
    """仅户主可创建用户账号（通过用户管理页面）"""
    data = request.get_json()
    if not data:
        return jsonify({'message': '请求数据为空'}), 400

    name = data.get('name')
    phone = data.get('phone')
    password = data.get('password')
    role = data.get('role', 'owner')

    if not name or not password:
        return jsonify({'message': '姓名和密码不能为空'}), 400

    if role not in User.VALID_ROLES:
        return jsonify({'message': f'无效角色，有效角色: {User.VALID_ROLES}'}), 400

    if User.query.filter_by(name=name).first():
        return jsonify({'message': '用户名已存在'}), 400

    user = User(name=name, phone=phone, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': '注册成功', 'user': user.to_dict()}), 201


@auth_bp.route('/change-password', methods=['POST'])
@token_required
def change_password(current_user):
    """修改当前用户密码"""
    data = request.get_json()
    if not data:
        return jsonify({'message': '请求数据为空'}), 400

    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not old_password or not new_password:
        return jsonify({'message': '旧密码和新密码不能为空'}), 400

    if not current_user.check_password(old_password):
        return jsonify({'message': '旧密码错误'}), 400

    current_user.set_password(new_password)
    db.session.commit()

    return jsonify({'message': '密码修改成功'}), 200
