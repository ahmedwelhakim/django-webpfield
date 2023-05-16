from django.conf import settings

WEBP_FIELD_SETTINGS = {
    "saving_kwargs": {
        "quality": 100,
        "lossless": False,
    },
    "delete_original": True,
    "enable_svg": True,
}

USER_DEFINED = getattr(settings, "WEBP_FIELD_SETTINGS", None)
if USER_DEFINED:
    WEBP_FIELD_SETTINGS.update(USER_DEFINED)

DELETE_ORIGINAL = WEBP_FIELD_SETTINGS.get("delete_original", True)
ENABLE_SVG = WEBP_FIELD_SETTINGS.get("enable_svg", True)
SAVING_KWARGS = WEBP_FIELD_SETTINGS.get("saving_kwargs", {})
