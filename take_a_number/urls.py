from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.courses_list),
    url(r'^(?P<course_abbreviation>[A-Z]+[_.-][0-9]+)/office_hours/identity',
        views.course_office_hours_identity),
    url(r'^(?P<course_abbreviation>[A-Z]+[_.-][0-9]+)/office_hours',
        views.course_office_hours),
    url(r'^(?P<course_abbreviation>[A-Z]+[_.-][0-9]+)/office_hours/queue',
        views.course_office_hours_queue),
    url(r'^(?P<course_abbreviation>[A-Z]+[_.-][0-9]+)/office_hours/teaching_assistants',
        views.course_office_hours_teaching_assistants),
    # url(r'^class/create/', views.course_create),
    # url('r^class/search/(?P<terms>[a-zA-Z0-9_.-]+)', views.index),
]
