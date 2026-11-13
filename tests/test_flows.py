from app.models.users import User
from app.models.catalog import Course
from app.models.content import Enrollment

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'LearnHub' in response.data


def test_catalog_browse(client):
    response = client.get('/courses')
    assert response.status_code == 200
    assert b'Course Catalog' in response.data
    assert b'Test Course 101' in response.data


def test_auth_registration(client, app):
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'role': 'student',
        'password': 'Password123!',
        'confirm_password': 'Password123!'
    }, follow_redirects=False)

    # PRG pattern: successful post redirects to login
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/auth/login')

    with app.app_context():
        user = User.query.filter_by(username='newuser').first()
        assert user is not None
        assert user.check_password('Password123!') is True


def test_login_and_logout(client, auth):
    # Valid login
    res = auth.login('student_test', 'StudentPass123!')
    assert res.status_code == 200
    assert b'student_test' in res.data

    # Logout
    res_logout = auth.logout()
    assert res_logout.status_code == 200
    assert b'You have been logged out' in res_logout.data


def test_rbac_admin_protection(client, auth):
    # Anonymous -> Redirect to login
    res = client.get('/admin/', follow_redirects=False)
    assert res.status_code == 302
    assert '/auth/login' in res.headers['Location']

    # Log in as Student -> 403 Forbidden
    auth.login('student_test', 'StudentPass123!')
    res_student = client.get('/admin/')
    assert res_student.status_code == 403

    # Log in as Admin -> 200 OK
    auth.logout()
    auth.login('admin_test', 'AdminPass123!')
    res_admin = client.get('/admin/')
    assert res_admin.status_code == 200
    assert b'Admin Control Center' in res_admin.data


def test_free_course_enrollment(client, auth, app):
    auth.login('student_test', 'StudentPass123!')
    with app.app_context():
        course = Course.query.filter_by(slug='test-course-101').first()
        course_id = course.id

    res = client.post(f'/learn/enroll/{course_id}', follow_redirects=True)
    assert res.status_code == 200
    assert b'Successfully enrolled' in res.data or b'Learning Hub' in res.data


def test_course_completion_action(client, auth, app):
    auth.login('student_test', 'StudentPass123!')
    with app.app_context():
        course = Course.query.filter_by(slug='test-course-101').first()
        course_id = course.id

    # Test JSON endpoint
    res = client.post(f'/learn/course/{course_id}/complete', headers={'Accept': 'application/json'})
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert data['progress_pct'] == 100.0
    assert data['certificate_url'] is not None

    with app.app_context():
        user = User.query.filter_by(username='student_test').first()
        enrollment = Enrollment.query.filter_by(user_id=user.id, course_id=course_id).first()
        assert enrollment.status == 'completed'
        assert enrollment.progress_pct == 100.0
        assert enrollment.certificate is not None
        cert_code = enrollment.certificate.code

    # Test viewing certificate HTML
    res_view = client.get(f'/learn/certificate/{cert_code}')
    assert res_view.status_code == 200
    assert cert_code.encode() in res_view.data
    assert b'Certificate of Completion' in res_view.data

    # Test downloading certificate PDF
    res_pdf = client.get(f'/learn/certificate/{cert_code}/download')
    assert res_pdf.status_code == 200
    assert res_pdf.mimetype == 'application/pdf'
    assert res_pdf.data.startswith(b'%PDF')

    # Test course certificate direct shortcut
    res_shortcut = client.get(f'/learn/course/{course_id}/certificate')
    assert res_shortcut.status_code == 302
    assert cert_code in res_shortcut.headers['Location']


def test_start_course_and_star_wishlist(client, auth, app):
    auth.login('student_test', 'StudentPass123!')
    with app.app_context():
        from app.models.catalog import Roadmap
        course = Course.query.filter_by(slug='test-course-101').first()
        course_id = course.id
        roadmap = Roadmap.query.first()
        roadmap_slug = roadmap.slug if roadmap else None

    # Test toggling star (wishlist) via JSON
    res_star = client.post(f'/learn/wishlist/toggle/{course_id}', headers={'Accept': 'application/json'})
    assert res_star.status_code == 200
    star_data = res_star.get_json()
    assert star_data['success'] is True
    assert star_data['wishlisted'] is True

    # Toggle off
    res_unstar = client.post(f'/learn/wishlist/toggle/{course_id}', headers={'Accept': 'application/json'})
    assert res_unstar.status_code == 200
    unstar_data = res_unstar.get_json()
    assert unstar_data['success'] is True
    assert unstar_data['wishlisted'] is False

    # Test start_course route (redirects to course_overview)
    res_start = client.get(f'/learn/course/{course_id}/start', follow_redirects=False)
    assert res_start.status_code == 302
    assert f'/learn/course/{course_id}' in res_start.headers['Location']

    # Test roadmap detail page loads with 200 OK
    if roadmap_slug:
        res_rm = client.get(f'/roadmaps/{roadmap_slug}')
        assert res_rm.status_code == 200
        assert b'Ready to Start' in res_rm.data or b'Stage 1' in res_rm.data
