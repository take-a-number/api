from django.http import HttpResponse, HttpResponseNotFound, HttpRequest, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
import json
from typing import Dict
import random
import uuid

from .models import Course, OfficeHours, Student, TeachingAssistant
from take_a_number.class_queue import ClassQueue, QueueStudent, QueueTA

# Dictionary where keys are the course names and values the queues of each active course
# Associates the course abbreviation with an active class
courses: Dict[str, Course] = {'CS3251': Course(
    'CS3251', 'Intermediate Software Design', '43eaa6d8-5def-4567-a50c-293dc3566640', 'TA1234')}
#   {
#     abbreviation: 'CS3251',
#     description: 'Intermediate Software Design',
#     id: '43eaa6d8-5def-4567-a50c-293dc3566640',
#   },
#   {
#     abbreviation: 'CS3250',
#     description: 'Algorithms',
#     id: '2b77c97b-1708-401c-bbc3-5323a480ee48',
#   },
#   {
#     abbreviation: 'CS3270',
#     description: 'Programming Languages',
#     id: 'd9367a7d-4ec8-4ab6-a680-017a7326d1fd',
#   },
#   {
#     abbreviation: 'CS2212',
#     description: 'Discrete Structures',
#     id: '7c3dc539-6b47-4772-a9a9-5384c0e420b9',
#   },

office_hours_sessions: Dict[str, OfficeHours] = {}


def random_join_code() -> str:
    ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            for i in range(6))


def get_identity(req: HttpRequest, course_abbreviation):
    if course_abbreviation not in courses or course_abbreviation not in office_hours_sessions:
        return None
    office_hours = office_hours_sessions[course_abbreviation]
    if 'id' in req.session:
        id = req.session['id']
        if id in office_hours.student_sessions:
            return office_hours.student_sessions[id]
        elif id in office_hours.teaching_assistant_sessions:
            return office_hours.teaching_assistant_sessions[id]


def course_office_hours_identity(request: HttpRequest, course_abbreviation):
    identity = get_identity(request, course_abbreviation)
    if identity == None:
        return HttpResponseForbidden()
    else:
        return HttpResponse(json.dumps(identity._asdict()))


def courses_list(request: HttpRequest):
    return HttpResponse(content=json.dumps(courses.values()))


def course_office_hours(request: HttpRequest, course_abbreviation):
    if course_abbreviation not in courses:
        return HttpResponseNotFound()
    if course_abbreviation not in office_hours_sessions:
        office_hours_sessions[course_abbreviation] = OfficeHours(
            course_abbreviation, random_join_code(), [], []),
    # Get a course's office hours
    if request.method == 'GET':
        # return a JSON from the dict
        office_hours = office_hours_sessions[course_abbreviation]
        officeHours = {'courseAbbreviation': office_hours.course_abbreviation,
                       'teachingAssistants': office_hours.teaching_assistants,
                       'students': office_hours.students,
                       }
        return HttpResponse(content=json.dumps(officeHours))

    # Modify the course office hours. Does nothing right now.
    elif request.method == 'POST':
        return HttpResponseBadRequest()

    # A user has entered a join code, create a session.
    elif request.method == 'PUT':
        body: Dict[str, str] = json.loads(request.body)
        # TODO Use constant time comparison here
        if 'joinCode' in body and 'name' in body:
            if body['joinCode'] == office_hours_sessions[course_abbreviation].student_join_code:
                new_uuid = uuid.uuid4()
                office_hours_sessions[course_abbreviation].student_sessions[new_uuid] = Student(body['name'], )
                return HttpResponse()
            elif body['joinCode'] == courses[course_abbreviation].teaching_assistant_join_code:
                office_hours_sessions[course_abbreviation].teaching_assistants.append(
                    Student())
                return HttpResponse()
            else:
                return HttpResponseForbidden()
        else:
            return HttpResponseBadRequest()

    # A user has left office hours
    elif request.method == 'DELETE':
        req: Dict[str, str] = json.loads(request.body)
        # TODO grab user info from session

    return HttpResponseBadRequest()


def course_office_hours_queue(request: HttpRequest, course_abbreviation):
    if course_abbreviation not in courses or course_abbreviation not in office_hours_sessions:
        return HttpResponseNotFound()
    if request.method == 'PUT':  # student adds self to queue
        pass
    elif request.method == 'DELETE':  # student removes self from queue
        pass
    elif request.method == 'POST':  # student updates own state on queue
        pass
    else:
        return HttpResponseBadRequest()


def course_office_hours_teaching_assistants(request: HttpRequest, course_abbreviation):
    if course_abbreviation not in courses or course_abbreviation not in office_hours_sessions:
        return HttpResponseNotFound()
    if request.method == 'PUT':  # TA adds self to office hours
        pass
    elif request.method == 'DELETE':  # TA removes self from office hours
        pass
    # TA updates own state (i.e. can start helping someone)
    elif request.method == 'POST':
        pass
    else:
        return HttpResponseBadRequest()
