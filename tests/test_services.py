from app.models.content import Enrollment, LessonProgress, Lesson
from app.models.assessments import Quiz, QuestionOption, QuizAttempt
from app.models.catalog import Course
from app.models.users import User
from app.services.progress import calculate_enrollment_progress, toggle_lesson_completion
from app.services.grading import grade_quiz_attempt, grade_submission, compute_final_grade
from app.services.certificates import issue_certificate_if_eligible
from app.services.orders import calculate_cart_breakdown, process_checkout

def test_progress_calculation(app):
    with app.app_context():
        user = User.query.filter_by(username='student_test').first()
        course = Course.query.filter_by(slug='test-course-101').first()

        enrollment = Enrollment(user_id=user.id, course_id=course.id, status='active', progress_pct=0.0)
        from app.extensions import db
        db.session.add(enrollment)
        db.session.commit()

        # Initially 0%
        prog = calculate_enrollment_progress(enrollment.id)
        assert prog == 0.0

        # Mark 1 of 2 lessons complete -> 50%
        lesson1 = Lesson.query.filter_by(title='Lesson 1').first()
        toggle_lesson_completion(enrollment.id, lesson1.id)

        enrollment = Enrollment.query.get(enrollment.id)
        assert enrollment.progress_pct == 50.0

        # Mark 2nd lesson complete -> 100% and completed status
        lesson2 = Lesson.query.filter_by(title='Lesson 2').first()
        toggle_lesson_completion(enrollment.id, lesson2.id)

        enrollment = Enrollment.query.get(enrollment.id)
        assert enrollment.progress_pct == 100.0
        assert enrollment.status == 'completed'
        assert enrollment.certificate is not None


def test_quiz_auto_grading(app):
    with app.app_context():
        user = User.query.filter_by(username='student_test').first()
        quiz = Quiz.query.first()
        correct_opt = QuestionOption.query.filter_by(is_correct=True).first()

        # Submit correct answer
        attempt = grade_quiz_attempt(quiz.id, user.id, {str(quiz.questions[0].id): str(correct_opt.id)})
        assert attempt.score == 100.0
        assert attempt.passed is True

        # Submit incorrect answer
        incorrect_opt = QuestionOption.query.filter_by(is_correct=False).first()
        attempt2 = grade_quiz_attempt(quiz.id, user.id, {str(quiz.questions[0].id): str(incorrect_opt.id)})
        assert attempt2.score == 0.0
        assert attempt2.passed is False


def test_cart_and_coupon_breakdown(app):
    with app.app_context():
        course = Course.query.first()
        course.price = 100.0
        from app.extensions import db
        db.session.commit()

        # Without coupon
        courses, subtotal, discount, total, coupon, err = calculate_cart_breakdown([course.id], None)
        assert subtotal == 100.0
        assert discount == 0.0
        assert total == 100.0

        # With 20% coupon
        courses, subtotal, discount, total, coupon, err = calculate_cart_breakdown([course.id], 'TEST20')
        assert subtotal == 100.0
        assert discount == 20.0
        assert total == 80.0
        assert coupon is not None
        assert err is None


def test_simulated_checkout_and_auto_enrollment(app):
    with app.app_context():
        user = User.query.filter_by(username='student_test').first()
        course = Course.query.first()
        course.price = 50.0
        from app.extensions import db
        db.session.commit()

        order, err = process_checkout(user, [course.id], 'TEST20', 'simulated_card')
        assert err is None
        assert order is not None
        assert order.status == 'paid'
        assert order.total == 40.0
        assert order.payment is not None
        assert order.payment.status == 'completed'

        # Verify auto-enrollment
        enrollment = Enrollment.query.filter_by(user_id=user.id, course_id=course.id).first()
        assert enrollment is not None
        assert enrollment.status == 'active'
