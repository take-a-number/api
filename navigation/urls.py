from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^class/(?P<name>[a-zA-Z0-9_.-]+)', views.course),
]
