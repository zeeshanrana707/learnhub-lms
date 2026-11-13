from datetime import datetime, timezone
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models.catalog import Course
from app.models.content import Module, Enrollment
from app.models.assessments import (
    Quiz, Question, QuestionOption, QuizAttempt, AttemptAnswer,
    Assignment, Submission, Rubric, RubricCriterion, Grade
)
from app.forms.assessments import (
    QuizForm, QuestionForm, QuestionOptionForm,
    AssignmentForm, SubmissionForm, RubricForm, RubricCriterionForm, GradeForm
)
from app.services.grading import grade_quiz_attempt, grade_submission
from app.utils.decorators import instructor_or_admin_required
from app.utils.helpers import log_action, save_file

assessments_bp = Blueprint('assessments', __name__, url_prefix='/assess')

# --- QUIZ MANAGEMENT (INSTRUCTOR) ---

@assessments_bp.route('/course/<int:course_id>/quiz/new', methods=['GET', 'POST'])
@login_required
@instructor_or_admin_required
def create_quiz(course_id):
    course = Course.query.get_or_404(course_id)
    if not current_user.is_admin and not course.is_instructor(current_user.id):
        abort(403)

    form = QuizForm()
    form.module_id.choices = [(0, '-- None (Course-Wide) --')] + [(m.id, m.title) for m in course.modules]

    if form.validate_on_submit():
        quiz = Quiz(
            course_id=course.id,
            module_id=form.module_id.data if form.module_id.data != 0 else None,
            title=form.title.data.strip(),
            time_limit_min=form.time_limit_min.data,
            max_attempts=form.max_attempts.data,
            pass_mark=float(form.pass_mark.data)
        )
        db.session.add(quiz)
        db.session.commit()
        log_action(current_user, 'create', 'Quiz', quiz.id, f"Created quiz '{quiz.title}'")
        flash(f"Quiz '{quiz.title}' created. Now add questions below.", 'success')
        return redirect(url_for('assessments.edit_quiz', quiz_id=quiz.id))

    return render_template('assessments/quiz_form.html', form=form, course=course, title="Create New Quiz")


@assessments_bp.route('/quiz/<int:quiz_id>/edit', methods=['GET', 'POST'])
@login_required
@instructor_or_admin_required
def edit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    course = quiz.course
    if not current_user.is_admin and not course.is_instructor(current_user.id):
        abort(403)

    form = QuizForm(obj=quiz)
    form.module_id.choices = [(0, '-- None (Course-Wide) --')] + [(m.id, m.title) for m in course.modules]

    if request.method == 'GET':
        form.module_id.data = quiz.module_id or 0

    if form.validate_on_submit():
        quiz.title = form.title.data.strip()
        quiz.module_id = form.module_id.data if form.module_id.data != 0 else None
        quiz.time_limit_min = form.time_limit_min.data
        quiz.max_attempts = form.max_attempts.data
        quiz.pass_mark = float(form.pass_mark.data)
        db.session.commit()
        log_action(current_user, 'update', 'Quiz', quiz.id, f"Updated quiz '{quiz.title}'")
        flash('Quiz updated successfully.', 'success')
        return redirect(url_for('assessments.edit_quiz', quiz_id=quiz.id))

    return render_template('assessments/quiz_builder.html', form=form, quiz=quiz, course=course)


@assessments_bp.route('/quiz/<int:quiz_id>/delete', methods=['POST'])
@login_required
@instructor_or_admin_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    course_id = quiz.course_id
    if not current_user.is_admin and not quiz.course.is_instructor(current_user.id):
        abort(403)

    db.session.delete(quiz)
    db.session.commit()
    log_action(current_user, 'delete', 'Quiz', quiz_id, f"Deleted quiz '{quiz.title}'")
    flash('Quiz deleted.', 'info')
    return redirect(url_for('learning.manage_course_curriculum', course_id=course_id))


@assessments_bp.route('/quiz/<int:quiz_id>/question/new', methods=['GET', 'POST'])
@login_required
@instructor_or_admin_required
def add_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if not current_user.is_admin and not quiz.course.is_instructor(current_user.id):
        abort(403)

    form = QuestionForm()
    if form.validate_on_submit():
        q = Question(
            quiz_id=quiz.id,
            text=form.text.data.strip(),
            question_type=form.question_type.data,
            points=float(form.points.data),
            position=form.position.data or (len(quiz.questions) + 1)
        )
        db.session.add(q)
        db.session.flush()

        # If true/false question, automatically seed options
        if q.question_type == 'true_false':
            db.session.add(QuestionOption(question_id=q.id, text='True', is_correct=True))
            db.session.add(QuestionOption(question_id=q.id, text='False', is_correct=False))

        db.session.commit()
        log_action(current_user, 'create', 'Question', q.id, f"Added question to quiz {quiz.id}")
        flash('Question created! Add answer choices below.', 'success')
        return redirect(url_for('assessments.edit_question', question_id=q.id))

    return render_template('assessments/question_form.html', form=form, quiz=quiz, title="Add Question")


