from datetime import datetime, timezone
from app.extensions import db

def utcnow():
    return datetime.now(timezone.utc)

class Certificate(db.Model):
    __tablename__ = 'certificates'

    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.id', ondelete='CASCADE'), unique=True, nullable=False)
    code = db.Column(db.String(64), unique=True, nullable=False, index=True)
    issued_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    enrollment = db.relationship('Enrollment', back_populates='certificate')

    def __repr__(self):
        return f'<Certificate {self.code}>'


class Badge(db.Model):
    __tablename__ = 'badges'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(80), default='bi-trophy', nullable=False)
    rule_code = db.Column(db.String(50), nullable=False)  # first_course, perfect_quiz, top_student
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    user_badges = db.relationship('UserBadge', back_populates='badge', cascade='all, delete-orphan', lazy='select')

    def __repr__(self):
        return f'<Badge {self.name}>'


class UserBadge(db.Model):
    __tablename__ = 'user_badges'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'badge_id', name='uq_user_badge'),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badges.id', ondelete='CASCADE'), nullable=False)
    awarded_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    user = db.relationship('User', back_populates='user_badges')
    badge = db.relationship('Badge', back_populates='user_badges')


class Review(db.Model):
    __tablename__ = 'reviews'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'course_id', name='uq_user_course_review'),
        db.CheckConstraint('rating >= 1 AND rating <= 5', name='check_review_rating_1_to_5'),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    user = db.relationship('User', back_populates='reviews')
    course = db.relationship('Course', back_populates='reviews')

    def __repr__(self):
        return f'<Review Course:{self.course_id} Stars:{self.rating}>'
