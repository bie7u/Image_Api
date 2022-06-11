from distutils.command.upload import upload
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiTypes
from django import views
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins, status
from rest_framework.parsers import MultiPartParser, FormParser


from datetime import datetime

from rest_framework.generics import ListAPIView
import json
from django.http import HttpResponse

from .serializers import ImageSerializer
from core import models

class ImageViewSet(
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """Manage a image in APIs."""
    serializer_class = ImageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = models.ImgUpload.objects.filter(user=self.request.user)
        return queryset


class UploadImageViewset(
                        mixins.CreateModelMixin,
                        viewsets.GenericViewSet,):

    serializer_class = ImageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
