from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, session
from flask_login import current_user, login_required
from app.extensions import db
from app.models.catalog import Course, Department, Category, Tag, CourseTag, CoursePrerequisite, Roadmap, RoadmapStage
from app.models.content import CourseInstructor, Module, Lesson, Enrollment, Wishlist
from app.models.assessments import Submission, Quiz
from app.models.community import ForumThread
from app.forms.catalog import CourseForm
from app.utils.decorators import instructor_or_admin_required, instructor_course_owner_required
from app.utils.helpers import slugify, log_action, fuzzy_search_courses

catalog_bp = Blueprint('catalog', __name__)

ROADMAP_META = {
    'ai-engineer-roadmap': {
        'icon': 'bi-cpu-fill',
        'color': '#6366f1',
        'bg_gradient': 'linear-gradient(135deg, #4338ca 0%, #312e81 100%)',
        'badge': 'Hot Career Track',
        'tagline': 'Master Artificial Intelligence from Python & Math to Machine Learning, Deep Learning, and Generative AI / LLMs with LangChain.',
        'estimated_duration': '6 - 9 Months',
        'target_roles': ['AI Engineer', 'Machine Learning Engineer', 'LLM Application Developer', 'Data Scientist'],
        'skills': ['Python', 'NumPy & Pandas', 'Scikit-Learn', 'PyTorch', 'Transformers', 'LangChain', 'Vector DBs (RAG)']
    },
    'full-stack-web-roadmap': {
        'icon': 'bi-code-slash',
        'color': '#0ea5e9',
        'bg_gradient': 'linear-gradient(135deg, #0369a1 0%, #0c4a6e 100%)',
        'badge': 'High Demand',
        'tagline': 'Complete pathway from Modern JavaScript and DOM to Python Flask backends and React 18 single-page applications.',
        'estimated_duration': '4 - 6 Months',
        'target_roles': ['Full-Stack Web Developer', 'Backend Software Engineer', 'Frontend Engineer'],
        'skills': ['HTML5/CSS3', 'Modern ES6+ JS', 'Python 3.x', 'Flask 3.x', 'Flask-SQLAlchemy', 'React 18', 'JWT Auth', 'REST APIs']
    },
    'cloud-devops-roadmap': {
        'icon': 'bi-cloud-check-fill',
        'color': '#059669',
        'bg_gradient': 'linear-gradient(135deg, #047857 0%, #064e3b 100%)',
        'badge': 'Enterprise Essential',
        'tagline': 'Master Linux systems administration, Docker containerization, automated GitHub Actions CI/CD, and Kubernetes orchestration.',
        'estimated_duration': '4 - 6 Months',
        'target_roles': ['DevOps Engineer', 'Cloud Infrastructure Architect', 'Site Reliability Engineer (SRE)'],
        'skills': ['Linux CLI', 'Bash Scripting', 'Docker', 'Docker Compose', 'GitHub Actions', 'AWS Cloud', 'Kubernetes']
    },
    'cybersecurity-roadmap': {
        'icon': 'bi-shield-lock-fill',
        'color': '#dc2626',
        'bg_gradient': 'linear-gradient(135deg, #b91c1c 0%, #7f1d1d 100%)',
        'badge': 'Mission Critical',
        'tagline': 'Learn networking fundamentals, OWASP Top 10 web vulnerabilities, SQLi/XSS defense, and hands-on ethical hacking penetration testing.',
        'estimated_duration': '5 - 7 Months',
        'target_roles': ['Cybersecurity Analyst', 'Penetration Tester', 'Application Security Specialist'],
        'skills': ['Computer Networking', 'Wireshark', 'OWASP Top 10', 'SQLi & XSS', 'Nmap', 'Cryptography', 'Kali Linux']
    },
    'data-engineering-roadmap': {
        'icon': 'bi-database-fill-gear',
        'color': '#d97706',
        'bg_gradient': 'linear-gradient(135deg, #b45309 0%, #78350f 100%)',
        'badge': 'High Growth',
        'tagline': 'From relational SQL modeling and normalization to high-throughput REST APIs and Apache Kafka event-driven architectures.',
        'estimated_duration': '4 - 6 Months',
        'target_roles': ['Data Engineer', 'Database Administrator', 'Backend Data Architect'],
        'skills': ['SQL', 'Relational Schema', 'Indexing & Query Plans', 'Redis Caching', 'Apache Kafka', 'RESTful APIs']
    },
    'cs-foundations-roadmap': {
        'icon': 'bi-mortarboard-fill',
        'color': '#8b5cf6',
        'bg_gradient': 'linear-gradient(135deg, #6d28d9 0%, #4c1d95 100%)',
        'badge': 'Core Foundations',
        'tagline': 'Harvard CS50 computational thinking, memory and pointers, Big-O algorithmic complexity, data structures, and Figma design systems.',
        'estimated_duration': '3 - 5 Months',
        'target_roles': ['Software Engineer', 'Computer Scientist', 'Product Designer'],
        'skills': ['Binary & Memory', 'C Programming', 'Algorithms & Big-O', 'Data Structures (Trees/Lists)', 'Figma Design']
    }
}

