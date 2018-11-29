from django import forms
# from .models import Course
# from django.core.validators import validate_email


# class CourseForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = ['instr_name', 'instr_email',
#                   'school', 'course_name', 'keywords']

#     def clean(self):
#         email = self.cleaned_data.get('instr_email')
#         try:
#             validate_email(email)
#         except:
#             raise forms.ValidationError("Please enter a valid email address")
