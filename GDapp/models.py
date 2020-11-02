import os
from django.db import models
from django import forms
from django.core.validators import MinValueValidator
from django.core.files import File

TRAINED_MODEL_CHOICES = [
    ('43kGoldDigger', '43kGoldDigger'),
    ('87kGoldDigger', '87kGoldDigger')
]

# async image upload form follows this tutorial:
# https://medium.com/@adamking0126/asynchronous-file-uploads-with-django-forms-b741720dc952


class RelatedImage(models.Model):
    image = models.FileField(upload_to="Input/")

    def __unicode__(self):
        return self.image.url


class RelatedMask(models.Model):
    mask = models.FileField(upload_to="Mask/", blank=True)

    def __unicode__(self):
        return self.mask.url


class GoldParticleData(models.Model):
    particle_groups = models.IntegerField(
        blank=False, default=1, validators=[MinValueValidator(1)])
    trained_model = models.CharField(max_length=100,
                                     blank=False,
                                     default='87kGoldDigger',
                                     choices=TRAINED_MODEL_CHOICES)
    gold_particle_coordinates = models.FileField(
        upload_to="analyzed/coordinates", null=True)
    analyzed_image = models.ImageField(
        upload_to="analyzed/images", null=True)
    histogram_image = models.ImageField(
        upload_to="analyzed/histograms", null=True)


class GoldParticleDataImage(models.Model):
    image = models.ForeignKey(RelatedImage, on_delete=models.CASCADE)
    mask = models.ForeignKey(RelatedMask, on_delete=models.CASCADE)
    gold_particle_data = models.ForeignKey(
        GoldParticleData, on_delete=models.CASCADE)


def get_data_dict(pk):
    data = GoldParticleDataImage.objects.select_related(
        'gold_particle_data').get(pk=pk)
    image = GoldParticleDataImage.objects.select_related('image').get(pk=pk)
    mask = GoldParticleDataImage.objects.select_related('mask').get(pk=pk)
    results = {
        'particle_groups': data.particle_groups,
        'trained_model': data.trained_model,
        'gold_particle_coordinates': data.gold_particle_coordinates,
        'histogram_image': data.histogram_image,
        'analyzed_image': data.analyzed_image,
        'mask': mask,
        'image': image,
    }
    return results


def add_histogram_image(pk, url):
    # gd_data = EMImage.objects.get(pk=pk)
    gd_data = GoldParticleDataImage.objects.select_related(
        'gold_particle_data').get(pk=pk)
    temp_image = File(open(url, "rb"))
    _, ext = os.path.splitext(url)
    gd_data.histogram_image.save(f'histogram_{pk}{ext}', temp_image)


def add_analyzed_image(pk, url):
    # gd_data = EMImage.objects.get(pk=pk)
    gd_data = GoldParticleDataImage.objects.select_related(
        'gold_particle_data').get(pk=pk)
    temp_image = File(open(url, "rb"))
    _, ext = os.path.splitext(url)
    gd_data.analyzed_image.save(f'image_{pk}{ext}', temp_image)


def add_gold_particle_coordinates(pk, url):
    # gd_data = EMImage.objects.get(pk=pk)
    gd_data = GoldParticleDataImage.objects.select_related(
        'gold_particle_data').get(pk=pk)
    temp_file = File(open(url, "rb"))
    gd_data.gold_particle_coordinates.save(f'coordinates_{pk}_.csv', temp_file)


def get_histogram_image_url(pk):
    gd_data = GoldParticleDataImage.objects.select_related(
        'gold_particle_data').get(pk=pk)
    # gd_data = EMImage.objects.get(pk=pk)
    return gd_data.histogram_image.url


def get_analyzed_image_url(pk):
    gd_data = GoldParticleDataImage.objects.select_related(
        'gold_particle_data').get(pk=pk)
    # gd_data = EMImage.objects.get(pk=pk)
    return gd_data.analyzed_image.url


def get_gold_particle_coordinates_url(pk):
    gd_data = GoldParticleDataImage.objects.select_related(
        'gold_particle_data').get(pk=pk)
    # gd_data = EMImage.objects.get(pk=pk)
    return gd_data.gold_particle_coordinates.url