@catalog_bp.route('/dashboard')
def dashboard_shortcut():
    return redirect(url_for('learning.my_learning'))


@catalog_bp.route('/')
def home():
    """Home landing page with featured courses, roadmaps, and categories."""
    # When admin is active, redirect to admin dashboard unless preview mode is explicitly requested via Live Site
    if current_user.is_authenticated and current_user.is_admin and not (request.args.get('preview') or session.get('live_preview')):
        return redirect(url_for('admin.dashboard'))

    featured_courses = Course.query.filter_by(status='published', is_active=True).order_by(Course.created_at.desc()).limit(6).all()
    categories = Category.query.all()
    departments = Department.query.all()
    
    # Load career roadmaps
    roadmap_list = []
    active_roadmaps = Roadmap.query.filter_by(is_active=True).all()
    for rm in active_roadmaps:
        courses = rm.courses
        if courses:
            meta = {
                'icon': rm.icon or 'bi-diagram-3-fill',
                'color': rm.color or '#3b82f6',
                'bg_gradient': rm.bg_gradient or 'linear-gradient(135deg, #1d4ed8 0%, #1e3a8a 100%)',
                'badge': rm.badge or 'Career Roadmap',
                'tagline': rm.tagline or f'Structured topic-by-topic learning track for {rm.title}.',
                'estimated_duration': rm.estimated_duration or '3 - 5 Months',
                'target_roles': rm.target_roles or [f'{rm.title} Specialist'],
                'skills': rm.skills or [rm.title]
            }
            if rm.slug in ROADMAP_META:
                for k, v in ROADMAP_META[rm.slug].items():
                    if not meta.get(k):
                        meta[k] = v

            roadmap_list.append({
                'category': rm,
                'roadmap': rm,
                'courses': courses,
                'meta': meta,
                'total_lessons': rm.total_lessons,
                'total_hours': rm.total_hours
            })

    return render_template(
        'catalog/home.html',
        featured_courses=featured_courses,
        categories=categories,
        departments=departments,
        roadmaps=roadmap_list
    )


@catalog_bp.route('/roadmaps')
def roadmaps():
    """Explore Career Field Roadmaps (Beginner to Advanced pathways)."""
    active_roadmaps = Roadmap.query.filter_by(is_active=True).all()
    roadmap_list = []
    for rm in active_roadmaps:
        courses = rm.courses
        if courses:
            meta = {
                'icon': rm.icon or 'bi-diagram-3-fill',
                'color': rm.color or '#3b82f6',
                'bg_gradient': rm.bg_gradient or 'linear-gradient(135deg, #1d4ed8 0%, #1e3a8a 100%)',
                'badge': rm.badge or 'Career Roadmap',
                'tagline': rm.tagline or f'Structured topic-by-topic learning track for {rm.title}.',
                'estimated_duration': rm.estimated_duration or '3 - 5 Months',
                'target_roles': rm.target_roles or [f'{rm.title} Specialist'],
                'skills': rm.skills or [rm.title]
            }
            if rm.slug in ROADMAP_META:
                for k, v in ROADMAP_META[rm.slug].items():
                    if not meta.get(k):
                        meta[k] = v
            roadmap_list.append({
                'category': rm,
                'roadmap': rm,
                'courses': courses,
                'meta': meta,
                'total_lessons': rm.total_lessons,
                'total_hours': rm.total_hours
            })

    return render_template('catalog/roadmaps.html', roadmaps=roadmap_list)


