from datetime import datetime, timezone, date
from extensions import db


class FertilizationRecord(db.Model):
    __tablename__ = 'fertilization_records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cycle_id = db.Column(db.Integer, db.ForeignKey('planting_cycles.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, comment='施肥日期')
    fertilizer_type = db.Column(db.String(50), comment='肥料类型')
    fertilizer_name = db.Column(db.String(100), comment='肥料名称')
    npk_content = db.Column(db.String(50), comment='NPK含量')
    amount = db.Column(db.Float, comment='用量（kg/亩）')
    method = db.Column(db.String(50), comment='施肥方式')
    related_plots = db.Column(db.JSON, nullable=True, comment='关联地块')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'cycle_id': self.cycle_id,
            'date': self.date.isoformat() if self.date else None,
            'fertilizer_type': self.fertilizer_type,
            'fertilizer_name': self.fertilizer_name,
            'npk_content': self.npk_content,
            'amount': self.amount,
            'method': self.method,
            'related_plots': self.related_plots,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<FertilizationRecord {self.fertilizer_name} on {self.date}>'


class IrrigationRecord(db.Model):
    __tablename__ = 'irrigation_records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cycle_id = db.Column(db.Integer, db.ForeignKey('planting_cycles.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, comment='灌溉日期')
    method = db.Column(db.String(50), comment='灌溉方式')
    water_amount = db.Column(db.Float, comment='用水量（m³/亩）')
    water_source = db.Column(db.String(100), comment='水源')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'cycle_id': self.cycle_id,
            'date': self.date.isoformat() if self.date else None,
            'method': self.method,
            'water_amount': self.water_amount,
            'water_source': self.water_source,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<IrrigationRecord {self.method} on {self.date}>'


class PestDiseaseRecord(db.Model):
    __tablename__ = 'pest_disease_records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cycle_id = db.Column(db.Integer, db.ForeignKey('planting_cycles.id'), nullable=False)
    discovery_date = db.Column(db.Date, nullable=False, comment='发现日期')
    pest_type = db.Column(db.String(100), comment='病虫害类型')
    affected_part = db.Column(db.String(50), comment='受害部位')
    severity = db.Column(db.String(20), comment='严重程度')
    control_date = db.Column(db.Date, comment='防治日期')
    pesticide_name = db.Column(db.String(100), comment='农药名称')
    dosage = db.Column(db.String(100), comment='用量')
    effect = db.Column(db.String(50), comment='防治效果')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'cycle_id': self.cycle_id,
            'discovery_date': self.discovery_date.isoformat() if self.discovery_date else None,
            'pest_type': self.pest_type,
            'affected_part': self.affected_part,
            'severity': self.severity,
            'control_date': self.control_date.isoformat() if self.control_date else None,
            'pesticide_name': self.pesticide_name,
            'dosage': self.dosage,
            'effect': self.effect,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<PestDiseaseRecord {self.pest_type} on {self.discovery_date}>'


class HarvestRecord(db.Model):
    __tablename__ = 'harvest_records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cycle_id = db.Column(db.Integer, db.ForeignKey('planting_cycles.id'), nullable=False)
    planned_date = db.Column(db.Date, comment='计划收获日期')
    actual_date = db.Column(db.Date, comment='实际收获日期')
    harvest_area = db.Column(db.Float, comment='收获面积（亩）')
    yield_tons = db.Column(db.Float, comment='产量（吨）')
    brix_percent = db.Column(db.Float, comment='蔗汁糖度（%）')
    sugar_percent = db.Column(db.Float, comment='含糖分（%）')
    unit_price = db.Column(db.Float, comment='单价（元/吨）')
    sugar_factory = db.Column(db.String(100), comment='交售糖厂')
    transport_cost = db.Column(db.Float, comment='运输费用（元）')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'cycle_id': self.cycle_id,
            'planned_date': self.planned_date.isoformat() if self.planned_date else None,
            'actual_date': self.actual_date.isoformat() if self.actual_date else None,
            'harvest_area': self.harvest_area,
            'yield_tons': self.yield_tons,
            'brix_percent': self.brix_percent,
            'sugar_percent': self.sugar_percent,
            'unit_price': self.unit_price,
            'sugar_factory': self.sugar_factory,
            'transport_cost': self.transport_cost,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<HarvestRecord {self.yield_tons}t on {self.actual_date}>'