@assessments_bp.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
@login_required
@instructor_or_admin_required
def edit_question(question_id):
    question = Question.query.get_or_404(question_id)
    quiz = question.quiz
    if not current_user.is_admin and not quiz.course.is_instructor(current_user.id):
        abort(403)

    form = QuestionForm(obj=question)
    option_form = QuestionOptionForm()

    if form.validate_on_submit():
        question.text = form.text.data.strip()
        question.question_type = form.question_type.data
        question.points = float(form.points.data)
        question.position = form.position.data
        db.session.commit()
        flash('Question updated.', 'success')
        return redirect(url_for('assessments.edit_quiz', quiz_id=quiz.id))

    return render_template('assessments/question_form.html', form=form, option_form=option_form, question=question, quiz=quiz, title="Edit Question")


@assessments_bp.route('/question/<int:question_id>/option/new', methods=['POST'])
@login_required
@instructor_or_admin_required
def add_question_option(question_id):
    question = Question.query.get_or_404(question_id)
    quiz = question.quiz
    if not current_user.is_admin and not quiz.course.is_instructor(current_user.id):
        abort(403)

    form = QuestionOptionForm()
    if form.validate_on_submit():
        # If single choice and marked correct, unset any existing correct
        if form.is_correct.data and question.question_type == 'single_choice':
            for opt in question.options:
                opt.is_correct = False

        opt = QuestionOption(
            question_id=question.id,
            text=form.text.data.strip(),
            is_correct=form.is_correct.data
        )
        db.session.add(opt)
        db.session.commit()
        flash(f"Option '{opt.text}' added.", 'success')

    return redirect(url_for('assessments.edit_question', question_id=question.id))


@assessments_bp.route('/option/<int:option_id>/delete', methods=['POST'])
@login_required
@instructor_or_admin_required
def delete_question_option(option_id):
    opt = QuestionOption.query.get_or_404(option_id)
    qid = opt.question_id
    db.session.delete(opt)
    db.session.commit()
    flash('Option deleted.', 'info')
    return redirect(url_for('assessments.edit_question', question_id=qid))


@assessments_bp.route('/question/<int:question_id>/delete', methods=['POST'])
@login_required
@instructor_or_admin_required
def delete_question(question_id):
    q = Question.query.get_or_404(question_id)
    quiz_id = q.quiz_id
    db.session.delete(q)
    db.session.commit()
    flash('Question removed.', 'info')
    return redirect(url_for('assessments.edit_quiz', quiz_id=quiz_id))


# --- QUIZ TAKING & ATTEMPTS (STUDENT) ---

@assessments_bp.route('/quiz/<int:quiz_id>/attempt', methods=['GET', 'POST'])
@login_required
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=quiz.course_id).first()

    if not enrollment and not current_user.is_admin and not quiz.course.is_instructor(current_user.id):
        flash('You must be enrolled in this course to take this quiz.', 'danger')
        return redirect(url_for('catalog.detail', course_id=quiz.course_id))

    # Check attempt limit
    attempts_count = QuizAttempt.query.filter_by(quiz_id=quiz.id, user_id=current_user.id).count()
    if attempts_count >= quiz.max_attempts and not current_user.is_admin:
        flash(f"You have reached the maximum allowed attempts ({quiz.max_attempts}) for this quiz.", 'warning')
        latest = QuizAttempt.query.filter_by(quiz_id=quiz.id, user_id=current_user.id).order_by(QuizAttempt.created_at.desc()).first()
        return redirect(url_for('assessments.quiz_result', quiz_id=quiz.id, attempt_id=latest.id))

    if request.method == 'POST':
        answers = {}
        for key, value in request.form.items():
            if key.startswith('question_'):
                qid = key.replace('question_', '')
                answers[qid] = value

        attempt = grade_quiz_attempt(quiz.id, current_user.id, answers)
        log_action(current_user, 'attempt_quiz', 'Quiz', quiz.id, f"Completed quiz attempt {attempt.id}. Score: {attempt.score}%")
        flash(f"Quiz submitted! Your score: {attempt.score}%", 'success' if attempt.passed else 'warning')
        return redirect(url_for('assessments.quiz_result', quiz_id=quiz.id, attempt_id=attempt.id))

    return render_template('assessments/quiz_attempt.html', quiz=quiz, attempts_count=attempts_count)


