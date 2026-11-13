from datetime import datetime, timezone
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models.users import User, Role, Permission, RolePermission, UserProfile
from app.models.catalog import Course, Department, Category, Tag, Roadmap, RoadmapStage
from app.models.content import Enrollment
from app.models.commerce import Order, Coupon, Payment
from app.models.recognition import Badge
from app.models.admin import AuditLog, Setting
from app.forms.admin import UserAdminForm, RoleForm, CouponForm, BadgeForm, SettingForm, RoadmapForm, RoadmapStageForm
from app.forms.catalog import DepartmentForm, CategoryForm, TagForm
from app.utils.decorators import admin_required
from app.utils.helpers import log_action, slugify

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
@login_required
@admin_required
def require_admin():
    """Ensure all admin routes are strictly guarded."""
    pass


@admin_bp.route('/')
def dashboard():
    """Admin dashboard overview and KPIs."""
    total_users = User.query.count()
    total_students = User.query.join(Role).filter(Role.name == 'student').count()
    total_instructors = User.query.join(Role).filter(Role.name == 'instructor').count()

    total_courses = Course.query.count()
    published_courses = Course.query.filter_by(status='published').count()

    total_enrollments = Enrollment.query.count()
    completed_enrollments = Enrollment.query.filter_by(status='completed').count()

    # Revenue
    revenue = db.session.query(db.func.sum(Order.total)).filter(Order.status == 'paid').scalar() or 0.0

    recent_logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(8).all()

    return render_template(
        'admin/dashboard.html',
        total_users=total_users,
        total_students=total_students,
        total_instructors=total_instructors,
        total_courses=total_courses,
        published_courses=published_courses,
        total_enrollments=total_enrollments,
        completed_enrollments=completed_enrollments,
        revenue=revenue,
        recent_logs=recent_logs
    )


# --- USERS MANAGEMENT ---

@admin_bp.route('/users')
def users_list():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    role_id = request.args.get('role', type=int)

    query = User.query
    if search:
        query = query.filter((User.username.ilike(f'%{search}%')) | (User.email.ilike(f'%{search}%')))
    if role_id:
        query = query.filter_by(role_id=role_id)

    users = query.order_by(User.created_at.desc()).paginate(page=page, per_page=15, error_out=False)
    roles = Role.query.all()
    return render_template('admin/users.html', users=users, roles=roles, search=search, selected_role=role_id)


@admin_bp.route('/user/new', methods=['GET', 'POST'])
def create_user():
    form = UserAdminForm()
    form.role_id.choices = [(r.id, r.name.capitalize()) for r in Role.query.all()]

    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower(),
            role_id=form.role_id.data,
            is_active=form.is_active.data
        )
        pwd = form.password.data or 'StudentPass123!'
        user.set_password(pwd)
        db.session.add(user)
        db.session.flush()

        profile = UserProfile(user_id=user.id, full_name=user.username)
        db.session.add(profile)
        db.session.commit()

        log_action(current_user, 'create', 'User', user.id, f"Admin created user {user.username}")
        flash(f"User '{user.username}' created successfully.", 'success')
        return redirect(url_for('admin.users_list'))

    return render_template('admin/user_form.html', form=form, title="Create New User")


@admin_bp.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserAdminForm(obj=user)
    form.role_id.choices = [(r.id, r.name.capitalize()) for r in Role.query.all()]

    if form.validate_on_submit():
        user.username = form.username.data.strip()
        user.email = form.email.data.strip().lower()
        user.role_id = form.role_id.data
        user.is_active = form.is_active.data

        if form.password.data:
            user.set_password(form.password.data)

        db.session.commit()
        log_action(current_user, 'update', 'User', user.id, f"Admin updated user {user.username}")
        flash(f"User '{user.username}' updated successfully.", 'success')
        return redirect(url_for('admin.users_list'))

    return render_template('admin/user_form.html', form=form, user=user, title="Edit User")


