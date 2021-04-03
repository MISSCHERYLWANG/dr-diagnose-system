# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from app.models import Patient, PatientCase
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.template import loader
from django.http import HttpResponse

from .forms import PatientForm


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

        template = loader.get_template( 'pages/error-404.html' )
        return HttpResponse(template.render(context, request))



class PatientListView(ListView):
    model = Patient
    paginate_by = 20
    template_name = "pages/patient-list.html"

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        if getattr(self.request, '_post', None) and self.request._post.get('search'):
            return super().get_queryset().filter(name__icontains=self.request._post.get('search'))

        return super().get_queryset()


class PatientCaseListView(ListView):
    model = PatientCase
    paginate_by = 10
    template_name = "pages/patientcase-list.html"


class PatientDetailView(DetailView):
    model = Patient
    template_name = "pages/patient.html"


    def get_context_data(self, **kwargs):        
        ctx = super().get_context_data(**kwargs)
        cases = kwargs['object'].patientcase_set.order_by('-id').all()[:5]
        ctx['form'] = PatientForm(instance=kwargs['object'])
        ctx['cases'] = cases
        return ctx

    def post(self, request, *args, **kwargs):
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.pk = kwargs['pk']
            patient.save()
        return self.get(request, *args, **kwargs)