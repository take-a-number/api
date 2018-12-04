from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.courses_list),
    url(r'^(?P<course_id>[0-9A-Fa-f]{8}(-[0-9A-Fa-f]{4}){3}-[0-9A-Fa-f]{12})/office_hours/identity',
        views.course_office_hours_identity),
    url(r'^(?P<course_id>[0-9A-Fa-f]{8}(-[0-9A-Fa-f]{4}){3}-[0-9A-Fa-f]{12})/office_hours/students',
        views.course_office_hours_queue),
    url(r'^(?P<course_id>[0-9A-Fa-f]{8}(-[0-9A-Fa-f]{4}){3}-[0-9A-Fa-f]{12})/office_hours/teaching_assistants',
        views.course_office_hours_teaching_assistants),
    url(r'^(?P<course_id>[0-9A-Fa-f]{8}(-[0-9A-Fa-f]{4}){3}-[0-9A-Fa-f]{12})/office_hours',
        views.course_office_hours),
]
