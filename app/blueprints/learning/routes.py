from datetime import datetime, timezone
import re
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, Response, jsonify
from flask_login import login_required, current_user
from app.extensions import db, csrf
from app.models.catalog import Course
from app.models.content import Module, Lesson, LessonResource, Announcement, Enrollment, LessonProgress, Wishlist
from app.models.recognition import Certificate, Review
from app.models.users import Notification
from app.forms.learning import ModuleForm, LessonForm, LessonResourceForm, AnnouncementForm, ReviewForm
from app.services.progress import calculate_enrollment_progress, toggle_lesson_completion
from app.utils.decorators import instructor_course_owner_required
from app.utils.helpers import log_action

learning_bp = Blueprint('learning', __name__, url_prefix='/learn')

@learning_bp.route('/enroll/<int:course_id>', methods=['POST'])
@login_required
def enroll(course_id):
    """Enroll student in a free course."""
    course = Course.query.get_or_404(course_id)

    if not course.is_active or course.status != 'published':
        flash('This course is not available for enrollment.', 'warning')
        return redirect(url_for('catalog.index'))

    # If course is paid, redirect to cart checkout
    if not course.is_free:
        flash('This is a paid course. Please add it to your cart to purchase.', 'info')
        return redirect(url_for('commerce.add_to_cart', course_id=course.id))

    existing = Enrollment.query.filter_by(user_id=current_user.id, course_id=course.id).first()
    if existing:
        flash('You are already enrolled in this course!', 'info')
        return redirect(url_for('learning.course_overview', course_id=course.id))

    # Check prerequisites
    if course.prerequisites:
        for prereq in course.prerequisites:
            prereq_enroll = Enrollment.query.filter_by(
                user_id=current_user.id,
                course_id=prereq.id,
                status='completed'
            ).first()
            if not prereq_enroll:
                flash(f"Prerequisite not met: You must first complete '{prereq.title}' before enrolling in this course.", 'danger')
                return redirect(url_for('catalog.detail', course_id=course.id))

    enrollment = Enrollment(
        user_id=current_user.id,
        course_id=course.id,
        status='active',
        progress_pct=0.0,
        enrolled_at=datetime.now(timezone.utc)
    )
    db.session.add(enrollment)
    # Remove from wishlist if present
    Wishlist.query.filter_by(user_id=current_user.id, course_id=course.id).delete()
    db.session.commit()

    log_action(current_user, 'enroll', 'Course', course.id, f"Enrolled in free course '{course.title}'")
    flash(f"Successfully enrolled in '{course.title}'! Happy learning!", 'success')
    return redirect(url_for('learning.course_overview', course_id=course.id))


@learning_bp.route('/enroll-all-featured', methods=['POST'])
@login_required
def enroll_all_featured():
    """One-click enroll student in all published courses."""
    courses = Course.query.filter_by(status='published', is_active=True).all()
    count = 0
    for c in courses:
        if not Enrollment.query.filter_by(user_id=current_user.id, course_id=c.id).first():
            db.session.add(Enrollment(
                user_id=current_user.id,
                course_id=c.id,
                status='active',
                progress_pct=0.0,
                enrolled_at=datetime.now(timezone.utc)
            ))
            count += 1
    db.session.commit()
    flash(f"Successfully enrolled in all {count} YouTube courses! Start watching below.", 'success')
    return redirect(url_for('learning.my_learning'))


@learning_bp.route('/my-learning')
@login_required
def my_learning():
    """Student dashboard showing active courses, completed courses, and achievements."""
    enrollments = Enrollment.query.filter_by(user_id=current_user.id).order_by(Enrollment.enrolled_at.desc()).all()
    active_enrollments = [e for e in enrollments if e.status != 'completed']
    completed_enrollments = [e for e in enrollments if e.status == 'completed']
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()

    return render_template(
        'learning/my_learning.html',
        active_enrollments=active_enrollments,
        completed_enrollments=completed_enrollments,
        wishlist_items=wishlist_items
    )


