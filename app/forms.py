from django import forms

from .models import Patient, PatientCase

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'sex', 'age', 'phone_number', 'address']


class PatientCaseForm(forms.ModelForm):
    class Meta:
        model = PatientCase
        fields = ['sick_cause', 'symptom']
