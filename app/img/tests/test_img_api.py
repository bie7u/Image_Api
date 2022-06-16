"""
Tests for img APIs.
"""
import tempfile
from PIL import Image
import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from django.test.client import RequestFactory
from django.core.files.images import ImageFile
from django.contrib.auth.models import Group

from rest_framework.test import APIClient
from rest_framework import status

from core.models import ImgUpload, ImgThumbnail

IMAGES_LIST = reverse('img:images-yours_images')
IMAGES_LINKS = reverse('img:images-links_to_images')
CREATE_EXPIRY_IMAGE = reverse('img:images-get_expiry_link')
UPLOAD_IMAGE = reverse('img:upload-image-list')


def create_user(**params):
    """Create a test user."""
    return get_user_model().objects.create_user(**params)


def create_original_image(user):
    """Create a original image."""
    with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
        img = Image.new('RGB', (10, 10))
        img.save(image_file, format='JPEG')
        image_file.seek(0)
        image = ImgUpload.objects.create(user=user,
                                         image=ImageFile(image_file))
        return image


def create_premium_tier(user):
    """Create a Premium tier images."""
    with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
        img = Image.new('RGB', (10, 10))
        img.save(image_file, format='JPEG')
        image_file.seek(0)
        image = ImgUpload.objects.create(user=user,
                                         image=ImageFile(image_file))
        image2 = ImgThumbnail.objects.create(user=user,
                                             original_image=image,
                                             image=ImageFile(image_file),
                                             image_type='2')
        image3 = ImgThumbnail.objects.create(user=user,
                                             original_image=image,
                                             image=ImageFile(image_file),
                                             image_type='3')
        return [image, image2, image3]


class ImageTests(TestCase):
    """Tests for the image upload and list APIs."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)
        self.request = RequestFactory().get('/')

    def test_yours_images(self):
        """Test yours images."""
        image1 = create_original_image(user=self.user)
        image2 = create_original_image(user=self.user)
        res = self.client.get(IMAGES_LIST)
        file_name1 = image1.image.path.split('__file_name--')[1]
        file_name2 = image2.image.path.split('__file_name--')[1]
        content = json.loads(res.content.decode('utf-8'))
        images_id = [int(i.split('=')[1]) for i in list(content.keys())]

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual([file_name1, file_name2], list(content.values()))
        self.assertEqual(images_id, [image1.id, image2.id])

    def test_links_to_images_enterprise_tier(self):
        """Test links to images - Enterprise group."""
        self.group = Group(name='Enterprise')
        self.group.save()
        self.user.groups.add(self.group)
        # Used Premium tier because this levels have same thumbnails.
        user_images = create_premium_tier(user=self.user)
        res = self.client.get(IMAGES_LINKS)
        content = json.loads(res.content.decode('utf-8'))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(user_images), len(list(content.values())[0][0]))

    def test_links_to_images_premium_tier(self):
        """Test links to images - Premium group."""
        self.group = Group(name='Premium')
        self.group.save()
        self.user.groups.add(self.group)
        user_images = create_premium_tier(user=self.user)
        res = self.client.get(IMAGES_LINKS)
        content = json.loads(res.content.decode('utf-8'))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(user_images), len(list(content.values())[0][0]))

    def test_create_expiry_link_permission_basic(self):
        """Check a permission in create expiry link by Basic user."""
        self.group = Group(name='Basic')
        self.group.save()
        self.user.groups.add(self.group)
        original_image = create_original_image(user=self.user)
        payload = {"original_image": original_image.id,
                   "image_type": "1",
                   "time_of_expiry": 300}
        res = self.client.post(CREATE_EXPIRY_IMAGE, payload)
        content = res.content.decode('utf-8')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(content, 'You have not a permission to do this.')

    def test_create_expiry_link_permission_premium(self):
        """Check a permission in create expiry link by Premium user."""
        self.group = Group(name='Premium')
        self.group.save()
        self.user.groups.add(self.group)
        original_image = create_original_image(user=self.user)
        payload = {"original_image": original_image.id,
                   "image_type": "1",
                   "time_of_expiry": 300}
        res = self.client.post(CREATE_EXPIRY_IMAGE, payload)
        content = res.content.decode('utf-8')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(content, 'You have not a permission to do this.')

    def test_create_expiry_link_permission_enterprise(self):
        """Check a permission in create expiry link by Enterprise user."""
        self.group = Group(name='Enterprise')
        self.group.save()
        self.user.groups.add(self.group)
        original_image = create_original_image(user=self.user)
        payload = {"original_image": original_image.id,
                   "image_type": "1",
                   "time_of_expiry": 300}
        res = self.client.post(CREATE_EXPIRY_IMAGE, payload)
        content = json.loads(res.content.decode('utf-8'))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsInstance(content["expiry_link"], str)

    def test_upload_image(self):
        """Test upload image."""
        self.group = Group(name='Basic')
        self.group.save()
        self.user.groups.add(self.group)
        res = self.client.post(UPLOAD_IMAGE)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {
                        "image": ImageFile(image_file)
                        }
            res = self.client.post(UPLOAD_IMAGE, payload, format='multipart')
            content = json.loads(res.content.decode('utf-8'))

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(content['image'], 'The image uploaded.')

    def test_upload_image_bad_request(self):
        """Test uploading invalid image."""
        payload = {'image': 'notanimage'}
        res = self.client.post(UPLOAD_IMAGE, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
