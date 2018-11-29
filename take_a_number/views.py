from django.http import HttpResponse, HttpResponseNotFound, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Class, OfficeHoursSession
from .forms import ClassForm
from django.views.decorators.csrf import csrf_protect
from uuid import UUID
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from datetime import datetime, timedelta


def index(request, terms = ''):
    return render(request, 'index.html')


def course(request, name = ''):
    # course = get_object_or_404(Class, name=name)
    user = {'id': '', 'name': 'Emily'}

    # Get class state if exists, else do a search
    if request.method == 'GET':
        return render(request, 'class-remote.html', {'name': name})
    # Modify class state
    elif request.method == 'POST':
        code = request.POST['join_input']

        if code[0].isnumeric():  # instructor
            active_session = list(OfficeHoursSession.objects.filter(instructorCode=code))
            if len(active_session) == 0:  # no active session, create new session
                s = OfficeHoursSession()
                data = s.get_decoded()
                data['teachingAssistants'] = [user]
                data['students'] = []
                s.instructorCode = code
                s.expire_date = datetime.now() + timedelta(hours=12)
                s.session_data = SessionStore().encode(data)
                s.save()
                active_session.append(OfficeHoursSession.objects.get(pk=s.session_key))
        else:  # student
            active_session = list(OfficeHoursSession.objects.filter(studentCode=code))
            if len(active_session) == 0:
                return HttpResponseNotFound('<h1>The join code entered was invalid</h1>')
        data = active_session[0].get_decoded()
        return render(request, 'class-student.html')
    # Create a class
    elif request.method == 'PUT':
        pass
    # Delete a class
    elif request.method == 'DELETE':
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

