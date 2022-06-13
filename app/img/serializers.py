"""
Serializers from images manager.
"""
from rest_framework import serializers
from core.models import ImgUpload


class ImageSerializer(serializers.ModelSerializer):
    """Upload original image serializer."""
    image = serializers.ImageField(required=True)

    class Meta:
        model = ImgUpload
        fields = ( 'image',)
