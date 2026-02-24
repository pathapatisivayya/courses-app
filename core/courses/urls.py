from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('ramesh-sir/', ramesh_sir, name='ramesh_sir'),
    path('contact/', contact, name='contact'),
    path('courses/', course_list, name='courses'),
    # path('devops/', devops_list, name='devops'),
    path('devops/', devops, name='devops'),
    path('enrollments/', enrollment_list, name='enrollment_list'),
]
