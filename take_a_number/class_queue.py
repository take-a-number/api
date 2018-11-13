# Objects which will go on the queue, holding the person's name and a unique ID
class QueueMember:
    def __init__(self, name, id):
        self.name = name
        self.id = id


# Underlying queue which which be created for each class
class ClassQueue:
    def __init__(self):
        self.items = []

    # Check whether the ClassQueue is empty
    def isEmpty(self):
        return self.items == []

    # Add a student to the end of the ClassQueue
    def enqueue(self, item):
        self.items.append(item)

    # Remove the student from the beginning of the ClassQueue
    def dequeue(self):
        return self.items.pop(0)

    # Get the size of the ClassQueue
    def size(self):
        return len(self.items)

    # Remove a student from the ClassQueue by ID
    def remove(self, id):
        i = 0
        while i < len(self.items):
            if self.items[i].id == id:
                return self.items.pop(i)
            i+=1
        return -1 # did not find the student

    # Get how many students preceded someone in the queue, based on ID
    def position(self, id):
        i = 0
        while i < len(self.items):
            if self.items[i].id == id:
                return i
            i+=1
        return -1 # did not find the student

