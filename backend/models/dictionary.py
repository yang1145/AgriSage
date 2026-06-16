from extensions import db


class Variety(db.Model):
    __tablename__ = 'varieties'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, comment='品种名称')
    breeding_unit = db.Column(db.String(200), comment='育种单位')
    maturity_type = db.Column(db.String(50), comment='熟期类型')
    avg_yield = db.Column(db.Float, comment='平均亩产（吨）')
    avg_sugar = db.Column(db.Float, comment='平均含糖分（%）')
    resistance_rating = db.Column(db.String(50), comment='抗性评级')
    suggested_ratoon_years = db.Column(db.Integer, comment='建议宿根年限')
    suitable_area = db.Column(db.String(200), comment='适宜区域')
    is_custom = db.Column(db.Boolean, default=False, comment='是否自定义品种')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'breeding_unit': self.breeding_unit,
            'maturity_type': self.maturity_type,
            'avg_yield': self.avg_yield,
            'avg_sugar': self.avg_sugar,
            'resistance_rating': self.resistance_rating,
            'suggested_ratoon_years': self.suggested_ratoon_years,
            'suitable_area': self.suitable_area,
            'is_custom': self.is_custom,
        }

    def __repr__(self):
        return f'<Variety {self.name}>'


class SugarFactory(db.Model):
    __tablename__ = 'sugar_factories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, comment='糖厂名称')
    city_county = db.Column(db.String(100), comment='所在市县')
    service_scope = db.Column(db.String(200), comment='服务范围')
    contact_phone = db.Column(db.String(20), comment='联系电话')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city_county': self.city_county,
            'service_scope': self.service_scope,
            'contact_phone': self.contact_phone,
        }

    def __repr__(self):
        return f'<SugarFactory {self.name}>'


class WeatherStation(db.Model):
    __tablename__ = 'weather_stations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, comment='站点名称')
    region = db.Column(db.String(100), comment='所属区域')
    historical_data = db.Column(db.JSON, comment='历史气象数据')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'region': self.region,
            'historical_data': self.historical_data,
        }

    def __repr__(self):
        return f'<WeatherStation {self.name}>'


class SoilTemplate(db.Model):
    __tablename__ = 'soil_templates'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    township = db.Column(db.String(50), nullable=False, comment='乡镇')
    soil_type = db.Column(db.String(50), nullable=False, comment='土壤类型')
    default_ph = db.Column(db.Float, comment='默认pH')
    default_organic_matter = db.Column(db.Float, comment='默认有机质')
    default_soil_depth = db.Column(db.Float, comment='默认土层深度（cm）')

    def to_dict(self):
        return {
            'id': self.id,
            'township': self.township,
            'soil_type': self.soil_type,
            'default_ph': self.default_ph,
            'default_organic_matter': self.default_organic_matter,
            'default_soil_depth': self.default_soil_depth,
        }

    def __repr__(self):
        return f'<SoilTemplate {self.township} - {self.soil_type}>'
