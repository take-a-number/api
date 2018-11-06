from django.db import models


class Class(models.model):
    instr_name = models.CharField(max_length=200, blank="")
    instr_email = models.CharField(max_length=200, blank="")
    school = models.CharField(max_length=200, blank="")
    course_name = models.CharField(max_length=200, blank="")
    term = models.CharField(max_length=200, blank="")
    keywords = models.CharField(max_length=500, blank="")