@learning_bp.route('/course/<int:course_id>/start', methods=['GET', 'POST'])
@login_required
def start_course(course_id):
    """Start learning a course: auto-enroll if free and eligible, then redirect directly to learning hub."""
    course = Course.query.get_or_404(course_id)
    enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course.id).first()
    if enrollment:
        return redirect(url_for('learning.course_overview', course_id=course.id))

    is_owner = course.is_instructor(current_user.id) or current_user.is_admin
    if is_owner:
        return redirect(url_for('learning.course_overview', course_id=course.id))

    if not course.is_active or course.status != 'published':
        flash('This course is not currently available.', 'warning')
        return redirect(url_for('catalog.index'))

    # If course is paid, redirect to cart/detail
    if not course.is_free:
        flash('This is a premium course. Please purchase to start learning.', 'info')
        return redirect(url_for('catalog.detail', course_id=course.id))

    # Check prerequisites
    if course.prerequisites and not is_owner:
        for prereq in course.prerequisites:
            prereq_enroll = Enrollment.query.filter_by(
                user_id=current_user.id,
                course_id=prereq.id,
                status='completed'
            ).first()
            if not prereq_enroll:
                flash(f"Prerequisite not met: You must first complete '{prereq.title}' before starting this course.", 'warning')
                return redirect(url_for('catalog.detail', course_id=course.id))

    # Auto-enroll in free course
    enrollment = Enrollment(
        user_id=current_user.id,
        course_id=course.id,
        status='active',
        progress_pct=0.0,
        enrolled_at=datetime.now(timezone.utc)
    )
    db.session.add(enrollment)
    Wishlist.query.filter_by(user_id=current_user.id, course_id=course.id).delete()
    db.session.commit()

    log_action(current_user, 'enroll', 'Course', course.id, f"Started learning '{course.title}' via roadmap")
    flash(f"Welcome to '{course.title}'! Let's get started.", 'success')
    return redirect(url_for('learning.course_overview', course_id=course.id))


@learning_bp.route('/roadmap/<slug>/enroll-all', methods=['POST'])
@login_required
def enroll_all_roadmap(slug):
    """Enroll the current user in all eligible free stages of this career roadmap."""
    from app.models.catalog import Roadmap, Category
    roadmap = Roadmap.query.filter_by(slug=slug, is_active=True).first()
    if not roadmap:
        cat = Category.query.filter_by(slug=slug).first()
        if cat:
            roadmap = Roadmap.query.filter_by(slug=cat.slug).first()
    if not roadmap:
        flash('Roadmap not found.', 'danger')
        return redirect(url_for('catalog.roadmaps'))

    courses = roadmap.courses
    user_enrollments = {e.course_id: e for e in Enrollment.query.filter_by(user_id=current_user.id).all()}
    enrolled_count = 0

    for course in courses:
        if course.id not in user_enrollments and course.is_free and course.is_active and course.status == 'published':
            enrollment = Enrollment(
                user_id=current_user.id,
                course_id=course.id,
                status='active',
                progress_pct=0.0,
                enrolled_at=datetime.now(timezone.utc)
            )
            db.session.add(enrollment)
            Wishlist.query.filter_by(user_id=current_user.id, course_id=course.id).delete()
            enrolled_count += 1

    if enrolled_count > 0:
        db.session.commit()
        log_action(current_user, 'enroll_roadmap', 'Roadmap', roadmap.id, f"Enrolled in {enrolled_count} courses of roadmap '{roadmap.title}'")
        flash(f"🎉 Great choice! You are now enrolled in all {enrolled_count} stages of {roadmap.title}.", 'success')
    else:
        flash(f"You are already enrolled in all active stages of this roadmap!", 'info')

    return redirect(url_for('catalog.roadmap_detail', slug=slug))


@learning_bp.route('/course/<int:course_id>')
@login_required
def course_overview(course_id):
    """Student course curriculum overview and learning hub."""
    course = Course.query.get_or_404(course_id)
    enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course.id).first()

    is_owner = course.is_instructor(current_user.id) or current_user.is_admin
    if not enrollment and not is_owner:
        flash('You must enroll in this course first.', 'warning')
        return redirect(url_for('catalog.detail', course_id=course.id))

    completed_lesson_ids = set()
    if enrollment:
        completed_lesson_ids = {
            lp.lesson_id for lp in LessonProgress.query.filter_by(enrollment_id=enrollment.id, is_completed=True).all()
        }

    all_lessons = [l for mod in course.modules for l in mod.lessons]
    req_lesson_id = request.args.get('lesson', type=int)
    active_lesson = None
    if req_lesson_id:
        active_lesson = next((l for l in all_lessons if l.id == req_lesson_id), None)
    if not active_lesson and all_lessons:
        uncomp = [l for l in all_lessons if l.id not in completed_lesson_ids]
        active_lesson = uncomp[0] if uncomp else all_lessons[0]

    review_form = ReviewForm()
    user_review = Review.query.filter_by(user_id=current_user.id, course_id=course.id).first()

    return render_template(
        'learning/course_overview.html',
        course=course,
        enrollment=enrollment,
        completed_lesson_ids=completed_lesson_ids,
        active_lesson=active_lesson,
        all_lessons=all_lessons,
        is_owner=is_owner,
        review_form=review_form,
        user_review=user_review
    )