@assessments_bp.route('/quiz/<int:quiz_id>/result/<int:attempt_id>')
@login_required
def quiz_result(quiz_id, attempt_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    attempt = QuizAttempt.query.get_or_404(attempt_id)
    if attempt.user_id != current_user.id and not current_user.is_admin and not quiz.course.is_instructor(current_user.id):
        abort(403)

    return render_template('assessments/quiz_result.html', quiz=quiz, attempt=attempt)


# --- ASSIGNMENTS & RUBRICS ---

@assessments_bp.route('/rubrics')
@login_required
@instructor_or_admin_required
def rubrics():
    rubrics = Rubric.query.order_by(Rubric.created_at.desc()).all()
    form = RubricForm()
    return render_template('assessments/rubrics.html', rubrics=rubrics, form=form)


@assessments_bp.route('/rubric/new', methods=['POST'])
@login_required
@instructor_or_admin_required
def create_rubric():
    form = RubricForm()
    if form.validate_on_submit():
        rubric = Rubric(title=form.title.data.strip(), created_by=current_user.id)
        db.session.add(rubric)
        db.session.commit()
        log_action(current_user, 'create', 'Rubric', rubric.id, f"Created rubric '{rubric.title}'")
        flash(f"Rubric '{rubric.title}' created. Add evaluation criteria below.", 'success')
        return redirect(url_for('assessments.edit_rubric', rubric_id=rubric.id))
    return redirect(url_for('assessments.rubrics'))


@assessments_bp.route('/rubric/<int:rubric_id>/edit', methods=['GET', 'POST'])
@login_required
@instructor_or_admin_required
def edit_rubric(rubric_id):
    rubric = Rubric.query.get_or_404(rubric_id)
    form = RubricForm(obj=rubric)
    crit_form = RubricCriterionForm()

    if form.validate_on_submit():
        rubric.title = form.title.data.strip()
        db.session.commit()
        flash('Rubric updated.', 'success')
        return redirect(url_for('assessments.edit_rubric', rubric_id=rubric.id))

    return render_template('assessments/rubric_detail.html', rubric=rubric, form=form, crit_form=crit_form)


@assessments_bp.route('/rubric/<int:rubric_id>/criterion/new', methods=['POST'])
@login_required
@instructor_or_admin_required
def add_rubric_criterion(rubric_id):
    rubric = Rubric.query.get_or_404(rubric_id)
    form = RubricCriterionForm()
    if form.validate_on_submit():
        crit = RubricCriterion(
            rubric_id=rubric.id,
            description=form.description.data.strip(),
            max_points=float(form.max_points.data)
        )
        db.session.add(crit)
        db.session.commit()
        flash('Criterion added.', 'success')

    return redirect(url_for('assessments.edit_rubric', rubric_id=rubric.id))


@assessments_bp.route('/criterion/<int:criterion_id>/delete', methods=['POST'])
@login_required
@instructor_or_admin_required
def delete_criterion(criterion_id):
    crit = RubricCriterion.query.get_or_404(criterion_id)
    rid = crit.rubric_id
    db.session.delete(crit)
    db.session.commit()
    flash('Criterion removed.', 'info')
    return redirect(url_for('assessments.edit_rubric', rubric_id=rid))


@assessments_bp.route('/course/<int:course_id>/assignment/new', methods=['GET', 'POST'])
@login_required
@instructor_or_admin_required
def create_assignment(course_id):
    course = Course.query.get_or_404(course_id)
    if not current_user.is_admin and not course.is_instructor(current_user.id):
        abort(403)

    form = AssignmentForm()
    form.rubric_id.choices = [(0, '-- No Rubric --')] + [(r.id, r.title) for r in Rubric.query.order_by(Rubric.title).all()]

    if form.validate_on_submit():
        assign = Assignment(
            course_id=course.id,
            title=form.title.data.strip(),
            instructions=form.instructions.data.strip(),
            due_date=form.due_date.data,
            max_points=float(form.max_points.data),
            rubric_id=form.rubric_id.data if form.rubric_id.data != 0 else None
        )
        db.session.add(assign)
        db.session.commit()
        log_action(current_user, 'create', 'Assignment', assign.id, f"Created assignment '{assign.title}'")
        flash(f"Assignment '{assign.title}' created successfully.", 'success')
        return redirect(url_for('learning.manage_course_curriculum', course_id=course.id))

    return render_template('assessments/assignment_form.html', form=form, course=course, title="Create Assignment")


@assessments_bp.route('/assignment/<int:id>', methods=['GET', 'POST'])
@login_required
def view_assignment(id):
    assignment = Assignment.query.get_or_404(id)
    course = assignment.course

    enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course.id).first()
    is_owner = course.is_instructor(current_user.id) or current_user.is_admin
    if not enrollment and not is_owner:
        flash('You must be enrolled in this course to access this assignment.', 'warning')
        return redirect(url_for('catalog.detail', course_id=course.id))

    user_submission = Submission.query.filter_by(assignment_id=assignment.id, user_id=current_user.id).first()
    form = SubmissionForm()

    if form.validate_on_submit():
        file_path = None
        if form.file.data:
            file_path = save_file(form.file.data, subfolder='assignments')

        # Check due date
        now = datetime.now()
        is_late = now > assignment.due_date

        if not user_submission:
            user_submission = Submission(
                assignment_id=assignment.id,
                user_id=current_user.id,
                text=form.text.data.strip() if form.text.data else '',
                file_path=file_path,
                is_late=is_late,
                status='submitted'
            )
            db.session.add(user_submission)
            flash('Assignment submitted successfully!', 'success')
        else:
            user_submission.text = form.text.data.strip() if form.text.data else user_submission.text
            if file_path:
                user_submission.file_path = file_path
            user_submission.is_late = is_late
            user_submission.status = 'submitted'
            user_submission.submitted_at = datetime.now(timezone.utc)
            flash('Assignment submission updated!', 'success')

        db.session.commit()
        log_action(current_user, 'submit_assignment', 'Assignment', assignment.id, f"Submitted assignment. Late: {is_late}")
        return redirect(url_for('assessments.view_assignment', id=assignment.id))

    return render_template(
        'assessments/assignment_detail.html',
        assignment=assignment,
        submission=user_submission,
        form=form,
        is_owner=is_owner
    )


