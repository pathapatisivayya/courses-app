from django.shortcuts import render
from .models import Enrollment

from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')


def ramesh_sir(request):
    success = request.GET.get('sent') == '1'

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and message:
            try:
                send_mail(
                    'Ramesh Sir – Contact form',
                    f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}",
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
                send_mail(
                    'We received your message – Ramesh Sir',
                    f"Hi {name},\n\nThank you for getting in touch. We have received your message and will get back to you soon.\n\nRegards,\nRamesh Sir",
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
            except Exception:
                pass
        return redirect('ramesh_sir' + '?sent=1')

    return render(request, 'ramesh_sir.html', {'success': success})

def course_list(request):
    return render(request, 'courses.html')

def devops_list(request):
    return render(request, 'devops.html')




from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .models import Enrollment

from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from .models import SampleEnrollment, Assignment



def devops(request):
    success = False

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("mobile")

        SampleEnrollment.objects.create(
            name=name,
            email=email,
            phone=phone,
            course_name="DevOps & Cloud Training"
        )

        # Email to Admin
        send_mail(
            "New DevOps Enrollment",
            f"""
            New student enrolled

            Name: {name}
            Email: {email}
            Phone: {phone}
            """,
            settings.DEFAULT_FROM_EMAIL,
            ['pathapatisivayya12@gmail.com'],
        )

        # Email to Student
        send_mail(
            "Enrollment Confirmation",
            f"""
            Hi {name},

            Thank you for enrolling in DevOps Training at Teja Technologies.
            Our team will contact you soon.

            Regards,
            Teja Technologies
            """,
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )

        success = True

    return render(request, "devops.html", {"success": success})


def enrollment_list(request):
    enrollments = SampleEnrollment.objects.all().order_by('-created_at')
    return render(request, 'enrollment_list.html', {
        'enrollments': enrollments
    })




from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)

            if user.user_type == 'admin':
                return redirect('admin_dashboard')
            elif user.user_type == 'trainer':
                return redirect('trainer_dashboard')
            else:
                return redirect('student_dashboard')


@login_required
def trainer_dashboard(request):
    if request.user.user_type != 'trainer':
        return redirect('login')

    students = Enrollment.objects.filter(trainer=request.user)
    return render(request, 'trainer/dashboard.html', {'students': students})



@login_required
def student_dashboard(request):
    if request.user.user_type != 'student':
        return redirect('login')

    assignments = Assignment.objects.all()
    return render(request, 'student/dashboard.html', {'assignments': assignments})

@login_required
def admin_dashboard(request):
    if request.user.user_type != 'admin':
        return redirect('login')

    enrollments = Enrollment.objects.all()
    return render(request, 'admin/dashboard.html', {'enrollments': enrollments})