@learning_bp.route('/course/<int:course_id>/quick-add-video', methods=['POST'])
@login_required
@instructor_course_owner_required
def quick_add_video(course_id):
    """Instructor quick tool to add a YouTube video lesson under a specific heading."""
    course = Course.query.get_or_404(course_id)
    module_heading = request.form.get('module_heading', '').strip()
    lesson_title = request.form.get('lesson_title', '').strip()
    video_url = request.form.get('video_url', '').strip()
    duration_min = request.form.get('duration_min', 30, type=int)
    notes = request.form.get('notes', '').strip()

    if not module_heading or not lesson_title or not video_url:
        flash('Module heading, lesson title, and YouTube URL are required.', 'danger')
        return redirect(url_for('learning.manage_course_curriculum', course_id=course.id))

    # Find or create module with this heading
    module = Module.query.filter_by(course_id=course.id, title=module_heading).first()
    if not module:
        pos = len(course.modules) + 1
        module = Module(course_id=course.id, title=module_heading, position=pos)
        db.session.add(module)
        db.session.flush()

    les_pos = len(module.lessons) + 1
    content_text = f"{video_url}\n\n{notes}" if notes else video_url
    lesson = Lesson(
        module_id=module.id,
        title=lesson_title,
        content=content_text,
        content_type='video_url',
        duration_min=duration_min,
        position=les_pos
    )
    db.session.add(lesson)
    db.session.commit()

    log_action(current_user, 'create', 'Lesson', lesson.id, f"Quick-added YouTube lesson '{lesson_title}' under heading '{module_heading}'")
    flash(f"Successfully added video lesson '{lesson_title}' under heading '{module_heading}'!", 'success')
    return redirect(url_for('learning.manage_course_curriculum', course_id=course.id))


@learning_bp.route('/course/<int:course_id>/batch-add-playlist', methods=['POST'])
@login_required
@instructor_course_owner_required
def batch_add_playlist(course_id):
    """Batch add multiple YouTube playlist videos under a defined heading."""
    course = Course.query.get_or_404(course_id)
    module_heading = request.form.get('module_heading', '').strip()
    raw_playlist = request.form.get('raw_playlist', '').strip()

    if not module_heading or not raw_playlist:
        flash('Module heading and playlist video items are required.', 'danger')
        return redirect(url_for('learning.manage_course_curriculum', course_id=course.id))

    module = Module.query.filter_by(course_id=course.id, title=module_heading).first()
    if not module:
        pos = len(course.modules) + 1
        module = Module(course_id=course.id, title=module_heading, position=pos)
        db.session.add(module)
        db.session.flush()

    count = 0
    cur_pos = len(module.lessons) + 1
    for line in raw_playlist.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 2:
            t, u = parts[0], parts[1]
            d = 30
            if len(parts) >= 3 and parts[2].isdigit():
                d = int(parts[2])
            les = Lesson(
                module_id=module.id,
                title=t,
                content=u,
                content_type='video_url',
                duration_min=d,
                position=cur_pos
            )
            db.session.add(les)
            cur_pos += 1
            count += 1
        elif 'youtube.com' in line or 'youtu.be' in line:
            les = Lesson(
                module_id=module.id,
                title=f"Video Lecture #{cur_pos}",
                content=line,
                content_type='video_url',
                duration_min=30,
                position=cur_pos
            )
            db.session.add(les)
            cur_pos += 1
            count += 1

    db.session.commit()
    log_action(current_user, 'batch_create', 'Module', module.id, f"Batch imported {count} playlist videos under heading '{module_heading}'")
    flash(f"Successfully added {count} playlist videos under heading '{module_heading}'!", 'success')
    return redirect(url_for('learning.manage_course_curriculum', course_id=course.id))


@learning_bp.route('/lesson/<int:lesson_id>')
@login_required
def lesson_player(lesson_id):
    """Lesson content player."""
    lesson = Lesson.query.get_or_404(lesson_id)
    course = lesson.module.course

    enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course.id).first()
    is_owner = course.is_instructor(current_user.id) or current_user.is_admin
    if not enrollment and not is_owner:
        flash('You must enroll in this course first to access lessons.', 'warning')
        return redirect(url_for('catalog.detail', course_id=course.id))

    # Find previous and next lessons
    all_lessons = []
    for mod in course.modules:
        for les in mod.lessons:
            all_lessons.append(les)

    curr_index = next((i for i, l in enumerate(all_lessons) if l.id == lesson.id), -1)
    prev_lesson = all_lessons[curr_index - 1] if curr_index > 0 else None
    next_lesson = all_lessons[curr_index + 1] if curr_index >= 0 and curr_index < len(all_lessons) - 1 else None

    # Check if completed
    is_completed = False
    if enrollment:
        prog = LessonProgress.query.filter_by(enrollment_id=enrollment.id, lesson_id=lesson.id).first()
        is_completed = prog.is_completed if prog else False

    return render_template(
        'learning/lesson_player.html',
        lesson=lesson,
        course=course,
        enrollment=enrollment,
        is_completed=is_completed,
        prev_lesson=prev_lesson,
        next_lesson=next_lesson
    )


