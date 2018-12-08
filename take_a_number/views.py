# from flask import Flask, session, request, jsonify, abort
# from flask_cors import CORS
# from flask_uuid import FlaskUUID
from django.http import HttpResponse

from typing import Dict
import random
import uuid
from uuid import UUID

import json


from .models import Course, OfficeHours, Student, TeachingAssistant
from .utils.class_queue import ClassQueue, QueueMember, QueueTA

# TODO remove this block of code
# app = Flask(__name__)
# CORS(app, supports_credentials=True)
# app.secret_key = os.urandom(24)
# app.config.update(SESSION_COOKIE_HTTPONLY=False, SESSION_COOKIE_SECURE=False)
# FlaskUUID(app)

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

# Holds the state of the running application
# Maps from the ID of a course (provided by uuid) to relevant information
office_hours_sessions: Dict[uuid.UUID, OfficeHours] = {}

office_hours_state: Dict[uuid.UUID, ClassQueue] = {}


def random_join_code() -> str:
    return ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                   for i in range(6))


# get the uuid for the user session
def get_identity(request, course_id):
    # check whether the course exists or has active office hours
    if course_id not in courses or course_id not in office_hours_state:
        return None
    # obtain the OfficeHours model based on course_id
    office_hours = office_hours_state[course_id]
    # cookie used to track the browser session
    if 'whoami' in request.session:
        whoami: str = request.session['whoami'] # get the uuid of the session
        # user is a student
        if whoami in office_hours.studentSessions:
            return office_hours.studentSessions[whoami]
        # user is a ta; cannot be student and ta of same class
        elif whoami in office_hours.taSessions:
            return office_hours.taSessions[whoami]
    return None


def course_office_hours_identity(request, course_id):
    course_id = UUID(course_id)
    identity = get_identity(request, course_id)
    # could not find information on desired course
    if identity is None:
        return HttpResponse(status=404)
    return HttpResponse(json.dumps(identity._asdict()))


def courses_list(request):
    return HttpResponse(json.dumps(list(map(lambda x: x._asdict(), courses.values())), cls=UUIDEncoder))


def course_office_hours(request, course_id):
    course_id = UUID(course_id)
    if course_id not in courses:
        return HttpResponse(status=404)
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
        identity = get_identity(request, course_id)
        if identity is None:
            return HttpResponse(json.dumps(officeHours))
        if identity.id in office_hours.teaching_assistant_sessions:
            print(office_hours.student_join_code)
            officeHours['studentJoinCode'] = office_hours.student_join_code
        return HttpResponse(json.dumps(officeHours))



    # @@@@@ old code above this line

    course_id = UUID(course_id)
    # check whether the course exists
    if course_id not in courses:
        return HttpResponse(status=404)
    # if the course has no active session, create an entry for it
    if course_id not in office_hours_state:
        office_hours_state[course_id] = ClassQueue(
            course_id, random_join_code(), [], [], {}, {})
    # Get a course's office hours
    if request.method == 'GET':
        # return a JSON from the dict
        office_hours = office_hours_state[course_id]
        course = courses[course_id]
        # return the course, tas, and students
        officeHours = {
            'courseAbbreviation': course.abbreviation,
            'teachingAssistants': list(map(lambda x: x.asDict(), office_hours.tas)), #list(map(lambda x: x._asdict(), office_hours.tas)),
            'students': list(map(lambda x: x.asDict(), office_hours.students)) #list(map(lambda x: x._asdict(), office_hours.students)),
        }
        identity = get_identity(request, course_id)
        if identity is None:
            return HttpResponse(json.dumps(officeHours))
        # if the current user is a known ta (by id), return the student join code as well
        if identity.id in office_hours.taSessions:
            print(office_hours.studentJoinCode)
            officeHours['studentJoinCode'] = office_hours.studentJoinCode
        return HttpResponse(json.dumps(officeHours))

    # Modify the course office hours session. Does nothing right now.
    elif request.method == 'POST':
        return HttpResponse(status=400)

    # A user has entered a join code; create a session if DNE.
    # Important note: joining the seesion != joining the queue
    elif request.method == 'PUT':
        json_req = json.loads(request.body)
        if json_req is None:
            return HttpResponse(status=401)
        json_req: Dict[str, str] = json.loads(json_req)
        # TODO Use constant time comparison here
        # makes sure the user entered a join code and name field
        if 'joinCode' in json_req and 'name' in json_req:
            if json_req['joinCode'] == office_hours_state[course_id].studentJoinCode:
                new_uuid = str(uuid.uuid4())
                # TODO figure out logic of adding new student (what sessions map to)
                office_hours_state[course_id].studentSessions[new_uuid] = QueueMember(
                    json_req['name'], new_uuid, "student")
                request.session['whoami'] = new_uuid
                return HttpResponse("{}") # return an empty result
            elif json_req['joinCode'] == courses[course_id].teaching_assistant_join_code:
                new_uuid = str(uuid.uuid4())
                office_hours_state[course_id].taSessions[new_uuid] = QueueTA(
                    json_req['name'], new_uuid, "teaching_assistant", None)
                request.session['whoami'] = new_uuid
                return HttpResponse("{}") # return empty result
            else:
                # join code was not valid for student or ta
                return HttpResponse(status=401)
        else:
            # one of the fields was missing in the request
            return HttpResponse(status=400)

    # A user has left office hours; does not change anything yet
    elif request.method == 'DELETE':
        # TODO grab user info from session
        req: Dict[str, str] = json.loads(request.get_json())
        return HttpResponse(status=401)