@catalog_bp.route('/roadmaps/<slug>')
def roadmap_detail(slug):
    """Detailed visual timeline for a specific career field roadmap."""
    roadmap = Roadmap.query.filter_by(slug=slug, is_active=True).first()
    if not roadmap:
        cat = Category.query.filter_by(slug=slug).first()
        if cat:
            roadmap = Roadmap.query.filter_by(slug=cat.slug).first()
    if not roadmap:
        abort(404)

    courses = roadmap.courses
    meta = {
        'icon': roadmap.icon or 'bi-diagram-3-fill',
        'color': roadmap.color or '#3b82f6',
        'bg_gradient': roadmap.bg_gradient or 'linear-gradient(135deg, #1d4ed8 0%, #1e3a8a 100%)',
        'badge': roadmap.badge or 'Career Roadmap',
        'tagline': roadmap.tagline or f'Structured topic-by-topic learning track for {roadmap.title}.',
        'estimated_duration': roadmap.estimated_duration or '3 - 5 Months',
        'target_roles': roadmap.target_roles or [f'{roadmap.title} Specialist'],
        'skills': roadmap.skills or [roadmap.title]
    }
    if roadmap.slug in ROADMAP_META:
        for k, v in ROADMAP_META[roadmap.slug].items():
            if not meta.get(k):
                meta[k] = v

    # If student is logged in, determine enrollment, completed, and unlock status
    student_status = {}
    if current_user.is_authenticated:
        from app.models.content import Enrollment, Wishlist
        user_enrollments = {e.course_id: e for e in Enrollment.query.filter_by(user_id=current_user.id).all()}
        user_wishlists = {w.course_id for w in Wishlist.query.filter_by(user_id=current_user.id).all()}
        is_staff = current_user.is_admin or current_user.is_instructor
        for idx, c in enumerate(courses):
            enrollment = user_enrollments.get(c.id)
            prereqs_met = True
            if not is_staff:
                for req in c.prerequisites:
                    req_enroll = user_enrollments.get(req.id)
                    if not req_enroll or req_enroll.status != 'completed':
                        prereqs_met = False
                        break
            student_status[c.id] = {
                'enrolled': bool(enrollment),
                'completed': bool(enrollment and enrollment.status == 'completed'),
                'progress_pct': enrollment.progress_pct if enrollment else 0.0,
                'prereqs_met': prereqs_met,
                'is_wishlisted': c.id in user_wishlists
            }

    return render_template(
        'catalog/roadmap_detail.html',
        category=roadmap,
        courses=courses,
        meta=meta,
        student_status=student_status,
        total_hours=roadmap.total_hours
    )


