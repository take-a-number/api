from django.http import HttpResponse, HttpResponseNotFound, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Class, OfficeHoursSession
from .forms import ClassForm
from django.views.decorators.csrf import csrf_protect
import json
from take_a_number.class_queue import ClassQueue, QueueStudent, QueueTA


# Dictionary where keys are the course names and values the queues of each active course
# Associates the course abbreviation with an active class
state = {}

def index(request, terms = ''):
    return render(request, 'index.html')


def course(request, name = ''):
    # course = get_object_or_404(Class, name=name)
    user = {'id': '', 'name': 'Emily'}

    # Get class state if exists, else do a search
    if request.method == 'GET':
        # query DB for the course
        req = json.loads(request.body)
        courseAbbreviation = req.courseAbbreviation
        # get the lists of students and TAs, and make a dictionary from them
        resp = state[courseAbbreviation]
        resp['courseAbbreviation'] = courseAbbreviation
        return HttpResponse(content=json.dumps(resp)) # return a JSON from the dict

    # Modify session (queue) state based on ID of student/TA to join/leave
    elif request.method == 'POST':
        # modify DB with the course
        req = json.loads(request.body)
        courseAbbreviation = req.courseAbbreviation
        # modifying a session that does not exist yet; throw an error
        if not courseAbbreviation in state:
            return HttpResponseNotFound()
        queue = state[courseAbbreviation]
        # TODO do some action on the queue with the ID, name, and join/leave
        return render(request, 'class-student.html')

    # Create a session (queue) with a list of TAs
    elif request.method == 'PUT':
        # add new course to DB
        req = json.loads(request.body)
        courseAbbreviation = req.courseAbbreviation
        tas = req.teachingAssistants
        # TODO make a new QueueTA for each TA and add to a new ClassQueue object
        # newQueue = QueueTA(name="PLACEHOLDER", id=)
        # TODO add ClassQueue to the state
        pass

    # Delete a session (queue)
    elif request.method == 'DELETE':
        # remove course from DB
        req = json.loads(request.body)
        courseAbbreviation = req.courseAbbreviation
        if not courseAbbreviation in state: # make sure the course exists
            return HttpResponseNotFound()
        state.pop(courseAbbreviation) # remove the element from the state

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

