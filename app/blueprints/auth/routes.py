from datetime import datetime, timezone
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, session
from flask_login import login_user, logout_user, login_required, current_user
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from app.extensions import db
from app.models.users import User, Role, UserProfile
from app.forms.auth import LoginForm, RegisterForm, ProfileForm, ChangePasswordForm, ResetPasswordRequestForm, ResetPasswordForm
from app.utils.helpers import log_action

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def get_serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('catalog.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        role_name = form.role.data.lower()
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            # Fallback to student
            role = Role.query.filter_by(name='student').first()

        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower(),
            role_id=role.id,
            is_active=True
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()

        # Create linked profile
        profile = UserProfile(user_id=user.id, full_name=form.username.data.strip())
        db.session.add(profile)

        # If student, automatically enroll them in all published courses so their dashboard has all YouTube courses ready
        if role_name == 'student':
            from app.models.catalog import Course
            from app.models.content import Enrollment
            active_courses = Course.query.filter_by(status='published', is_active=True).all()
            for ac in active_courses:
                db.session.add(Enrollment(
                    user_id=user.id,
                    course_id=ac.id,
                    status='active',
                    progress_pct=0.0,
                    enrolled_at=datetime.now(timezone.utc)
                ))

        db.session.commit()

        log_action(user, 'register', 'User', user.id, f"Registered new account as {role_name}")
        flash('Registration successful! Please log in to your new account.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        next_url = request.args.get('next')
        if next_url and next_url.startswith('/'):
            return redirect(next_url)
        return redirect_by_role(current_user)

    form = LoginForm()
    if form.validate_on_submit():
        from sqlalchemy import func
        login_val = form.login_id.data.strip()
        user = User.query.filter(
            (func.lower(User.email) == login_val.lower()) |
            (func.lower(User.username) == login_val.lower())
        ).first()

        if not user:
            flash(f'No account found matching "{login_val}". Please verify your email or username, or create an account.', 'danger')
            return render_template('auth/login.html', form=form)

        if not user.check_password(form.password.data):
            flash(f'Incorrect password for account "{user.username}". Please try again or use the link below to reset your password.', 'danger')
            return render_template('auth/login.html', form=form, reset_email=user.email)

        if not user.is_active:
            flash('Your account has been deactivated. Please contact administrator.', 'danger')
            return render_template('auth/login.html', form=form)

        user.last_login = datetime.now(timezone.utc)
        db.session.commit()

        login_user(user, remember=form.remember_me.data)
        log_action(user, 'login', 'User', user.id, f"User {user.username} logged in")

        flash(f'Welcome back, {user.username}!', 'success')
        next_url = request.args.get('next')
        if next_url and next_url.startswith('/'):
            return redirect(next_url)
        return redirect_by_role(user)

    return render_template('auth/login.html', form=form)


def redirect_by_role(user):
    """Direct user to their personalized dashboard based on role."""
    if user.is_admin:
        return redirect(url_for('admin.dashboard'))
    elif user.is_instructor:
        return redirect(url_for('catalog.instructor_dashboard'))
    else:
        return redirect(url_for('learning.my_learning'))


@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    log_action(current_user, 'logout', 'User', current_user.id, f"User {current_user.username} logged out")
    session.pop('live_preview', None)
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('catalog.index'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user.profile)
    if form.validate_on_submit():
        if not current_user.profile:
            current_user.profile = UserProfile(user_id=current_user.id)
            db.session.add(current_user.profile)

        current_user.profile.full_name = form.full_name.data
        current_user.profile.phone = form.phone.data
        current_user.profile.country = form.country.data
        current_user.profile.bio = form.bio.data
        db.session.commit()

        log_action(current_user, 'update', 'UserProfile', current_user.profile.id, "Profile updated")
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('auth/profile.html', form=form, user=current_user)


@auth_bp.route('/password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('Current password is incorrect.', 'danger')
            return render_template('auth/change_password.html', form=form)

        current_user.set_password(form.new_password.data)
        db.session.commit()
        log_action(current_user, 'update_password', 'User', current_user.id, "Changed password")
        flash('Your password has been updated. Please log in again.', 'success')
        logout_user()
        return redirect(url_for('auth.login'))

    return render_template('auth/change_password.html', form=form)


@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('catalog.index'))

    form = ResetPasswordRequestForm()
    if request.method == 'GET' and request.args.get('email'):
        form.email.data = request.args.get('email')

    if form.validate_on_submit():
        from sqlalchemy import func
        user = User.query.filter(func.lower(User.email) == form.email.data.strip().lower()).first()
        if user:
            s = get_serializer()
            token = s.dumps(user.email, salt='password-reset-salt')
            flash(f'Account found for {user.email}! Please enter your new password below.', 'success')
            return redirect(url_for('auth.reset_password_token', token=token))
        else:
            flash(f'No account registered with email "{form.email.data.strip()}". Please check your spelling or register.', 'warning')
            return render_template('auth/reset_request.html', form=form)

    return render_template('auth/reset_request.html', form=form)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('catalog.index'))

    s = get_serializer()
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)  # 1 hour
    except (SignatureExpired, BadSignature):
        flash('The password reset link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.reset_password_request'))

    user = User.query.filter_by(email=email).first_or_404()
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.new_password.data)
        db.session.commit()
        log_action(user, 'reset_password', 'User', user.id, "Password reset via token")
        flash('Your password has been reset successfully. You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_token.html', form=form)