@learning_bp.route('/lesson/<int:lesson_id>/complete', methods=['POST'])
@login_required
def toggle_complete(lesson_id):
    """Toggle lesson completion state."""
    lesson = Lesson.query.get_or_404(lesson_id)
    course = lesson.module.course
    enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course.id).first_or_404()

    is_now_completed = toggle_lesson_completion(enrollment.id, lesson.id)
    if is_now_completed:
        flash(f"Lesson '{lesson.title}' marked as completed! (+progress)", 'success')
    else:
        flash(f"Lesson '{lesson.title}' marked as incomplete.", 'info')

    if request.is_json or request.headers.get('Accept') == 'application/json':
        cert = enrollment.certificate
        cert_url = url_for('learning.view_certificate', code=cert.code) if cert else None
        return {
            'success': True,
            'is_completed': is_now_completed,
            'progress_pct': enrollment.progress_pct,
            'status': enrollment.status,
            'certificate_url': cert_url,
            'certificate_code': cert.code if cert else None
        }, 200

    return redirect(request.referrer or url_for('learning.lesson_player', lesson_id=lesson.id))


@learning_bp.route('/course/<int:course_id>/complete', methods=['POST'])
@login_required
def complete_course(course_id):
    """Mark all lessons in the course as complete and issue certificate."""
    course = Course.query.get_or_404(course_id)
    enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course.id).first()
    if not enrollment:
        enrollment = Enrollment(
            user_id=current_user.id,
            course_id=course.id,
            status='active',
            progress_pct=0.0,
            enrolled_at=datetime.now(timezone.utc)
        )
        db.session.add(enrollment)
        db.session.flush()

    all_lessons = [l for mod in course.modules for l in mod.lessons]
    for les in all_lessons:
        prog = LessonProgress.query.filter_by(enrollment_id=enrollment.id, lesson_id=les.id).first()
        if not prog:
            prog = LessonProgress(
                enrollment_id=enrollment.id,
                lesson_id=les.id,
                is_completed=True,
                completed_at=datetime.now(timezone.utc)
            )
            db.session.add(prog)
        elif not prog.is_completed:
            prog.is_completed = True
            prog.completed_at = datetime.now(timezone.utc)

    db.session.commit()
    calculate_enrollment_progress(enrollment.id)

    from app.services.certificates import issue_certificate_if_eligible
    cert = issue_certificate_if_eligible(enrollment)

    log_action(current_user, 'complete', 'Course', course.id, f"Completed course '{course.title}'")
    flash(f"Congratulations! You completed '{course.title}'!", 'success')

    cert_url = url_for('learning.view_certificate', code=cert.code) if cert else None

    if request.is_json or request.headers.get('Accept') == 'application/json':
        return {
            'success': True,
            'message': f"Course '{course.title}' completed successfully!",
            'progress_pct': 100.0,
            'status': 'completed',
            'certificate_url': cert_url,
            'certificate_code': cert.code if cert else None
        }, 200

    if cert_url:
        return redirect(cert_url)
    return redirect(url_for('learning.course_overview', course_id=course.id))


@learning_bp.route('/wishlist', methods=['GET'])
@login_required
def wishlist():
    """View student wishlist."""
    items = Wishlist.query.filter_by(user_id=current_user.id).all()
    return render_template('learning/wishlist.html', items=items)


@learning_bp.route('/wishlist/toggle/<int:course_id>', methods=['POST'])
@login_required
def toggle_wishlist(course_id):
    """Add or remove a course from wishlist."""
    Course.query.get_or_404(course_id)
    existing = Wishlist.query.filter_by(user_id=current_user.id, course_id=course_id).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
        msg = 'Course removed from your wishlist.'
        wishlisted = False
    else:
        item = Wishlist(user_id=current_user.id, course_id=course_id)
        db.session.add(item)
        db.session.commit()
        msg = 'Course added to your wishlist!'
        wishlisted = True

    if request.headers.get('Accept') == 'application/json' or request.is_json:
        return jsonify({'success': True, 'wishlisted': wishlisted, 'message': msg})

    flash(msg, 'info' if not wishlisted else 'success')
    return redirect(request.referrer or url_for('learning.wishlist'))


@learning_bp.route('/certificate/<string:code>')
def view_certificate(code):
    """Public certificate verification and printable credential."""
    cert = Certificate.query.filter_by(code=code.strip()).first_or_404()
    return render_template('learning/certificate.html', cert=cert)


