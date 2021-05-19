from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import Textarea
from .models import Patient, PatientCase


class UserForm(forms.ModelForm):
    introduction = forms.CharField(widget=Textarea)
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field_key, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'sex', 'age', 'phone_number', 'address']

    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        for field_key, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class PatientCaseForm(forms.ModelForm):
    class Meta:
        model = PatientCase
        fields = ['sick_cause', 'symptom']

    def __init__(self, *args, **kwargs):
        super(PatientCaseForm, self).__init__(*args, **kwargs)
        for field_key, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class UploadDiagnoseFileForm(forms.Form):
    file = forms.ImageField()
