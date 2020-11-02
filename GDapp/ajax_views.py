from rest_framework import viewsets
from .models import RelatedImage, RelatedMask
from .serializers import RelatedImageSerializer, RelatedMaskSerializer

class RelatedImageAJAXView(viewsets.ModelViewSet):
    serializer_class = RelatedImageSerializer
    queryset = RelatedImage.objects.all()

class RelatedMaskAJAXView(viewsets.ModelViewSet):
    serializer_class = RelatedMaskSerializer
    queryset = RelatedMask.objects.all()