@learning_bp.route('/certificate/<string:code>/download')
def download_certificate_pdf(code):
    """Download official high-resolution landscape PDF certificate."""
    cert = Certificate.query.filter_by(code=code.strip()).first_or_404()
    from app.services.certificates import generate_certificate_pdf
    pdf_bytes = generate_certificate_pdf(cert)
    filename = f"Certificate_{cert.code}.pdf"
    return Response(
        pdf_bytes,
        mimetype='application/pdf',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )


@learning_bp.route('/course/<int:course_id>/certificate')
@login_required
def course_certificate_shortcut(course_id):
    """Direct route for student to access or generate their course certificate."""
    enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course_id).first_or_404()
    from app.services.certificates import issue_certificate_if_eligible
    cert = issue_certificate_if_eligible(enrollment)
    if cert:
        return redirect(url_for('learning.view_certificate', code=cert.code))
    flash("Complete all lessons in this course to earn your verified certificate!", "info")
    return redirect(url_for('learning.course_overview', course_id=course_id))


@learning_bp.route('/course/<int:course_id>/review', methods=['POST'])
@login_required
def submit_review(course_id):
    """Submit or update course review."""
    course = Course.query.get_or_404(course_id)
    enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course.id).first()
    if not enrollment:
        flash('Only enrolled students can review this course.', 'danger')
        return redirect(url_for('catalog.detail', course_id=course.id))

    form = ReviewForm()
    if form.validate_on_submit():
        review = Review.query.filter_by(user_id=current_user.id, course_id=course.id).first()
        if not review:
            review = Review(
                user_id=current_user.id,
                course_id=course.id,
                rating=int(form.rating.data),
                comment=form.comment.data.strip()
            )
            db.session.add(review)
            flash('Thank you! Your review has been published.', 'success')
        else:
            review.rating = int(form.rating.data)
            review.comment = form.comment.data.strip()
            flash('Your review has been updated.', 'success')

        db.session.commit()
        log_action(current_user, 'review', 'Course', course.id, f"Submitted review: {review.rating} stars")

    return redirect(url_for('learning.course_overview', course_id=course.id))


# --- INSTRUCTOR CURRICULUM BUILDER ENDPOINTS ---

@learning_bp.route('/course/<int:course_id>/curriculum')
@login_required
@instructor_course_owner_required
def manage_course_curriculum(course_id):
    """Instructor portal to organize modules, lessons, and resources."""
    course = Course.query.get_or_404(course_id)
    module_form = ModuleForm()
    return render_template('learning/curriculum_builder.html', course=course, module_form=module_form)


@learning_bp.route('/course/<int:course_id>/module/new', methods=['POST'])
@login_required
@instructor_course_owner_required
def add_module(course_id):
    """Add a module to a course."""
    course = Course.query.get_or_404(course_id)
    form = ModuleForm()
    if form.validate_on_submit():
        pos = form.position.data or (len(course.modules) + 1)
        mod = Module(course_id=course.id, title=form.title.data.strip(), position=pos)
        db.session.add(mod)
        db.session.commit()
        log_action(current_user, 'create', 'Module', mod.id, f"Added module '{mod.title}' to course '{course.title}'")
        flash(f"Module '{mod.title}' added successfully.", 'success')
    return redirect(url_for('learning.manage_course_curriculum', course_id=course.id))


@learning_bp.route('/module/<int:module_id>/delete', methods=['POST'])
@login_required
def delete_module(module_id):
    """Delete a module."""
    mod = Module.query.get_or_404(module_id)
    course = mod.course
    if not current_user.is_admin and not course.is_instructor(current_user.id):
        abort(403)

    db.session.delete(mod)
    db.session.commit()
    log_action(current_user, 'delete', 'Module', module_id, f"Deleted module '{mod.title}'")
    flash(f"Module '{mod.title}' and its lessons were removed.", 'info')
    return redirect(url_for('learning.manage_course_curriculum', course_id=course.id))


@learning_bp.route('/module/<int:module_id>/lesson/new', methods=['GET', 'POST'])
@login_required
def add_lesson(module_id):
    """Add a lesson to a module."""
    mod = Module.query.get_or_404(module_id)
    course = mod.course
    if not current_user.is_admin and not course.is_instructor(current_user.id):
        abort(403)

    form = LessonForm()
    if form.validate_on_submit():
        pos = form.position.data or (len(mod.lessons) + 1)
        lesson = Lesson(
            module_id=mod.id,
            title=form.title.data.strip(),
            content=form.content.data,
            content_type=form.content_type.data,
            duration_min=form.duration_min.data or 10,
            position=pos
        )
        db.session.add(lesson)
        db.session.commit()
        log_action(current_user, 'create', 'Lesson', lesson.id, f"Added lesson '{lesson.title}'")
        flash(f"Lesson '{lesson.title}' created.", 'success')
        return redirect(url_for('learning.manage_course_curriculum', course_id=course.id))

    return render_template('learning/lesson_form.html', form=form, module=mod, course=course, title="Add Lesson")


