# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
import io
import tempfile

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from PIL import Image

from app.models import Patient, PatientCase, ExtendUserInfo, PatientFundusImage
from app.forms import PatientForm, PatientCaseForm, UploadDiagnoseFileForm, UserForm


@login_required(login_url="/login/")
def index(request):
    return render(request, "index.html")


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        template = loader.get_template('pages/' + load_template)
        return HttpResponse(template.render(context, request))
    except:
        template = loader.get_template('pages/error-404.html')
        return HttpResponse(template.render(context, request))


class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    paginate_by = 20
    template_name = "pages/patient-list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = PatientForm()
        return ctx

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        if getattr(self.request, '_post', None) and self.request._post.get('search'):
            return super().get_queryset().filter(name__icontains=self.request._post.get('search'))

        return super().get_queryset()


class PatientCaseListView(LoginRequiredMixin, ListView):
    model = PatientCase
    paginate_by = 20
    template_name = "pages/patientcase-list.html"

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        if getattr(self.request, '_post', None) and self.request._post.get('search'):
            return super().get_queryset().filter(patient__name__icontains=self.request._post.get('search'))

        return super().get_queryset()



class ImageListView(LoginRequiredMixin, ListView):
    model = PatientFundusImage
    paginate_by = 10
    template_name = "pages/image-list.html"


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = "pages/patient.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        cases = kwargs['object'].patientcase_set.order_by('-id').all()[:5]
        fundus = kwargs['object'].patientfundusimage_set.order_by('-id').all()[:5]
        ctx['form'] = PatientForm(instance=kwargs['object'])
        ctx['caseform'] = PatientCaseForm()
        ctx['diagnoseform'] = UploadDiagnoseFileForm()
        ctx['cases'] = cases
        ctx['fundus'] = fundus
        return ctx

    def post(self, request, *args, **kwargs):
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.pk = kwargs['pk']
            patient.save()
        return self.get(request, *args, **kwargs)


class PatientCaseDetailView(LoginRequiredMixin, DetailView):
    model = PatientCase
    template_name = "pages/patientcase.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = PatientCaseForm(instance=kwargs['object'])
        ctx['patient'] = kwargs['object'].patient
        return ctx

    def post(self, request, *args, **kwargs):
        form = PatientCaseForm(request.POST)
        if form.is_valid():
            patientcase = PatientCase.objects.get(pk=kwargs['pk'])
            patientcase.sick_cause = form.data['sick_cause']
            patientcase.symptom = form.data['symptom']
            patientcase.save()
        return self.get(request, *args, **kwargs)


class ImageDetailView(LoginRequiredMixin, DetailView):
    model = PatientFundusImage
    template_name = "pages/image.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['image_result'] = kwargs['object'].image_result
        ctx['patient'] = kwargs['object'].patient
        return ctx

    def post(self, request, *args, **kwargs):
        form = UploadDiagnoseFileForm(request.POST)
        if form.is_valid():
            image = PatientFundusImage.objects.get(pk=kwargs['pk'])
            image.image_content = form.data['image_content']
            image.image_result = form.data['image_result']
            image.save()
        return self.get(request, *args, **kwargs)


@login_required(login_url="/login/")
def add_patient_case(request, *args, **kwargs):
    form = PatientCaseForm(request.POST)
    if form.is_valid():
        patient = Patient.objects.get(pk=kwargs['pk'])
        patient_case = form.save(commit=False)
        patient_case.patient = patient
        patient_case.doctor = request.user
        patient_case.save()
    return redirect(reverse('patient-detail', kwargs=kwargs))


@login_required(login_url="/login/")
def add_patient(request, *args, **kwargs):
    form = PatientForm(request.POST)
    if form.is_valid():
        patient = form.save()
    return redirect(reverse('patient-list'))


@login_required(login_url="/login/")
def diagnose_image(request, *args, **kwargs):
    fundus_image = PatientFundusImage.objects.get(pk=kwargs['pk'])
    img = Image.open(io.BytesIO(fundus_image.image_content))
    response = HttpResponse(content_type='image/png')
    img.save(response, "PNG")
    return response


# 如果是文件
def handle_image_file(path):
    return "中度非增殖性糖尿病视网膜病变"


@login_required(login_url="/login/")
def diagnose(request, *args, **kwargs):
    form = UploadDiagnoseFileForm(request.POST, request.FILES)
    if request.method == 'POST':
        result = "暂无结果"
        if form.is_valid():
            UploadDiagnoseFileForm(request.FILES['file'])
            # 如果模型需要保存到文件才能调用
            with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
                for chunk in request.FILES['file']:
                    f.write(chunk)
                result = handle_image_file(f.name)
            # 如果可以直接用内存中的图片作为调用参数，可以直接拿request.FILES['file']
            return render(request, template_name="pages/diagnose.html", context={'form': form, 'check_result': result})
    return render(request, template_name="pages/diagnose.html", context={'form': form})


@login_required(login_url="/login/")
def patient_diagnose(request, *args, **kwargs):
    if request.method == 'POST':
        patient = Patient.objects.get(pk=kwargs['pk'])
        form = UploadDiagnoseFileForm(request.POST, request.FILES)
        result = "暂无结果"
        if form.is_valid():
            # 如果模型需要保存到文件才能调用
            img_byte_arr = io.BytesIO()
            with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
                for chunk in request.FILES['file']:
                    f.write(chunk)
                    img_byte_arr.write(chunk)
                result = handle_image_file(f.name)

                fundus = PatientFundusImage.objects.create(image_content=img_byte_arr.getvalue(), patient=patient, image_result=result)

            # 如果可以直接用内存中的图片作为调用参数，可以直接拿request.FILES['file']
    return redirect(reverse('patient-detail', kwargs=kwargs))


@login_required(login_url="/login/")
def profile_update(request):
    user = request.user

    try:
        extend_user_info = ExtendUserInfo.objects.get(user__pk=user.pk)
    except ExtendUserInfo.DoesNotExist:
        extend_user_info = ExtendUserInfo.objects.create(user=user, age=1, introduction="")

    if request.method == "POST":
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user.email = user_form.data['email']
            user.first_name = user_form.data['first_name']
            user.last_name = user_form.data['last_name']
            user.save()
            extend_user_info.introduction = user_form.data['introduction']
            extend_user_info.save()
        return redirect('/profile')
    else:
        user_form = UserForm(initial={'username': user.username, 'email': user.email,
                             'first_name': user.first_name, 'last_name': user.last_name, 'introduction': extend_user_info.introduction})
        return render(request, template_name='pages/profile.html', context={"user_form": user_form})
