from app.models.users import Role, Permission, RolePermission, User, UserProfile, Notification
from app.models.catalog import Department, Category, Course, CoursePrerequisite, Tag, CourseTag, Roadmap, RoadmapStage
from app.models.content import CourseInstructor, Module, Lesson, LessonResource, Announcement, Enrollment, LessonProgress, Wishlist
from app.models.assessments import Quiz, Question, QuestionOption, QuizAttempt, AttemptAnswer, Rubric, RubricCriterion, Assignment, Submission, Grade
from app.models.community import ForumThread, ForumPost, PostLike, Message
from app.models.recognition import Certificate, Badge, UserBadge, Review
from app.models.commerce import Coupon, Order, OrderItem, Payment
from app.models.admin import AuditLog, Setting

__all__ = [
    # Users & Access (6)
    'Role',
    'Permission',
    'RolePermission',
    'User',
    'UserProfile',
    'Notification',
    # Catalog (6)
    'Department',
    'Category',
    'Course',
    'CoursePrerequisite',
    'Tag',
    'CourseTag',
    # Content & Learning (8)
    'CourseInstructor',
    'Module',
    'Lesson',
    'LessonResource',
    'Announcement',
    'Enrollment',
    'LessonProgress',
    'Wishlist',
    # Assessments (10)
    'Quiz',
    'Question',
    'QuestionOption',
    'QuizAttempt',
    'AttemptAnswer',
    'Rubric',
    'RubricCriterion',
    'Assignment',
    'Submission',
    'Grade',
    # Community (4)
    'ForumThread',
    'ForumPost',
    'PostLike',
    'Message',
    # Recognition (4)
    'Certificate',
    'Badge',
    'UserBadge',
    'Review',
    # Commerce (4)
    'Coupon',
    'Order',
    'OrderItem',
    'Payment',
    # Admin (2)
    'AuditLog',
    'Setting',
]
