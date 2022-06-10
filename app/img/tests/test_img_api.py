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

from rest_framework.test import APIClient
from rest_framework import status

from core import models

def image_upload_url(image_id):
    """Create and return an image upload URL."""
    return reverse('img:img-upload-image', args=[image_id])

def create_user(**params):
    """Create a test user."""
    return get_user_model().objects.create_user(**params)

def create_img(user, **params):
    """Create a test image model."""
    defaults = {
        'date': datetime.now(),
    }

    defaults.update(params)

    img = models.ImgUpload.objects.create(user=user, **defaults)
    return img


class PrivateImageUploadApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

class ImageUploadTests(TestCase):
    """Tests for the image upload API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)
        self.imageload = create_img(user=self.user)

    def tearDown(self):
        self.imageload.delete()

    def test_upload_image(self):
        """Test uploading an image to a database."""
        url = image_upload_url(self.imageload.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.post(url, payload, format='multipart')

        self.imageload.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.imageload.path))