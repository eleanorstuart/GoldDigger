from django import forms
from .models import *

# async upload form done by this tutorial:
# https://medium.com/@adamking0126/asynchronous-file-uploads-with-django-forms-b741720dc952


class GoldParticleDataForm(forms.ModelForm):

    image = forms.ModelChoiceField(
        queryset=RelatedImage.objects.all(), required=False)

    mask = forms.ModelChoiceField(
        queryset=RelatedMask.objects.all(), required=False)


    class Meta:
        model = GoldParticleData
        fields = ['trained_model', 'particle_groups']

    def __init__(self, *args, **kwargs):
        super(GoldParticleDataForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['image'].initial = RelatedImage.objects.get(
                goldparticledataimage__gold_particle_data=self.instance).values_list('id', flat=True)
            self.fields['mask'].initial = RelatedMask.objects.get(
                goldparticledataimage__gold_particle_data=self.instance).values_list('id', flat=True)

    def save(self, commit=True):
        super(GoldParticleDataForm, self).save(commit)
        image = self.cleaned_data.pop('image', None)
        mask = self.cleaned_data.pop('mask', None)
        if image:
            self.instance.goldparticledataimage.delete()
            GoldParticleDataImage.objects.create(
                gold_particle_data=self.instance, image=image, mask=mask)
