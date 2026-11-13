from datetime import datetime, timezone
from app.extensions import db

def utcnow():
    return datetime.now(timezone.utc)

class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    courses = db.relationship('Course', back_populates='department', lazy='select')

    def __repr__(self):
        return f'<Department {self.name}>'


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='SET NULL'), nullable=True)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    parent = db.relationship('Category', remote_side=[id], back_populates='children')
    children = db.relationship('Category', back_populates='parent', lazy='select')
    courses = db.relationship('Course', back_populates='category', lazy='select')

    @property
    def roadmap_courses(self):
        """Returns courses explicitly assigned to the roadmap for this category, or empty if none."""
        rm = Roadmap.query.filter_by(slug=self.slug).first()
        if rm:
            return rm.courses
        return []

    def __repr__(self):
        return f'<Category {self.name}>'


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    courses = db.relationship('Course', secondary='course_tags', back_populates='tags', lazy='select')

    def __repr__(self):
        return f'<Tag {self.name}>'


class CourseTag(db.Model):
    __tablename__ = 'course_tags'
    __table_args__ = (
        db.UniqueConstraint('course_id', 'tag_id', name='uq_course_tag'),
    )

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)


class CoursePrerequisite(db.Model):
    __tablename__ = 'course_prerequisites'
    __table_args__ = (
        db.UniqueConstraint('course_id', 'prerequisite_id', name='uq_course_prerequisite'),
    )

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    prerequisite_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)


