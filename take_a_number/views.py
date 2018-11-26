from django.http import HttpResponse, HttpResponseNotFound, HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from .models import Class
from .forms import ClassForm
from django.views.decorators.csrf import csrf_protect

# Dictionary where keys are the course names and values the queues of each active course
state = {}

def index(request, terms = ''):
    return render(request, 'index.html')


def course(request, name = ''):
    # Get class state if exists, else do a search
    if request.method == 'GET':
        # query DB for the course
        return render(request, 'class-remote.html')
    # Modify session (queue) state
    elif request.method == 'POST':
        # modify DB with the course
        return render(request, 'class-student.html')
    # Create a session (queue)
    elif request.method == 'PUT':
        # add new course to DB
        pass
    # Delete a session (queue)
    elif request.method == 'DELETE':
        # remove course from DB
        pass
    return HttpResponseNotFound()


@csrf_protect
def course_create(request):
    form = ClassForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        class_instance = Class(**form.cleaned_data)
        class_instance.save()
        course = class_instance.course_name
        return HttpResponseRedirect('/class/state/' + course)

    return render(request, 'class-create.html')

