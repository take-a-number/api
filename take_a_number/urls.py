from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^class/state/(?P<name>[a-zA-Z0-9_.-]+)', views.course),
    url(r'^class/create/', views.course_create),
    url('r^class/search/(?P<terms>[a-zA-Z0-9_.-]+)', views.index),
]