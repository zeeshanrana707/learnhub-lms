from datetime import datetime, timezone
from app.extensions import db
from app.models.content import Enrollment, LessonProgress, Lesson, Module
from app.models.recognition import Badge, UserBadge
from app.models.users import Notification

def calculate_enrollment_progress(enrollment_id: int) -> float:
    """Calculate and update the completion percentage for an enrollment."""
    enrollment = Enrollment.query.get(enrollment_id)
    if not enrollment:
        return 0.0

    # Total published lessons in this course
    total_lessons = Lesson.query.join(Module).filter(
        Module.course_id == enrollment.course_id
    ).count()

    if total_lessons == 0:
        enrollment.progress_pct = 100.0
    else:
        completed_count = LessonProgress.query.filter_by(
            enrollment_id=enrollment.id,
            is_completed=True
        ).count()
        enrollment.progress_pct = round(min(100.0, (completed_count / total_lessons) * 100.0), 1)

    if enrollment.progress_pct >= 100.0:
        if not enrollment.completed_at:
            enrollment.status = 'completed'
            enrollment.completed_at = datetime.now(timezone.utc)
            evaluate_badges_for_user(enrollment.user_id, 'course_completion')
        # Check eligibility and guarantee certificate issuance
        from app.services.certificates import issue_certificate_if_eligible
        issue_certificate_if_eligible(enrollment)

    db.session.commit()
    return enrollment.progress_pct


def toggle_lesson_completion(enrollment_id: int, lesson_id: int) -> bool:
    """Mark a lesson complete or incomplete for an enrollment."""
    record = LessonProgress.query.filter_by(
        enrollment_id=enrollment_id,
        lesson_id=lesson_id
    ).first()

    if record:
        record.is_completed = not record.is_completed
        if record.is_completed:
            record.completed_at = datetime.now(timezone.utc)
        completed = record.is_completed
    else:
        record = LessonProgress(
            enrollment_id=enrollment_id,
            lesson_id=lesson_id,
            is_completed=True,
            completed_at=datetime.now(timezone.utc)
        )
        db.session.add(record)
        completed = True

    db.session.commit()
    calculate_enrollment_progress(enrollment_id)
    return completed


def evaluate_badges_for_user(user_id: int, event_type: str):
    """Award badges dynamically to a student based on rules."""
    now = datetime.now(timezone.utc)

    if event_type == 'course_completion':
        completed_count = Enrollment.query.filter_by(user_id=user_id, status='completed').count()
        # Rule 1: First course completed
        if completed_count >= 1:
            award_badge(user_id, 'first_course', 'Pioneer Scholar', 'Completed your first course!', 'bi-award')
        # Rule 2: Course master (completed 3 or more courses)
        if completed_count >= 3:
            award_badge(user_id, 'course_master', 'Knowledge Seeker', 'Completed 3 or more courses!', 'bi-mortarboard')

    elif event_type == 'perfect_quiz':
        award_badge(user_id, 'perfect_quiz', 'Quiz Prodigy', 'Scored a perfect 100% on a quiz!', 'bi-star-fill')


def award_badge(user_id: int, rule_code: str, name: str, description: str, icon: str):
    badge = Badge.query.filter_by(rule_code=rule_code).first()
    if not badge:
        badge = Badge(name=name, description=description, icon=icon, rule_code=rule_code)
        db.session.add(badge)
        db.session.flush()

    existing = UserBadge.query.filter_by(user_id=user_id, badge_id=badge.id).first()
    if not existing:
        user_badge = UserBadge(user_id=user_id, badge_id=badge.id, awarded_at=datetime.now(timezone.utc))
        db.session.add(user_badge)

        # Notify user
        notif = Notification(
            user_id=user_id,
            title='Badge Unlocked!',
            message=f"Congratulations! You unlocked the '{name}' badge: {description}",
            link='/learn/my-learning'
        )
        db.session.add(notif)
        db.session.commit()
