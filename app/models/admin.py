from datetime import datetime, timezone
from app.extensions import db

def utcnow():
    return datetime.now(timezone.utc)

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    action = db.Column(db.String(50), nullable=False, index=True)  # create, update, delete, login, logout
    entity_type = db.Column(db.String(50), nullable=False, index=True)  # User, Course, Quiz, Assignment, etc.
    entity_id = db.Column(db.Integer, nullable=True)
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False, index=True)

    user = db.relationship('User', back_populates='audit_logs')

    def __repr__(self):
        return f'<AuditLog {self.action} on {self.entity_type}:{self.entity_id}>'


class Setting(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    value = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    @classmethod
    def get_value(cls, key: str, default=None):
        item = cls.query.filter_by(key=key).first()
        return item.value if item else default

    @classmethod
    def set_value(cls, key: str, value: str, description: str = None):
        item = cls.query.filter_by(key=key).first()
        if not item:
            item = cls(key=key, value=value, description=description)
            db.session.add(item)
        else:
            item.value = value
            if description:
                item.description = description
        db.session.commit()
        return item

    def __repr__(self):
        return f'<Setting {self.key}={self.value}>'
