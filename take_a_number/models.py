from django.db import models
from django.contrib.sessions.backends.db import SessionStore as DBStore
from django.contrib.sessions.base_session import AbstractBaseSession



class Class(models.Model):
    instr_name = models.CharField(max_length=200, blank="")
    instr_email = models.EmailField(max_length=200, blank="")
    school = models.CharField(max_length=200, blank="")
    course_name = models.SlugField(max_length=200, blank="")
    keywords = models.CharField(max_length=500, blank="")

    # def get_class_data(self):
    #     return {
    #         'instr_name': self.instr_name,
    #         'instr_email': self.instr_email,
    #         'school': self.school,
    #         'course_name': self.course_name,
    #         'keywords': self.keywords
    #     }

class OfficeHoursSession(AbstractBaseSession):
    instructorCode = models.SlugField(max_length=6, default ="", db_index=True)
    studentCode = models.SlugField(max_length=6, default="", db_index=True)

    @classmethod
    def get_session_store_class(cls):
        return SessionStore


class SessionStore(DBStore):
    @classmethod
    def get_model_class(cls):
        return OfficeHoursSession

    def create_model_instance(self, data):
        obj = super.create_model_instance(data)
        try:
            instructor_code = '' # ?
            student_code = ''
        except (ValueError, TypeError):
            instructor_code, student_code = None
        obj.instructor_code = instructor_code
        obj.student_code = student_code
        return obj