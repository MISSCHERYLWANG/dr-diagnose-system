from django import forms
from django.contrib.auth.models import User
from .models import Patient, PatientCase


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name',
                  'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff']


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'sex', 'age', 'phone_number', 'address']


class PatientCaseForm(forms.ModelForm):
    class Meta:
        model = PatientCase
        fields = ['sick_cause', 'symptom']


class UploadDiagnoseFileForm(forms.Form):
    file = forms.ImageField()
