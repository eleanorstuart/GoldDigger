from GDapp.tasks import celery_timer_task
from GDapp.prediction.FrontEndUpdater import FrontEndUpdater
from GDapp.apps import GdappConfig
from django.shortcuts import render, redirect
from .forms import GoldParticleDataForm
from django.core.files.storage import FileSystemStorage

import csv
from django.http import HttpResponse
from .models import GoldParticleDataImage

import sys

def home(request):
    return render(request, 'GDapp/home.html')


def image_view(request):
    if request.method == 'POST':
        form = GoldParticleDataForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            return run_gd(request, {'pk': instance.id})
    else:
        form = GoldParticleDataForm()
    return render(request, 'GDapp/upload.html', {'form': form})


def run_gd(request, inputs):
    pk = inputs['pk']
    gold_digger = GdappConfig.gold_particle_detector
    gold_digger(pk)
    return render(request, 'GDapp/run_gd.html', {'pk': pk})
