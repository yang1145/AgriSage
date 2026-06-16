from datetime import datetime, timezone, date
from extensions import db


class PlantingCycle(db.Model):
    __tablename__ = 'planting_cycles'

    VALID_CYCLE_TYPES = ('新植蔗', '宿根1年', '宿根2年', '宿根3年+')
    VALID_STATUSES = ('种植中', '收获完毕', '已废弃')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plot_id = db.Column(db.Integer, db.ForeignKey('plots.id'), nullable=False)
    cycle_type = db.Column(db.String(20), nullable=False, comment='轮作类型')
    variety_id = db.Column(db.Integer, db.ForeignKey('varieties.id'), nullable=True)
    plant_date = db.Column(db.Date, comment='种植日期')
    seed_source = db.Column(db.String(100), comment='种茎来源')
    seed_amount = db.Column(db.Float, comment='下种量（吨/亩）')
    row_spacing = db.Column(db.Float, comment='行距（cm）')
    mulch = db.Column(db.Boolean, default=False, comment='地膜覆盖')
    status = db.Column(db.String(20), default='种植中', comment='状态')
    parent_cycle_id = db.Column(db.Integer, nullable=True, comment='宿根继承的父轮作ID')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    farming_records_fertilization = db.relationship('FertilizationRecord', backref='cycle', lazy='dynamic')
    farming_records_irrigation = db.relationship('IrrigationRecord', backref='cycle', lazy='dynamic')
    farming_records_pest = db.relationship('PestDiseaseRecord', backref='cycle', lazy='dynamic')
    farming_records_harvest = db.relationship('HarvestRecord', backref='cycle', lazy='dynamic')
    images = db.relationship('PlotImage', backref='cycle', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'plot_id': self.plot_id,
            'cycle_type': self.cycle_type,
            'variety_id': self.variety_id,
            'plant_date': self.plant_date.isoformat() if self.plant_date else None,
            'seed_source': self.seed_source,
            'seed_amount': self.seed_amount,
            'row_spacing': self.row_spacing,
            'mulch': self.mulch,
            'status': self.status,
            'parent_cycle_id': self.parent_cycle_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<PlantingCycle {self.cycle_type} (Plot#{self.plot_id})>'
