from django.db import models



class Class(models.Model):
    instr_name = models.CharField(max_length=200, blank="")
    instr_email = models.EmailField(max_length=200, blank="")
    school = models.CharField(max_length=200, blank="")
    course_name = models.SlugField(max_length=200, blank="")
    keywords = models.CharField(max_length=500, blank="")