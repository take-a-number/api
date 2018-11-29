from flask import Flask, session, request, jsonify, abort
from flask_cors import CORS
from flask_uuid import FlaskUUID
from typing import Dict
import random
import uuid
import os
import json

from models import Course, OfficeHours, Student, TeachingAssistant
from take_a_number.class_queue import ClassQueue, QueueStudent, QueueTA

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = os.urandom(24)
app.config.update(SESSION_COOKIE_HTTPONLY=False, SESSION_COOKIE_SECURE=False)
FlaskUUID(app)

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
    return ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                   for i in range(6))


def get_identity(course_id) -> str:
    if course_id not in courses or course_id not in office_hours_sessions:
        return None
    office_hours = office_hours_sessions[course_id]
    if 'whoami' in session:
        whoami: str = session['whoami']
        if whoami in office_hours.student_sessions:
            return office_hours.student_sessions[whoami]
        elif whoami in office_hours.teaching_assistant_sessions:
            return office_hours.teaching_assistant_sessions[whoami]
    return None


@app.route("/<uuid:course_id>/office_hours/identity")
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
        office_hours_sessions[course_id] = OfficeHours(
            course_id, random_join_code(), [], [], {}, {})
    # Get a course's office hours
    if request.method == 'GET':
        # return a JSON from the dict
        office_hours = office_hours_sessions[course_id]
        course = courses[course_id]
        officeHours = {'courseAbbreviation': course.abbreviation,
                       'teachingAssistants': list(map(lambda x: x._asdict(), office_hours.teaching_assistants)),
                       'students': list(map(lambda x: x._asdict(), office_hours.students)),
                       }
        identity = get_identity(course_id)
        if identity is None:
            return json.dumps(officeHours)
        if identity.id in office_hours.teaching_assistant_sessions:
            print(office_hours.student_join_code)
            officeHours['studentJoinCode'] = office_hours.student_join_code
        return json.dumps(officeHours)

    # Modify the course office hours session. Does nothing right now.
    elif request.method == 'POST':
        return abort(400)

    # A user has entered a join code, create a session if DNE.
    elif request.method == 'PUT':
        json_req = request.get_json()
        if json_req is None:
            abort(401)
        json_req: Dict[str, str] = json.loads(json_req)
        # TODO Use constant time comparison here
        if 'joinCode' in json_req and 'name' in json_req:
            if json_req['joinCode'] == office_hours_sessions[course_id].student_join_code:
                new_uuid = uuid.uuid4().hex
                office_hours_sessions[course_id].student_sessions[new_uuid] = Student(
                    json_req['name'], new_uuid, "student")
                session['whoami'] = new_uuid
                return "{}"
            elif json_req['joinCode'] == courses[course_id].teaching_assistant_join_code:
                new_uuid = uuid.uuid4().hex
                office_hours_sessions[course_id].teaching_assistant_sessions[new_uuid] = TeachingAssistant(
                    json_req['name'], new_uuid, "teaching_assistant", None)
                session['whoami'] = new_uuid
                return "{}"
            else:
                abort(401)
        else:
            abort(400)

    # A user has left office hours
    elif request.method == 'DELETE':
        req: Dict[str, str] = json.loads(request.get_json())
        # TODO grab user info from session


@app.route("/<uuid:course_id>/office_hours/students", methods=['POST', 'PUT', 'DELETE'])
def course_office_hours_queue(course_id):
    if course_id not in courses or course_id not in office_hours_sessions:
        abort(404)
    identity = get_identity(course_id)
    if identity is None or identity.id not in office_hours_sessions[course_id].student_sessions:
        abort(401)
    student = office_hours_sessions[course_id].student_sessions[identity.id]

    if request.method == 'PUT':  # student adds self to queue
        session_dict = office_hours_sessions[course_id]._asdict()
        session_dict['students'].append(student)
        office_hours_sessions[course_id] = OfficeHours(**session_dict)
        return '{}'

    if student not in office_hours_sessions[course_id].students:
        abort(400)

    if request.method == 'DELETE':  # student removes self from queue
        session_dict = office_hours_sessions[course_id]._asdict()
        session_dict['students'].remove(student)
        office_hours_sessions[course_id] = OfficeHours(**session_dict)
        return '{}'
    elif request.method == 'POST':  # student updates own state on queue. No-op for now
        pass


@app.route("/<uuid:course_id>/office_hours/teaching_assistants", methods=['POST', 'PUT', 'DELETE'])
def course_office_hours_teaching_assistants(course_id):
    if course_id not in courses or course_id not in office_hours_sessions:
        abort(404)
    identity = get_identity(course_id)
    if identity is None or identity.id not in office_hours_sessions[course_id].teaching_assistant_sessions:
        abort(401)
    teaching_assistant = office_hours_sessions[course_id].teaching_assistant_sessions[identity.id]

    if request.method == 'PUT':  # TA adds self
        session_dict = office_hours_sessions[course_id]._asdict()
        session_dict['teaching_assistants'].append(teaching_assistant)
        office_hours_sessions[course_id] = OfficeHours(**session_dict)
        return '{}'

    if len(filter(lambda x: x.id == teaching_assistant.id, office_hours_sessions[course_id].teaching_assistants)) == 0:
        abort(400)

    if request.method == 'DELETE':  # TA removes self
        session_dict = office_hours_sessions[course_id]._asdict()
        session_dict['teaching_assistants'].remove(teaching_assistant)
        office_hours_sessions[course_id] = OfficeHours(**session_dict)
        return '{}'
    # TA updates own state. For now, just polling the queue.
    elif request.method == 'POST':
        student_json = request.get_json()
        if student_json is None:
            abort(400)
        print(type(student_json))
        if 'id' not in student_json:
            abort(400)
        if student_json['id'] not in office_hours_sessions[course_id].student_sessions:
            abort(404)
        student = office_hours_sessions[course_id].student_sessions[student_json['id']]
        if student not in office_hours_sessions[course_id].students:
            abort(404)
        session_dict = office_hours_sessions[course_id]._asdict()
        session_dict['students'].remove(student)
        session_dict['teaching_assistants'].remove(teaching_assistant)
        ta_dict = teaching_assistant._asdict()
        ta_dict['helping'] = student._asdict()
        teaching_assistant = TeachingAssistant(**ta_dict)
        session_dict['teaching_assistant_sessions'][identity] = teaching_assistant
        session_dict['teaching_assistants'].append(session_dict['teaching_assistant_sessions'][identity])
        office_hours_sessions[course_id] = OfficeHours(**session_dict)
        return '{}'


if __name__ == "__main__":
    app.run()
