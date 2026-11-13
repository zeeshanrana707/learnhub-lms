"""
LearnHub Official Lecture Notes PDF Generator
Generates clean, professional PDF documentation for lessons using PyMuPDF.
"""

import pymupdf
import re

def generate_lesson_notes_pdf(lesson) -> bytes:
    course = lesson.module.course
    course_title = course.title or "Course Curriculum"
    lesson_title = lesson.title or "Lecture Notes"
    module_title = lesson.module.title or "Module"
    instructor = course.instructor_name or "LearnHub Faculty"
    duration = getattr(lesson, 'formatted_duration', f"{lesson.duration_min} mins")
    breakdown = lesson.breakdown or {}

    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842) # Standard A4 page
    
    # 1. Header Banner
    header_rect = pymupdf.Rect(0, 0, 595, 75)
    page.draw_rect(header_rect, color=None, fill=(0.04, 0.11, 0.19)) # #0b1c30 deep navy
    
    # Header Accent Blue Line
    page.draw_line(pymupdf.Point(0, 75), pymupdf.Point(595, 75), color=(0.14, 0.39, 0.92), width=3) # primary blue
    
    # Header Text
    page.insert_text(pymupdf.Point(40, 32), "LEARNHUB ACADEMY  •  OFFICIAL LECTURE NOTES & CURRICULUM", fontsize=9, color=(0.7, 0.8, 1.0), fontname="helv")
    page.insert_text(pymupdf.Point(40, 54), course_title[:65], fontsize=13, color=(1, 1, 1), fontname="hebo")
    
    y = 100
    
    # Module & Duration Pill
    meta_text = f"MODULE: {module_title.upper()[:45]}   |   DURATION: {duration}   |   INSTRUCTOR: {instructor[:30]}"
    page.insert_text(pymupdf.Point(40, y), meta_text, fontsize=8, color=(0.35, 0.42, 0.52), fontname="hebo")
    y += 20
    
    # Lesson Title
    title_rect = pymupdf.Rect(40, y, 555, y + 50)
    page.insert_textbox(title_rect, lesson_title, fontsize=15, color=(0.04, 0.11, 0.19), fontname="hebo")
    y += 45
    
    # Divider line
    page.draw_line(pymupdf.Point(40, y), pymupdf.Point(555, y), color=(0.88, 0.91, 0.95), width=1)
    y += 18
    
    # SECTION 1: LECTURE OVERVIEW
    page.draw_rect(pymupdf.Rect(40, y, 555, y + 20), color=None, fill=(0.94, 0.96, 1.0))
    page.insert_text(pymupdf.Point(48, y + 14), "1. LECTURE OVERVIEW & CONCEPTUAL FOUNDATION", fontsize=9, color=(0.0, 0.29, 0.78), fontname="hebo")
    y += 28
    
    overview = breakdown.get("overview", "Comprehensive conceptual breakdown and implementation patterns for this lecture.")
    ov_rect = pymupdf.Rect(45, y, 550, y + 65)
    page.insert_textbox(ov_rect, overview, fontsize=9.5, color=(0.2, 0.25, 0.3), fontname="helv", lineheight=1.35)
    y += 70
    
    # SECTION 2: KEY ARCHITECTURAL COMPONENTS
    components = breakdown.get("components", [])
    if components:
        page.draw_rect(pymupdf.Rect(40, y, 555, y + 20), color=None, fill=(0.94, 0.96, 1.0))
        page.insert_text(pymupdf.Point(48, y + 14), "2. KEY ARCHITECTURAL & TECHNICAL COMPONENTS", fontsize=9, color=(0.0, 0.29, 0.78), fontname="hebo")
        y += 28
        
        for comp in components[:3]:
            c_title = comp.get("title", "Core Architecture")
            c_badge = comp.get("badge", "System")
            c_desc = comp.get("desc", "")
            
            card_rect = pymupdf.Rect(45, y, 550, y + 42)
            page.draw_rect(card_rect, color=(0.88, 0.91, 0.95), fill=(0.98, 0.99, 1.0), width=0.8)
            page.insert_text(pymupdf.Point(55, y + 15), f"• {c_title}  [{c_badge}]", fontsize=9.5, color=(0.05, 0.15, 0.3), fontname="hebo")
            desc_rect = pymupdf.Rect(55, y + 18, 540, y + 40)
            page.insert_textbox(desc_rect, c_desc, fontsize=8.5, color=(0.3, 0.35, 0.42), fontname="helv", lineheight=1.3)
            y += 48
            
    # SECTION 3: CORE TAKEAWAYS
    takeaways = breakdown.get("takeaways", [])
    if takeaways:
        y += 5
        page.draw_rect(pymupdf.Rect(40, y, 555, y + 20), color=None, fill=(0.94, 0.96, 1.0))
        page.insert_text(pymupdf.Point(48, y + 14), "3. CORE TECHNICAL COMPETENCIES & WHAT YOU MASTERED", fontsize=9, color=(0.0, 0.29, 0.78), fontname="hebo")
        y += 26
        
        for t in takeaways[:4]:
            t_rect = pymupdf.Rect(48, y, 550, y + 22)
            page.insert_textbox(t_rect, f" •  {t}", fontsize=9, color=(0.15, 0.2, 0.25), fontname="helv")
            y += 22

    # SECTION 4: ROADMAP CONTEXT
    why = breakdown.get("why_it_matters", "")
    if why and y < 735:
        y += 8
        page.draw_rect(pymupdf.Rect(40, y, 555, y + 36), color=(0.8, 0.88, 1.0), fill=(0.95, 0.97, 1.0), width=0.8)
        page.insert_text(pymupdf.Point(50, y + 14), "CAREER ROADMAP & INDUSTRY APPLICATION:", fontsize=8.5, color=(0.0, 0.29, 0.78), fontname="hebo")
        why_rect = pymupdf.Rect(50, y + 16, 545, y + 34)
        page.insert_textbox(why_rect, why, fontsize=8.5, color=(0.25, 0.3, 0.38), fontname="helv")
        y += 45

    # Footer
    page.draw_line(pymupdf.Point(40, 800), pymupdf.Point(555, 800), color=(0.88, 0.91, 0.95), width=1)
    page.insert_text(pymupdf.Point(40, 815), "LearnHub Interactive LMS  •  Courseware Material  •  Verified Student Copy", fontsize=8, color=(0.5, 0.55, 0.65), fontname="helv")
    page.insert_text(pymupdf.Point(510, 815), "Page 1 of 1", fontsize=8, color=(0.5, 0.55, 0.65), fontname="helv")

    return doc.tobytes()
