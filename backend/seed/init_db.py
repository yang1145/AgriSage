import sys
import os

# 确保从 backend 目录运行时能正确导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extensions import db
from models.user import User
from models.dictionary import Variety, SugarFactory, WeatherStation, SoilTemplate
from seed.varieties import VARIETIES
from seed.sugar_factories import SUGAR_FACTORIES
from seed.weather_stations import WEATHER_STATIONS
from seed.soil_templates import SOIL_TEMPLATES


def seed_varieties():
    """插入品种种子数据"""
    for item in VARIETIES:
        exists = Variety.query.filter_by(name=item["name"]).first()
        if not exists:
            v = Variety(
                name=item["name"],
                breeding_unit=item["breeding_unit"],
                maturity_type=item["maturity_type"],
                avg_yield=item["avg_yield"],
                avg_sugar=item["avg_sugar"],
                resistance_rating=item["resistance_rating"],
                suggested_ratoon_years=item["suggested_ratoon_years"],
                suitable_area=item["suitable_area"],
            )
            db.session.add(v)
    db.session.commit()
    print(f"  品种数据: {len(VARIETIES)} 条")


def seed_sugar_factories():
    """插入糖厂种子数据"""
    for item in SUGAR_FACTORIES:
        exists = SugarFactory.query.filter_by(name=item["name"]).first()
        if not exists:
            f = SugarFactory(
                name=item["name"],
                city_county=item["city_county"],
                service_scope=item["service_scope"],
                contact_phone=item["contact_phone"],
            )
            db.session.add(f)
    db.session.commit()
    print(f"  糖厂数据: {len(SUGAR_FACTORIES)} 条")


def seed_weather_stations():
    """插入气象站种子数据"""
    for item in WEATHER_STATIONS:
        exists = WeatherStation.query.filter_by(name=item["name"]).first()
        if not exists:
            s = WeatherStation(
                name=item["name"],
                region=item["region"],
                historical_data=item["historical_data"],
            )
            db.session.add(s)
    db.session.commit()
    print(f"  气象站数据: {len(WEATHER_STATIONS)} 条")


def seed_soil_templates():
    """插入土壤模板种子数据"""
    for item in SOIL_TEMPLATES:
        exists = SoilTemplate.query.filter_by(township=item["township"]).first()
        if not exists:
            t = SoilTemplate(
                township=item["township"],
                soil_type=item["soil_type"],
                default_ph=item["default_ph"],
                default_organic_matter=item["default_organic_matter"],
                default_soil_depth=item["default_soil_depth"],
            )
            db.session.add(t)
    db.session.commit()
    print(f"  土壤模板数据: {len(SOIL_TEMPLATES)} 条")


def seed_admin_user():
    """创建默认管理员用户"""
    exists = User.query.filter_by(name="admin").first()
    if not exists:
        admin = User(
            name="admin",
            role="owner",
            phone="13800000000",
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("  默认管理员: admin / admin123")
    else:
        print("  默认管理员已存在，跳过")


def init_db(app=None):
    """初始化数据库：建表 + 种子数据"""
    if app is None:
        from app import create_app
        app = create_app()

    with app.app_context():
        print("正在创建数据库表...")
        db.create_all()
        print("数据库表创建完成。")

        print("正在插入种子数据...")
        seed_varieties()
        seed_sugar_factories()
        seed_weather_stations()
        seed_soil_templates()
        seed_admin_user()

        print("\n✅ 数据库初始化完成！")


if __name__ == "__main__":
    init_db()
