from datetime import datetime, timezone
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models.catalog import Course
from app.models.community import ForumThread, ForumPost, PostLike, Message
from app.models.users import User, Notification
from app.forms.community import ThreadForm, PostForm, MessageForm
from app.utils.helpers import log_action

community_bp = Blueprint('community', __name__, url_prefix='/community')

# --- FORUM ---

@community_bp.route('/forum/<int:course_id>')
def course_forum(course_id):
    """View forum threads for a course."""
    course = Course.query.get_or_404(course_id)
    threads = ForumThread.query.filter_by(course_id=course.id).order_by(ForumThread.is_pinned.desc(), ForumThread.created_at.desc()).all()
    return render_template('community/forum.html', course=course, threads=threads)


@community_bp.route('/forum/<int:course_id>/thread/new', methods=['GET', 'POST'])
@login_required
def create_thread(course_id):
    course = Course.query.get_or_404(course_id)
    form = ThreadForm()
    if form.validate_on_submit():
        thread = ForumThread(
            course_id=course.id,
            author_id=current_user.id,
            title=form.title.data.strip()
        )
        db.session.add(thread)
        db.session.flush()

        initial_post = ForumPost(
            thread_id=thread.id,
            author_id=current_user.id,
            body=form.body.data.strip()
        )
        db.session.add(initial_post)
        db.session.commit()

        log_action(current_user, 'create', 'ForumThread', thread.id, f"Started discussion thread '{thread.title}'")
        flash('Discussion thread started!', 'success')
        return redirect(url_for('community.view_thread', thread_id=thread.id))

    return render_template('community/thread_form.html', form=form, course=course)


@community_bp.route('/thread/<int:thread_id>', methods=['GET', 'POST'])
def view_thread(thread_id):
    thread = ForumThread.query.get_or_404(thread_id)
    course = thread.course
    post_form = PostForm() if current_user.is_authenticated else None

    if post_form and post_form.validate_on_submit():
        if thread.is_locked and not current_user.is_admin and not course.is_instructor(current_user.id):
            flash('This discussion thread is locked for new replies.', 'warning')
            return redirect(url_for('community.view_thread', thread_id=thread.id))

        parent_id = request.form.get('parent_post_id', type=int)
        post = ForumPost(
            thread_id=thread.id,
            author_id=current_user.id,
            parent_post_id=parent_id if parent_id else None,
            body=post_form.body.data.strip()
        )
        db.session.add(post)

        # Notify thread author if different user
        if thread.author_id != current_user.id:
            notif = Notification(
                user_id=thread.author_id,
                title=f"New reply on '{thread.title}'",
                message=f"{current_user.username} replied to your forum thread.",
                link=f"/community/thread/{thread.id}"
            )
            db.session.add(notif)

        db.session.commit()
        log_action(current_user, 'reply', 'ForumPost', post.id, f"Replied to thread {thread.id}")
        flash('Reply posted successfully.', 'success')
        return redirect(url_for('community.view_thread', thread_id=thread.id))

    # Top-level posts
    top_posts = [p for p in thread.posts if p.parent_post_id is None]
    return render_template('community/thread_detail.html', thread=thread, course=course, top_posts=top_posts, form=post_form)


@community_bp.route('/post/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    post = ForumPost.query.get_or_404(post_id)
    existing_like = PostLike.query.filter_by(post_id=post.id, user_id=current_user.id).first()

    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()
        flash('Unliked post.', 'info')
    else:
        like = PostLike(post_id=post.id, user_id=current_user.id)
        db.session.add(like)
        db.session.commit()
        flash('Liked post!', 'success')

    return redirect(url_for('community.view_thread', thread_id=post.thread_id))


@community_bp.route('/thread/<int:thread_id>/toggle-lock', methods=['POST'])
@login_required
def toggle_thread_lock(thread_id):
    thread = ForumThread.query.get_or_404(thread_id)
    if not current_user.is_admin and not thread.course.is_instructor(current_user.id):
        abort(403)
    thread.is_locked = not thread.is_locked
    db.session.commit()
    flash(f"Thread {'locked' if thread.is_locked else 'unlocked'}.", 'info')
    return redirect(url_for('community.view_thread', thread_id=thread.id))


@community_bp.route('/thread/<int:thread_id>/toggle-pin', methods=['POST'])
@login_required
def toggle_thread_pin(thread_id):
    thread = ForumThread.query.get_or_404(thread_id)
    if not current_user.is_admin and not thread.course.is_instructor(current_user.id):
        abort(403)
    thread.is_pinned = not thread.is_pinned
    db.session.commit()
    flash(f"Thread {'pinned' if thread.is_pinned else 'unpinned'}.", 'info')
    return redirect(url_for('community.course_forum', course_id=thread.course_id))


# --- DIRECT MESSAGING ---

@community_bp.route('/inbox')
@login_required
def inbox():
    received = Message.query.filter_by(recipient_id=current_user.id).order_by(Message.created_at.desc()).all()
    sent = Message.query.filter_by(sender_id=current_user.id).order_by(Message.created_at.desc()).all()
    return render_template('community/inbox.html', received=received, sent=sent)


@community_bp.route('/message/send', methods=['GET', 'POST'])
@login_required
def send_message():
    form = MessageForm()
    # Populate recipients (all active users except current_user)
    users = User.query.filter(User.id != current_user.id, User.is_active == True).order_by(User.username).all()
    form.recipient_id.choices = [(u.id, f"{u.username} ({u.role.name})") for u in users]

    recipient_preset = request.args.get('to', type=int)
    if request.method == 'GET' and recipient_preset:
        form.recipient_id.data = recipient_preset

    if form.validate_on_submit():
        msg = Message(
            sender_id=current_user.id,
            recipient_id=form.recipient_id.data,
            subject=form.subject.data.strip(),
            body=form.body.data.strip(),
            is_read=False
        )
        db.session.add(msg)

        # Notify recipient
        notif = Notification(
            user_id=msg.recipient_id,
            title=f"Direct message from {current_user.username}",
            message=f"{msg.subject}: {msg.body[:80]}...",
            link=f"/community/message/{msg.id}"
        )
        db.session.add(notif)
        db.session.commit()

        log_action(current_user, 'send_message', 'Message', msg.id, f"Sent direct message to user {msg.recipient_id}")
        flash('Message delivered!', 'success')
        return redirect(url_for('community.inbox'))

    return render_template('community/message_form.html', form=form)


@community_bp.route('/message/<int:message_id>')
@login_required
def view_message(message_id):
    msg = Message.query.get_or_404(message_id)
    if msg.sender_id != current_user.id and msg.recipient_id != current_user.id and not current_user.is_admin:
        abort(403)

    if msg.recipient_id == current_user.id and not msg.is_read:
        msg.is_read = True
        db.session.commit()

    return render_template('community/message_detail.html', message=msg)


# --- NOTIFICATIONS ---

@community_bp.route('/notifications')
@login_required
def notifications():
    notifs = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    return render_template('community/notifications.html', notifications=notifs)


@community_bp.route('/notifications/read-all', methods=['POST'])
@login_required
def mark_all_notifications_read():
    Notification.query.filter_by(user_id=current_user.id, is_read=False).update({'is_read': True})
    db.session.commit()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
        return {'success': True}
    flash('All notifications marked as read.', 'info')
    return redirect(request.referrer or url_for('community.notifications'))
