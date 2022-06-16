"""
Tests for the Django admin modifications.
"""
import tempfile
from PIL import Image

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client
from django.core.files.images import ImageFile
from django.test.client import RequestFactory

from core.models import ImgUpload, ImgThumbnail, TimeGenerateImg


def create_original_image(user):
    """Create a original image."""
    with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
        img = Image.new('RGB', (10, 10))
        img.save(image_file, format='JPEG')
        image_file.seek(0)
        image = ImgUpload.objects.create(user=user,
                                         image=ImageFile(image_file))
        return image


def create_thumbnail(user, image_type):
    """Create a original image."""
    with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
        img = Image.new('RGB', (10, 10))
        img.save(image_file, format='JPEG')
        image_file.seek(0)
        image = ImgUpload.objects.create(user=user,
                                         image=ImageFile(image_file))
        thumb_image = ImgThumbnail.objects.create(user=user,
                                                  original_image=image,
                                                  image=ImageFile(image_file),
                                                  image_type=image_type)
        return thumb_image


def create_expiry_image(user, image_type, time_of_expiry):
    """Create a original image."""
    with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
        img = Image.new('RGB', (10, 10))
        img.save(image_file, format='JPEG')
        image_file.seek(0)
        image = ImgUpload.objects.create(user=user,
                                         image=ImageFile(image_file))
        img = TimeGenerateImg.objects.create(user=user,
                                             original_image=image,
                                             image=ImageFile(image_file),
                                             image_type=image_type,
                                             time_of_expiry=time_of_expiry)
        return img


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """Create user and client."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User',
        )
        self.request = RequestFactory().get('/')

    def test_users_list(self):
        """Test that users are listed on page."""
        # More info shorturl.at/lwCFJ
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works."""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works."""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_img_uploads_list(self):
        """Test that images are listed on page."""
        image = create_original_image(user=self.user)
        url = reverse('admin:core_imgupload_changelist')
        res = self.client.get(url)
        image_url = self.request.build_absolute_uri(image.image.url)

        self.assertContains(res, self.user)
        self.assertContains(res, image.id)
        self.assertContains(res, image_url)

    def test_img_thumbnail_list(self):
        """Test that thumbnails are listed on page."""
        thumb = create_thumbnail(user=self.user, image_type='2')
        url = reverse('admin:core_imgthumbnail_changelist')
        res = self.client.get(url)
        image_url = self.request.build_absolute_uri(thumb.image.url)

        self.assertContains(res, self.user)
        self.assertContains(res, thumb.image_type)
        self.assertContains(res, thumb.original_image.id)
        self.assertContains(res, image_url)

    def test_expiry_image_list(self):
        """Test that thumbnails are listed on page."""
        thumb = create_expiry_image(user=self.user,
                                    image_type='2',
                                    time_of_expiry=300)
        url = reverse('admin:core_timegenerateimg_changelist')
        res = self.client.get(url)
        image_url = self.request.build_absolute_uri(thumb.image.url)

        self.assertContains(res, self.user)
        self.assertContains(res, thumb.image_type)
        self.assertContains(res, thumb.original_image.id)
        self.assertContains(res, image_url)

    def test_create_thumbnail_page(self):
        """Test the create user page works."""
        url = reverse('admin:core_imgthumbnail_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_expiryty_image_page(self):
        """Test the create user page works."""
        url = reverse('admin:core_timegenerateimg_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
