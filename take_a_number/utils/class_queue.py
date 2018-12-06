# Objects which will go on the queue, holding the person's name and a unique ID
class QueueMember:
    def __init__(self, name, id):
        self.name = name
        self.id = id

class QueueTA:
    def __init__(self, name, id):
        self.name = name
        self.id = id

# Underlying queue which which be created for each class
class ClassQueue:
    def __init__(self):
        self.students = []
        self.tas = []

    # Check whether the ClassQueue is empty
    def isEmpty(self):
        return self.students == []

    # Check whether the ClassQueue has any TAs
    def hasTas(self):
        return self.tas != []

    def getTas(self):
        return self.tas

    def hasStudents(self):
        return self.students != []

    def getStudents(self):
        return self.students

    def asDict(self):
        resp = {}
        resp['students'] = self.getStudents()
        resp['teachingAssistants'] = self.getTas()
        return resp

    # Add a TA to the class (object of type QueueTA)
    def addTA(self, ta):
        self.students.append(ta)

    # Remove a TA from the class by ID
    def removeTA(self, taId):
        i = 0
        while i < len(self.tas):
            if self.students[i].id == taId:
                return self.students.pop(i)
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