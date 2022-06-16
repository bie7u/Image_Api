"""
Serializers from images manager.
"""
from rest_framework import serializers
from core.models import ImgUpload, TimeGenerateImg


class ImageSerializer(serializers.ModelSerializer):
    """Upload original image serializer."""
    image = serializers.ImageField(required=True)

    class Meta:
        model = ImgUpload
        fields = ('image',)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['image'] = 'The image uploaded.'
        return ret


class TimeGenerateImgSerializer(serializers.ModelSerializer):
    """Create a expiry image serializer."""

    class Meta:
        model = TimeGenerateImg
        fields = ('original_image', 'image_type', 'time_of_expiry')
