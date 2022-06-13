from crypt import methods
from distutils.command.upload import upload
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiTypes


from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins, status
from rest_framework.parsers import MultiPartParser, FormParser

from PIL import Image

from datetime import datetime

from rest_framework.generics import ListAPIView
import json
from django.http import Http404, HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.core.files.images import ImageFile


from .serializers import ImageSerializer
from core import models


from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

class ImageViewSet(
                   viewsets.GenericViewSet):
    """Manage a image in APIs."""
    serializer_class = ImageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='yours_images', url_name="yours_images") #not test !!!!
    def yours_images(self, request):
        """Return a user images."""
        queryset = models.ImgUpload.objects.filter(user=request.user)
        user_files = {}
        for img in queryset:
            name_of_file = img.image.path.split('__file_name--')[1]
            user_files[f'image_id={img.id}'] = name_of_file

        return JsonResponse(user_files)

    @action(detail=False, methods=['get'], url_path='links_to_images',)
    def links_to_images(self, request):
        """Return a links to images in dependences from a user group."""
        return Response({'something': 'my custom JSON'})


class UploadImageViewset(mixins.CreateModelMixin, # not test!!!
                         viewsets.GenericViewSet):

    serializer_class = ImageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer): # not test!!!
        """Upload image."""
        serializer.save(user=self.request.user)
        models.UserManager.create_thumbnail(self, serializer)



