"""
Test for models.
"""
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model

from datetime import datetime

from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Create a test user."""
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):
    """Test models."""

    def test_craete_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_upload_image(self):
        """Test a image upload by user."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        upload_image = models.ImgUpload(
            user=user,
            added_at=datetime.now()
        )

        self.assertEqual(str(upload_image),
                         str(upload_image.user) + ' ' + str(upload_image.id))

    @patch('core.models.uuid.uuid4')
    def test_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.image_file_path(None, 'example.jpg')

        self.assertEqual(file_path,
                         f'uploads/user/unique_id--{uuid}__file_name--example.jpg')

    def test_img_thumbnail(self):
        """Test thumbnail model."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        original_image = models.ImgUpload.objects.create(
            user=user
        )
        thumbnail = models.ImgThumbnail.objects.create(
            user=user,
            original_image=original_image,
        )

        self.assertEqual(original_image.user, thumbnail.user)
        self.assertEqual(thumbnail.original_image, original_image)
