# LearnHub - Enterprise Learning Management System (LMS)

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-black.svg)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-44%20Models-red.svg)](https://www.sqlalchemy.org/)
[![Tests](https://img.shields.io/badge/Tests-10%20Passed-brightgreen.svg)]()

> **Course:** Web Engineering (CSE601330) — Flask Weeks 5-8 Project  
> **Schema Scope:** Exactly **44 SQLAlchemy models** across 8 distinct business domains  
> **Design Patterns:** Application Factory, Blueprints, PRG (Post/Redirect/Get), RBAC, Service Layer

---

## 1. Project Purpose & Overview

**LearnHub** is an end-to-end web-based Learning Management System where:
- **Instructors** build structured curriculums (Courses > Modules > Lessons > Resources), author quizzes and assignments with rubrics, grade submissions, post announcements, and moderate course discussions.
- **Students** browse the catalog, verify prerequisites, enroll in free courses or purchase paid courses via simulated sandbox payments, complete interactive lessons, track progress, take timed auto-graded quizzes, submit assignments, earn verifiable certificates and badges, and message peers and instructors.
- **Administrators** control user accounts, configure Role-Based Access Control (RBAC), curate departments, categories, and tags, manage promo coupons, customize system settings, and inspect security audit logs.

---

## 2. Key Features

- **Strict RBAC & Security:** Role (`admin`, `instructor`, `student`) and permission checking via `@role_required` and ownership decorators; passwords hashed using Werkzeug; full CSRF protection using Flask-WTF.
- **Server-Side Validation & PRG:** Every create, update, and delete operation uses POST with strict WTForms server-side validation, redirecting upon success to eliminate duplicate form submissions.
- **Progress & Gamification Engine:** Dynamic percentage tracking (`completed_lessons / total_lessons * 100`), automatic issuance of unique certificates (`CERT-XXXX`), and automated rule-based badge awards.
- **Simulated E-Commerce:** Session-backed cart, discount coupon validation engine, simulated payment transactions, and automatic course enrollment.
- **Full Community Platform:** Threaded course forums with nested replies and post likes, user-to-user direct messages, and system notifications.
- **Auditing & Traceability:** Immutable audit trail logging user actions, affected entities, IP addresses, and timestamps.

---

## 3. Database Schema: 44 SQLAlchemy Models

The database strictly meets the 44-model specification divided across 8 domains:

```
├── Domain 1: Users & Access (6 Models)
│   ├── User, Role, Permission, RolePermission, UserProfile, Notification
├── Domain 2: Catalog Taxonomy (6 Models)
│   ├── Department, Category, Course, CoursePrerequisite, Tag, CourseTag
├── Domain 3: Content & Learning (8 Models)
│   ├── CourseInstructor, Module, Lesson, LessonResource, Announcement,
│   └── Enrollment, LessonProgress, Wishlist
├── Domain 4: Assessments & Grading (10 Models)
│   ├── Quiz, Question, QuestionOption, QuizAttempt, AttemptAnswer,
│   └── Rubric, RubricCriterion, Assignment, Submission, Grade
├── Domain 5: Community & Messaging (4 Models)
│   ├── ForumThread, ForumPost, PostLike, Message
├── Domain 6: Recognition & Feedback (4 Models)
│   ├── Certificate, Badge, UserBadge, Review
├── Domain 7: Commerce & Billing (4 Models)
│   ├── Order, OrderItem, Payment, Coupon
└── Domain 8: Platform Administration (2 Models)
    └── AuditLog, Setting
```

---

## 4. Quick Start & Setup

### 4.1 Clone and Environment Setup
```bash
# 1. Clone repository or navigate to workspace
cd rana

# 2. (Optional) Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate       # On Windows
# source venv/bin/activate  # On macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt
```

### 4.2 Configuration (.env)
Copy the example environment configuration:
```bash
cp .env.example .env
```
Default `.env` contents:
```ini
SECRET_KEY=super-secret-lms-key-change-in-production
FLASK_ENV=development
FLASK_APP=run.py
DATABASE_URL=sqlite:///lms.db
UPLOAD_FOLDER=app/static/uploads
```

### 4.3 Database Migration & Seeding
Run the seed script to create all 44 tables and populate them with realistic sample data:
```bash
python seed.py
```

### 4.4 Running the Application
```bash
python run.py
# or
flask run --port=5000
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 5. Demo Accounts

The database comes pre-seeded with ready-to-test accounts across all three personas:

| Role | Username | Email | Password | Permissions & Scope |
|---|---|---|---|---|
| **Admin** | `admin` | `admin@lms.local` | `AdminPass123!` | Full control center, user toggles, audit logs, taxonomy |
| **Instructor** | `instructor1` | `instructor1@lms.local` | `InstructorPass123!` | Course author, curriculum editor, grading queue |
| **Instructor** | `instructor2` | `instructor2@lms.local` | `InstructorPass123!` | Course author, curriculum editor, grading queue |
| **Student** | `student1` | `student1@lms.local` | `StudentPass123!` | Active student (has 100% course, certificate & badges) |
| **Student** | `student2` | `student2@lms.local` | `StudentPass123!` | Active student in progress |

*Note: Students 1 through 30 are pre-seeded with the password `StudentPass123!`.*

---

## 6. Demo Promo Coupons

During checkout, test the simulated coupon discounts:
- `WELCOME20` (20% off)
- `STUDENT50` (50% off)
- `FLASHSALE` (15% off)

---

## 7. Automated Testing

Run the automated test suite with pytest:
```bash
python -m pytest
```
Tests verify:
- Unit tests for services: lesson progress calculations, quiz auto-grading, rubric grading, cart breakdown, coupon validation, and simulated checkout.
- Integration tests for flows: registration, authentication, role-based redirects, RBAC access denials (403), course enrollment, and PRG patterns.

---

## 8. Project Structure

```
rana/
├── app/
│   ├── __init__.py           # Application Factory (create_app, SQLite PRAGMA, blueprints)
│   ├── extensions.py         # SQLAlchemy, Migrate, LoginManager, CSRFProtect
│   ├── models/               # 44 SQLAlchemy Models split by domain
│   │   ├── users.py          # User, Role, Permission, RolePermission, UserProfile, Notification
│   │   ├── catalog.py        # Department, Category, Course, CoursePrerequisite, Tag, CourseTag
│   │   ├── content.py        # CourseInstructor, Module, Lesson, LessonResource, Announcement, Enrollment, LessonProgress, Wishlist
│   │   ├── assessments.py    # Quiz, Question, QuestionOption, QuizAttempt, AttemptAnswer, Rubric, RubricCriterion, Assignment, Submission, Grade
│   │   ├── community.py      # ForumThread, ForumPost, PostLike, Message
│   │   ├── recognition.py    # Certificate, Badge, UserBadge, Review
│   │   ├── commerce.py       # Coupon, Order, OrderItem, Payment
│   │   └── admin.py          # AuditLog, Setting
│   ├── forms/                # WTForms with server-side validation per blueprint
│   ├── services/             # Pure business logic (progress, grading, certificates, orders)
│   ├── blueprints/           # 7 Blueprints: auth, catalog, learning, assessments, community, commerce, admin
│   ├── templates/            # Jinja2 templates (base.html, partials, errors, view folders)
│   ├── static/               # CSS, JS, and file uploads
│   └── utils/                # Decorators (role_required, ownership) and helpers (log_action)
├── tests/                    # Pytest conftest, test_services.py, test_flows.py
├── migrations/               # Alembic database migrations
├── seed.py                   # One-command seed script
├── config.py                 # Environment configurations
├── run.py                    # Entry point executable
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # Project documentation
```