@learning_bp.route('/lesson/<int:lesson_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_lesson(lesson_id):
    """Edit lesson details and resources."""
    lesson = Lesson.query.get_or_404(lesson_id)
    course = lesson.module.course
    if not current_user.is_admin and not course.is_instructor(current_user.id):
        abort(403)

    form = LessonForm(obj=lesson)
    resource_form = LessonResourceForm()

    if form.validate_on_submit():
        lesson.title = form.title.data.strip()
        lesson.content = form.content.data
        lesson.content_type = form.content_type.data
        lesson.duration_min = form.duration_min.data
        lesson.position = form.position.data
        db.session.commit()
        log_action(current_user, 'update', 'Lesson', lesson.id, f"Updated lesson '{lesson.title}'")
        flash('Lesson saved successfully.', 'success')
        return redirect(url_for('learning.manage_course_curriculum', course_id=course.id))

    return render_template('learning/lesson_form.html', form=form, resource_form=resource_form, lesson=lesson, course=course, title="Edit Lesson")


@learning_bp.route('/lesson/<int:lesson_id>/delete', methods=['POST'])
@login_required
def delete_lesson(lesson_id):
    """Delete a lesson."""
    lesson = Lesson.query.get_or_404(lesson_id)
    course = lesson.module.course
    if not current_user.is_admin and not course.is_instructor(current_user.id):
        abort(403)

    db.session.delete(lesson)
    db.session.commit()
    log_action(current_user, 'delete', 'Lesson', lesson_id, f"Deleted lesson '{lesson.title}'")
    flash(f"Lesson '{lesson.title}' was deleted.", 'info')
    return redirect(url_for('learning.manage_course_curriculum', course_id=course.id))


@learning_bp.route('/lesson/<int:lesson_id>/resource/new', methods=['POST'])
@login_required
def add_lesson_resource(lesson_id):
    """Add a resource to a lesson."""
    lesson = Lesson.query.get_or_404(lesson_id)
    course = lesson.module.course
    if not current_user.is_admin and not course.is_instructor(current_user.id):
        abort(403)

    form = LessonResourceForm()
    if form.validate_on_submit():
        res = LessonResource(
            lesson_id=lesson.id,
            title=form.title.data.strip(),
            resource_type=form.resource_type.data,
            url_or_path=form.url_or_path.data.strip()
        )
        db.session.add(res)
        db.session.commit()
        log_action(current_user, 'create', 'LessonResource', res.id, f"Added resource '{res.title}' to lesson '{lesson.title}'")
        flash(f"Resource '{res.title}' attached.", 'success')

    return redirect(url_for('learning.edit_lesson', lesson_id=lesson.id))


@learning_bp.route('/resource/<int:resource_id>/delete', methods=['POST'])
@login_required
def delete_lesson_resource(resource_id):
    """Delete a resource."""
    res = LessonResource.query.get_or_404(resource_id)
    course = res.lesson.module.course
    if not current_user.is_admin and not course.is_instructor(current_user.id):
        abort(403)

    lesson_id = res.lesson_id
    db.session.delete(res)
    db.session.commit()
    flash('Resource removed.', 'info')
    return redirect(url_for('learning.edit_lesson', lesson_id=lesson_id))


@learning_bp.route('/lesson/<int:lesson_id>/challenges', methods=['GET', 'POST'])
@csrf.exempt
@login_required
def manage_lesson_challenges(lesson_id):
    """Instructor & Admin management portal for lesson's 3-Tier Interactive Coding Challenges."""
    lesson = Lesson.query.get_or_404(lesson_id)
    course = lesson.module.course
    is_auth = current_user.is_admin or course.is_instructor(current_user.id) or (current_user.role and current_user.role.name in ['admin', 'instructor'])
    if not is_auth:
        flash('You do not have permission to manage challenges for this lesson.', 'danger')
        abort(403)

    from app.services.programming_challenges import get_programming_quiz, generate_smart_challenges_template

    if request.method == 'POST':
        data = request.get_json(silent=True)
        if not data:
            # Form-based submission
            lang = request.form.get('language', 'python').strip()
            challenges = {}
            for diff in ['basic', 'intermediate', 'advance']:
                badge = 'bg-success' if diff == 'basic' else ('bg-primary' if diff == 'intermediate' else 'bg-purple')
                diff_title = diff.capitalize()
                title = request.form.get(f'{diff}_title', '').strip() or f"{diff_title} Challenge"
                func_name = request.form.get(f'{diff}_function_name', '').strip() or 'solution'
                approach = request.form.get(f'{diff}_approach', 'function').strip()
                prompt = request.form.get(f'{diff}_prompt', '').strip()
                constraints = request.form.get(f'{diff}_constraints', '').strip()
                starter = request.form.get(f'{diff}_starter_code', '').strip()
                solution = request.form.get(f'{diff}_solution_code', '').strip()
                hint = request.form.get(f'{diff}_hint', '').strip()
                tc_raw = request.form.get(f'{diff}_test_cases', '').strip()

                test_cases = []
                if tc_raw:
                    import json
                    try:
                        parsed = json.loads(tc_raw)
                        if isinstance(parsed, list):
                            test_cases = parsed
                    except Exception:
                        pass
                if not test_cases:
                    test_cases = [{'desc': 'Default assertion test', 'input': [], 'expected': True}]

                challenges[diff] = {
                    'id': f'l{lesson.id}-{diff[0]}',
                    'difficulty': diff_title,
                    'badge_class': badge,
                    'approach': approach,
                    'title': title,
                    'function_name': func_name,
                    'prompt': prompt,
                    'constraints': constraints,
                    'starter_code': starter,
                    'solution_code': solution,
                    'hint': hint,
                    'test_cases': test_cases
                }

            custom_payload = {
                'language': lang,
                'challenges': challenges
            }
        else:
            custom_payload = data

        lesson.custom_challenges = custom_payload
        db.session.commit()
        log_action(current_user, 'update', 'Lesson', lesson.id, f"Updated 3-tier coding challenges for lesson '{lesson.title}'")
        flash(f"Successfully saved 3-tier Interactive Code Lab challenges for '{lesson.title}'!", 'success')

        if request.is_json:
            return {'success': True, 'message': 'Saved successfully', 'quiz': get_programming_quiz(lesson)}, 200
        return redirect(url_for('learning.manage_lesson_challenges', lesson_id=lesson.id))

    quiz_data = get_programming_quiz(lesson)
    smart_template = generate_smart_challenges_template(lesson)
    has_custom = bool(lesson.custom_challenges)

    return render_template(
        'learning/manage_challenges.html',
        lesson=lesson,
        course=course,
        quiz_data=quiz_data,
        smart_template=smart_template,
        has_custom=has_custom
    )


@learning_bp.route('/lesson/<int:lesson_id>/challenges/reset', methods=['POST'])
@csrf.exempt
@login_required
def reset_lesson_challenges(lesson_id):
    """Reset custom challenges back to system defaults."""
    lesson = Lesson.query.get_or_404(lesson_id)
    course = lesson.module.course
    is_auth = current_user.is_admin or course.is_instructor(current_user.id) or (current_user.role and current_user.role.name in ['admin', 'instructor'])
    if not is_auth:
        abort(403)

    lesson.custom_challenges = None
    db.session.commit()
    log_action(current_user, 'reset', 'Lesson', lesson.id, f"Reset custom challenges to default for lesson '{lesson.title}'")
    flash(f"Reset challenges for '{lesson.title}' back to standard system templates.", 'info')
    return redirect(url_for('learning.manage_lesson_challenges', lesson_id=lesson.id))


@learning_bp.route('/api/lesson/<int:lesson_id>/generate-challenges-template', methods=['POST'])
@csrf.exempt
@login_required
def api_generate_challenges_template(lesson_id):
    """AJAX endpoint to generate smart challenge templates tailored to the lesson."""
    lesson = Lesson.query.get_or_404(lesson_id)
    course = lesson.module.course
    is_auth = current_user.is_admin or course.is_instructor(current_user.id) or (current_user.role and current_user.role.name in ['admin', 'instructor'])
    if not is_auth:
        abort(403)

    from app.services.programming_challenges import generate_smart_challenges_template
    template_data = generate_smart_challenges_template(lesson)
    return {'success': True, 'template': template_data}, 200


@learning_bp.route('/course/<int:course_id>/announcements', methods=['GET', 'POST'])
@login_required
def course_announcements(course_id):
    """View and post course announcements."""
    course = Course.query.get_or_404(course_id)
    is_owner = course.is_instructor(current_user.id) or current_user.is_admin

    form = AnnouncementForm() if is_owner else None

    if form and form.validate_on_submit():
        ann = Announcement(
            course_id=course.id,
            author_id=current_user.id,
            title=form.title.data.strip(),
            body=form.body.data.strip()
        )
        db.session.add(ann)
        db.session.flush()

        # Notify all enrolled students
        for enroll in course.enrollments:
            notif = Notification(
                user_id=enroll.user_id,
                title=f"New Announcement: {course.title}",
                message=f"{ann.title}: {ann.body[:120]}...",
                link=f"/learn/course/{course.id}/announcements"
            )
            db.session.add(notif)

        db.session.commit()
        log_action(current_user, 'create', 'Announcement', ann.id, f"Posted announcement in '{course.title}'")
        flash('Announcement posted and notifications dispatched to all students.', 'success')
        return redirect(url_for('learning.course_announcements', course_id=course.id))

    return render_template('learning/announcements.html', course=course, announcements=course.announcements, form=form, is_owner=is_owner)


@learning_bp.route('/api/evaluate_code', methods=['POST'])
@csrf.exempt
@login_required
def evaluate_code():
    """Evaluate student's programming challenge code in real-time."""
    from app.services.code_evaluator import evaluate_solution
    data = request.get_json(silent=True) or {}
    lesson_id = data.get('lesson_id')
    difficulty = data.get('difficulty', 'basic')
    code = data.get('code', '')
    custom_input = data.get('custom_input', None)

    if not lesson_id:
        return {'passed': False, 'message': 'Missing lesson_id'}, 400

    lesson = Lesson.query.get_or_404(lesson_id)
    result = evaluate_solution(lesson, difficulty, code, custom_input=custom_input)

    # If passed, update LessonProgress and award completion
    if result.get('passed'):
        enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=lesson.module.course_id).first()
        if enrollment:
            prog = LessonProgress.query.filter_by(enrollment_id=enrollment.id, lesson_id=lesson.id).first()
            if not prog:
                prog = LessonProgress(enrollment_id=enrollment.id, lesson_id=lesson.id, is_completed=True, completed_at=datetime.now(timezone.utc))
                db.session.add(prog)
            else:
                prog.is_completed = True
                prog.completed_at = datetime.now(timezone.utc)
            db.session.commit()
            calculate_enrollment_progress(enrollment.id)
            result['auto_completed'] = True

    return result, 200


