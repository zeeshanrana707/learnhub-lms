import sys
sys.path.insert(0, r"c:\Users\Zeeshan\Desktop\rana")

from app import create_app
from app.extensions import db
from app.models.content import Module, Lesson, LessonProgress, LessonResource
from app.models.catalog import Course

app = create_app('development')
with app.app_context():
    # Old legacy modules were created prior to expansion (id <= 54)
    old_modules = Module.query.filter(Module.id <= 54).all()
    print(f"Found {len(old_modules)} old legacy modules to clean up.")
    
    for mod in old_modules:
        for les in mod.lessons:
            # Delete progresses and resources
            LessonProgress.query.filter_by(lesson_id=les.id).delete()
            LessonResource.query.filter_by(lesson_id=les.id).delete()
            db.session.delete(les)
        db.session.delete(mod)

    db.session.commit()
    print("Old legacy modules cleaned up successfully.")

    # Re-sequence positions for all remaining modules (1..6)
    courses = Course.query.order_by(Course.id).all()
    for c in courses:
        for idx, m in enumerate(c.modules, start=1):
            m.position = idx
            for lidx, l in enumerate(m.lessons, start=1):
                l.position = lidx
    db.session.commit()

    print("\nVerification of all 19 courses:")
    for c in courses:
        print(f"Course #{c.id:2d}: '{c.title[:35]}' -> {len(c.modules)} Chapters, {len([l for m in c.modules for l in m.lessons])} Topic Videos")
