# Objects which will go on the queue, holding the person's name and a unique ID
class QueueMember:
    def __init__(self, name, id, type = None):
        self.name = name
        self.id = id
        self.type = type

    # return the student as a dictionary, to be used with json response
    def asDict(self):
        return {
            'name': self.name,
            'id': self.id,
            'type': self.type
        }

# TAs for each class, which will also be held in a ClassQueue object
class QueueTA:
    def __init__(self, name, id, type = None, helping = None):
        self.name = name
        self.id = id
        self.type = type
        self.helping = helping # helping contains the QueueMember being helped

    # get the student who is being helped
    def getHelping(self):
        return self.helping

    # check whether ta is helping a particular student
    def isHelping(self, rhs):
        return self.helping == rhs

    # check whether ta is helping anyone
    def isHelpingSomeone(self):
        return self.helping != None

    # indicate that the ta is no longer helping anyone
    def stopHelping(self):
        self.helping = None

    # indicate that the ta is now helping someone else
    def startHelping(self, helping):
        self.helping = helping

    # return the ta as a dictionary, to be used in json response
    def asDict(self):
        if self.helping == None:
            helpingDict = None
        else:
            helpingDict = self.helping.asDict()
        return {
            'name': self.name,
            'id': self.id,
            'type': self.type,
            'helping': helpingDict
        }


# Underlying queue which which be created for each class
# Note: not all of this functionality is currently being used in production
class ClassQueue:
    # default arguments must be "None" to fix issue with mutable default args
    def __init__(self, courseAbbrev = None, studentJoinCode = None, students = None,
                 tas = None, studentSessions = None, taSessions = None):
        # uuid of the course, which the frontend is aware of
        self.courseAbbreviation = courseAbbrev
        # student join code
        self.studentJoinCode = studentJoinCode
        if students is None:
            self.students = [] # list (queue) of students
        else:
            self.students = students
        if tas is None:
            self.tas = [] # list of tas
        else:
            self.tas = tas
        if studentSessions is None:
            self.studentSessions = {} # will hold map of QueueMember
        else:
            self.studentSessions = studentSessions
        if taSessions is None:
            self.taSessions = {} # will hold map of QueueTA
        else:
            self.taSessions = taSessions

    # Check whether the ClassQueue is empty
    def isEmpty(self):
        return self.students == []

    # get the number of students
    def studentCount(self):
        return len(self.students)

    # get the number of tas
    def taCount(self):
        return len(self.tas)

    # Check whether the ClassQueue has any TAs
    def hasTas(self):
        return self.tas != []

    # check whether the queue is nonempty
    def hasStudents(self):
        return self.students != []

    # get a list of the students with course sessions by id
    def getStudentSessionIds(self):
        ret = []
        for id, student in self.studentSessions:
            ret.append(id)
        return ret

    # get a list of the tas with course sessions by id
    def getTaSessionIds(self):
        ret = []
        for ta in self.taSessions:
            ret.append(ta.id)
        return ret

    # return the class queue's students and tas as a dictionary
    def asDict(self):
        resp = {}
        resp['students'] = self.students
        resp['teachingAssistants'] = self.tas
        return resp

    # Add a TA to the class (object of type QueueTA)
    def addTA(self, ta):
        self.tas.append(ta)

    # Remove a TA from the class by ID
    def removeTA(self, taId):
        i = 0
        while i < len(self.tas):
            if self.tas[i].id == taId:
                return self.tas.pop(i)
            i += 1
        return -1  # did not find the TA

    # Add a student to the end of the ClassQueue (object of type QueueStudent)
    def enqueue(self, student):
        self.students.append(student)

    # Remove the student from the beginning of the ClassQueue
    def dequeue(self):
        return self.students.pop(0)

    # Get the size of the ClassQueue
    def size(self):
        return len(self.students)

    # Remove a student from the ClassQueue by ID
    def removeStudent(self, studentId):
        i = 0
        while i < len(self.students):
            if self.students[i].id == studentId:
                return self.students.pop(i)
            i += 1
        return -1  # did not find the student

    # Get how many students preceded someone in the queue, based on ID
    def position(self, studentId):
        i = 0
        while i < len(self.students):
            if self.students[i].id == studentId:
                return i
            i += 1
        return -1  # did not find the student