# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    path('patient/<int:pk>', views.PatientDetailView.as_view(), name='patient-detail'),
    path('patients', views.PatientListView.as_view(), name='patient-list'),
    path('patient/add', views.add_patient, name='add-patient'),
    path('patient/<int:pk>/case', views.add_patient_case, name='add-patient-case'),
    path('patient/<int:pk>/diagnose', views.patient_diagnose, name='add-patient-case'),
    path('diagnose_image/<int:pk>', views.diagnose_image, name='diagnose_image'),
    path('patientcase/<int:pk>', views.PatientCaseDetailView.as_view(), name='patientcase-detail'),
    path('patientCases', views.PatientCaseListView.as_view(), name='patientcase-list'),
    path('diagnose', views.diagnose, name='diagnose'),
    path('profile', views.profile_update, name="edit_profile"),
    path('patient_images', views.ImageListView.as_view(), name='patient-images-list'),
    path('image/<int:pk>', views.ImageDetailView.as_view(), name='patient-image-detail'),

    re_path(r'^.*\.html', views.pages, name='pages'),

    # The home page
    path('', views.index, name='home'),
]
