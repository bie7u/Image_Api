"""
Forms to admin panel.
"""
from django import forms

from core.models import ImgThumbnail, TimeGenerateImg


class ImgThumbnailAdminForm(forms.ModelForm):
    """Create a admin thumbnail form with custom width and height"""
    width = forms.IntegerField()
    height = forms.IntegerField()
    image = forms.ImageField(required=False)

    class Meta:
        model = ImgThumbnail
        fields = '__all__'
        exclude = ['user', 'image', 'image_type']


class TimeGenerateImgAdminForm(forms.ModelForm):
    """Create a expiry image by admin - form."""
    image = forms.ImageField(required=False)

    class Meta:
        model = TimeGenerateImg
        fields = '__all__'
        exclude = ['user', 'image']
