import importlib

from django.conf import settings

WEBP_FIELD_SETTINGS = {
    "saving_kwargs": {
        "quality": 90,
        "lossless": False,
    },
    "delete_original": False,
    "enable_svg": True,
    "image_field_class": {"module": "django.db.models", "class_name": "ImageField"},
}

USER_DEFINED = getattr(settings, "WEBP_FIELD_SETTINGS", None)
if USER_DEFINED:
    WEBP_FIELD_SETTINGS.update(USER_DEFINED)

DELETE_ORIGINAL = WEBP_FIELD_SETTINGS.get("delete_original", True)
ENABLE_SVG = WEBP_FIELD_SETTINGS.get("enable_svg", True)
SAVING_KWARGS = WEBP_FIELD_SETTINGS.get("saving_kwargs", {})

_image_field_class = WEBP_FIELD_SETTINGS.get("image_field_class", {})
_image_module = importlib.import_module(_image_field_class.get("module", ""))
IMAGE_FIELD_CLASS = getattr(_image_module, _image_field_class.get("class_name", ""))
