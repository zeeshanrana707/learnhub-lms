from datetime import datetime, timezone
from sqlalchemy import event
from app.extensions import db

def utcnow():
    return datetime.now(timezone.utc)

class CourseInstructor(db.Model):
    __tablename__ = 'course_instructors'
    __table_args__ = (
        db.UniqueConstraint('course_id', 'user_id', name='uq_course_instructor'),
    )

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    is_lead = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    course = db.relationship('Course', back_populates='instructors')
    user = db.relationship('User', back_populates='course_instructors')


class Module(db.Model):
    __tablename__ = 'modules'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    position = db.Column(db.Integer, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    course = db.relationship('Course', back_populates='modules')
    lessons = db.relationship('Lesson', back_populates='module', cascade='all, delete-orphan', order_by='Lesson.position', lazy='select')
    quizzes = db.relationship('Quiz', back_populates='module', lazy='select')

    def __repr__(self):
        return f'<Module {self.title}>'


class Lesson(db.Model):
    __tablename__ = 'lessons'

    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id', ondelete='CASCADE'), nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    content_type = db.Column(db.String(30), default='text', nullable=False)  # text, video_url, article
    duration_min = db.Column(db.Integer, default=10, nullable=False)
    duration_sec = db.Column(db.Integer, nullable=True)
    custom_challenges = db.Column(db.JSON, nullable=True)
    position = db.Column(db.Integer, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    module = db.relationship('Module', back_populates='lessons')
    resources = db.relationship('LessonResource', back_populates='lesson', cascade='all, delete-orphan', lazy='select')
    progress_records = db.relationship('LessonProgress', back_populates='lesson', cascade='all, delete-orphan', lazy='select')

    @property
    def formatted_duration(self):
        """Format duration as MM:SS (or HH:MM:SS) if seconds known, else X mins."""
        if self.duration_sec and self.duration_sec > 0:
            s = self.duration_sec
            h = s // 3600
            m = (s % 3600) // 60
            sec = s % 60
            if h > 0:
                return f"{h}:{m:02d}:{sec:02d}"
            return f"{m}:{sec:02d}"
        if self.duration_min:
            mins = self.duration_min
            if mins < 60:
                return f"{mins} mins"
            h = mins // 60
            m = mins % 60
            return f"{h}h {m}m" if m > 0 else f"{h} hr"
        return "0 mins"

    @property
    def breakdown(self):
        """Structured key components, overview explanation, and takeaways."""
        from app.utils.helpers import get_lesson_breakdown
        return get_lesson_breakdown(self)

    @property
    def programming_quiz(self):
        """Interactive 3-tier programming quiz (Basic, Intermediate, Advance)."""
        from app.services.programming_challenges import get_programming_quiz
        return get_programming_quiz(self)

    def __repr__(self):
        return f'<Lesson {self.title}>'


@event.listens_for(Lesson, 'before_insert')
@event.listens_for(Lesson, 'before_update')
def auto_sync_lesson_duration_listener(mapper, connection, target):
    """Automatically resolve true YouTube video length in minutes for present and future videos."""
    if target.content and ('youtube.com' in target.content or 'youtu.be' in target.content):
        # Auto-fetch if duration is default or unset
        if not target.duration_min or target.duration_min in (10, 30, 45):
            try:
                from app.services.youtube import get_youtube_duration_minutes
                real_min = get_youtube_duration_minutes(target.content)
                if real_min and real_min > 0:
                    target.duration_min = real_min
            except Exception:
                pass


class LessonResource(db.Model):
    __tablename__ = 'lesson_resources'

    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id', ondelete='CASCADE'), nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    resource_type = db.Column(db.String(30), default='link', nullable=False)  # link, pdf, code, file
    url_or_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    lesson = db.relationship('Lesson', back_populates='resources')

    def __repr__(self):
        return f'<LessonResource {self.title}>'


class Announcement(db.Model):
    __tablename__ = 'announcements'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    course = db.relationship('Course', back_populates='announcements')
    author = db.relationship('User', lazy='joined')

    def __repr__(self):
        return f'<Announcement {self.title}>'


class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'course_id', name='uq_user_course_enrollment'),
        db.Index('idx_enrollment_user_course', 'user_id', 'course_id'),
        db.CheckConstraint('progress_pct >= 0 AND progress_pct <= 100', name='check_progress_pct_range'),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    status = db.Column(db.String(20), default='active', nullable=False)  # active, completed, dropped
    enrolled_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    progress_pct = db.Column(db.Float, default=0.0, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    user = db.relationship('User', back_populates='enrollments')
    course = db.relationship('Course', back_populates='enrollments')
    lesson_progresses = db.relationship('LessonProgress', back_populates='enrollment', cascade='all, delete-orphan', lazy='select')
    certificate = db.relationship('Certificate', back_populates='enrollment', uselist=False, cascade='all, delete-orphan')
    grades = db.relationship('Grade', back_populates='enrollment', cascade='all, delete-orphan', lazy='select')

    def __repr__(self):
        return f'<Enrollment User:{self.user_id} Course:{self.course_id} {self.progress_pct}%>'


class LessonProgress(db.Model):
    __tablename__ = 'lesson_progresses'
    __table_args__ = (
        db.UniqueConstraint('enrollment_id', 'lesson_id', name='uq_enrollment_lesson_progress'),
    )

    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.id', ondelete='CASCADE'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id', ondelete='CASCADE'), nullable=False)
    is_completed = db.Column(db.Boolean, default=True, nullable=False)
    completed_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    enrollment = db.relationship('Enrollment', back_populates='lesson_progresses')
    lesson = db.relationship('Lesson', back_populates='progress_records')


class Wishlist(db.Model):
    __tablename__ = 'wishlists'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'course_id', name='uq_user_course_wishlist'),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    user = db.relationship('User', back_populates='wishlists')
    course = db.relationship('Course', back_populates='wishlists')
