from django.test import TestCase
from django.test import Client
from take_a_number.views import random_join_code
from typing import Dict
from take_a_number.models import Course
import uuid
import json


class JoinCodeTest(TestCase):
    def test_jc(self):
        code1 = random_join_code()
        valid = True
        for elem in code1:
            if not elem.isdigit() and not elem.isupper():
                valid = False
        self.assertEqual(True, valid)


class ViewsTest(TestCase):
    def test_course_create(self):
        c = Client()

        create_response = c.put('',
                                b'"{\\"description\\":\\"Algorithms\\",\\"abbreviation\\":\\"CS 3250\\",\\"email\\":\\"e@m.vanderbilt.edu\\"}"')
        self.assertEqual(create_response.status_code, 200)

        # can't register the same class twice
        create_response2 = c.put('',
                                b'"{\\"description\\":\\"Algorithms\\",\\"abbreviation\\":\\"CS 3250\\",\\"email\\":\\"e@m.vanderbilt.edu\\"}"')
        self.assertEqual(create_response2.status_code, 400)

    def test_identity(self):
        c = Client()

        create_response = c.put('', b'"{\\"description\\":\\"Algorithms\\",\\"abbreviation\\":\\"CS 3250\\",\\"email\\":\\"e@m.vanderbilt.edu\\"}"')
        course_id = json.loads(create_response.content)

        # id_response = c.get('{}/office_hours/identity'.format(course_id))
        # course_dict = json.loads(id_response.content)
        # self.assertEqual("Vanderbilt University", course_dict["school"])
        # self.assertEqual("Algorithms", course_dict["description"])
        # self.assertEqual("CS 3250", course_dict["abbreviation"])
        # self.assertEqual("e.m@vanderbilt.edu", course_dict["email"])

    def test_course_lookup(self):
        c = Client()

        create_response = c.put('',
                                b'"{\\"description\\":\\"ISD\\",\\"abbreviation\\":\\"CS 3251\\",\\"email\\":\\"e@m.vanderbilt.edu\\"}"')
        course_id = json.loads(create_response.content)

        lookup_response = c.get('')
        course_dict = json.loads(lookup_response.content)
        # full_course_dict = {c_id: val.__dict__ for c_id, val in course_dict[0].items()}
        self.assertEqual(course_dict[0]['id'], course_id)

    def test_students(self):
        return

    def test_course_teaching_assistants(self):
        return

    def test_office_hours(self):
        return





# TODO add tests for the views.py logic
#class ViewsTest(TestCase):
