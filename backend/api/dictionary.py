import requests
from flask import Blueprint, request, jsonify

from extensions import db
from models import Variety, SugarFactory, WeatherStation, SoilTemplate
from api.auth import token_required

dict_bp = Blueprint('dict', __name__)

# 中国气象局 API 基础地址
CMA_BASE_URL = 'https://weather.cma.cn/api'

# 默认监测站 ID（三水，广东佛山）
DEFAULT_STATION_ID = '59279'

# 请求头 - 模拟浏览器以绕过 WAF
CMA_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://weather.cma.cn/',
}


def _fetch_cma(path, params=None):
    """请求中国气象局 API，返回 JSON 数据"""
    url = f"{CMA_BASE_URL}{path}"
    try:
        resp = requests.get(url, params=params, headers=CMA_HEADERS, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get('code') != 0:
            return None
        return data.get('data')
    except Exception as e:
        print(f'[Weather API Error] {path}: {e}')
        return None


@dict_bp.route('/weather/current', methods=['GET'])
def get_current_weather():
    """获取指定城市的当前气象数据"""
    station_id = request.args.get('station_id', DEFAULT_STATION_ID)
    data = _fetch_cma(f'/now/{station_id}')
    if not data:
        return jsonify({'message': '获取天气数据失败'}), 502
    return jsonify({'data': data}), 200


@dict_bp.route('/weather/forecast', methods=['GET'])
def get_weather_forecast():
    """获取指定城市的天气预报（含实时 + 未来多日）"""
    station_id = request.args.get('station_id', DEFAULT_STATION_ID)
    data = _fetch_cma(f'/weather/{station_id}')
    if not data:
        return jsonify({'message': '获取天气预报失败'}), 502
    return jsonify({'data': data}), 200


@dict_bp.route('/weather/search', methods=['GET'])
def search_stations():
    """搜索监测站"""
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify({'message': '搜索关键词不能为空'}), 400
    data = _fetch_cma('/autocomplete', params={'q': q, 'limit': 10})
    if not data:
        return jsonify({'stations': []}), 200
    # 解析 "id|中文名|英文名|国家" 格式
    stations = []
    for item in (data or []):
        parts = item.split('|')
        if len(parts) >= 4:
            stations.append({
                'id': parts[0],
                'name_cn': parts[1],
                'name_en': parts[2],
                'country': parts[3],
            })
    return jsonify({'stations': stations}), 200


@dict_bp.route('/weather/alarm', methods=['GET'])
def get_weather_alarm():
    """获取气象预警信息"""
    adcode = request.args.get('adcode', '')  # 省份行政区划代码前两位
    data = _fetch_cma('/map/alarm', params={'adcode': adcode})
    if not data:
        return jsonify({'alarms': []}), 200
    return jsonify({'alarms': data or []}), 200


@dict_bp.route('/varieties', methods=['GET'])
def list_varieties():
    """获取品种列表，支持 ?search= 按名称/选育单位/适宜区域模糊搜索"""
    query = Variety.query

    search = request.args.get('search')
    if search:
        query = query.filter(
            db.or_(
                Variety.name.contains(search),
                Variety.breeding_unit.contains(search),
                Variety.suitable_area.contains(search),
            )
        )

    varieties = query.all()
    return jsonify({'varieties': [v.to_dict() for v in varieties]}), 200


@dict_bp.route('/varieties/<int:variety_id>', methods=['GET'])
def get_variety(variety_id):
    """获取品种详情"""
    variety = Variety.query.get(variety_id)
    if not variety:
        return jsonify({'message': '品种不存在'}), 404

    return jsonify({'variety': variety.to_dict()}), 200


@dict_bp.route('/varieties', methods=['POST'])
@token_required
def create_variety(current_user):
    """添加自定义品种"""
    data = request.get_json()
    if not data:
        return jsonify({'message': '请求数据为空'}), 400

    name = data.get('name')
    if not name:
        return jsonify({'message': '品种名称不能为空'}), 400

    if Variety.query.filter_by(name=name).first():
        return jsonify({'message': '品种名称已存在'}), 400

    variety = Variety(
        name=name,
        breeding_unit=data.get('breeding_unit'),
        maturity_type=data.get('maturity_type'),
        avg_yield=data.get('avg_yield'),
        avg_sugar=data.get('avg_sugar'),
        resistance_rating=data.get('resistance_rating'),
        suggested_ratoon_years=data.get('suggested_ratoon_years'),
        suitable_area=data.get('suitable_area'),
        is_custom=True,
    )

    db.session.add(variety)
    db.session.commit()

    return jsonify({'variety': variety.to_dict(), 'message': '品种添加成功'}), 201


@dict_bp.route('/sugar-factories', methods=['GET'])
def list_sugar_factories():
    """获取糖厂列表，支持 ?search= 按名称/区域搜索"""
    query = SugarFactory.query

    search = request.args.get('search')
    if search:
        query = query.filter(
            db.or_(
                SugarFactory.name.contains(search),
                SugarFactory.city_county.contains(search),
                SugarFactory.service_scope.contains(search),
            )
        )

    factories = query.all()
    return jsonify({'factories': [f.to_dict() for f in factories]}), 200


@dict_bp.route('/weather-stations', methods=['GET'])
def list_weather_stations():
    """获取气象站列表，支持 ?region= 按区域筛选"""
    query = WeatherStation.query

    region = request.args.get('region')
    if region:
        query = query.filter(WeatherStation.region.contains(region))

    stations = query.all()
    return jsonify({'stations': [s.to_dict() for s in stations]}), 200


@dict_bp.route('/soil-templates', methods=['GET'])
def list_soil_templates():
    """获取土壤模板列表，支持 ?township= 按乡镇筛选"""
    query = SoilTemplate.query

    township = request.args.get('township')
    if township:
        query = query.filter(SoilTemplate.township.contains(township))

    templates = query.all()
    return jsonify({'templates': [t.to_dict() for t in templates]}), 200