# --- GRADING QUEUE (INSTRUCTOR) ---

@assessments_bp.route('/grading-queue')
@login_required
@instructor_or_admin_required
def grading_queue():
    if current_user.is_admin:
        courses = Course.query.all()
    else:
        assigned_ids = [ci.course_id for ci in current_user.course_instructors]
        courses = Course.query.filter((Course.created_by == current_user.id) | (Course.id.in_(assigned_ids))).all()

    course_ids = [c.id for c in courses]
    pending = Submission.query.join(Assignment).filter(
        Assignment.course_id.in_(course_ids),
        Submission.status == 'submitted'
    ).order_by(Submission.submitted_at.asc()).all() if course_ids else []

    graded = Submission.query.join(Assignment).filter(
        Assignment.course_id.in_(course_ids),
        Submission.status == 'graded'
    ).order_by(Submission.submitted_at.desc()).limit(20).all() if course_ids else []

    return render_template('assessments/grading_queue.html', pending=pending, graded=graded)


@assessments_bp.route('/submission/<int:id>/grade', methods=['GET', 'POST'])
@login_required
@instructor_or_admin_required
def grade_single_submission(id):
    sub = Submission.query.get_or_404(id)
    assignment = sub.assignment
    course = assignment.course
    if not current_user.is_admin and not course.is_instructor(current_user.id):
        abort(403)

    form = GradeForm()
    if request.method == 'GET' and sub.grade:
        form.score.data = sub.grade.score
        form.feedback.data = sub.grade.feedback

    if form.validate_on_submit():
        score = float(form.score.data)
        grade_submission(sub.id, current_user.id, score, form.feedback.data)
        log_action(current_user, 'grade_submission', 'Submission', sub.id, f"Graded submission {sub.id}: Score {score}")
        flash(f"Submission for student {sub.user.username} successfully graded!", 'success')
        return redirect(url_for('assessments.grading_queue'))

    return render_template('assessments/grade_submission.html', submission=sub, assignment=assignment, form=form)


@assessments_bp.route('/grades')
@login_required
def student_grades():
    """Student view of their performance across enrolled courses."""
    enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
    quiz_attempts = QuizAttempt.query.filter_by(user_id=current_user.id).order_by(QuizAttempt.created_at.desc()).all()
    submissions = Submission.query.filter_by(user_id=current_user.id).order_by(Submission.created_at.desc()).all()

    return render_template(
        'assessments/grades.html',
        enrollments=enrollments,
        quiz_attempts=quiz_attempts,
        submissions=submissions
    )
