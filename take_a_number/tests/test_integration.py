from django.test import TestCase
from django.test import Client
from take_a_number.views import random_join_code
from typing import Dict
from take_a_number.models import Course
import uuid


class JoinCodeTest(TestCase):
    def test_jc(self):
        code1 = random_join_code()
        valid = True
        for elem in code1:
            if not elem.isdigit() and not elem.isupper():
                valid = False
        self.assertEqual(True, valid)


class ViewsTest(TestCase):
    def test_identity(self):
        return

    def test_students(self):
        return

    def test_course_teaching_assistants(self):
        return

    def test_office_hours(self):
        return




# TODO add tests for the views.py logic
#class ViewsTest(TestCase):
