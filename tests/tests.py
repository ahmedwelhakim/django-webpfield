import io
import os
from shutil import rmtree

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from PIL import Image, ImageChops

from webpfield.webp_storage import WebPStorage

from .test_settings import MEDIA_ROOT
from .utils import override_webpfield_settings


class TestBase(TestCase):
    def setUp(self):
        self.jpg_path = os.path.join(MEDIA_ROOT, "python-logo.jpg")
        self.png_path = os.path.join(MEDIA_ROOT, "python-logo.png")
        self.webp_path = os.path.join(MEDIA_ROOT, "python-logo.webp")
        self.gif_path = os.path.join(MEDIA_ROOT, "python-logo.gif")

        self.storage = WebPStorage()

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


class WebPStorageTest(TestBase):
    @override_webpfield_settings(DELETE_ORIGINAL=False)
    def test_save_jpg_to_webp_image_with_no_delete(self):
        file_name, file = self._get_image_file(self.jpg_path, "image/jpeg", "JPEG")
        saved_name = self.storage.save(file_name, file)
        # Check that the file was saved as a WebP image
        self.assertTrue(saved_name.endswith(".webp"))
        # Check original image exist
        self.assertTrue(self.storage.exists(file_name))

    @override_webpfield_settings(DELETE_ORIGINAL=True)
    def test_save_jpg_to_webp_image_with_delete(self):
        file_name, file = self._get_image_file(self.jpg_path, "image/jpeg", "JPEG")
        saved_name = self.storage.save(file_name, file)
        # Check that the file was saved as a WebP image
        self.assertTrue(saved_name.endswith(".webp"))
        # Check original image does not exist
        self.assertFalse(self.storage.exists(file_name))

    @override_webpfield_settings(DELETE_ORIGINAL=False)
    def test_save_png_to_webp_image_with_no_delete(self):
        file_name, file = self._get_image_file(self.png_path, "image/png", "PNG")
        saved_name = self.storage.save(file_name, file)
        # Check that the file was saved as a WebP image
        self.assertTrue(saved_name.endswith(".webp"))
        # Check original image exist
        self.assertTrue(self.storage.exists(file_name))

    @override_webpfield_settings(DELETE_ORIGINAL=True)
    def test_save_png_to_webp_image_with_delete(self):
        file_name, file = self._get_image_file(self.png_path, "image/png", "PNG")
        saved_name = self.storage.save(file_name, file)
        # Check that the file was saved as a WebP image
        self.assertTrue(saved_name.endswith(".webp"))
        # Check original image does not exist
        self.assertFalse(self.storage.exists(file_name))

    def test_save_webp_is_same_as_original(self):
        file_name, file = self._get_image_file(self.webp_path, "image/webp", "WEBP")
        saved_name = self.storage.save(file_name, file)
        self.assertTrue(
            os.path.basename(saved_name) == self.path_to_name(self.webp_path)
        )

        image1 = Image.open(self.webp_path)
        image2 = Image.open(file_name)

        diff = ImageChops.difference(image1, image2)
        self.assertTrue(diff.getbbox() is None)

    def _get_image_file(self, path, content_type, img_format):
        img = Image.open(path)
        file_name = self.path(self.path_to_name(path))
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
