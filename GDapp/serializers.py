from rest_framework import serializers
from .models import RelatedImage, RelatedMask

class RelatedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedImage
        fields = ('id', 'image')


class RelatedMaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedMask
        fields = ('id', 'mask')


        