@catalog_bp.route('/courses')
def index():
    """Full searchable, filterable catalog with pagination."""
    page = request.args.get('page', 1, type=int)
    search_q = request.args.get('q', '').strip()
    cat_id = request.args.get('category', type=int)
    dept_id = request.args.get('department', type=int)
    tag_id = request.args.get('tag', type=int)
    level = request.args.get('level', '').strip()
    price_filter = request.args.get('price', '').strip()  # 'free', 'paid'

    query = Course.query.filter_by(status='published', is_active=True)

    fuzzy_used = False
    if search_q:
        exact_check = query.filter((Course.title.ilike(f'%{search_q}%')) | (Course.description.ilike(f'%{search_q}%'))).count()
        if exact_check > 0:
            query = query.filter((Course.title.ilike(f'%{search_q}%')) | (Course.description.ilike(f'%{search_q}%')))
        else:
            # Smart typo tolerance
            all_published = Course.query.filter_by(status='published', is_active=True).all()
            fuzzy_matches = fuzzy_search_courses(all_published, search_q, limit=24)
            if fuzzy_matches:
                fuzzy_used = True
                fuzzy_ids = [c.id for c in fuzzy_matches]
                query = query.filter(Course.id.in_(fuzzy_ids))
            else:
                query = query.filter((Course.title.ilike(f'%{search_q}%')) | (Course.description.ilike(f'%{search_q}%')))
    if cat_id:
        query = query.filter(Course.category_id == cat_id)
    if dept_id:
        query = query.filter(Course.department_id == dept_id)
    if tag_id:
        query = query.join(CourseTag).filter(CourseTag.tag_id == tag_id)
    if level in ('Beginner', 'Intermediate', 'Advanced'):
        query = query.filter(Course.level == level)
    if price_filter == 'free':
        query = query.filter(Course.price <= 0.0)
    elif price_filter == 'paid':
        query = query.filter(Course.price > 0.0)

    courses = query.order_by(Course.created_at.desc()).paginate(page=page, per_page=9, error_out=False)
    categories = Category.query.all()
    departments = Department.query.all()
    tags = Tag.query.all()

    return render_template(
        'catalog/index.html',
        courses=courses,
        categories=categories,
        departments=departments,
        tags=tags,
        search_q=search_q,
        selected_category=cat_id,
        selected_department=dept_id,
        selected_tag=tag_id,
        selected_level=level,
        selected_price=price_filter,
        fuzzy_used=fuzzy_used
    )


@catalog_bp.route('/courses/<int:course_id>')
def detail(course_id):
    """Course detail page."""
    course = Course.query.get_or_404(course_id)
    if not course.is_active or (course.status != 'published' and not (current_user.is_authenticated and (current_user.is_admin or course.is_instructor(current_user.id)))):
        flash('This course is not currently available.', 'warning')
        return redirect(url_for('catalog.index'))

    is_enrolled = False
    in_wishlist = False
    missing_prereqs = []

    if current_user.is_authenticated:
        enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course.id).first()
        is_enrolled = bool(enrollment)
        in_wishlist = bool(Wishlist.query.filter_by(user_id=current_user.id, course_id=course.id).first())

        # Check prerequisite completion
        if course.prerequisites:
            for req in course.prerequisites:
                passed = Enrollment.query.filter_by(
                    user_id=current_user.id,
                    course_id=req.id,
                    status='completed'
                ).first()
                if not passed:
                    missing_prereqs.append(req)

    all_lessons = [l for m in course.modules for l in m.lessons]
    preview_lesson = all_lessons[0] if all_lessons else None

    return render_template(
        'catalog/detail.html',
        course=course,
        is_enrolled=is_enrolled,
        in_wishlist=in_wishlist,
        missing_prereqs=missing_prereqs,
        preview_lesson=preview_lesson,
        all_lessons=all_lessons
    )


@catalog_bp.route('/instructor/dashboard')
@login_required
@instructor_or_admin_required
def instructor_dashboard():
    """Instructor portal dashboard."""
    if current_user.is_admin:
        courses = Course.query.all()
    else:
        # Created or assigned courses
        assigned_ids = [ci.course_id for ci in current_user.course_instructors]
        courses = Course.query.filter((Course.created_by == current_user.id) | (Course.id.in_(assigned_ids))).all()

    course_ids = [c.id for c in courses]
    pending_submissions = Submission.query.join(Submission.assignment).filter(
        Submission.assignment.has(Course.id.in_(course_ids)),
        Submission.status == 'submitted'
    ).all() if course_ids else []

    recent_threads = ForumThread.query.filter(ForumThread.course_id.in_(course_ids)).order_by(ForumThread.created_at.desc()).limit(5).all() if course_ids else []

    total_students = Enrollment.query.filter(Enrollment.course_id.in_(course_ids)).count() if course_ids else 0

    return render_template(
        'catalog/instructor_dashboard.html',
        courses=courses,
        pending_submissions=pending_submissions,
        recent_threads=recent_threads,
        total_students=total_students
    )


