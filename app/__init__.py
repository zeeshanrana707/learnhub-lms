import os
from datetime import datetime, timezone
from flask import Flask, render_template, session
from sqlalchemy import event
from sqlalchemy.engine import Engine

from config import config_by_name
from app.extensions import db, migrate, login_manager, csrf
from app.models.users import User, Notification
from app.models.community import Message

def create_app(config_name: str = None) -> Flask:
    """Application factory for the LMS Flask Application."""
    if not config_name:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Enforce SQLite foreign key constraints
    with app.app_context():
        @event.listens_for(Engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            if 'sqlite' in app.config.get('SQLALCHEMY_DATABASE_URI', ''):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.blueprints.auth import auth_bp
    from app.blueprints.catalog import catalog_bp
    from app.blueprints.learning import learning_bp
    from app.blueprints.assessments import assessments_bp
    from app.blueprints.community import community_bp
    from app.blueprints.commerce import commerce_bp
    from app.blueprints.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(catalog_bp)
    app.register_blueprint(learning_bp)
    app.register_blueprint(assessments_bp)
    app.register_blueprint(community_bp)
    app.register_blueprint(commerce_bp)
    app.register_blueprint(admin_bp)

    # Jinja template filter for YouTube video embedding
    from app.utils.helpers import extract_youtube_id
    @app.template_filter('youtube_embed')
    def youtube_embed_filter(text):
        video_id = extract_youtube_id(text)
        return f"https://www.youtube.com/embed/{video_id}" if video_id else None

    @app.template_filter('youtube_id')
    def youtube_id_filter(text):
        return extract_youtube_id(text) or ''

    # Jinja template filter for human-friendly video duration formatting
    @app.template_filter('format_duration')
    def format_duration_filter(minutes):
        """Format duration in minutes into a clean string (e.g. 18m, 1h 15m, 4h 27m)."""
        if not minutes or minutes <= 0:
            return "0 mins"
        try:
            mins = int(minutes)
        except (ValueError, TypeError):
            return f"{minutes} mins"
        if mins < 60:
            return f"{mins} mins"
        hours = mins // 60
        rem = mins % 60
        if rem == 0:
            return f"{hours} hr" if hours == 1 else f"{hours} hrs"
        return f"{hours}h {rem}m"

    # Context processors for global navbar indicators
    @app.context_processor
    def inject_global_data():
        from flask_login import current_user
        from flask import url_for
        from app.models.catalog import Course, Category, Roadmap
        from app.models.content import Wishlist
        cart_count = len(session.get('cart', []))
        unread_notifs = 0
        unread_msgs = 0
        wishlist_count = 0
        recent_notifs = []
        recent_msgs = []
        resume_learning = None
        pending_grading_count = 0

        if current_user.is_authenticated:
            unread_notifs = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
            unread_msgs = Message.query.filter_by(recipient_id=current_user.id, is_read=False).count()
            recent_notifs = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).limit(4).all()
            recent_msgs = Message.query.filter_by(recipient_id=current_user.id).order_by(Message.created_at.desc()).limit(4).all()
            wishlist_count = Wishlist.query.filter_by(user_id=current_user.id).count()

            # 1. Resume Learning Quick Action for Students
            try:
                from app.models.content import Enrollment, LessonProgress
                active_enr = Enrollment.query.filter_by(user_id=current_user.id, status='active').order_by(Enrollment.progress_pct.desc(), Enrollment.enrolled_at.desc()).first()
                if not active_enr:
                    active_enr = Enrollment.query.filter(Enrollment.user_id == current_user.id, Enrollment.progress_pct < 100).order_by(Enrollment.enrolled_at.desc()).first()

                if active_enr and active_enr.course:
                    c = active_enr.course
                    completed_ids = {lp.lesson_id for lp in LessonProgress.query.filter_by(enrollment_id=active_enr.id, is_completed=True).all()}
                    all_lessons = [l for m in c.modules for l in m.lessons]
                    target_lesson = next((l for l in all_lessons if l.id not in completed_ids), None)
                    if not target_lesson and all_lessons:
                        target_lesson = all_lessons[0]

                    if target_lesson:
                        resume_learning = {
                            'course_id': c.id,
                            'course_title': c.title,
                            'lesson_id': target_lesson.id,
                            'lesson_title': target_lesson.title,
                            'progress_pct': int(round(active_enr.progress_pct)),
                            'url': url_for('learning.lesson_player', lesson_id=target_lesson.id)
                        }
            except Exception:
                resume_learning = None

            # 2. Grading Queue Badge for Instructors & Admins
            try:
                if current_user.is_instructor or current_user.is_admin:
                    from app.models.assessments import Submission, Assignment
                    from app.models.content import CourseInstructor
                    if current_user.is_admin:
                        pending_grading_count = Submission.query.filter_by(status='submitted').count()
                    else:
                        inst_course_ids = [c.id for c in Course.query.filter_by(created_by=current_user.id).all()]
                        inst_course_ids += [ci.course_id for ci in CourseInstructor.query.filter_by(user_id=current_user.id).all()]
                        if inst_course_ids:
                            pending_grading_count = Submission.query.join(Assignment).filter(
                                Assignment.course_id.in_(inst_course_ids),
                                Submission.status == 'submitted'
                            ).count()
            except Exception:
                pending_grading_count = 0

        try:
            courses = Course.query.filter_by(status='published', is_active=True).with_entities(Course.title).all()
            course_titles = [c.title for c in courses]
        except Exception:
            course_titles = []
        try:
            navbar_categories = Category.query.order_by(Category.name).all()
        except Exception:
            navbar_categories = []
        try:
            navbar_roadmaps = Roadmap.query.filter_by(is_active=True).order_by(Roadmap.id).all()
        except Exception:
            navbar_roadmaps = []
        return {
            'cart_count': cart_count,
            'wishlist_count': wishlist_count,
            'unread_notifications_count': unread_notifs,
            'unread_messages_count': unread_msgs,
            'navbar_recent_notifications': recent_notifs,
            'navbar_recent_messages': recent_msgs,
            'navbar_categories': navbar_categories,
            'navbar_roadmaps': navbar_roadmaps,
            'resume_learning': resume_learning,
            'pending_grading_count': pending_grading_count,
            'current_year': datetime.now().year,
            'navbar_course_titles': course_titles
        }

    # Error Handlers
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    return app