class Course(db.Model):
    __tablename__ = 'courses'
    __table_args__ = (
        db.CheckConstraint('price >= 0', name='check_course_price_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(180), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, default=0.0, nullable=False)
    level = db.Column(db.String(30), default='Beginner', nullable=False)  # Beginner, Intermediate, Advanced
    status = db.Column(db.String(20), default='draft', nullable=False, index=True)  # draft, published, archived
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    # Relationships
    department = db.relationship('Department', back_populates='courses', lazy='joined')
    category = db.relationship('Category', back_populates='courses', lazy='joined')
    creator = db.relationship('User', back_populates='created_courses', foreign_keys=[created_by], lazy='joined')

    tags = db.relationship('Tag', secondary='course_tags', back_populates='courses', lazy='selectin')

    # Prerequisites: courses that must be completed before enrolling in this course
    prerequisites = db.relationship(
        'Course',
        secondary='course_prerequisites',
        primaryjoin='Course.id == CoursePrerequisite.course_id',
        secondaryjoin='Course.id == CoursePrerequisite.prerequisite_id',
        backref=db.backref('required_for', lazy='select'),
        lazy='selectin'
    )

    instructors = db.relationship('CourseInstructor', back_populates='course', cascade='all, delete-orphan', lazy='selectin')
    modules = db.relationship('Module', back_populates='course', cascade='all, delete-orphan', order_by='Module.position', lazy='select')
    announcements = db.relationship('Announcement', back_populates='course', cascade='all, delete-orphan', lazy='select', order_by='Announcement.created_at.desc()')
    quizzes = db.relationship('Quiz', back_populates='course', cascade='all, delete-orphan', lazy='select')
    assignments = db.relationship('Assignment', back_populates='course', cascade='all, delete-orphan', lazy='select')
    enrollments = db.relationship('Enrollment', back_populates='course', lazy='select')
    reviews = db.relationship('Review', back_populates='course', cascade='all, delete-orphan', lazy='select', order_by='Review.created_at.desc()')
    forum_threads = db.relationship('ForumThread', back_populates='course', cascade='all, delete-orphan', lazy='select')
    order_items = db.relationship('OrderItem', back_populates='course', lazy='select')
    wishlists = db.relationship('Wishlist', back_populates='course', cascade='all, delete-orphan', lazy='select')

    @property
    def is_free(self) -> bool:
        return self.price <= 0.0

    @property
    def real_reviews(self):
        """Reviews authored by real students only."""
        return [
            r for r in self.reviews
            if r.user and getattr(r.user, 'is_active', True)
            and not (
                (getattr(r.user, 'email', '') or '').endswith('@lms.local')
                and (getattr(r.user, 'username', '') or '').startswith('student')
            )
        ]

    @property
    def average_rating(self) -> float:
        valid_revs = self.real_reviews
        if not valid_revs:
            return 0.0
        return round(sum(r.rating for r in valid_revs) / len(valid_revs), 1)

    @property
    def total_lessons(self) -> int:
        return sum(len(m.lessons) for m in self.modules)

    @property
    def youtube_video_id(self) -> str | None:
        """First YouTube video ID for the course curriculum."""
        import re
        first_lesson = None
        for mod in self.modules:
            if mod.lessons:
                first_lesson = mod.lessons[0]
                break
        if first_lesson and first_lesson.content:
            yt_match = re.search(r'(?:v=|\/embed\/|\/watch\?v=|\.be\/)([a-zA-Z0-9_-]{11})', first_lesson.content)
            if yt_match:
                return yt_match.group(1)
        return None

    @property
    def thumbnail_url(self) -> str:
        """High-definition YouTube video thumbnail image or clean fallback."""
        vid_id = self.youtube_video_id
        if vid_id:
            return f"https://img.youtube.com/vi/{vid_id}/hqdefault.jpg"
        return "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&auto=format&fit=crop&q=80"

    @property
    def total_enrolled_students(self) -> int:
        """Total number of real students actively enrolled in this course."""
        count = 0
        for e in self.enrollments:
            if getattr(e, 'status', 'active') not in ('active', 'completed'):
                continue
            u = getattr(e, 'user', None)
            if not u or not getattr(u, 'is_active', True):
                continue
            # Exclude any dummy/seed accounts with @lms.local
            uname = (getattr(u, 'username', '') or '').lower()
            uemail = (getattr(u, 'email', '') or '').lower()
            if uemail.endswith('@lms.local') and uname.startswith('student'):
                continue
            count += 1
        return count

    @property
    def primary_instructor(self):
        """Lead instructor user object for this course."""
        if self.instructors:
            for ci in self.instructors:
                if getattr(ci, 'is_lead', False):
                    return ci.user
            return self.instructors[0].user
        return self.creator

    @property
    def instructor_name(self) -> str:
        """Full name or display username of the lead instructor."""
        inst = self.primary_instructor
        if not inst:
            return "Lead Instructor"
        if hasattr(inst, 'profile') and inst.profile and inst.profile.full_name:
            return inst.profile.full_name
        return inst.username

    def is_instructor(self, user_id: int) -> bool:
        if self.created_by == user_id:
            return True
        return any(ci.user_id == user_id for ci in self.instructors)

    def __repr__(self):
        return f'<Course {self.title}>'


class Roadmap(db.Model):
    __tablename__ = 'roadmaps'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=True, nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False, index=True)
    tagline = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    badge = db.Column(db.String(80), default='Career Roadmap')
    icon = db.Column(db.String(80), default='bi-diagram-3-fill')
    color = db.Column(db.String(30), default='#3b82f6')
    bg_gradient = db.Column(db.String(255), default='linear-gradient(135deg, #1d4ed8 0%, #1e3a8a 100%)')
    estimated_duration = db.Column(db.String(80), default='3 - 5 Months')
    skills_csv = db.Column(db.Text, nullable=True)
    target_roles_csv = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    stages = db.relationship(
        'RoadmapStage',
        back_populates='roadmap',
        cascade='all, delete-orphan',
        order_by='RoadmapStage.stage_number'
    )

    @property
    def name(self):
        return self.title

    @property
    def skills(self):
        if not self.skills_csv:
            return []
        return [s.strip() for s in self.skills_csv.split(',') if s.strip()]

    @property
    def target_roles(self):
        if not self.target_roles_csv:
            return []
        return [r.strip() for r in self.target_roles_csv.split(',') if r.strip()]

    @property
    def courses(self):
        """Published and active courses in this roadmap strictly ordered by stage number."""
        ordered = sorted(self.stages, key=lambda s: s.stage_number)
        return [s.course for s in ordered if s.course and s.course.is_active and s.course.status == 'published']

    @property
    def all_stage_courses(self):
        """All courses currently assigned to stages regardless of status (for admin stage manager)."""
        ordered = sorted(self.stages, key=lambda s: s.stage_number)
        return [s.course for s in ordered if s.course]

    @property
    def total_lessons(self):
        return sum(c.total_lessons for c in self.courses)

    @property
    def total_duration_mins(self):
        return sum(sum(l.duration_min for m in c.modules for l in m.lessons) for c in self.courses)

    @property
    def total_hours(self):
        return round(self.total_duration_mins / 60, 1)

    def __repr__(self):
        return f'<Roadmap {self.title}>'


class RoadmapStage(db.Model):
    __tablename__ = 'roadmap_stages'

    id = db.Column(db.Integer, primary_key=True)
    roadmap_id = db.Column(db.Integer, db.ForeignKey('roadmaps.id', ondelete='CASCADE'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    stage_number = db.Column(db.Integer, nullable=False, default=1)
    stage_label = db.Column(db.String(80), nullable=True)

    roadmap = db.relationship('Roadmap', back_populates='stages')
    course = db.relationship('Course', backref=db.backref('roadmap_stages', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<RoadmapStage RM:{self.roadmap_id} Stage:{self.stage_number} Course:{self.course_id}>'
