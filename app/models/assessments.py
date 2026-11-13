from datetime import datetime, timezone
from app.extensions import db

def utcnow():
    return datetime.now(timezone.utc)

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    __table_args__ = (
        db.CheckConstraint('pass_mark >= 0 AND pass_mark <= 100', name='check_quiz_pass_mark_range'),
    )

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False, index=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id', ondelete='SET NULL'), nullable=True)
    title = db.Column(db.String(150), nullable=False)
    time_limit_min = db.Column(db.Integer, default=15, nullable=False)  # minutes
    max_attempts = db.Column(db.Integer, default=3, nullable=False)
    pass_mark = db.Column(db.Float, default=70.0, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    course = db.relationship('Course', back_populates='quizzes')
    module = db.relationship('Module', back_populates='quizzes')
    questions = db.relationship('Question', back_populates='quiz', cascade='all, delete-orphan', order_by='Question.position', lazy='select')
    attempts = db.relationship('QuizAttempt', back_populates='quiz', cascade='all, delete-orphan', lazy='select')

    @property
    def total_points(self) -> float:
        return sum(q.points for q in self.questions)

    def __repr__(self):
        return f'<Quiz {self.title}>'


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id', ondelete='CASCADE'), nullable=False, index=True)
    text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(30), default='single_choice', nullable=False)  # single_choice, multiple_choice, true_false
    points = db.Column(db.Float, default=1.0, nullable=False)
    position = db.Column(db.Integer, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    quiz = db.relationship('Quiz', back_populates='questions')
    options = db.relationship('QuestionOption', back_populates='question', cascade='all, delete-orphan', lazy='selectin')
    attempt_answers = db.relationship('AttemptAnswer', back_populates='question', cascade='all, delete-orphan', lazy='select')

    def __repr__(self):
        return f'<Question {self.id}: {self.text[:30]}>'


class QuestionOption(db.Model):
    __tablename__ = 'question_options'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False, index=True)
    text = db.Column(db.String(255), nullable=False)
    is_correct = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    question = db.relationship('Question', back_populates='options')

    def __repr__(self):
        return f'<QuestionOption {self.text} (Correct: {self.is_correct})>'


class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempts'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    started_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    submitted_at = db.Column(db.DateTime, nullable=True)
    score = db.Column(db.Float, default=0.0, nullable=False)
    passed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    quiz = db.relationship('Quiz', back_populates='attempts')
    user = db.relationship('User', back_populates='quiz_attempts')
    answers = db.relationship('AttemptAnswer', back_populates='attempt', cascade='all, delete-orphan', lazy='select')

    def __repr__(self):
        return f'<QuizAttempt Quiz:{self.quiz_id} User:{self.user_id} Score:{self.score}>'


class AttemptAnswer(db.Model):
    __tablename__ = 'attempt_answers'

    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('quiz_attempts.id', ondelete='CASCADE'), nullable=False, index=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('question_options.id', ondelete='SET NULL'), nullable=True)
    answer_text = db.Column(db.Text, nullable=True)
    is_correct = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    attempt = db.relationship('QuizAttempt', back_populates='answers')
    question = db.relationship('Question', back_populates='attempt_answers')
    option = db.relationship('QuestionOption')


class Rubric(db.Model):
    __tablename__ = 'rubrics'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    creator = db.relationship('User')
    criteria = db.relationship('RubricCriterion', back_populates='rubric', cascade='all, delete-orphan', lazy='selectin')
    assignments = db.relationship('Assignment', back_populates='rubric', lazy='select')

    @property
    def total_max_points(self) -> float:
        return sum(c.max_points for c in self.criteria)

    def __repr__(self):
        return f'<Rubric {self.title}>'


class RubricCriterion(db.Model):
    __tablename__ = 'rubric_criteria'

    id = db.Column(db.Integer, primary_key=True)
    rubric_id = db.Column(db.Integer, db.ForeignKey('rubrics.id', ondelete='CASCADE'), nullable=False, index=True)
    description = db.Column(db.String(255), nullable=False)
    max_points = db.Column(db.Float, default=10.0, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    rubric = db.relationship('Rubric', back_populates='criteria')

    def __repr__(self):
        return f'<RubricCriterion {self.description[:30]}>'


class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    max_points = db.Column(db.Float, default=100.0, nullable=False)
    rubric_id = db.Column(db.Integer, db.ForeignKey('rubrics.id', ondelete='SET NULL'), nullable=True)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    course = db.relationship('Course', back_populates='assignments')
    rubric = db.relationship('Rubric', back_populates='assignments')
    submissions = db.relationship('Submission', back_populates='assignment', cascade='all, delete-orphan', lazy='select')

    def __repr__(self):
        return f'<Assignment {self.title}>'


class Submission(db.Model):
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    text = db.Column(db.Text, nullable=True)
    file_path = db.Column(db.String(255), nullable=True)
    submitted_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    is_late = db.Column(db.Boolean, default=False, nullable=False)
    status = db.Column(db.String(20), default='submitted', nullable=False)  # submitted, graded
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    assignment = db.relationship('Assignment', back_populates='submissions')
    user = db.relationship('User', back_populates='submissions')
    grade = db.relationship('Grade', back_populates='submission', uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Submission Assignment:{self.assignment_id} User:{self.user_id}>'


class Grade(db.Model):
    __tablename__ = 'grades'

    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id', ondelete='CASCADE'), unique=True, nullable=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.id', ondelete='CASCADE'), nullable=False, index=True)
    graded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    feedback = db.Column(db.Text, nullable=True)
    grade_type = db.Column(db.String(30), default='assignment', nullable=False)  # assignment, final
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    submission = db.relationship('Submission', back_populates='grade')
    enrollment = db.relationship('Enrollment', back_populates='grades')
    grader = db.relationship('User')

    def __repr__(self):
        return f'<Grade Score:{self.score} Type:{self.grade_type}>'