@learning_bp.route('/api/programming_quiz/<int:lesson_id>')
@login_required
def get_quiz_api(lesson_id):
    """Retrieve full programming quiz data (Basic, Intermediate, Advance) for a lesson."""
    from app.services.programming_challenges import get_programming_quiz
    lesson = Lesson.query.get_or_404(lesson_id)
    return get_programming_quiz(lesson), 200


@learning_bp.route('/api/sync_lesson_duration/<int:lesson_id>', methods=['POST'])
@csrf.exempt
@login_required
def sync_lesson_duration(lesson_id):
    """Sync exact video duration reported by YouTube player or calculated from metadata."""
    lesson = Lesson.query.get_or_404(lesson_id)
    data = request.get_json(silent=True) or {}
    dur_min = data.get('duration_min')
    dur_sec = data.get('duration_sec')

    if dur_sec and not dur_min:
        try:
            dur_min = max(1, round(float(dur_sec) / 60))
        except (ValueError, TypeError):
            pass

    if dur_min:
        try:
            dur_min_val = max(1, int(dur_min))
            lesson.duration_min = dur_min_val
            if dur_sec:
                try:
                    lesson.duration_sec = int(float(dur_sec))
                except (ValueError, TypeError):
                    pass
            db.session.commit()

            return {
                'success': True,
                'lesson_id': lesson.id,
                'duration_min': lesson.duration_min,
                'duration_sec': lesson.duration_sec,
                'formatted': lesson.formatted_duration
            }, 200
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500

    return {'success': False, 'message': 'Missing valid duration_min or duration_sec'}, 400


