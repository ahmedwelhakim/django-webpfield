from django.db import models

from webpfield.fields import WebPField


class TestImageModel(models.Model):
    name = models.CharField(max_length=255)
    image = WebPField(upload_to="test_outputs")
