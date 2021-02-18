from GDapp.tasks import celery_timer_task, run_gold_digger_task
from GDapp.prediction.FrontEndUpdater import FrontEndUpdater
from GDapp.apps import GdappConfig
from django.shortcuts import render, redirect
from .forms import EMImageForm, LocalFilesForm
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.views.generic.list import ListView
import csv
from django.http import HttpResponse
from .models import EMImage, MyChunkedUpload, MyChunkedMaskUpload, add_image
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from django.views.generic import ListView
import os
from celery import chain


import sys
import logging

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': '/tmp/debug.log'
        },
        #'celery': {
        #    'level': 'DEBUG',
        #    'class': 'logging.handlers.RotatingFileHandler',
        #    'filename': 'celery.log',
        #    'formatter': 'simple',
        #    'maxBytes': 1024 * 1024 * 100,  # 100 mb
        #},
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
        ##'celery': {
        ##    'handlers': ['celery', 'console'],
        ##    'level': 'DEBUG',
        ##},
        'django.utils.autoreload': {
            'level': 'INFO',
        },
        'daphne.http_protocol': {
            'level': 'INFO',
        },
        'django.db.backends': {
            'level': 'INFO',
        },
        'daphne.ws_protocol': {
            'level': 'INFO',
        },

    }
})

logger = logging.getLogger(__name__)


class MyChunkedUploadView(ChunkedUploadView):

    model = MyChunkedUpload
    field_name = 'the_file'

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass


class MyChunkedUploadCompleteView(ChunkedUploadCompleteView):

    model = MyChunkedUpload

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass

    def on_completion(self, uploaded_file, request):
        # Do something with the uploaded file. E.g.:
        # * Store the uploaded file on another model:
        # SomeModel.objects.create(user=request.user, file=uploaded_file)
        instance = EMImage.objects.create(image=uploaded_file)
        self.pk = instance.id
        instance.save()
        # * Pass it as an argument to a function:
        # function_that_process_file(uploaded_file)
        # print(request.POST)

    def get_response_data(self, chunked_upload, request):
        # form = EMImageForm(instance=self.instance)
        # return render(request, "GDapp/upload.html", {'form': form})
        # print(request.POST)
        return {'message': ("You successfully uploaded '%s' (%s bytes)!" %
                            (chunked_upload.filename, chunked_upload.offset)),
                'upload_id': chunked_upload.upload_id,
                'filename': chunked_upload.filename,
                'pk': self.pk}


class MyChunkedMaskUploadView(ChunkedUploadView):

    model = MyChunkedMaskUpload
    field_name = 'the_mask'

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass


class MyChunkedMaskUploadCompleteView(ChunkedUploadCompleteView):

    model = MyChunkedMaskUpload

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass

    def on_completion(self, uploaded_file, request):
        obj = EMImage.objects.get(pk=request.POST['pk'])
        obj.mask = uploaded_file
        obj.save()

        print(request.POST)

    def get_response_data(self, chunked_upload, request):
        return {'message': ("You successfully uploaded '%s' (%s bytes)!" %
                            (chunked_upload.filename, chunked_upload.offset)),
                'upload_id': chunked_upload.upload_id,
                'filename': chunked_upload.filename}


class RunListView(ListView):
    model = EMImage
    context_object_name = 'run_list'
    queryset = EMImage.objects.exclude(analyzed_image='').order_by('-id')
    template_name = 'runs.html'


def home(request):
    logger.debug("homepage accessed")
    return render(request, 'GDapp/home.html')

def populate_em_obj(obj, form):
    obj.trained_model = form.cleaned_data['trained_model']
    obj.particle_groups = form.cleaned_data['particle_groups']
    obj.threshold_string = form.cleaned_data['threshold_string']
    return obj

def create_single_local_image_obj(form, local_files_form, image_path=None):
    obj = form.save(commit=False)
    if image_path:
        obj.local_image = image_path
    else:
        obj.local_image = local_files_form.cleaned_data["local_image"]
    obj.local_mask = local_files_form.cleaned_data["local_mask"]
    obj = populate_em_obj(obj, form)
    obj.pk = None
    obj.id = None
    obj.save()
    return obj

    
def load_all_images_from_dir(form, local_files_form):
    dir_path = local_files_form.cleaned_data["local_image"]
    logger.debug(f"directory path: {dir_path}")
    files = os.listdir(dir_path)
    logger.debug(files)
    pk_list = []
    for f in files:
        file_path = os.path.join(dir_path, f)
        logger.debug(f"local_image (path): (in load all images from dir) {file_path}")
        obj = create_single_local_image_obj(form, local_files_form, image_path=file_path)
        log_obj(obj)
        pk_list.append(obj.id)
    return pk_list

def chunked_file_upload(form):
        obj = EMImage.objects.get(pk=form.cleaned_data['preloaded_pk'])
        #moved these inside the if statement
        obj.trained_model = form.cleaned_data['trained_model']
        obj.particle_groups = form.cleaned_data['particle_groups']
        obj.threshold_string = form.cleaned_data['threshold_string']
        obj.save()
        return obj

def image_view(request):
    if request.method == 'POST':
        form = EMImageForm(request.POST, request.FILES)
        local_files_form = LocalFilesForm(request.POST)
        if form.is_valid() and local_files_form.is_valid() and not (local_files_form.cleaned_data["local_image"] == "" and form.cleaned_data["preloaded_pk"] == ""):
            if form.cleaned_data['preloaded_pk'] == '': # local file used
                if os.path.isfile(local_files_form.cleaned_data["local_image"]):  #if single file (not directory)
                    logger.debug("SINGLE FILE INPUT")
                    obj = create_single_local_image_obj(form, local_files_form)
                elif os.path.isdir(local_files_form.cleaned_data["local_image"]):
                    logger.debug("DIRECTORY INPUT")
                    pk_list = load_all_images_from_dir(form, local_files_form)
                    return run_gd(request, {'pk': pk_list})
            else: # chunked file upload
                obj = chunked_file_upload(form)
            logger.debug("form valid, object saved")
            return run_gd(request, {'pk': obj.id})
    else:
        form = EMImageForm()
        local_files_form = LocalFilesForm()
        logger.debug("form not valid")
    return render(request, 'GDapp/upload.html', {'form': form, 'local_files_form': local_files_form})


def run_gd(request, inputs):
    pk = inputs['pk']
    gold_digger_queue = GdappConfig.gold_particle_detector
    if type(pk) == list:
        tasks = []
        for pk_single in pk:
            tasks.append(run_gold_digger_task.si(pk_single))
        chain(*tasks)()
        return render(request, 'GDapp/run_gd.html', {'pk': pk_single})
    else:
        gold_digger_queue(pk)
        logger.debug("inside run_gd function")
        return render(request, 'GDapp/run_gd.html', {'pk': pk})
 


# attempt to make a downloadable csv
def export(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)

def log_obj(obj):
        logger.debug(f"local_image (path): {obj.local_image}")
        logger.debug(f"trained_model: {obj.trained_model}")
        logger.debug(f"particle_groups: {obj.particle_groups}")
        logger.debug(f"threshold_string: {obj.threshold_string}")
        try:
            logger.debug(f"id: {obj.id}") #always prints "None" ... why?
            logger.debug(f"pk: {obj.id}") #always prints "None" ... why?
        except:
            logger.debug(f"could not print obj.id")
            