@learning_bp.route('/lesson/<int:lesson_id>/download-notes')
@login_required
def download_lesson_notes(lesson_id):
    """Generate and download comprehensive PDF lecture notes for the lesson."""
    lesson = db.session.get(Lesson, lesson_id)
    if not lesson:
        abort(404)
    from app.services.notes_generator import generate_lesson_notes_pdf
    pdf_bytes = generate_lesson_notes_pdf(lesson)
    safe_title = re.sub(r'[^a-zA-Z0-9_-]', '_', lesson.title)[:40]
    filename = f"lecture_notes_{safe_title}.pdf"
    return Response(
        pdf_bytes,
        mimetype='application/pdf',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )


@learning_bp.route('/lesson/<int:lesson_id>/download-starter-code')
@login_required
def download_starter_code(lesson_id):
    """Download starter code for the lesson's programming challenge."""
    lesson = db.session.get(Lesson, lesson_id)
    if not lesson:
        abort(404)
    quiz = lesson.programming_quiz or {}
    lang = quiz.get('language', 'python')
    ext = 'js' if lang == 'javascript' else 'py'
    ch = (quiz.get('challenges') or {}).get('basic') or {}
    code = ch.get('starter_code') or f"# Starter code for {lesson.title}\n\ndef solution():\n    pass\n"
    safe_title = re.sub(r'[^a-zA-Z0-9_-]', '_', lesson.title)[:40]
    filename = f"solution_{safe_title}.{ext}"
    return Response(
        code,
        mimetype='text/plain',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )

