from datetime import datetime, timezone
from app.extensions import db
from app.models.assessments import Quiz, Question, QuestionOption, QuizAttempt, AttemptAnswer, Submission, Grade, Assignment
from app.models.content import Enrollment
from app.models.users import Notification
from app.services.progress import evaluate_badges_for_user

def grade_quiz_attempt(quiz_id: int, user_id: int, user_answers: dict) -> QuizAttempt:
    """
    Grade a submitted quiz attempt.
    user_answers: dict of {question_id: selected_option_id or text}
    """
    quiz = Quiz.query.get_or_404(quiz_id)
    attempt = QuizAttempt(
        quiz_id=quiz.id,
        user_id=user_id,
        started_at=datetime.now(timezone.utc),
        submitted_at=datetime.now(timezone.utc)
    )
    db.session.add(attempt)
    db.session.flush()

    total_earned = 0.0
    total_points = 0.0

    for question in quiz.questions:
        total_points += question.points
        user_choice = user_answers.get(str(question.id)) or user_answers.get(question.id)

        is_correct = False
        option_id = None
        ans_text = None

        if question.question_type in ('single_choice', 'true_false'):
            if user_choice:
                try:
                    option_id = int(user_choice)
                    selected_opt = QuestionOption.query.get(option_id)
                    if selected_opt and selected_opt.is_correct:
                        is_correct = True
                        total_earned += question.points
                except (ValueError, TypeError):
                    pass
        elif question.question_type == 'multiple_choice':
            # user_choice could be a list of option IDs
            choice_list = user_choice if isinstance(user_choice, list) else [user_choice]
            correct_opts = {str(opt.id) for opt in question.options if opt.is_correct}
            user_opts = {str(c) for c in choice_list if c}
            if correct_opts == user_opts:
                is_correct = True
                total_earned += question.points
            ans_text = ",".join(user_opts)
        else:
            ans_text = str(user_choice or '')

        ans_record = AttemptAnswer(
            attempt_id=attempt.id,
            question_id=question.id,
            option_id=option_id,
            answer_text=ans_text,
            is_correct=is_correct
        )
        db.session.add(ans_record)

    pct_score = round((total_earned / total_points * 100.0), 1) if total_points > 0 else 100.0
    attempt.score = pct_score
    attempt.passed = pct_score >= quiz.pass_mark

    # Check for perfect quiz badge
    if pct_score >= 100.0:
        evaluate_badges_for_user(user_id, 'perfect_quiz')

    # Notify student
    notif = Notification(
        user_id=user_id,
        title=f"Quiz Graded: {quiz.title}",
        message=f"You scored {pct_score}% on '{quiz.title}'. Status: {'PASSED' if attempt.passed else 'FAILED'}.",
        link=f"/assess/quiz/{quiz.id}/result/{attempt.id}"
    )
    db.session.add(notif)
    db.session.commit()

    return attempt


def grade_submission(submission_id: int, grader_id: int, score: float, feedback: str = None) -> Grade:
    """Grade an assignment submission and notify the student."""
    submission = Submission.query.get_or_404(submission_id)
    assignment = submission.assignment

    # Find the corresponding enrollment
    enrollment = Enrollment.query.filter_by(
        user_id=submission.user_id,
        course_id=assignment.course_id
    ).first()

    if not enrollment:
        # Create enrollment if somehow missing
        enrollment = Enrollment(user_id=submission.user_id, course_id=assignment.course_id)
        db.session.add(enrollment)
        db.session.flush()

    grade = Grade.query.filter_by(submission_id=submission.id).first()
    if not grade:
        grade = Grade(
            submission_id=submission.id,
            enrollment_id=enrollment.id,
            graded_by=grader_id,
            score=score,
            feedback=feedback,
            grade_type='assignment'
        )
        db.session.add(grade)
    else:
        grade.score = score
        grade.feedback = feedback
        grade.graded_by = grader_id

    submission.status = 'graded'

    # Notify student
    notif = Notification(
        user_id=submission.user_id,
        title=f"Assignment Graded: {assignment.title}",
        message=f"Your submission for '{assignment.title}' received a score of {score}/{assignment.max_points}.",
        link=f"/assess/assignment/{assignment.id}"
    )
    db.session.add(notif)
    db.session.commit()

    return grade


def compute_final_grade(enrollment_id: int, grader_id: int = None) -> float:
    """Compute weighted composite grade for an enrolled course."""
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    course = enrollment.course

    # Gather all quiz scores for this user in this course
    quiz_attempts = QuizAttempt.query.join(Quiz).filter(
        Quiz.course_id == course.id,
        QuizAttempt.user_id == enrollment.user_id
    ).all()
    quiz_avg = (sum(a.score for a in quiz_attempts) / len(quiz_attempts)) if quiz_attempts else 100.0

    # Gather all assignment scores
    grades = Grade.query.filter_by(enrollment_id=enrollment.id, grade_type='assignment').all()
    assignment_avg = (sum(g.score for g in grades) / len(grades)) if grades else 100.0

    # Simple 50-50 weighted combination
    final_score = round((quiz_avg * 0.5) + (assignment_avg * 0.5), 1)

    final_grade = Grade.query.filter_by(enrollment_id=enrollment.id, grade_type='final').first()
    if not final_grade:
        final_grade = Grade(
            enrollment_id=enrollment.id,
            graded_by=grader_id or course.created_by,
            score=final_score,
            feedback="Calculated overall final grade.",
            grade_type='final'
        )
        db.session.add(final_grade)
    else:
        final_grade.score = final_score

    db.session.commit()

    from app.services.certificates import issue_certificate_if_eligible
    issue_certificate_if_eligible(enrollment)

    return final_score
