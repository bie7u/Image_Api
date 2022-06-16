"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from datetime import timedelta

from core import models

from app.forms import ImgThumbnailAdminForm, TimeGenerateImgAdminForm

from core.functions import get_height

class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
            )
        }),
    )


class ImgThumbnailAdmin(admin.ModelAdmin):
    """Custom thumbnail by admin."""
    form = ImgThumbnailAdminForm
    list_display = ('user', 'image_type', 'original_image_id', 'get_link')

    def __init__(self, model, admin_site):
        self.request = None
        super().__init__(model, admin_site)

    def get_queryset(self, request):
        self.request = request
        return super().get_queryset(request)

    def get_link(self, obj):
        link = self.request.build_absolute_uri(obj.image.url)
        return format_html('<a href={}>{}</a>', link, link)

    readonly_fields = ['image', 'added_at']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        original_image = form.cleaned_data['original_image']
        image_path = form.cleaned_data['original_image'].image
        model = models.ImgThumbnail
        width = form.cleaned_data['width']
        height = form.cleaned_data['height']

        models.CustomImage.make_thumbnail(self=request,
                                          height=height,
                                          image_type=None,
                                          width=width,
                                          original_image=original_image,
                                          image_path=image_path,
                                          model=model,
                                          user=request.user)


class TimeGenerateImageAdmin(admin.ModelAdmin):
    """Generate expiry image by admin."""
    form = TimeGenerateImgAdminForm
    readonly_fields = ['image', 'added_at']
    list_display = ('user', 'image_type', 'original_image_id', 'get_link', 'expiry_hour')

    def __init__(self, model, admin_site):
        self.request = None
        super().__init__(model, admin_site)

    def get_queryset(self, request):
        self.request = request
        return super().get_queryset(request)

    def get_link(self, obj):
        link = self.request.build_absolute_uri(obj.image.url)
        return format_html('<a href={}>{}</a>', link, link)

    def expiry_hour(self, obj):
        return obj.added_at + timedelta(seconds=obj.time_of_expiry)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        original_image = form.cleaned_data['original_image']
        image_path = form.cleaned_data['original_image'].image
        image_type = form.cleaned_data['image_type']
        time_of_expiry = form.cleaned_data['time_of_expiry']
        model = models.TimeGenerateImg

        models.CustomImage.make_thumbnail(self=request,
                                          height=get_height(image_type),
                                          image_type=image_type,
                                          original_image=original_image,
                                          image_path=image_path,
                                          model=model,
                                          user=request.user,
                                          time_of_expiry=time_of_expiry,)


class OriginalImageAdmin(admin.ModelAdmin):
    """Show urls to original image."""
    date_hierarchy = 'added_at'
    list_display = ('user','get_link', 'added_at', 'id')

    def __init__(self, model, admin_site):
        self.request = None
        super().__init__(model, admin_site)

    def get_queryset(self, request):
        self.request = request
        return super().get_queryset(request)

    def get_link(self, obj):
        link = self.request.build_absolute_uri(obj.image.url)
        return format_html('<a href={}>{}</a>', link, link)


admin.site.register(models.ImgUpload, OriginalImageAdmin)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.ImgThumbnail, ImgThumbnailAdmin)
admin.site.register(models.TimeGenerateImg, TimeGenerateImageAdmin)
