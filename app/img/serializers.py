"""
Serializers from images manager.
"""
from rest_framework import serializers
from core.models import ImgUpload


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImgUpload
        fields = ( 'image',)