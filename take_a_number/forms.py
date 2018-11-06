from django import forms
from .models import Class
from django.core.validators import validate_email


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['instr_name', 'instr_email', 'school', 'course_name', 'keywords']

    def clean(self):
        email = self.cleaned_data.get('instr_email')
        try:
            validate_email(email)
        except validate_email.ValidationError:
            raise forms.ValidationError("Please enter a valid email address")
