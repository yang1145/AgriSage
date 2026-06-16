from datetime import datetime, timezone
from extensions import db


class Plot(db.Model):
    __tablename__ = 'plots'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    area = db.Column(db.Float, comment='面积（亩）')
    elevation = db.Column(db.Float, comment='海拔（米）')
    slope = db.Column(db.Float, comment='坡度（度）')
    slope_aspect = db.Column(db.String(20), comment='坡向')
    soil_type = db.Column(db.String(50), comment='土壤类型')
    soil_ph = db.Column(db.Float, comment='土壤pH')
    organic_matter = db.Column(db.Float, comment='有机质含量')
    soil_depth = db.Column(db.Float, comment='土层深度（cm）')
    boundary_geojson = db.Column(db.Text, comment='边界GeoJSON')
    status = db.Column(db.String(20), default='闲置', comment='地块状态')
    township = db.Column(db.String(50), comment='乡镇')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    planting_cycles = db.relationship('PlantingCycle', backref='plot', lazy='dynamic')
    images = db.relationship('PlotImage', backref='plot', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'area': self.area,
            'elevation': self.elevation,
            'slope': self.slope,
            'slope_aspect': self.slope_aspect,
            'soil_type': self.soil_type,
            'soil_ph': self.soil_ph,
            'organic_matter': self.organic_matter,
            'soil_depth': self.soil_depth,
            'boundary_geojson': self.boundary_geojson,
            'status': self.status,
            'township': self.township,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<Plot {self.name} ({self.area}亩)>'
