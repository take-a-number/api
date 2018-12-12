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
                                b'"{\\"description\\":\\"Algorithms\\",\\"abbreviation\\":\\"CS 3250\\",\\"email\\":\\"e@vanderbilt.edu\\"}"')
        self.assertEqual(create_response.status_code, 200)

        # can't register the same class twice
        create_response2 = c.put('',
                                b'"{\\"description\\":\\"Algorithms\\",\\"abbreviation\\":\\"CS 3250\\",\\"email\\":\\"e@vanderbilt.edu\\"}"')
        self.assertEqual(create_response2.status_code, 400)

        # course form submission missing a field
        create_response2 = c.put('',
                                 b'"{\\"description\\":\\"Algorithms\\",\\"email\\":\\"e@vanderbilt.edu\\"}"')
        self.assertEqual(create_response2.status_code, 400)

    # def test_identity(self):
    #     c = Client()
    #     session = c.session
    #     session['whoami'] = str(uuid.uuid4())
    #     session.save
    #
    #     create_response = c.put('', b'"{\\"description\\":\\"Algorithms\\",\\"abbreviation\\":\\"CS 3250\\",\\"email\\":\\"e@m.vanderbilt.edu\\"}"')
    #     course_id = json.loads(create_response.content)
    #
    #     id_response = c.get('/{}/office_hours/identity'.format(course_id))
    #     course_dict = json.loads(id_response.content)
    #     self.assertEqual("Vanderbilt University", course_dict["school"])
    #     self.assertEqual("Algorithms", course_dict["description"])
    #     self.assertEqual("CS 3250", course_dict["abbreviation"])
    #     self.assertEqual("e.m@vanderbilt.edu", course_dict["email"])

    def test_course_lookup(self):
        c = Client()
        create_response = c.put('',
                                b'"{\\"description\\":\\"ISD\\",\\"abbreviation\\":\\"CS 3251\\",\\"email\\":\\"e@vanderbilt.edu\\"}"')
        course_id = json.loads(create_response.content)

        lookup_response = c.get('')
        course_dict_list = json.loads(lookup_response.content)
        self.assertEqual(len(course_dict_list), 1)

        course_dict = course_dict_list[0]
        self.assertEqual(course_dict['id'], course_id)
        self.assertEqual(course_dict['school'], 'Vanderbilt University')
        self.assertEqual(course_dict['description'], 'ISD')
        self.assertEqual(course_dict['abbreviation'], 'CS 3251')
        self.assertEqual(course_dict['email'], 'e@vanderbilt.edu')


    def test_students(self):
        session = self.client.session
        session['whoami'] = str(uuid.uuid4())
        session.save
        return

    def test_course_teaching_assistants(self):
        return

    def test_office_hours(self):
        c = Client()
        create_response = c.put('',
                                b'"{\\"description\\":\\"ISD\\",\\"abbreviation\\":\\"CS 3251\\",\\"email\\":\\"e@vanderbilt.edu\\"}"')
        course_id = json.loads(create_response.content)

        # intial office hours configuration
        get_response = c.get('/{}/office_hours/'.format(course_id))
        office_hours = json.loads(get_response.content)
        self.assertEqual(office_hours, {"courseAbbreviation": "CS 3251",
                                        "teachingAssistants": [],
                                        "students": []})






# TODO add tests for the views.py logic
#class ViewsTest(TestCase):
