from flask import Flask, session, request, jsonify, abort
from flask_cors import CORS
from flask_uuid import FlaskUUID
from typing import Dict
import random
import uuid
import os
import json

from models import Course, OfficeHours, Student, TeachingAssistant, UserType
from take_a_number.class_queue import ClassQueue, QueueStudent, QueueTA

app = Flask(__name__)
FlaskUUID(app)
CORS(app, supports_credentials=True)
app.secret_key = os.urandom(24)
app.config.update(SESSION_COOKIE_HTTPONLY=False, SESSION_COOKIE_SECURE=True)

# Dictionary where keys are the course names and values the queues of each active course
# Associates the course abbreviation with an active class
courses: Dict[uuid.UUID, Course] = {uuid.UUID(hex='43eaa6d8-5def-4567-a50c-293dc3566640'): Course(
    'CS3251', 'Intermediate Software Design', uuid.UUID(hex='43eaa6d8-5def-4567-a50c-293dc3566640'), 'TA1234')}
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

office_hours_sessions: Dict[uuid.UUID, OfficeHours] = {}


def random_join_code() -> str:
    ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            for i in range(6))


def get_identity(course_id):
    if course_id not in courses or course_id not in office_hours_sessions:
        return None
    office_hours = office_hours_sessions[course_id]
    if 'whoami' in session:
        whoami: uuid.UUID = session['whoami']
        if whoami in office_hours.student_sessions:
            return office_hours.student_sessions[whoami]
        elif whoami in office_hours.teaching_assistant_sessions:
            return office_hours.teaching_assistant_sessions[whoami]

    # url(r'^$', views.courses_list),
    # url(r'^(?P<course_abbreviation>[A-Z]+[_.-][0-9]+)/office_hours/identity',
    #     views.course_office_hours_identity),
    # url(r'^(?P<course_abbreviation>[A-Z]+[_.-][0-9]+)/office_hours',
    #     views.course_office_hours),
    # url(r'^(?P<course_abbreviation>[A-Z]+[_.-][0-9]+)/office_hours/queue',
    #     views.course_office_hours_queue),
    # url(r'^(?P<course_abbreviation>[A-Z]+[_.-][0-9]+)/office_hours/teaching_assistants',


@app.route("/<uuid:course_id>/office_hours/identity/")
def course_office_hours_identity(course_id):
    identity = get_identity(course_id)
    if identity is None:
        abort(404)
    return jsonify(identity._asdict())


@app.route("/")
def courses_list():
    return jsonify(list(map(lambda x: x._asdict(), courses.values())))


@app.route("/<uuid:course_id>/office_hours", methods=['GET', 'POST', 'PUT', 'DELETE'])
def course_office_hours(course_id):
    if course_id not in courses:
        abort(404)
    if course_id not in office_hours_sessions:
        office_hours_sessions[course_id] = OfficeHours(course_id, random_join_code(), [], [], {}, {})
    # Get a course's office hours
    if request.method == 'GET':
        # return a JSON from the dict
        office_hours = office_hours_sessions[course_id]
        print(office_hours)
        course = courses[course_id]
        officeHours = {'courseAbbreviation': course.abbreviation,
                       'teachingAssistants': office_hours.teaching_assistants,
                       'students': office_hours.students,
                       }
        return jsonify(officeHours)

    # Modify the course office hours. Does nothing right now.
    elif request.method == 'POST':
        return abort(400)

    # A user has entered a join code, create a session.
    elif request.method == 'PUT':
        json_req: Dict[str, str] = json.loads(request.get_json())
        print(json_req)
        print(type(json_req))
        if json_req is None:
            abort(401)
        # TODO Use constant time comparison here
        if 'joinCode' in json_req and 'name' in json_req:
            if json_req['joinCode'] == office_hours_sessions[course_id].student_join_code:
                new_uuid = uuid.uuid4()
                office_hours_sessions[course_id].student_sessions[new_uuid] = Student(json_req['name'], new_uuid, UserType.Student)
                return "{}"
            elif json_req['joinCode'] == courses[course_id].teaching_assistant_join_code:
                new_uuid = uuid.uuid4()
                office_hours_sessions[course_id].teaching_assistants.append(TeachingAssistant(json_req['name'], new_uuid, UserType.Student, None))
                return "{}"
            else:
                abort(401)
        else:
            abort(400)

    # A user has left office hours
    elif request.method == 'DELETE':
        req: Dict[str, str] = request.get_json()
        # TODO grab user info from session


@app.route("/<uuid:course_id>/office_hours/queue", methods=['POST', 'PUT', 'DELETE'])
def course_office_hours_queue(course_id):
    if course_id not in courses or course_id not in office_hours_sessions:
        abort(404)
    if request.method == 'PUT':  # student adds self to queue
        pass
    elif request.method == 'DELETE':  # student removes self from queue
        pass
    elif request.method == 'POST':  # student updates own state on queue
        pass


@app.route("/<uuid:course_id>/office_hours/teaching_assistants", methods=['POST', 'PUT', 'DELETE'])
def course_office_hours_teaching_assistants(course_id):
    if course_id not in courses or course_id not in office_hours_sessions:
        abort(404)
    if request.method == 'PUT':  # TA adds self to office hours
        pass
    elif request.method == 'DELETE':  # TA removes self from office hours
        pass
    # TA updates own state (i.e. can start helping someone)
    elif request.method == 'POST':
        pass

if __name__ == "__main__":
    app.run()
