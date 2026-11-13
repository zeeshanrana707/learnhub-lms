import pytest
from app import create_app
from app.extensions import db
from app.models.users import Role, User, UserProfile
from app.models.catalog import Department, Category, Course
from app.models.content import Module, Lesson, Enrollment
from app.models.assessments import Quiz, Question, QuestionOption, Rubric, Assignment
from app.models.commerce import Coupon

@pytest.fixture
def app():
    app = create_app('testing')

    with app.app_context():
        db.create_all()

        # Seed roles
        role_admin = Role(name='admin', description='Admin')
        role_inst = Role(name='instructor', description='Instructor')
        role_stu = Role(name='student', description='Student')
        db.session.add_all([role_admin, role_inst, role_stu])
        db.session.flush()

        # Seed users
        admin = User(username='admin_test', email='admin@test.local', role_id=role_admin.id)
        admin.set_password('AdminPass123!')

        instructor = User(username='inst_test', email='inst@test.local', role_id=role_inst.id)
        instructor.set_password('InstPass123!')

        student = User(username='student_test', email='student@test.local', role_id=role_stu.id)
        student.set_password('StudentPass123!')

        db.session.add_all([admin, instructor, student])
        db.session.flush()

        db.session.add(UserProfile(user_id=admin.id, full_name='Admin Tester'))
        db.session.add(UserProfile(user_id=instructor.id, full_name='Instructor Tester'))
        db.session.add(UserProfile(user_id=student.id, full_name='Student Tester'))

        # Seed catalog
        dept = Department(name='CS Dept')
        cat = Category(name='Web Dev', slug='web-dev')
        db.session.add_all([dept, cat])
        db.session.flush()

        course = Course(
            title='Test Course 101',
            slug='test-course-101',
            description='Test course description text exceeding twenty characters.',
            price=0.0,
            level='Beginner',
            status='published',
            department_id=dept.id,
            category_id=cat.id,
            created_by=instructor.id
        )
        db.session.add(course)
        db.session.flush()

        # Module and lesson
        mod = Module(course_id=course.id, title='Module 1', position=1)
        db.session.add(mod)
        db.session.flush()

        l1 = Lesson(module_id=mod.id, title='Lesson 1', content='Content 1', position=1)
        l2 = Lesson(module_id=mod.id, title='Lesson 2', content='Content 2', position=2)
        db.session.add_all([l1, l2])
        db.session.flush()

        # Quiz
        quiz = Quiz(course_id=course.id, title='Quiz 1', time_limit_min=10, max_attempts=2, pass_mark=70.0)
        db.session.add(quiz)
        db.session.flush()

        q1 = Question(quiz_id=quiz.id, text='Question 1 text prompt?', points=10.0, position=1)
        db.session.add(q1)
        db.session.flush()
        db.session.add(QuestionOption(question_id=q1.id, text='Option A (Correct)', is_correct=True))
        db.session.add(QuestionOption(question_id=q1.id, text='Option B', is_correct=False))

        # Coupon
        from datetime import datetime, timezone, timedelta
        now = datetime.now(timezone.utc)
        coupon = Coupon(code='TEST20', discount_percent=20, valid_from=now - timedelta(days=1), valid_to=now + timedelta(days=30), usage_limit=10)
        db.session.add(coupon)

        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username='student_test', password='StudentPass123!'):
        return self._client.post('/auth/login', data={
            'login_id': username,
            'password': password
        }, follow_redirects=True)

    def logout(self):
        return self._client.post('/auth/logout', follow_redirects=True)


@pytest.fixture
def auth(client):
    return AuthActions(client)
