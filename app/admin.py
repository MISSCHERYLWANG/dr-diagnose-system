# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin

# Register your models here.

from .models import Patient, PatientCase, ExtendUserInfo, PatientFundusImage

admin.site.register(Patient)
admin.site.register(PatientCase)
admin.site.register(ExtendUserInfo)
admin.site.register(PatientFundusImage)
