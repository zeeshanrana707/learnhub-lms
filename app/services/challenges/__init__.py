"""
Course-specific challenge dispatcher.
Maps course_id -> CHALLENGES dict (keyed by (module_pos, lesson_pos)).
Courses without a dedicated file fall back to keyword matching in programming_challenges.py.
"""

from app.services.challenges import c01, c02, c03, c04, c05, c06
from app.services.challenges.extra_challenges import EXTRA_CHALLENGES

COURSE_CHALLENGES = {
    1: c01.CHALLENGES,
    2: c02.CHALLENGES,
    3: c03.CHALLENGES,
    4: c04.CHALLENGES,
    5: c05.CHALLENGES,
    6: c06.CHALLENGES,
}

# Additional courses are added here as their files are created:
# 7: c07.CHALLENGES,  # Full-Stack React 18 & Flask
# 8: c08.CHALLENGES,  # Enterprise Linux Server Administration
# ...
