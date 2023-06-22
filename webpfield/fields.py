from django import forms

from webpfield.webp_storage import WebPStorage

from .settings import ENABLE_SVG, IMAGE_FIELD_CLASS


class WebPField(IMAGE_FIELD_CLASS):
    def __init__(self, *args, **kwargs):
        kwargs.update({"storage": WebPStorage()})
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        if ENABLE_SVG:
            kwargs.update({"form_class": forms.FileField})
        return super().formfield(**kwargs)
