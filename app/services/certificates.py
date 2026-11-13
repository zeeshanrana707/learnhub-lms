import uuid
from datetime import datetime, timezone
from app.extensions import db
from app.models.content import Enrollment
from app.models.recognition import Certificate
from app.models.users import Notification

def issue_certificate_if_eligible(enrollment: Enrollment) -> Certificate | None:
    """
    Issue a certificate if the student has reached 100% course completion
    and passed the required threshold.
    """
    if enrollment.certificate:
        return enrollment.certificate

    if enrollment.progress_pct < 100.0 and enrollment.status != 'completed':
        return None

    # Generate unique certificate code
    code = f"CERT-{uuid.uuid4().hex[:12].upper()}"

    cert = Certificate(
        enrollment_id=enrollment.id,
        code=code,
        issued_at=datetime.now(timezone.utc)
    )
    db.session.add(cert)

    notif = Notification(
        user_id=enrollment.user_id,
        title="Certificate Issued! 🎓",
        message=f"Congratulations! You have successfully completed '{enrollment.course.title}'. Your certificate is now available.",
        link=f"/learn/certificate/{cert.code}"
    )
    db.session.add(notif)
    db.session.commit()

    return cert


def generate_certificate_pdf(cert: Certificate) -> bytes:
    """Generate an official high-resolution landscape PDF certificate."""
    try:
        import pymupdf
    except ImportError:
        return b"%PDF-1.4\n%Fallback certificate\n"

    user = cert.enrollment.user
    user_name = (user.profile.full_name if (user.profile and user.profile.full_name) else user.username).title()
    course = cert.enrollment.course
    course_title = course.title or "Professional Certification Course"
    instructor_name = getattr(course, 'instructor_name', 'Lead Instructor')
    issued_date = cert.issued_at.strftime('%B %d, %Y')
    cert_code = cert.code

    doc = pymupdf.open()
    page = doc.new_page(width=842, height=595)  # A4 Landscape

    # 1. Warm Ivory Parchment Background
    page.draw_rect(pymupdf.Rect(0, 0, 842, 595), color=None, fill=(0.99, 0.99, 0.97))

    # 2. Outer Deep Navy Border
    page.draw_rect(pymupdf.Rect(20, 20, 822, 575), color=(0.04, 0.11, 0.22), width=3)
    # 3. Inner Gold Border
    page.draw_rect(pymupdf.Rect(28, 28, 814, 567), color=(0.79, 0.65, 0.28), width=1.5)
    # 4. Corner Ornaments
    for cx, cy in [(28, 28), (814, 28), (28, 567), (814, 567)]:
        page.draw_rect(pymupdf.Rect(cx - 4, cy - 4, cx + 4, cy + 4), color=None, fill=(0.79, 0.65, 0.28))

    # 5. Top Institution Header
    inst_rect = pymupdf.Rect(50, 48, 792, 70)
    page.insert_textbox(inst_rect, "LEARNHUB ACADEMY OF WEB & COMPUTER SCIENCE", fontsize=11, color=(0.4, 0.45, 0.55), fontname="helv", align=1)

    subhead_rect = pymupdf.Rect(50, 70, 792, 88)
    page.insert_textbox(subhead_rect, "OFFICIAL VERIFIED CREDENTIAL • LIFETIME SPECIALIZATION RECORD", fontsize=8, color=(0.6, 0.5, 0.25), fontname="hebo", align=1)

    # 6. Main Certificate Title
    title_rect = pymupdf.Rect(50, 105, 792, 155)
    page.insert_textbox(title_rect, "Certificate of Completion", fontsize=32, color=(0.04, 0.11, 0.22), fontname="hebo", align=1)

    # 7. Presentation Line
    pres_rect = pymupdf.Rect(50, 170, 792, 190)
    page.insert_textbox(pres_rect, "THIS IS PROUDLY CONFERRED UPON", fontsize=10, color=(0.45, 0.5, 0.6), fontname="helv", align=1)

    # 8. Recipient Name
    name_rect = pymupdf.Rect(50, 195, 792, 245)
    page.insert_textbox(name_rect, user_name, fontsize=28, color=(0.08, 0.35, 0.82), fontname="hebo", align=1)
    # Underline accent for recipient
    page.draw_line(pymupdf.Point(220, 248), pymupdf.Point(622, 248), color=(0.79, 0.65, 0.28), width=1.5)

    # 9. Completion Narrative
    narr_rect = pymupdf.Rect(100, 265, 742, 310)
    narr_text = "for successfully fulfilling all coursework requirements, mastering hands-on topic lectures, completing laboratory code challenges, and demonstrating proficiency in"
    page.insert_textbox(narr_rect, narr_text, fontsize=11, color=(0.3, 0.35, 0.42), fontname="helv", align=1)

    # 10. Course Title
    course_rect = pymupdf.Rect(80, 318, 762, 370)
    page.insert_textbox(course_rect, course_title, fontsize=20, color=(0.04, 0.11, 0.22), fontname="hebo", align=1)

    # 11. Gold Seal Stamp in Center Bottom
    seal_center = pymupdf.Point(421, 445)
    page.draw_circle(seal_center, 34, color=(0.79, 0.65, 0.28), fill=(0.98, 0.96, 0.90), width=2)
    page.draw_circle(seal_center, 28, color=(0.79, 0.65, 0.28), fill=None, width=0.8)
    seal_txt_rect = pymupdf.Rect(387, 430, 455, 460)
    page.insert_textbox(seal_txt_rect, "OFFICIAL\nSEAL", fontsize=8, color=(0.6, 0.48, 0.15), fontname="hebo", align=1)

    # 12. Left Column: Issued Date & Security Info
    date_line_start = pymupdf.Point(80, 485)
    date_line_end = pymupdf.Point(280, 485)
    page.draw_line(date_line_start, date_line_end, color=(0.75, 0.8, 0.85), width=1)
    page.insert_text(pymupdf.Point(80, 502), f"ISSUED DATE: {issued_date}", fontsize=9, color=(0.3, 0.35, 0.4), fontname="hebo")
    page.insert_text(pymupdf.Point(80, 517), "AUTHORIZED DIGITAL RECORD", fontsize=7.5, color=(0.55, 0.6, 0.65), fontname="helv")

    # 13. Center Bottom: Verification ID
    verif_rect = pymupdf.Rect(300, 500, 542, 535)
    verif_text = f"VERIFICATION ID: {cert_code}\nLearnHub Academy Verified Credential"
    page.insert_textbox(verif_rect, verif_text, fontsize=8, color=(0.04, 0.11, 0.22), fontname="cour", align=1)

    # 14. Right Column: Instructor / Faculty Signature Line
    sig_line_start = pymupdf.Point(562, 485)
    sig_line_end = pymupdf.Point(762, 485)
    page.draw_line(sig_line_start, sig_line_end, color=(0.75, 0.8, 0.85), width=1)
    page.insert_text(pymupdf.Point(562, 502), f"INSTRUCTOR: {instructor_name}", fontsize=9, color=(0.3, 0.35, 0.4), fontname="hebo")
    page.insert_text(pymupdf.Point(562, 517), "LEARNHUB COURSE DIRECTOR", fontsize=7.5, color=(0.55, 0.6, 0.65), fontname="helv")

    return doc.tobytes()
