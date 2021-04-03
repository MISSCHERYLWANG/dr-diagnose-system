from django import forms

from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('name', 'sex', 'age', 'phone_number', 'address')

# class PatientForm(forms.Form):
#     name = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 "placeholder": "PatientName",
#                 "class": "form-control"
#             }
#         ))
#     sex = forms.ChoiceField(choices=Patient.Sex.choices)
#     age = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 "placeholder": "age",
#                 "class": "form-control"
#             }
#         ))
#     phone_number = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 "placeholder": "phoneNumber",
#                 "class": "form-control"
#             }
#         ))
#     address = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 "placeholder": "phoneNumber",
#                 "class": "form-control"
#             }
#         ))
