from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^class/(?P<username>[a-zA-Z0-9_.-]+)', views.course),
]