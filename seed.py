"""
Comprehensive Database Seeder for LMS Flask Application.
Populates all 44 relational models with realistic sample data.
Meets the exact requirements of Web Engineering (CSE601330).
"""

import os
from datetime import datetime, timezone, timedelta
from faker import Faker
from app import create_app
from app.extensions import db
from app.models.users import Role, Permission, RolePermission, User, UserProfile, Notification
from app.models.catalog import Department, Category, Course, CoursePrerequisite, Tag, CourseTag
from app.models.content import CourseInstructor, Module, Lesson, LessonResource, Announcement, Enrollment, LessonProgress, Wishlist
from app.models.assessments import Quiz, Question, QuestionOption, QuizAttempt, AttemptAnswer, Rubric, RubricCriterion, Assignment, Submission, Grade
from app.models.community import ForumThread, ForumPost, PostLike, Message
from app.models.recognition import Certificate, Badge, UserBadge, Review
from app.models.commerce import Coupon, Order, OrderItem, Payment
from app.models.admin import AuditLog, Setting
from app.utils.helpers import slugify

fake = Faker()
Faker.seed(42)

app = create_app()

def run_seed():
    with app.app_context():
        print("-> Dropping and recreating all tables...")
        db.drop_all()
        db.create_all()
        print("-> All tables verified.")

        # ---------------------------------------------------------
        # 1. ROLES & PERMISSIONS (Users & Access: 4 models)
        # ---------------------------------------------------------
        print("-> Seeding Roles and Permissions...")
        roles_data = [
            ('admin', 'Platform Superuser with full system access'),
            ('instructor', 'Course author, content creator, and evaluator'),
            ('student', 'Course learner, quiz taker, and community member')
        ]
        role_objs = {}
        for name, desc in roles_data:
            r = Role(name=name, description=desc)
            db.session.add(r)
            role_objs[name] = r
        db.session.flush()

        perms_data = [
            ('manage_users', 'Can create, edit, and deactivate users'),
            ('manage_roles', 'Can alter roles and permissions'),
            ('manage_catalog', 'Can manage departments, categories, and tags'),
            ('create_course', 'Can create and publish courses'),
            ('grade_submissions', 'Can evaluate assignments and quizzes'),
            ('enroll_course', 'Can purchase and enroll in courses'),
            ('post_community', 'Can create forum threads and post replies'),
            ('send_messages', 'Can send private messages to users'),
            ('view_audit', 'Can view platform security and audit logs')
        ]
        perm_objs = {}
        for code, desc in perms_data:
            p = Permission(code=code, description=desc)
            db.session.add(p)
            perm_objs[code] = p
        db.session.flush()

        # Link permissions
        for code, p in perm_objs.items():
            db.session.add(RolePermission(role_id=role_objs['admin'].id, permission_id=p.id))

        instructor_perms = ['create_course', 'grade_submissions', 'post_community', 'send_messages']
        for code in instructor_perms:
            db.session.add(RolePermission(role_id=role_objs['instructor'].id, permission_id=perm_objs[code].id))

        student_perms = ['enroll_course', 'post_community', 'send_messages']
        for code in student_perms:
            db.session.add(RolePermission(role_id=role_objs['student'].id, permission_id=perm_objs[code].id))

        db.session.flush()

        # ---------------------------------------------------------
        # 2. USERS & PROFILES (1 Admin, 5 Instructors, 30 Students)
        # ---------------------------------------------------------
        print("-> Seeding 36 Users & User Profiles...")
        # Admin
        admin = User(
            username='admin',
            email='admin@lms.local',
            role_id=role_objs['admin'].id,
            is_active=True
        )
        admin.set_password('AdminPass123!')
        db.session.add(admin)
        db.session.flush()
        db.session.add(UserProfile(user_id=admin.id, full_name='System Administrator', country='United States', bio='Master Administrator of LearnHub LMS.'))

        # 5 Instructors
        instructor_names = ['Dr. Sarah Connor', 'Prof. Alan Turing', 'Dr. Grace Hopper', 'Prof. Richard Feynman', 'Dr. Ada Lovelace']
        instructors = []
        for i, name in enumerate(instructor_names, 1):
            inst = User(
                username=f'instructor{i}',
                email=f'instructor{i}@lms.local',
                role_id=role_objs['instructor'].id,
                is_active=True
            )
            inst.set_password('InstructorPass123!')
            db.session.add(inst)
            db.session.flush()
            db.session.add(UserProfile(user_id=inst.id, full_name=name, country='United Kingdom', bio=f'Expert lecturer specializing in modern computer science and engineering.'))
            instructors.append(inst)

        # 30 Students
        students = []
        for i in range(1, 31):
            stu = User(
                username=f'student{i}',
                email=f'student{i}@lms.local',
                role_id=role_objs['student'].id,
                is_active=True
            )
            stu.set_password('StudentPass123!')
            db.session.add(stu)
            db.session.flush()
            db.session.add(UserProfile(
                user_id=stu.id,
                full_name=fake.name(),
                phone=fake.phone_number()[:25],
                country=fake.country()[:75],
                bio=fake.sentence(nb_words=12)
            ))
            students.append(stu)

        # User zee (current user account)
        zee_user = User(
            username='zee',
            email='rh3783901@gmail.com',
            role_id=role_objs['student'].id,
            is_active=True
        )
        zee_user.set_password('StudentPass123!')
        db.session.add(zee_user)
        db.session.flush()
        db.session.add(UserProfile(
            user_id=zee_user.id,
            full_name='Zeeshan Student',
            country='Pakistan',
            bio='Software engineer & active student learner.'
        ))
        students.append(zee_user)

        db.session.flush()

        # ---------------------------------------------------------
        # 3. DEPARTMENTS & CATEGORIES & TAGS (Catalog taxonomy: 3 models)
        # ---------------------------------------------------------
        print("-> Seeding Departments, Categories, and Tags...")
        dept_names = [
            'Computer Science',
            'Software Engineering',
            'Data Science & AI',
            'Cybersecurity',
            'Information Systems',
            'Design & Multimedia'
        ]
        dept_objs = []
        for dname in dept_names:
            dept = Department(name=dname, description=f"Academic curriculum of {dname}")
            db.session.add(dept)
            dept_objs.append(dept)
        db.session.flush()

        cat_data = [
            ('AI & Machine Learning Engineer Roadmap', 'ai-engineer-roadmap', None),
            ('Full-Stack Web Developer Roadmap', 'full-stack-web-roadmap', None),
            ('Cloud & DevOps Engineer Roadmap', 'cloud-devops-roadmap', None),
            ('Cybersecurity Specialist Roadmap', 'cybersecurity-roadmap', None),
            ('Data Engineering & Systems Roadmap', 'data-engineering-roadmap', None),
            ('Computer Science Foundations Roadmap', 'cs-foundations-roadmap', None)
        ]
        cat_map = {}
        for name, slug, parent_name in cat_data:
            parent_id = cat_map[parent_name].id if parent_name and parent_name in cat_map else None
            cat = Category(name=name, slug=slug, parent_id=parent_id)
            db.session.add(cat)
            db.session.flush()
            cat_map[name] = cat

        tags_list = ['python', 'ai-ml', 'deep-learning', 'llm', 'flask', 'javascript', 'react', 'docker', 'kubernetes', 'sql', 'security', 'api', 'algorithms']
        tag_objs = []
        for tname in tags_list:
            tag = Tag(name=tname)
            db.session.add(tag)
            tag_objs.append(tag)
        db.session.flush()

        # ---------------------------------------------------------
        # 4. COURSES (15 courses with modules, lessons, resources)
        # ---------------------------------------------------------
        print("-> Seeding Courses in Beginner-to-Advanced Career Roadmaps with Topic-by-Topic Videos...")

        # Full 6-Chapter, 12-Topic Video Curricula for all 19 courses
        from expand_curriculum import EXPANDED_CURRICULA as yt_curriculums

        # Courses organized strictly from Beginner to Advanced in each Career Roadmap Category
        courses_data = [
            # 1. AI & Machine Learning Engineer Roadmap (4 sequential courses)
            ("Python for AI & Data Science Foundations", 0.0, "Beginner", "Foundational Python programming, vectorized mathematics with NumPy, and exploratory data analysis with Pandas for AI engineering.", dept_objs[2], cat_map['AI & Machine Learning Engineer Roadmap']),
            ("Practical Machine Learning with Scikit-Learn", 49.99, "Intermediate", "Supervised learning, regression, classification, Random Forests, model evaluation metrics, and hyperparameter tuning.", dept_objs[2], cat_map['AI & Machine Learning Engineer Roadmap']),
            ("Deep Learning & Neural Networks with PyTorch", 69.99, "Advanced", "Deep artificial neural networks, backpropagation calculus, CNNs for computer vision, and transformer attention mechanisms.", dept_objs[2], cat_map['AI & Machine Learning Engineer Roadmap']),
            ("Generative AI, LLMs & LangChain Engineering", 79.99, "Advanced", "Large language model architectures, prompt engineering, Retrieval-Augmented Generation (RAG) with vector databases, and autonomous AI agents.", dept_objs[2], cat_map['AI & Machine Learning Engineer Roadmap']),

            # 2. Full-Stack Web Developer Roadmap (3 sequential courses)
            ("Frontend Engineering with Modern JavaScript", 0.0, "Beginner", "Modern ES6+ syntax, DOM manipulation, asynchronous Promises, the browser event loop, and web API integration.", dept_objs[1], cat_map['Full-Stack Web Developer Roadmap']),
            ("Modern Web Engineering with Flask", 49.99, "Intermediate", "Master Flask 3.x, Jinja2 inheritance, Flask-WTF validation, SQLAlchemy relational modeling, and enterprise session authentication.", dept_objs[1], cat_map['Full-Stack Web Developer Roadmap']),
            ("Full-Stack React 18 and Flask Integration", 59.99, "Advanced", "Building reactive single-page frontends with React 18 hooks, connecting to Flask REST APIs, and stateless JWT authentication.", dept_objs[1], cat_map['Full-Stack Web Developer Roadmap']),

            # 3. Cloud & DevOps Engineer Roadmap (3 sequential courses)
            ("Enterprise Linux Server Administration", 0.0, "Beginner", "Linux terminal mastery, bash shell scripting, POSIX user/group permissions, systemd daemons, and SSH security hardening.", dept_objs[0], cat_map['Cloud & DevOps Engineer Roadmap']),
            ("DevOps CI/CD Pipelines with Docker & GitHub Actions", 44.99, "Intermediate", "Containerization with Docker, multi-container Docker Compose, automated testing with Pytest, and GitHub Actions CI/CD workflows.", dept_objs[1], cat_map['Cloud & DevOps Engineer Roadmap']),
            ("Cloud-Native Kubernetes Operations & AWS", 64.99, "Advanced", "AWS core cloud architecture, VPC networking, Kubernetes pods, replica sets, declarative YAML manifests, and ingress controllers.", dept_objs[4], cat_map['Cloud & DevOps Engineer Roadmap']),

            # 4. Cybersecurity Specialist Roadmap (3 sequential courses)
            ("Computer Networking & Security Fundamentals", 0.0, "Beginner", "TCP/IP protocol suites, IP subnetting, Wireshark packet inspection, three-way handshakes, and DNS infrastructure.", dept_objs[3], cat_map['Cybersecurity Specialist Roadmap']),
            ("Applied Cybersecurity & Ethical Hacking", 49.99, "Intermediate", "Network penetration testing, port scanning with Nmap, OWASP Top 10 web vulnerabilities, SQL injection, and XSS defense.", dept_objs[3], cat_map['Cybersecurity Specialist Roadmap']),
            ("Advanced Penetration Testing & Cryptography", 69.99, "Advanced", "Symmetric and asymmetric encryption (AES, RSA), password hashing algorithms, digital signatures, and Kali Linux exploitation.", dept_objs[3], cat_map['Cybersecurity Specialist Roadmap']),

            # 5. Data Engineering & Systems Roadmap (3 sequential courses)
            ("Relational Database Design & SQL", 0.0, "Beginner", "Comprehensive relational modeling, SQL CRUD queries, multi-table joins, database normalization (1NF-3NF), and B-Tree indexing.", dept_objs[4], cat_map['Data Engineering & Systems Roadmap']),
            ("RESTful API Development with Python & OpenAPI", 39.99, "Intermediate", "Building production-grade web APIs with Flask, Marshmallow serialization, rate limiting, and interactive OpenAPI Swagger UI.", dept_objs[1], cat_map['Data Engineering & Systems Roadmap']),
            ("Advanced System Architecture & Distributed Systems", 79.99, "Advanced", "Scalable systems design, Redis in-memory caching, message queues with Apache Kafka, and microservices data consistency.", dept_objs[0], cat_map['Data Engineering & Systems Roadmap']),

            # 6. Computer Science Foundations Roadmap (3 sequential courses)
            ("Introduction to Computer Science", 0.0, "Beginner", "Harvard CS50 computational thinking, binary logic, C programming, memory allocation, and algorithmic problem solving.", dept_objs[0], cat_map['Computer Science Foundations Roadmap']),
            ("Data Structures & Algorithms in Python", 39.99, "Intermediate", "Big-O asymptotic complexity, two-pointer arrays, linked lists, stacks, queues, and binary search tree traversals.", dept_objs[0], cat_map['Computer Science Foundations Roadmap']),
            ("UI/UX Design Systems and Figma Prototyping", 34.99, "Advanced", "Visual hierarchy, typography, accessible contrast, Figma auto-layout, design tokens, and interactive clickable prototypes.", dept_objs[5], cat_map['Computer Science Foundations Roadmap'])
        ]

        course_objs = []
        for idx, (title, price, level, desc, dept, cat) in enumerate(courses_data):
            inst = instructors[idx % len(instructors)]
            slug = slugify(title)
            course = Course(
                title=title,
                slug=slug,
                description=desc,
                price=price,
                level=level,
                status='published',
                department_id=dept.id,
                category_id=cat.id,
                created_by=inst.id,
                is_active=True
            )
            db.session.add(course)
            db.session.flush()

            # Lead instructor
            db.session.add(CourseInstructor(course_id=course.id, user_id=inst.id, is_lead=True))

            # Tags
            db.session.add(CourseTag(course_id=course.id, tag_id=tag_objs[idx % len(tag_objs)].id))
            db.session.add(CourseTag(course_id=course.id, tag_id=tag_objs[(idx + 1) % len(tag_objs)].id))

            # Populate Modules & Real YouTube Lessons
            modules_data = yt_curriculums.get(title)
            if modules_data:
                for m_pos, (mod_title, lessons_list) in enumerate(modules_data, 1):
                    mod = Module(course_id=course.id, title=mod_title, position=m_pos)
                    db.session.add(mod)
                    db.session.flush()

                    for l_pos, (les_title, les_content, duration, res_url) in enumerate(lessons_list, 1):
                        lesson = Lesson(
                            module_id=mod.id,
                            title=les_title,
                            content=les_content,
                            content_type='video_url',
                            duration_min=duration,
                            position=l_pos
                        )
                        db.session.add(lesson)
                        db.session.flush()

                        res = LessonResource(
                            lesson_id=lesson.id,
                            title=f"Documentation & Reference: {les_title}",
                            resource_type='link',
                            url_or_path=res_url
                        )
                        db.session.add(res)
            else:
                # Fallback generator if needed
                for m_pos in range(1, 4):
                    mod = Module(course_id=course.id, title=f"Module {m_pos}: Core Foundations & Practice", position=m_pos)
                    db.session.add(mod)
                    db.session.flush()

                    for l_pos in range(1, 3):
                        lesson = Lesson(
                            module_id=mod.id,
                            title=f"Lesson {m_pos}.{l_pos}: Video Lecture & Technical Guide",
                            content="https://www.youtube.com/watch?v=k1RI5locZE4\n\nTechnical video lecture covering architectural principles, implementations, and best practices.",
                            content_type='video_url',
                            duration_min=30,
                            position=l_pos
                        )
                        db.session.add(lesson)
                        db.session.flush()

                        res = LessonResource(
                            lesson_id=lesson.id,
                            title="Lesson Resource & Code References",
                            resource_type='link',
                            url_or_path="https://github.com/"
                        )
                        db.session.add(res)

            # Announcements
            ann = Announcement(
                course_id=course.id,
                author_id=inst.id,
                title=f"Welcome to {course.title}!",
                body="Welcome students! Please review the syllabus, check due dates for quizzes, and ask questions in the discussion forum."
            )
            db.session.add(ann)

            course_objs.append(course)

        db.session.flush()

        # Wire Sequential Roadmap Prerequisites (Stage N requires Stage N-1 in each category)
        print("-> Wiring Sequential Roadmap Prerequisites (Beginner -> Intermediate -> Advanced)...")
        for cat in cat_map.values():
            cat_courses = cat.roadmap_courses
            for i in range(1, len(cat_courses)):
                prereq_course = cat_courses[i - 1]
                target_course = cat_courses[i]
                db.session.add(CoursePrerequisite(course_id=target_course.id, prerequisite_id=prereq_course.id))
        db.session.flush()

        # ---------------------------------------------------------
        # 5. RUBRICS & ASSESSMENTS (Quizzes, Questions, Assignments)
        # ---------------------------------------------------------
        print("-> Seeding Rubrics, Assignments, Quizzes & Questions...")
        rubric = Rubric(title="Standard Engineering Project Rubric", created_by=instructors[0].id)
        db.session.add(rubric)
        db.session.flush()

        crit1 = RubricCriterion(rubric_id=rubric.id, description="Architecture & Clean Code Structure", max_points=40.0)
        crit2 = RubricCriterion(rubric_id=rubric.id, description="Functional Requirements & Validation", max_points=40.0)
        crit3 = RubricCriterion(rubric_id=rubric.id, description="Documentation & Test Coverage", max_points=20.0)
        db.session.add_all([crit1, crit2, crit3])
        db.session.flush()

        for c_idx, course in enumerate(course_objs):
            # 1 Quiz per course
            quiz = Quiz(
                course_id=course.id,
                title=f"{course.title} - Midterm Assessment",
                time_limit_min=15,
                max_attempts=3,
                pass_mark=70.0
            )
            db.session.add(quiz)
            db.session.flush()

            # 2 Questions per quiz
            q1 = Question(
                quiz_id=quiz.id,
                text="Which pattern prevents duplicate form submissions upon browser refresh?",
                question_type='single_choice',
                points=10.0,
                position=1
            )
            db.session.add(q1)
            db.session.flush()
            db.session.add(QuestionOption(question_id=q1.id, text="Post/Redirect/Get (PRG) Pattern", is_correct=True))
            db.session.add(QuestionOption(question_id=q1.id, text="Direct Server Rendering Pattern", is_correct=False))
            db.session.add(QuestionOption(question_id=q1.id, text="AJAX polling without cookies", is_correct=False))

            q2 = Question(
                quiz_id=quiz.id,
                text="SQLAlchemy 2.0 requires declarative models or mapped classes for ORM mapping.",
                question_type='true_false',
                points=10.0,
                position=2
            )
            db.session.add(q2)
            db.session.flush()
            db.session.add(QuestionOption(question_id=q2.id, text="True", is_correct=True))
            db.session.add(QuestionOption(question_id=q2.id, text="False", is_correct=False))

            # 1 Assignment per course
            assign = Assignment(
                course_id=course.id,
                title=f"{course.title} - Capstone Submission",
                instructions="Build and submit your complete implementation repository link and brief architecture documentation.",
                due_date=datetime.now(timezone.utc) + timedelta(days=14),
                max_points=100.0,
                rubric_id=rubric.id
            )
            db.session.add(assign)

        db.session.flush()

        # ---------------------------------------------------------
        # 6. ENROLLMENTS & LESSON PROGRESS & CERTIFICATES (Recognition)
        # ---------------------------------------------------------
        print("-> Seeding Student Enrollments, Grades & Certificates...")
        now_dt = datetime.now(timezone.utc)

        # Enroll student1 into courses 0, 1, 2
        # Course 0 is 100% completed so student1 has certificate!
        e0 = Enrollment(user_id=students[0].id, course_id=course_objs[0].id, status='completed', progress_pct=100.0, enrolled_at=now_dt - timedelta(days=20), completed_at=now_dt - timedelta(days=5))
        db.session.add(e0)
        db.session.flush()

        # Mark all lessons completed for course 0
        for m in course_objs[0].modules:
            for l in m.lessons:
                db.session.add(LessonProgress(enrollment_id=e0.id, lesson_id=l.id, is_completed=True, completed_at=now_dt - timedelta(days=6)))

        # Certificate for student 1
        cert = Certificate(enrollment_id=e0.id, code="CERT-E39A7B1C8800", issued_at=now_dt - timedelta(days=5))
        db.session.add(cert)

        # Final grade for course 0
        db.session.add(Grade(enrollment_id=e0.id, graded_by=instructors[0].id, score=98.0, feedback="Exceptional work across all modules and tests.", grade_type='final'))

        # Enroll ALL students (including student1..30 and zee) in courses
        for stu in students:
            for c in course_objs:
                existing = Enrollment.query.filter_by(user_id=stu.id, course_id=c.id).first()
                if not existing:
                    enroll = Enrollment(
                        user_id=stu.id,
                        course_id=c.id,
                        status='active',
                        progress_pct=33.3,
                        enrolled_at=now_dt - timedelta(days=2)
                    )
                    db.session.add(enroll)

        db.session.flush()

        # Student 1 quiz attempt
        q_target = course_objs[0].quizzes[0]
        q_attempt = QuizAttempt(quiz_id=q_target.id, user_id=students[0].id, started_at=now_dt - timedelta(days=6), submitted_at=now_dt - timedelta(days=6), score=100.0, passed=True)
        db.session.add(q_attempt)
        db.session.flush()

        for q in q_target.questions:
            correct_opt = next((opt for opt in q.options if opt.is_correct), None)
            db.session.add(AttemptAnswer(
                attempt_id=q_attempt.id,
                question_id=q.id,
                option_id=correct_opt.id if correct_opt else None,
                is_correct=True
            ))

        # Student 1 assignment submission & grade
        target_assign = course_objs[0].assignments[0]
        subm = Submission(
            assignment_id=target_assign.id,
            user_id=students[0].id,
            text="GitHub Repository: https://github.com/example/flask-capstone\nImplemented full schema, PRG forms, and tests.",
            submitted_at=now_dt - timedelta(days=7),
            is_late=False,
            status='graded'
        )
        db.session.add(subm)
        db.session.flush()

        db.session.add(Grade(
            submission_id=subm.id,
            enrollment_id=e0.id,
            graded_by=instructors[0].id,
            score=95.0,
            feedback="Clean blueprint layout, proper CSRF tokens, and great coverage.",
            grade_type='assignment'
        ))

        # ---------------------------------------------------------
        # 7. BADGES & USER BADGES
        # ---------------------------------------------------------
        print("-> Seeding Gamification Badges...")
        badge_data = [
            ("Pioneer Scholar", "Completed your very first course on LearnHub!", "bi-award", "first_course"),
            ("Quiz Prodigy", "Scored 100% on a course midterm or final quiz!", "bi-star-fill", "perfect_quiz"),
            ("Knowledge Seeker", "Completed 3 or more courses successfully!", "bi-mortarboard", "course_master"),
            ("Top Contributor", "Active participant in community forum discussions!", "bi-chat-heart", "community_star")
        ]
        badge_objs = []
        for name, desc, icon, code in badge_data:
            badge = Badge(name=name, description=desc, icon=icon, rule_code=code)
            db.session.add(badge)
            badge_objs.append(badge)
        db.session.flush()

        db.session.add(UserBadge(user_id=students[0].id, badge_id=badge_objs[0].id, awarded_at=now_dt - timedelta(days=5)))
        db.session.add(UserBadge(user_id=students[0].id, badge_id=badge_objs[1].id, awarded_at=now_dt - timedelta(days=6)))

        # ---------------------------------------------------------
        # 8. COMMUNITY (Forum Threads, Posts, Likes, Messages, Notifications)
        # ---------------------------------------------------------
        print("-> Seeding Community Discussions, Direct Messages, and Notifications...")
        thread = ForumThread(
            course_id=course_objs[1].id,
            author_id=instructors[1].id,
            title="General Questions & Discussion for Week 1",
            is_pinned=True,
            is_locked=False
        )
        db.session.add(thread)
        db.session.flush()

        p1 = ForumPost(thread_id=thread.id, author_id=instructors[1].id, body="Feel free to post questions regarding blueprint routing and application factories here!")
        db.session.add(p1)
        db.session.flush()

        p2 = ForumPost(thread_id=thread.id, author_id=students[0].id, parent_post_id=p1.id, body="Thanks Professor! The factory pattern makes testing with in-memory SQLite very clean.")
        db.session.add(p2)
        db.session.flush()

        # Like
        db.session.add(PostLike(post_id=p2.id, user_id=instructors[1].id))

        # Direct messages
        db.session.add(Message(
            sender_id=students[0].id,
            recipient_id=instructors[0].id,
            subject="Question regarding Capstone Rubric",
            body="Hello Professor, could you clarify the requirements for the automated testing rubric criterion?",
            is_read=True
        ))
        db.session.add(Message(
            sender_id=instructors[0].id,
            recipient_id=students[0].id,
            subject="Re: Question regarding Capstone Rubric",
            body="Hi Student! Simply provide pytest test suites covering your service logic and blueprint routes.",
            is_read=False
        ))

        # Notifications
        db.session.add(Notification(
            user_id=students[0].id,
            title="Certificate Issued! 🎓",
            message="Congratulations! You have completed 'Introduction to Computer Science' and earned your certificate.",
            link=f"/learn/certificate/{cert.code}",
            is_read=True
        ))
        db.session.add(Notification(
            user_id=students[0].id,
            title="New Direct Message",
            message="You received a reply from Prof. Alan Turing.",
            link="/community/inbox",
            is_read=False
        ))

        # Reviews
        db.session.add(Review(
            user_id=students[0].id,
            course_id=course_objs[0].id,
            rating=5,
            comment="Outstanding course! Clear lectures, well-structured modules, and prompt feedback."
        ))
        db.session.add(Review(
            user_id=students[1].id,
            course_id=course_objs[0].id,
            rating=5,
            comment="The hands-on coding exercises really solidified my understanding of algorithms."
        ))

        # Wishlist
        db.session.add(Wishlist(user_id=students[0].id, course_id=course_objs[5].id))

        # ---------------------------------------------------------
        # 9. COMMERCE (Coupons, Orders, OrderItems, Payments)
        # ---------------------------------------------------------
        print("-> Seeding Commerce Orders, Simulated Payments, and Promo Coupons...")
        coupon1 = Coupon(code="WELCOME20", discount_percent=20, valid_from=now_dt - timedelta(days=30), valid_to=now_dt + timedelta(days=90), usage_limit=500, times_used=12)
        coupon2 = Coupon(code="STUDENT50", discount_percent=50, valid_from=now_dt - timedelta(days=10), valid_to=now_dt + timedelta(days=60), usage_limit=100, times_used=4)
        coupon3 = Coupon(code="FLASHSALE", discount_percent=15, valid_from=now_dt - timedelta(days=5), valid_to=now_dt + timedelta(days=15), usage_limit=250, times_used=8)
        db.session.add_all([coupon1, coupon2, coupon3])
        db.session.flush()

        order = Order(
            user_id=students[0].id,
            coupon_id=coupon1.id,
            subtotal=49.99,
            discount=10.00,
            total=39.99,
            status='paid',
            created_at=now_dt - timedelta(days=12)
        )
        db.session.add(order)
        db.session.flush()

        db.session.add(OrderItem(order_id=order.id, course_id=course_objs[1].id, price_at_purchase=49.99))
        db.session.add(Payment(
            order_id=order.id,
            method='simulated_card',
            transaction_ref='SIM-TXN-884A2C7B',
            amount=39.99,
            status='completed',
            paid_at=now_dt - timedelta(days=12)
        ))

        # ---------------------------------------------------------
        # 10. ADMIN & SETTINGS & AUDIT LOGS (Admin domain: 2 models)
        # ---------------------------------------------------------
        print("-> Seeding System Settings and Security Audit Logs...")
        settings_data = [
            ('site_name', 'LearnHub LMS', 'The official platform portal title'),
            ('contact_email', 'support@learnhub.local', 'Primary administrator contact email'),
            ('allow_registration', 'true', 'Whether public user self-registration is enabled'),
            ('default_pass_mark', '70', 'Standard passing threshold percentage for quizzes'),
            ('maintenance_mode', 'false', 'Platform maintenance toggle')
        ]
        for key, val, desc in settings_data:
            db.session.add(Setting(key=key, value=val, description=desc))

        audit_entries = [
            (admin.id, 'seed_database', 'System', 1, 'Initial database migration and schema provisioning complete.'),
            (admin.id, 'login', 'User', admin.id, 'Admin authenticated via web portal.'),
            (instructors[0].id, 'create', 'Course', course_objs[0].id, "Created course 'Introduction to Computer Science'."),
            (instructors[0].id, 'publish', 'Course', course_objs[0].id, "Published course 'Introduction to Computer Science'."),
            (students[0].id, 'enroll', 'Course', course_objs[0].id, "Enrolled in course 'Introduction to Computer Science'."),
            (students[0].id, 'checkout', 'Order', order.id, "Completed simulated order #1 for $39.99.")
        ]
        for uid, act, etype, eid, detail in audit_entries:
            db.session.add(AuditLog(
                user_id=uid,
                action=act,
                entity_type=etype,
                entity_id=eid,
                details=detail,
                ip_address='127.0.0.1',
                created_at=now_dt - timedelta(days=2)
            ))

        db.session.commit()
        print("\n=======================================================")
        print("DATABASE SEEDING COMPLETED SUCCESSFULLY!")
        print("Total Models Populated: Exactly 44 Models.")
        print("Accounts Created:")
        print("  - Admin:       admin / AdminPass123!")
        print("  - Instructors: instructor1 .. instructor5 / InstructorPass123!")
        print("  - Students:    student1 .. student30 / StudentPass123!")
        print("=======================================================\n")

if __name__ == '__main__':
    run_seed()
