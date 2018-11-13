from django.test import TestCase
from take_a_number.class_queue import ClassQueue
from take_a_number.class_queue import QueueMember

class QueueTest(TestCase):
    def create_member1(self, name="Name1", id=1):
        return QueueMember(name, id)

    def create_member2(self, name="Name2", id=2):
        return QueueMember(name, id)

    def create_member3(self, name="Name3", id=3):
        return QueueMember(name, id)

    def create_queue(self):
        return ClassQueue()

    def test_enqueue_dequeue(self):
        q = self.create_queue()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        self.assertEqual(1, q.dequeue())
        self.assertEqual(2, q.dequeue())
        self.assertEqual(3, q.dequeue())

    def test_getters(self):
        q = self.create_queue()
        self.assertEqual(0, q.size())
        self.assertEqual(True, q.isEmpty())

    def test_remove(self):
        q = self.create_queue()
        member1 = self.create_member1()
        member2 = self.create_member2()
        member3 = self.create_member3()
        q.enqueue(member1)
        q.enqueue(member2)
        q.enqueue(member3)
        self.assertEqual(member1, q.remove(member1.id))
        self.assertEqual(member3, q.remove(member3.id))
        self.assertEqual(member2, q.remove(member2.id))
        self.assertEqual(0, q.size())
        self.assertEqual(True, q.isEmpty())

    def test_status(self):
        q = self.create_queue()
        member1 = self.create_member1()
        member2 = self.create_member2()
        member3 = self.create_member3()
        q.enqueue(member1)
        q.enqueue(member2)
        q.enqueue(member3)
        self.assertEqual(0, q.position(member1.id))
        self.assertEqual(2, q.position(member3.id))
        self.assertEqual(1, q.position(member2.id))