@catalog_bp.route('/api/search')
def api_search():
    """Live AJAX search endpoint: returns top matching published courses as JSON."""
    q = request.args.get('q', '').strip()
    if len(q) < 2:
        return {'results': [], 'query': q}

    exact_matches = Course.query.filter(
        Course.status == 'published',
        Course.is_active == True,
        (Course.title.ilike(f'%{q}%')) | (Course.description.ilike(f'%{q}%'))
    ).order_by(Course.created_at.desc()).limit(6).all()

    if len(exact_matches) >= 3:
        matches = exact_matches
    else:
        # Typo-tolerant search fallback
        all_published = Course.query.filter_by(status='published', is_active=True).all()
        fuzzy_matches = fuzzy_search_courses(all_published, q, limit=6)
        matches = fuzzy_matches if fuzzy_matches else exact_matches

    results = []
    for c in matches:
        results.append({
            'id': c.id,
            'title': c.title,
            'level': c.level,
            'price': c.price,
            'is_free': c.is_free,
            'thumbnail': c.thumbnail_url,
            'category': c.category.name if c.category else None,
            'instructor': c.instructor_name,
            'url': url_for('catalog.detail', course_id=c.id),
            'total_lessons': c.total_lessons,
        })

    return {'results': results, 'query': q}


@catalog_bp.route('/courses/new', methods=['GET', 'POST'])
@login_required
@instructor_or_admin_required
def create_course():
    """Create a new course (Draft)."""
    form = CourseForm()
    # Populate dropdown choices
    form.department_id.choices = [(0, '-- Select Department --')] + [(d.id, d.name) for d in Department.query.order_by(Department.name).all()]
    form.category_id.choices = [(0, '-- Select Category --')] + [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
    form.tag_ids.choices = [(t.id, t.name) for t in Tag.query.order_by(Tag.name).all()]
    form.prerequisite_ids.choices = [(c.id, c.title) for c in Course.query.filter_by(is_active=True).all()]

    if form.validate_on_submit():
        slug = form.slug.data.strip() if form.slug.data else slugify(form.title.data)
        # Ensure unique slug
        base_slug = slug
        count = 1
        while Course.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{count}"
            count += 1

        course = Course(
            title=form.title.data.strip(),
            slug=slug,
            description=form.description.data.strip(),
            price=float(form.price.data or 0.0),
            level=form.level.data,
            status=form.status.data,
            department_id=form.department_id.data if form.department_id.data != 0 else None,
            category_id=form.category_id.data if form.category_id.data != 0 else None,
            created_by=current_user.id,
            is_active=True
        )
        db.session.add(course)
        db.session.flush()

        # Add creator as lead instructor
        ci = CourseInstructor(course_id=course.id, user_id=current_user.id, is_lead=True)
        db.session.add(ci)

        # Handle tags
        if form.tag_ids.data:
            for tag_id in form.tag_ids.data:
                db.session.add(CourseTag(course_id=course.id, tag_id=tag_id))

        # Handle prerequisites
        if form.prerequisite_ids.data:
            for prereq_id in form.prerequisite_ids.data:
                if prereq_id != course.id:
                    db.session.add(CoursePrerequisite(course_id=course.id, prerequisite_id=prereq_id))

        db.session.commit()
        log_action(current_user, 'create', 'Course', course.id, f"Created course '{course.title}'")
        flash(f"Course '{course.title}' created successfully! You can now add modules and lessons.", 'success')
        return redirect(url_for('learning.manage_course_curriculum', course_id=course.id))

    return render_template('catalog/course_form.html', form=form, title="Create New Course")


@catalog_bp.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
@login_required
@instructor_course_owner_required
def edit_course(course_id):
    """Edit course metadata and configuration."""
    course = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course)

    form.department_id.choices = [(0, '-- Select Department --')] + [(d.id, d.name) for d in Department.query.order_by(Department.name).all()]
    form.category_id.choices = [(0, '-- Select Category --')] + [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
    form.tag_ids.choices = [(t.id, t.name) for t in Tag.query.order_by(Tag.name).all()]
    form.prerequisite_ids.choices = [(c.id, c.title) for c in Course.query.filter(Course.id != course.id, Course.is_active == True).all()]

    if request.method == 'GET':
        form.department_id.data = course.department_id or 0
        form.category_id.data = course.category_id or 0
        form.tag_ids.data = [t.id for t in course.tags]
        form.prerequisite_ids.data = [p.id for p in course.prerequisites]

    if form.validate_on_submit():
        course.title = form.title.data.strip()
        if form.slug.data and form.slug.data != course.slug:
            course.slug = slugify(form.slug.data)
        course.description = form.description.data.strip()
        course.price = float(form.price.data or 0.0)
        course.level = form.level.data
        course.status = form.status.data
        course.department_id = form.department_id.data if form.department_id.data != 0 else None
        course.category_id = form.category_id.data if form.category_id.data != 0 else None

        # Update tags
        CourseTag.query.filter_by(course_id=course.id).delete()
        if form.tag_ids.data:
            for tid in form.tag_ids.data:
                db.session.add(CourseTag(course_id=course.id, tag_id=tid))

        # Update prerequisites
        CoursePrerequisite.query.filter_by(course_id=course.id).delete()
        if form.prerequisite_ids.data:
            for pid in form.prerequisite_ids.data:
                db.session.add(CoursePrerequisite(course_id=course.id, prerequisite_id=pid))

        db.session.commit()
        log_action(current_user, 'update', 'Course', course.id, f"Updated course '{course.title}'")
        flash('Course details saved successfully.', 'success')
        return redirect(url_for('catalog.edit_course', course_id=course.id))

    return render_template('catalog/course_form.html', form=form, course=course, title="Edit Course")


@catalog_bp.route('/courses/<int:course_id>/publish', methods=['POST'])
@login_required
@instructor_course_owner_required
def publish_course(course_id):
    """Publish a course with validation (requires at least 1 module and 1 lesson)."""
    course = Course.query.get_or_404(course_id)
    if not course.modules or not any(m.lessons for m in course.modules):
        flash('Cannot publish course: you must add at least one module with at least one lesson before publishing.', 'danger')
        return redirect(url_for('learning.manage_course_curriculum', course_id=course.id))

    course.status = 'published'
    db.session.commit()
    log_action(current_user, 'publish', 'Course', course.id, f"Published course '{course.title}'")
    flash(f"Course '{course.title}' is now published and visible to students!", 'success')
    return redirect(url_for('learning.manage_course_curriculum', course_id=course.id))


@catalog_bp.route('/courses/<int:course_id>/delete', methods=['POST'])
@login_required
@instructor_course_owner_required
def delete_course(course_id):
    """Soft delete or archive course."""
    course = Course.query.get_or_404(course_id)
    enrollment_count = Enrollment.query.filter_by(course_id=course.id).count()

    if enrollment_count > 0:
        # Soft delete / archive to protect enrolled students
        course.is_active = False
        course.status = 'archived'
        db.session.commit()
        flash(f"Course '{course.title}' has {enrollment_count} enrolled students, so it was archived instead of permanently deleted.", 'info')
    else:
        db.session.delete(course)
        db.session.commit()
        flash(f"Course '{course.title}' was permanently deleted.", 'success')

    log_action(current_user, 'delete', 'Course', course.id, f"Archived/Deleted course '{course.title}'")
    return redirect(url_for('catalog.instructor_dashboard'))
