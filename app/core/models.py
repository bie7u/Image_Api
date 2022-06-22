"""
Database models.
"""
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from django.core.files.temp import NamedTemporaryFile
from django.core.files.images import ImageFile
from django.core.validators import MaxValueValidator, MinValueValidator

from PIL import Image


KIND_OF_IMAGE = (
        ('1', 'original'),
        ('2', '200px'),
        ('3', '400px'),
    )


def image_file_path(instance, filename):
    """Generate file path for new image."""
    ext = os.path.basename(filename)
    filename = f"unique_id--{uuid.uuid4()}__file_name--{ext}"

    return os.path.join('uploads', 'user', filename)


class CustomImage:
    """Methods use to custom image."""

    def make_thumbnail(self, image_type,
                       original_image, image_path,
                       model, user,
                       width=None, height=None, **params):
        """Create a thumbnail with special parameters."""
        with NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.open(f"/vol/web/media/{str(image_path)}")
            if img.mode != 'RGB':
                img = img.convert('RGB')
            if width is None:
                width = img.size[0]
            else:
                width = width
            if height is None:
                height = img.size[1]
            else:
                height = height

            img = img.resize((width, height), Image.ANTIALIAS)
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            convert_image = model.objects.create(user=user,
                                                 original_image=original_image,
                                                 image=ImageFile(image_file),
                                                 image_type=image_type,
                                                 **params)
            convert_image.save()
            return convert_image

    def create_thumbnail_while_upload(self, serializer, user):
        """Create a thumbnail when uploaded a new image."""
        original_image = serializer.instance
        image_path = serializer.instance.image

        if str(self.request.user.groups.get()) == 'Basic':
            CustomImage.make_thumbnail(self,
                                       height=200,
                                       image_type=2,
                                       original_image=original_image,
                                       image_path=image_path,
                                       model=ImgThumbnail,
                                       user=user)
        elif str(self.request.user.groups.get()) == 'Premium' or 'Enterprise':
            CustomImage.make_thumbnail(self,
                                       height=200,
                                       image_type=2,
                                       original_image=original_image,
                                       image_path=image_path,
                                       model=ImgThumbnail,
                                       user=user)
            CustomImage.make_thumbnail(self,
                                       height=400,
                                       image_type=3,
                                       original_image=original_image,
                                       image_path=image_path,
                                       model=ImgThumbnail,
                                       user=user)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class ImgUpload(models.Model):
    """Image model."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, upload_to=image_file_path)

    def __str__(self):
        return str(self.user) + ' ' + str(self.id)


class ImgThumbnail(models.Model):
    """Image thumbnail model."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    original_image = models.ForeignKey(ImgUpload, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to=image_file_path)
    image_type = models.CharField(null=True,
                                  blank=True,
                                  max_length=255,
                                  choices=KIND_OF_IMAGE,
                                  default=KIND_OF_IMAGE[0][0])
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + ' ' + str(self.image_type)


class TimeGenerateImg(models.Model):
    """Image generate for particular seconds"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    original_image = models.ForeignKey(ImgUpload, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to=image_file_path)
    image_type = models.CharField(null=True,
                                  blank=True,
                                  max_length=255,
                                  choices=KIND_OF_IMAGE,
                                  default=KIND_OF_IMAGE[0][0])
    time_of_expiry = models.IntegerField(validators=[MinValueValidator(10),
                                         MaxValueValidator(30000)])
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {str(self.user)} - {str(self.time_of_expiry)}"
