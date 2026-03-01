"""
Test cases for courses app.
Run: python manage.py test courses
"""
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from .models import User, Enrollment, SampleEnrollment, Assignment

User = get_user_model()


# ---------- Model tests ----------
class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username='teststudent',
            password='testpass123',
            user_type='student'
        )
        self.assertEqual(user.username, 'teststudent')
        self.assertEqual(user.user_type, 'student')

    def test_create_admin_user(self):
        user = User.objects.create_superuser(
            username='admin1',
            email='admin@test.com',
            password='adminpass123'
        )
        user.user_type = 'admin'
        user.save()
        self.assertTrue(user.is_staff)
        self.assertEqual(user.user_type, 'admin')


class SampleEnrollmentModelTest(TestCase):
    def test_create_sample_enrollment(self):
        enrollment = SampleEnrollment.objects.create(
            name='John Doe',
            email='john@example.com',
            phone='9876543210',
            course_name='DevOps & Cloud Training'
        )
        self.assertEqual(enrollment.name, 'John Doe')
        self.assertEqual(enrollment.course_name, 'DevOps & Cloud Training')
        self.assertIsNotNone(enrollment.created_at)

    def test_sample_enrollment_str(self):
        enrollment = SampleEnrollment.objects.create(
            name='Jane',
            email='jane@test.com',
            phone='1234567890',
            course_name='Python'
        )
        self.assertIn('Jane', str(enrollment))
        self.assertIn('Python', str(enrollment))


class AssignmentModelTest(TestCase):
    def test_create_assignment(self):
        assignment = Assignment.objects.create(
            course_name='DevOps',
            title='Setup CI/CD',
            description='Create a pipeline'
        )
        self.assertEqual(assignment.title, 'Setup CI/CD')
        self.assertEqual(str(assignment), 'Setup CI/CD')


# ---------- View / URL tests ----------
class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.__name__, 'home')

    def test_home_returns_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class ContactViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact_url_resolves(self):
        url = reverse('contact')
        self.assertEqual(resolve(url).func.__name__, 'contact')

    def test_contact_returns_200(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')


class CourseListViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_courses_url_resolves(self):
        url = reverse('courses')
        self.assertEqual(resolve(url).func.__name__, 'course_list')

    def test_course_list_returns_200(self):
        response = self.client.get(reverse('courses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses.html')


class DevOpsViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_devops_get_returns_200(self):
        response = self.client.get(reverse('devops'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'devops.html')

    def test_devops_post_creates_enrollment(self):
        response = self.client.post(reverse('devops'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'mobile': '9999999999',
        })
        self.assertEqual(SampleEnrollment.objects.count(), 1)
        enrollment = SampleEnrollment.objects.first()
        self.assertEqual(enrollment.name, 'Test User')
        self.assertEqual(enrollment.email, 'test@example.com')
        self.assertEqual(enrollment.course_name, 'DevOps & Cloud Training')


class EnrollmentListViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_enrollment_list_returns_200(self):
        response = self.client.get(reverse('enrollment_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'enrollment_list.html')

    def test_enrollment_list_shows_enrollments(self):
        SampleEnrollment.objects.create(
            name='A', email='a@test.com', phone='111', course_name='DevOps'
        )
        response = self.client.get(reverse('enrollment_list'))
        self.assertContains(response, 'A')
        self.assertContains(response, 'a@test.com')


class RameshSirViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_ramesh_sir_get_returns_200(self):
        response = self.client.get(reverse('ramesh_sir'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ramesh_sir.html')
