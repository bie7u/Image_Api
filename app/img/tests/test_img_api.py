"""
Tests for img APIs.
"""
from datetime import datetime
import tempfile
import os

from datetime import datetime

from PIL import Image

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from django.contrib.auth.models import Group

from rest_framework.test import APIClient
from rest_framework import status
from img.serializers import ImageSerializer

from core import models

IMAGE_LIST = reverse('img:images-yours_images')

def image_upload_url():
    """Create and return an image upload URL."""
    return reverse('img:upload-image-list')

def create_user(**params):
    """Create a test user."""
    return get_user_model().objects.create_user(**params)

def create_img(user, **params):
    """Create a test image model."""
    img = models.ImgUpload.objects.create(user=user, **params)
    return img


class ImageTests(TestCase):
    """Tests for the image upload and list APIs."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)
        self.imageload = create_img(user=self.user)

    # def tearDown(self):
    #     self.imageload.delete()

    # def test_yours_images(self):
    #     """Test list user images."""
    #     with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
    #         img = Image.new('RGB', (10, 10))
    #         img.save(image_file, format='JPEG')
    #         image_file.seek(0)
    #         create_img(user=self.user, image=image_file)


    #     res = self.client.get(IMAGE_LIST)

    #     images = models.ImgUpload.objects.filter(user=self.user)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(res.data, serializer.data)


    # def test_upload_image(self):
    #     """Test uploading an image to a database."""
    #     url = image_upload_url()
    #     with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
    #         img = Image.new('RGB', (10, 10))
    #         img.save(image_file, format='JPEG')
    #         image_file.seek(0)
    #         payload = {'image': image_file}
    #         res = self.client.post(url, payload, format='multipart')

    #     self.imageload.refresh_from_db()
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertIn('image', res.data)

    def test_upload_image_bad_request(self):
        """Test uploading invalid image."""
        url = image_upload_url()
        payload = {'image': 'notanimage'}
        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
