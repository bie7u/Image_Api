"""
Test custom functions.
"""
import tempfile
from PIL import Image
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.images import ImageFile
from django.contrib.auth.models import Group
from django.test.client import RequestFactory

from rest_framework.test import APIClient

from core.models import ImgThumbnail, ImgUpload

from core.functions import give_yours_images, give_links_to_images, get_height


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


def create_basic_tier(user):
    """Create a Basic tier images."""
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
        return [image, image2]


class FunctionsTest(TestCase):
    """All functions tests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')

    def test_give_yours_images(self):
        """Test a list of user images."""
        image1 = create_original_image(self.user)
        image2 = create_original_image(self.user)

        name_image_1 = image1.image.path.split('__file_name--')[1]
        name_image_2 = image2.image.path.split('__file_name--')[1]

        res = give_yours_images(model=ImgUpload, user=self.user)

        self.assertIsInstance(res, dict)
        self.assertEqual(name_image_1, list(res.values())[0])
        self.assertEqual(name_image_2, list(res.values())[1])

    def test_give_links_to_images_enterprise_tier(self):
        """Test return links on Enterprise tier."""
        request = RequestFactory().get('/')
        self.group = Group(name='Enterprise')
        self.group.save()
        self.user.groups.add(self.group)
        self.user.save()
        # Used Premium tier because this levels have same thumbnails.
        images = create_premium_tier(user=self.user)

        links = give_links_to_images(user=self.user,
                                     request=request,
                                     model1=ImgUpload,
                                     model2=ImgThumbnail)

        self.assertEqual(len(images), len(list(links.values())[0][0]))

    def test_give_links_to_images_premium_tier(self):
        """Test return links on Premium tier."""
        request = RequestFactory().get('/')
        self.group = Group(name='Premium')
        self.group.save()
        self.user.groups.add(self.group)
        self.user.save()
        images = create_premium_tier(user=self.user)

        links = give_links_to_images(user=self.user,
                                     request=request,
                                     model1=ImgUpload,
                                     model2=ImgThumbnail)

        self.assertEqual(len(images), len(list(links.values())[0][0]))

    def test_give_links_to_images_basic_tier(self):
        """Test return links on Basic tier."""
        request = RequestFactory().get('/')
        self.group = Group(name='Basic')
        self.group.save()
        self.user.groups.add(self.group)
        self.user.save()
        images = create_basic_tier(user=self.user)

        links = give_links_to_images(user=self.user,
                                     request=request,
                                     model1=ImgUpload,
                                     model2=ImgThumbnail)

        # Minus one because basic tier have accesss only to 200px thumbnail
        self.assertEqual((len(images) - 1), len(list(links.values())[0][0]))

    def test_get_height(self):
        """Basic height function test."""
        height1 = get_height('1')
        height2 = get_height('2')
        height3 = get_height('3')

        self.assertEqual(height1, None)
        self.assertEqual(height2, 200)
        self.assertEqual(height3, 400)
