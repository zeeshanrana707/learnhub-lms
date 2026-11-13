from functools import wraps
from flask import abort, flash, redirect, url_for, request
from flask_login import current_user
from app.models.catalog import Course

def role_required(*role_names):
    """Decorator to require that current_user has one of the specified roles."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login', next=request.url))
            user_role = current_user.role.name.lower() if current_user.role else ''
            allowed_roles = [r.lower() for r in role_names]
            if user_role not in allowed_roles and not current_user.is_admin:
                flash('You do not have permission to view this resource.', 'danger')
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def instructor_or_admin_required(f):
    """Requires user to be either an instructor or an admin."""
    return role_required('instructor', 'admin')(f)


def admin_required(f):
    """Requires user to be an admin."""
    return role_required('admin')(f)


def instructor_course_owner_required(f):
    """
    Decorator for views with course_id in kwargs.
    Checks that an instructor owns or is assigned to this course,
    or current_user is an admin.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to continue.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        
        course_id = kwargs.get('course_id') or kwargs.get('id')
        if not course_id:
            abort(404)
        course = Course.query.get_or_404(course_id)
        if current_user.is_admin:
            return f(*args, **kwargs)
        if not course.is_instructor(current_user.id):
            flash('You do not have permission to modify this course.', 'danger')
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