@admin_bp.route('/user/<int:user_id>/toggle-active', methods=['POST'])
def toggle_user_active(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot deactivate your own admin account.', 'danger')
        return redirect(url_for('admin.users_list'))

    user.is_active = not user.is_active
    db.session.commit()
    log_action(current_user, 'toggle_active', 'User', user.id, f"Set is_active={user.is_active} for {user.username}")
    flash(f"User '{user.username}' is now {'active' if user.is_active else 'deactivated'}.", 'info')
    return redirect(url_for('admin.users_list'))


# --- ROLES & PERMISSIONS ---

@admin_bp.route('/roles', methods=['GET', 'POST'])
def roles_list():
    form = RoleForm()
    permissions = Permission.query.order_by(Permission.code).all()
    form.permission_ids.choices = [(p.id, f"{p.code} - {p.description}") for p in permissions]

    if form.validate_on_submit():
        role = Role(name=form.name.data.strip().lower(), description=form.description.data.strip())
        db.session.add(role)
        db.session.flush()

        if form.permission_ids.data:
            for pid in form.permission_ids.data:
                db.session.add(RolePermission(role_id=role.id, permission_id=pid))

        db.session.commit()
        log_action(current_user, 'create', 'Role', role.id, f"Created role {role.name}")
        flash(f"Role '{role.name}' created.", 'success')
        return redirect(url_for('admin.roles_list'))

    roles = Role.query.all()
    return render_template('admin/roles.html', roles=roles, form=form, permissions=permissions)


@admin_bp.route('/role/<int:role_id>/edit', methods=['GET', 'POST'])
def edit_role(role_id):
    role = Role.query.get_or_404(role_id)
    form = RoleForm(obj=role)
    permissions = Permission.query.order_by(Permission.code).all()
    form.permission_ids.choices = [(p.id, f"{p.code} - {p.description}") for p in permissions]

    if request.method == 'GET':
        form.permission_ids.data = [p.id for p in role.permissions]

    if form.validate_on_submit():
        role.name = form.name.data.strip().lower()
        role.description = form.description.data.strip()

        # Update permissions
        RolePermission.query.filter_by(role_id=role.id).delete()
        if form.permission_ids.data:
            for pid in form.permission_ids.data:
                db.session.add(RolePermission(role_id=role.id, permission_id=pid))

        db.session.commit()
        log_action(current_user, 'update', 'Role', role.id, f"Updated role {role.name}")
        flash('Role permissions updated.', 'success')
        return redirect(url_for('admin.roles_list'))

    return render_template('admin/role_edit.html', form=form, role=role)


# --- DEPARTMENTS & CATEGORIES & TAGS ---

@admin_bp.route('/departments', methods=['GET', 'POST'])
def departments():
    form = DepartmentForm()
    if form.validate_on_submit():
        dept = Department(name=form.name.data.strip(), description=form.description.data.strip())
        db.session.add(dept)
        db.session.commit()
        log_action(current_user, 'create', 'Department', dept.id, f"Created department {dept.name}")
        flash(f"Department '{dept.name}' created.", 'success')
        return redirect(url_for('admin.departments'))

    items = Department.query.order_by(Department.name).all()
    return render_template('admin/departments.html', departments=items, form=form)


@admin_bp.route('/department/<int:id>/delete', methods=['POST'])
def delete_department(id):
    dept = Department.query.get_or_404(id)
    db.session.delete(dept)
    db.session.commit()
    flash('Department deleted.', 'info')
    return redirect(url_for('admin.departments'))


@admin_bp.route('/categories', methods=['GET', 'POST'])
def categories():
    form = CategoryForm()
    form.parent_id.choices = [(0, '-- None (Top Level) --')] + [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]

    if form.validate_on_submit():
        slug = form.slug.data.strip() if form.slug.data else slugify(form.name.data)
        cat = Category(
            name=form.name.data.strip(),
            slug=slug,
            parent_id=form.parent_id.data if form.parent_id.data != 0 else None
        )
        db.session.add(cat)
        db.session.commit()
        log_action(current_user, 'create', 'Category', cat.id, f"Created category {cat.name}")
        flash(f"Category '{cat.name}' created.", 'success')
        return redirect(url_for('admin.categories'))

    items = Category.query.order_by(Category.name).all()
    return render_template('admin/categories.html', categories=items, form=form)


@admin_bp.route('/category/<int:id>/delete', methods=['POST'])
def delete_category(id):
    cat = Category.query.get_or_404(id)
    db.session.delete(cat)
    db.session.commit()
    flash('Category deleted.', 'info')
    return redirect(url_for('admin.categories'))


@admin_bp.route('/tags', methods=['GET', 'POST'])
def tags():
    form = TagForm()
    if form.validate_on_submit():
        tag = Tag(name=form.name.data.strip().lower())
        db.session.add(tag)
        db.session.commit()
        flash(f"Tag '#{tag.name}' added.", 'success')
        return redirect(url_for('admin.tags'))

    items = Tag.query.order_by(Tag.name).all()
    return render_template('admin/tags.html', tags=items, form=form)


@admin_bp.route('/tag/<int:id>/delete', methods=['POST'])
def delete_tag(id):
    tag = Tag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    flash('Tag deleted.', 'info')
    return redirect(url_for('admin.tags'))


# --- COUPONS ---

@admin_bp.route('/coupons', methods=['GET', 'POST'])
def coupons():
    form = CouponForm()
    if form.validate_on_submit():
        coupon = Coupon(
            code=form.code.data.strip().upper(),
            discount_percent=form.discount_percent.data,
            valid_from=form.valid_from.data,
            valid_to=form.valid_to.data,
            usage_limit=form.usage_limit.data,
            times_used=0
        )
        db.session.add(coupon)
        db.session.commit()
        log_action(current_user, 'create', 'Coupon', coupon.id, f"Created coupon {coupon.code}")
        flash(f"Coupon '{coupon.code}' created.", 'success')
        return redirect(url_for('admin.coupons'))

    items = Coupon.query.order_by(Coupon.created_at.desc()).all()
    return render_template('admin/coupons.html', coupons=items, form=form)


@admin_bp.route('/coupon/<int:id>/delete', methods=['POST'])
def delete_coupon(id):
    c = Coupon.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    flash('Coupon removed.', 'info')
    return redirect(url_for('admin.coupons'))


# --- BADGES ---

@admin_bp.route('/badges', methods=['GET', 'POST'])
def badges():
    form = BadgeForm()
    if form.validate_on_submit():
        badge = Badge(
            name=form.name.data.strip(),
            description=form.description.data.strip(),
            icon=form.icon.data.strip(),
            rule_code=form.rule_code.data.strip()
        )
        db.session.add(badge)
        db.session.commit()
        log_action(current_user, 'create', 'Badge', badge.id, f"Created badge {badge.name}")
        flash(f"Badge '{badge.name}' created.", 'success')
        return redirect(url_for('admin.badges'))

    items = Badge.query.all()
    return render_template('admin/badges.html', badges=items, form=form)


@admin_bp.route('/badge/<int:id>/delete', methods=['POST'])
def delete_badge(id):
    b = Badge.query.get_or_404(id)
    db.session.delete(b)
    db.session.commit()
    flash('Badge removed.', 'info')
    return redirect(url_for('admin.badges'))


# --- SETTINGS ---

@admin_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    form = SettingForm()
    if form.validate_on_submit():
        Setting.set_value(
            key=form.key.data.strip(),
            value=form.value.data.strip(),
            description=form.description.data.strip() if form.description.data else None
        )
        log_action(current_user, 'update_setting', 'Setting', None, f"Configured setting {form.key.data}")
        flash(f"Setting '{form.key.data}' saved.", 'success')
        return redirect(url_for('admin.settings'))

    items = Setting.query.order_by(Setting.key).all()
    return render_template('admin/settings.html', settings=items, form=form)


# --- AUDIT LOGS ---

@admin_bp.route('/audit')
def audit_logs():
    page = request.args.get('page', 1, type=int)
    action_filter = request.args.get('action', '').strip()
    entity_filter = request.args.get('entity', '').strip()

    query = AuditLog.query
    if action_filter:
        query = query.filter_by(action=action_filter)
    if entity_filter:
        query = query.filter_by(entity_type=entity_filter)

    logs = query.order_by(AuditLog.created_at.desc()).paginate(page=page, per_page=25, error_out=False)
    actions = [r[0] for r in db.session.query(AuditLog.action).distinct().all()]
    entities = [r[0] for r in db.session.query(AuditLog.entity_type).distinct().all()]

    return render_template(
        'admin/audit.html',
        logs=logs,
        actions=actions,
        entities=entities,
        selected_action=action_filter,
        selected_entity=entity_filter
    )


# --- CAREER ROADMAPS MANAGEMENT ---

@admin_bp.route('/roadmaps', methods=['GET', 'POST'])
def roadmaps():
    """Admin view to manage Career Roadmaps."""
    form = RoadmapForm()
    if form.validate_on_submit():
        slug = form.slug.data.strip() if form.slug.data else slugify(form.title.data)
        if Roadmap.query.filter_by(slug=slug).first():
            flash(f"A roadmap with slug '{slug}' already exists. Please choose a different title or slug.", 'danger')
            return redirect(url_for('admin.roadmaps'))

        roadmap = Roadmap(
            title=form.title.data.strip(),
            slug=slug,
            badge=form.badge.data.strip() if form.badge.data else 'Career Roadmap',
            icon=form.icon.data.strip() if form.icon.data else 'bi-diagram-3-fill',
            estimated_duration=form.estimated_duration.data.strip() if form.estimated_duration.data else '3 - 5 Months',
            bg_gradient=form.bg_gradient.data.strip() if form.bg_gradient.data else 'linear-gradient(135deg, #1d4ed8 0%, #1e3a8a 100%)',
            tagline=form.tagline.data.strip() if form.tagline.data else None,
            description=form.description.data.strip() if form.description.data else None,
            skills_csv=form.skills_csv.data.strip() if form.skills_csv.data else None,
            target_roles_csv=form.target_roles_csv.data.strip() if form.target_roles_csv.data else None,
            is_active=True
        )
        db.session.add(roadmap)
        db.session.commit()
        log_action(current_user, 'create_roadmap', 'Roadmap', roadmap.id, f"Created roadmap '{roadmap.title}'")
        flash(f"Roadmap '{roadmap.title}' created successfully! You can now add courses to it.", 'success')
        return redirect(url_for('admin.roadmap_manage', roadmap_id=roadmap.id))

    all_roadmaps = Roadmap.query.order_by(Roadmap.created_at.desc()).all()
    return render_template('admin/roadmaps.html', roadmaps=all_roadmaps, form=form)


@admin_bp.route('/roadmaps/<int:roadmap_id>/edit', methods=['GET', 'POST'])
def roadmap_edit(roadmap_id):
    """Edit roadmap metadata."""
    roadmap = Roadmap.query.get_or_404(roadmap_id)
    form = RoadmapForm(obj=roadmap)
    if form.validate_on_submit():
        slug = form.slug.data.strip() if form.slug.data else slugify(form.title.data)
        existing = Roadmap.query.filter(Roadmap.slug == slug, Roadmap.id != roadmap.id).first()
        if existing:
            flash(f"A roadmap with slug '{slug}' already exists.", 'danger')
            return render_template('admin/roadmap_edit.html', roadmap=roadmap, form=form)

        roadmap.title = form.title.data.strip()
        roadmap.slug = slug
        roadmap.badge = form.badge.data.strip() if form.badge.data else 'Career Roadmap'
        roadmap.icon = form.icon.data.strip() if form.icon.data else 'bi-diagram-3-fill'
        roadmap.estimated_duration = form.estimated_duration.data.strip() if form.estimated_duration.data else '3 - 5 Months'
        roadmap.bg_gradient = form.bg_gradient.data.strip() if form.bg_gradient.data else 'linear-gradient(135deg, #1d4ed8 0%, #1e3a8a 100%)'
        roadmap.tagline = form.tagline.data.strip() if form.tagline.data else None
        roadmap.description = form.description.data.strip() if form.description.data else None
        roadmap.skills_csv = form.skills_csv.data.strip() if form.skills_csv.data else None
        roadmap.target_roles_csv = form.target_roles_csv.data.strip() if form.target_roles_csv.data else None

        db.session.commit()
        log_action(current_user, 'edit_roadmap', 'Roadmap', roadmap.id, f"Updated roadmap '{roadmap.title}'")
        flash(f"Roadmap '{roadmap.title}' updated successfully.", 'success')
        return redirect(url_for('admin.roadmaps'))

    return render_template('admin/roadmap_edit.html', roadmap=roadmap, form=form)


@admin_bp.route('/roadmaps/<int:roadmap_id>/manage', methods=['GET', 'POST'])
def roadmap_manage(roadmap_id):
    """Manage stages for a roadmap (order, add, remove courses)."""
    roadmap = Roadmap.query.get_or_404(roadmap_id)
    form = RoadmapStageForm()

    all_courses = Course.query.order_by(Course.title).all()
    existing_course_ids = {s.course_id for s in roadmap.stages}
    form.course_id.choices = [(c.id, f"{c.title} ({c.level} • {c.category.name if c.category else 'No Category'})") for c in all_courses]

    if form.validate_on_submit():
        c_id = form.course_id.data
        if c_id in existing_course_ids:
            flash("This course is already assigned to a stage in this roadmap.", 'warning')
            return redirect(url_for('admin.roadmap_manage', roadmap_id=roadmap.id))

        course = Course.query.get_or_404(c_id)
        next_stage_num = (max([s.stage_number for s in roadmap.stages], default=0)) + 1
        stage = RoadmapStage(
            roadmap_id=roadmap.id,
            course_id=course.id,
            stage_number=next_stage_num,
            stage_label=form.stage_label.data.strip() if form.stage_label.data else None
        )
        db.session.add(stage)
        db.session.commit()
        log_action(current_user, 'add_stage', 'Roadmap', roadmap.id, f"Added '{course.title}' as Stage {next_stage_num} to '{roadmap.title}'")
        flash(f"Course '{course.title}' added to roadmap as Stage {next_stage_num}.", 'success')
        return redirect(url_for('admin.roadmap_manage', roadmap_id=roadmap.id))

    ordered_stages = sorted(roadmap.stages, key=lambda s: s.stage_number)
    return render_template('admin/roadmap_stages.html', roadmap=roadmap, stages=ordered_stages, form=form, existing_ids=existing_course_ids)


@admin_bp.route('/roadmaps/stage/<int:stage_id>/move/<string:direction>', methods=['POST'])
def roadmap_move_stage(stage_id, direction):
    """Move stage up or down in order."""
    stage = RoadmapStage.query.get_or_404(stage_id)
    roadmap = stage.roadmap
    ordered_stages = sorted(roadmap.stages, key=lambda s: s.stage_number)

    idx = None
    for i, s in enumerate(ordered_stages):
        if s.id == stage.id:
            idx = i
            break

    if idx is not None:
        if direction == 'up' and idx > 0:
            neighbor = ordered_stages[idx - 1]
            stage.stage_number, neighbor.stage_number = neighbor.stage_number, stage.stage_number
            db.session.commit()
            flash(f"Stage '{stage.course.title}' moved up to Stage {stage.stage_number}.", 'success')
        elif direction == 'down' and idx < len(ordered_stages) - 1:
            neighbor = ordered_stages[idx + 1]
            stage.stage_number, neighbor.stage_number = neighbor.stage_number, stage.stage_number
            db.session.commit()
            flash(f"Stage '{stage.course.title}' moved down to Stage {stage.stage_number}.", 'success')

    return redirect(url_for('admin.roadmap_manage', roadmap_id=roadmap.id))


@admin_bp.route('/roadmaps/stage/<int:stage_id>/remove', methods=['POST'])
def roadmap_remove_stage(stage_id):
    """Remove course stage from roadmap without deleting course."""
    stage = RoadmapStage.query.get_or_404(stage_id)
    roadmap_id = stage.roadmap_id
    course_title = stage.course.title if stage.course else 'Course'

    db.session.delete(stage)
    db.session.flush()

    roadmap = Roadmap.query.get(roadmap_id)
    if roadmap:
        remaining = sorted(roadmap.stages, key=lambda s: s.stage_number)
        for i, s in enumerate(remaining, 1):
            s.stage_number = i
    db.session.commit()

    log_action(current_user, 'remove_stage', 'Roadmap', roadmap_id, f"Removed course '{course_title}' from roadmap")
    flash(f"Course '{course_title}' removed from this roadmap. The course remains safe in the catalog.", 'info')
    return redirect(url_for('admin.roadmap_manage', roadmap_id=roadmap_id))


@admin_bp.route('/roadmaps/<int:roadmap_id>/delete', methods=['POST'])
def roadmap_delete(roadmap_id):
    """Delete roadmap without deleting underlying courses."""
    roadmap = Roadmap.query.get_or_404(roadmap_id)
    title = roadmap.title
    db.session.delete(roadmap)
    db.session.commit()
    log_action(current_user, 'delete_roadmap', 'Roadmap', roadmap_id, f"Deleted roadmap '{title}'")
    flash(f"Roadmap '{title}' deleted. All courses remain safe in the course catalog.", 'info')
    return redirect(url_for('admin.roadmaps'))

