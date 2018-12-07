# Objects which will go on the queue, holding the person's name and a unique ID
class QueueMember:
    def __init__(self, name, id, type = None):
        self.name = name
        self.id = id
        self.type = type

# TAs for each class, which will also be held in a ClassQueue object
class QueueTA:
    def __init__(self, name, id, type = None, helping = None):
        self.name = name
        self.id = id
        self.type = type
        self.helping = helping # helping contains the QueueMember being helped

    def getHelping(self):
        return self.helping

    def isHelping(self, rhs):
        return self.helping == rhs

    def isHelpingSomeone(self):
        return self.helping != None

    def stopHelping(self):
        self.helping = None

    def startHelping(self, helping):
        self.helping = helping


# Underlying queue which which be created for each class
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
        if tas is None:
            self.tas = [] # list of tas
        if studentSessions is None:
            self.studentSessions = {} # will hold map of QueueMember
        if taSessions is None:
            self.taSessions = {} # will hold map of QueueTA

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

    def hasStudents(self):
        return self.students != []

    def getStudentSessionIds(self):
        ret = []
        for student in self.studentSessions:
            ret.append(student.id)
        return ret

    def getTaSessionIds(self):
        ret = []
        for ta in self.taSessions:
            ret.append(ta.id)
        return ret

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