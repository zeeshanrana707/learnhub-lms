from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

def utcnow():
    return datetime.now(timezone.utc)

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    users = db.relationship('User', back_populates='role', lazy='select')
    permissions = db.relationship('Permission', secondary='role_permissions', back_populates='roles', lazy='selectin')

    def __repr__(self):
        return f'<Role {self.name}>'


class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    roles = db.relationship('Role', secondary='role_permissions', back_populates='permissions', lazy='select')

    def __repr__(self):
        return f'<Permission {self.code}>'


class RolePermission(db.Model):
    __tablename__ = 'role_permissions'
    __table_args__ = (
        db.UniqueConstraint('role_id', 'permission_id', name='uq_role_permission'),
    )

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    # Relationships
    role = db.relationship('Role', back_populates='users', lazy='joined')
    profile = db.relationship('UserProfile', back_populates='user', uselist=False, cascade='all, delete-orphan', lazy='joined')
    notifications = db.relationship('Notification', back_populates='user', cascade='all, delete-orphan', lazy='select', order_by='Notification.created_at.desc()')
    enrollments = db.relationship('Enrollment', back_populates='user', lazy='select')
    orders = db.relationship('Order', back_populates='user', lazy='select')
    course_instructors = db.relationship('CourseInstructor', back_populates='user', lazy='select')
    created_courses = db.relationship('Course', back_populates='creator', foreign_keys='Course.created_by', lazy='select')
    wishlists = db.relationship('Wishlist', back_populates='user', cascade='all, delete-orphan', lazy='select')
    quiz_attempts = db.relationship('QuizAttempt', back_populates='user', lazy='select')
    submissions = db.relationship('Submission', back_populates='user', lazy='select')
    forum_threads = db.relationship('ForumThread', back_populates='author', lazy='select')
    forum_posts = db.relationship('ForumPost', back_populates='author', lazy='select')
    post_likes = db.relationship('PostLike', back_populates='user', cascade='all, delete-orphan', lazy='select')
    sent_messages = db.relationship('Message', back_populates='sender', foreign_keys='Message.sender_id', lazy='select')
    received_messages = db.relationship('Message', back_populates='recipient', foreign_keys='Message.recipient_id', lazy='select')
    user_badges = db.relationship('UserBadge', back_populates='user', cascade='all, delete-orphan', lazy='select')
    reviews = db.relationship('Review', back_populates='user', lazy='select')
    audit_logs = db.relationship('AuditLog', back_populates='user', lazy='select')

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def has_role(self, role_name: str) -> bool:
        return bool(self.role and self.role.name.lower() == role_name.lower())

    def has_permission(self, perm_code: str) -> bool:
        if not self.role:
            return False
        return any(p.code == perm_code for p in self.role.permissions)

    @property
    def is_admin(self) -> bool:
        return self.has_role('admin')

    @property
    def is_instructor(self) -> bool:
        return self.has_role('instructor')

    @property
    def is_student(self) -> bool:
        return self.has_role('student')

    def __repr__(self):
        return f'<User {self.username}>'


class UserProfile(db.Model):
    __tablename__ = 'user_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    avatar = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    user = db.relationship('User', back_populates='profile')

    def __repr__(self):
        return f'<UserProfile for User {self.user_id}>'


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(255), nullable=True)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    user = db.relationship('User', back_populates='notifications')

    def __repr__(self):
        return f'<Notification {self.title}>'
