import io
import os
from shutil import rmtree

from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image, ImageChops

from webpfield.webp_storage import WebPStorage

from .models import TestImageModel
from .test_settings import MEDIA_ROOT
from .utils import override_webpfield_settings


class TestBase(TestCase):
    jpg_path = None
    png_path = None
    webp_path = None
    gif_path = None
    svg_path = None
    storage = None

    @classmethod
    def setUp(cls):
        cls.jpg_path = os.path.join(MEDIA_ROOT, "python-logo.jpg")
        cls.png_path = os.path.join(MEDIA_ROOT, "python-logo.png")
        cls.webp_path = os.path.join(MEDIA_ROOT, "python-logo.webp")
        cls.gif_path = os.path.join(MEDIA_ROOT, "python-logo.gif")
        cls.svg_path = os.path.join(MEDIA_ROOT, "python-logo.svg")

        cls.storage = WebPStorage()

    def tearDown(self):
        try:
            rmtree(os.path.join(MEDIA_ROOT, "test_outputs"))
        except FileNotFoundError:
            pass

    @staticmethod
    def path(*paths):
        return os.path.join(MEDIA_ROOT, "test_outputs", *paths)

    @staticmethod
    def path_to_name(path):
        return os.path.basename(path)

    @classmethod
    def _get_image_file(cls, path, content_type, img_format):
        img = Image.open(path)
        file_name = cls.path(cls.path_to_name(path))
        content_type = content_type
        bytes_io = io.BytesIO()
        img.save(bytes_io, img_format)
        bytes_io.seek(0)
        file = InMemoryUploadedFile(
            bytes_io,
            None,
            file_name,
            content_type,
            len(img.tobytes()),
            None,
        )
        return file_name, file

    @classmethod
    def get_jpg_image(cls):
        return cls._get_image_file(cls.jpg_path, "image/jpeg", "JPEG")

    @classmethod
    def get_png_image(cls):
        return cls._get_image_file(cls.png_path, "image/png", "PNG")

    @classmethod
    def get_webp_image(cls):
        return cls._get_image_file(cls.webp_path, "image/webp", "WEBP")

    @classmethod
    def get_gif_image(cls):
        return cls._get_image_file(cls.gif_path, "image/gif", "GIF")

    @classmethod
    def get_svg_image(cls):
        with open(cls.svg_path, "rb") as svg_file:
            svg_data = svg_file.read()
        file_name = cls.path(cls.path_to_name(cls.svg_path))
        content_type = "image/svg"
        # Create a BytesIO object from the SVG data
        svg_io = io.BytesIO(svg_data)
        file = InMemoryUploadedFile(
            svg_io,
            None,
            file_name,
            content_type,
            len(svg_data),
            None,
        )
        return file_name, file


class WebPStorageTest(TestBase):
    @override_webpfield_settings(DELETE_ORIGINAL=False)
    def test_save_jpg_to_webp_image_with_no_delete(self):
        file_name, file = self.get_jpg_image()
        saved_name = self.storage.save(file_name, file)
        # Check that the file was saved as a WebP image
        self.assertTrue(saved_name.endswith(".webp"))
        # Check original image exist
        self.assertTrue(self.storage.exists(file_name))

    @override_webpfield_settings(DELETE_ORIGINAL=True)
    def test_save_jpg_to_webp_image_with_delete(self):
        file_name, file = self.get_jpg_image()
        saved_name = self.storage.save(file_name, file)
        # Check that the file was saved as a WebP image
        self.assertTrue(saved_name.endswith(".webp"))
        # Check original image does not exist
        self.assertFalse(self.storage.exists(file_name))

    @override_webpfield_settings(DELETE_ORIGINAL=False)
    def test_save_png_to_webp_image_with_no_delete(self):
        file_name, file = self.get_png_image()
        saved_name = self.storage.save(file_name, file)
        # Check that the file was saved as a WebP image
        self.assertTrue(saved_name.endswith(".webp"))
        # Check original image exist
        self.assertTrue(self.storage.exists(file_name))

    @override_webpfield_settings(DELETE_ORIGINAL=True)
    def test_save_png_to_webp_image_with_delete(self):
        file_name, file = self.get_png_image()
        saved_name = self.storage.save(file_name, file)
        # Check that the file was saved as a WebP image
        self.assertTrue(saved_name.endswith(".webp"))
        # Check original image does not exist
        self.assertFalse(self.storage.exists(file_name))

    def test_save_webp_is_same_as_original(self):
        file_name, file = self.get_webp_image()
        saved_name = self.storage.save(file_name, file)
        self.assertTrue(
            os.path.basename(saved_name) == self.path_to_name(self.webp_path)
        )

        image1 = Image.open(self.webp_path)
        image2 = Image.open(file_name)

        diff = ImageChops.difference(image1, image2)
        self.assertTrue(diff.getbbox() is None)

    @override_webpfield_settings(ENABLE_SVG=True)
    def test_svg_with_enable_svg(self):
        file_name, file = self.get_svg_image()
        saved_name = self.storage.save(file_name, file)
        self.assertTrue(saved_name.endswith(".svg"))

    def test_gif_is_same(self):
        file_name, file = self.get_gif_image()
        saved_name = self.storage.save(file_name, file)
        self.assertTrue(saved_name.endswith(".gif"))


class AdminImageUploadTestCase(TestBase):
    def setUp(self):
        super().setUp()
        self.admin_user = User.objects.create_superuser(
            "admin", "admin@example.com", "password"
        )
        self.client.login(username="admin", password="password")

    def test_admin_upload_jpg_image(self):
        image_instance = self._post_assert_get_image_instance(
            "Test Jpg Image", self.get_jpg_image()[1]
        )
        self._assert_webp_and_delete_instance(image_instance)

    def test_admin_upload_png_image(self):
        image_instance = self._post_assert_get_image_instance(
            "Test Png Image", self.get_png_image()[1]
        )
        self._assert_webp_and_delete_instance(image_instance)

    def test_admin_upload_webp_image(self):
        image_instance = self._post_assert_get_image_instance(
            "Test WebP Image", self.get_webp_image()[1]
        )
        self._assert_webp_and_delete_instance(image_instance)

    def test_admin_upload_gif_image(self):
        image_instance = self._post_assert_get_image_instance(
            "Test GIF Image", self.get_gif_image()[1]
        )
        self._assert_is_same_delete_instance(image_instance, ".gif")

    @override_webpfield_settings(ENABLE_SVG=True)
    def test_admin_upload_svg_image(self):
        image_instance = self._post_assert_get_image_instance(
            "Test SVG Image", self.get_svg_image()[1]
        )
        self._assert_is_same_delete_instance(image_instance, ".svg")

    def _post_assert_get_image_instance(self, name, image):
        data = {
            "name": name,
            "image": image,
        }
        response = self.client.post(reverse("admin:tests_testimagemodel_add"), data)
        self.assertEqual(response.status_code, 302)
        image_instance = TestImageModel.objects.get(name=name)
        return image_instance

    def _assert_webp_and_delete_instance(self, image_instance):
        image = image_instance.image
        name = image.name
        image_instance.delete()
        self.assertTrue(name.endswith(".webp"))

    def _assert_is_same_delete_instance(self, image_instance, img_format):
        image = image_instance.image
        name = image.name
        image_instance.delete()
        self.assertTrue(name.endswith(img_format))