# do operations on the list of students
def course_office_hours_queue(request, course_id):
    course_id = UUID(course_id)
    # check that course exists and has an active session
    if course_id not in courses or course_id not in office_hours_state:
        return HttpResponse(status=404)
    identity = get_identity(request, course_id)
    if identity is None or identity.id not in office_hours_state[course_id].studentSessions:
        return HttpResponse(status=401)
    student = office_hours_state[course_id].studentSessions[identity.id]
    # some error occurred, id is in the session but the student is not
    if student not in office_hours_state[course_id].students:
        return HttpResponse(status=400)

    # student adds self to queue
    if request.method == 'PUT':
        session_dict = office_hours_state[course_id]
        # append to end of previous list; write the result back
        session_dict.enqueue(student) # TODO look at what "student" is
        # rewrite state with modified data
        office_hours_state[course_id] = session_dict
        return HttpResponse('{}')

    # student removes self from queue
    if request.method == 'DELETE':
        session_dict = office_hours_state[course_id]#._asdict()
        # remove from previous list; write the result back
        session_dict.removeStudent(student.id)
        office_hours_state[course_id] = session_dict
        return HttpResponse('{}')

    # student updates own state on queue; does not do anything yet
    elif request.method == 'POST':
        return HttpResponse()


# do operations on the list of tas
def course_office_hours_teaching_assistants(request, course_id):
    course_id = UUID(course_id)
    # makes sure the course exists and has a session
    if course_id not in courses or course_id not in office_hours_state:
        return HttpResponse(status=404)
    identity = get_identity(request, course_id)
    # handle if the user is not a ta
    if identity is None or identity.id not in office_hours_state[course_id].taSessions:
        return HttpResponse(status=401)
    teaching_assistant = office_hours_state[course_id].taSessions[identity.id]
    # TODO figure out why below logic does not work
    # some error occurred, id is in the session but the ta is not
    # if teaching_assistant not in office_hours_sessions[course_id].teaching_assistants:
    #     return HttpResponse(status=400)

    # TA adds self to course
    if request.method == 'PUT':
        session_dict = office_hours_state[course_id]
        session_dict.addTA(teaching_assistant)
        office_hours_state[course_id] = session_dict
        return HttpResponse('{}')

    # if there are no active tas for this session
    # if len(list(filter(lambda x: x.id == teaching_assistant.id, office_hours_state[course_id].tas))) == 0:
    if office_hours_state[course_id].taCount() == 0:
        return HttpResponse(status=400)

    # TA removes self from course
    if request.method == 'DELETE':
        session_dict = office_hours_state[course_id]
        session_dict.removeTA(teaching_assistant.id)
        office_hours_state[course_id] = session_dict
        return HttpResponse('{}')

    # TA updates own state; does not do anything yet
    elif request.method == 'POST':
        student_json = json.loads(request.body)
        # check that student json exists and has a valid id
        if student_json is None:
            return HttpResponse(status=400)
        if 'id' not in student_json:
            return HttpResponse(status=400)
        if student_json['id'] not in office_hours_state[course_id].studentSessions:
            return HttpResponse(status=404)

        student = office_hours_state[course_id].studentSessions[student_json['id']]
        if student not in office_hours_state[course_id].students:
            return HttpResponse(status=404)
        session_dict = office_hours_state[course_id]
        # remove the student in front from the queue
        # TODO student in front is being indicated from the frontend for now
        session_dict.removeStudent(student.id)
        # remove ta from list, modify to add a student (being helped)
        session_dict.removeTA(teaching_assistant.id)
        # TODO add code to directly start helping another student to QueueTA
        teaching_assistant.startHelping(student)
        # modify state of course using modified data on teaching assistant
        session_dict.taSessions[identity] = teaching_assistant
        session_dict.addTA(teaching_assistant)
        # write back to overall state of application
        office_hours_state[course_id] = session_dict
        return HttpResponse('{}')

# from https://stackoverflow.com/questions/36588126/uuid-is-not-json-serializable
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)