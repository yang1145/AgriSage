from datetime import datetime, timezone
from extensions import db


class PlotImage(db.Model):
    __tablename__ = 'plot_images'

    VALID_GROWTH_STAGES = ('萌芽', '分蘖', '伸长期', '成熟期', '收获')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plot_id = db.Column(db.Integer, db.ForeignKey('plots.id'), nullable=False)
    cycle_id = db.Column(db.Integer, db.ForeignKey('planting_cycles.id'), nullable=True)
    growth_stage = db.Column(db.String(20), comment='生长阶段')
    file_path = db.Column(db.String(255), nullable=False, comment='文件路径')
    annotations = db.Column(db.JSON, nullable=True, comment='标注信息')
    taken_at = db.Column(db.DateTime, comment='拍摄时间')

    def to_dict(self):
        return {
            'id': self.id,
            'plot_id': self.plot_id,
            'cycle_id': self.cycle_id,
            'growth_stage': self.growth_stage,
            'file_path': self.file_path,
            'annotations': self.annotations,
            'taken_at': self.taken_at.isoformat() if self.taken_at else None,
        }

    def __repr__(self):
        return f'<PlotImage Plot#{self.plot_id} {self.growth_stage}>'
