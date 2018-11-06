from django.http import HttpResponse, HttpResponseNotFound, HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from .models import Class
from .forms import ClassForm
from django.views.decorators.csrf import csrf_protect


def index(request, terms = ''):
    return render(request, 'index.html')


def course(request, name = ''):
    if request.method == 'POST':
        return render(request, 'class-student.html')
    return render(request, 'class-remote.html')

@csrf_protect
def course_create(request):
    form = ClassForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        class_instance = Class(**form.cleaned_data)
        # class_instance.save()
        course = class_instance.course_name
        return HttpResponseRedirect('/class/state/' + course)

    return render(request, 'class-create.html')

