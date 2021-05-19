# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _


# Create your models here.

class ExtendUserInfo(models.Model):
    introduction = models.TextField(verbose_name="自我介绍")
    age = models.IntegerField(verbose_name='年龄')
    user = models.OneToOneField(User, verbose_name="看病医生", on_delete=models.CASCADE)


class Patient(models.Model):
    class Sex(models.TextChoices):
        MAN = 'MAN', _('男性')
        WOMAN = 'WOMAN', _('女性')

    name = models.CharField(verbose_name="姓名", max_length=255)
    sex = models.CharField(verbose_name="性别", max_length=5, choices=Sex.choices, default=Sex.MAN)
    phone_number = models.CharField(verbose_name="电话号码", max_length=255)
    age = models.IntegerField(verbose_name="年龄")
    address = models.CharField(verbose_name="家庭住址", max_length=255)

    def __str__(self):
        return self.name


class PatientFundusImage(models.Model):
    image_content = models.BinaryField(verbose_name="图片信息")
    image_result = models.TextField(verbose_name="图片检查结果")
    patient = models.ForeignKey(Patient, verbose_name="病人", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}: {}".format(self.patient.name, self.image_result)


class PatientCase(models.Model):
    patient = models.ForeignKey(Patient, verbose_name="病人", on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, verbose_name="看病医生", on_delete=models.CASCADE)
    sick_cause = models.CharField(verbose_name="病因", max_length=255)
    symptom = models.TextField(verbose_name="症状")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}-{}-{}".format(self.patient.name, self.doctor.username, self.sick_cause)
