from tests import test_settings as tests_settings
from webpfield import fields, settings as webp_settings, webp_storage


def override_webpfield_settings(**decorator_kwargs: {}):
    """
    Decorator function that overrides the default settings of the `webpfield`
    library when running tests.

    Args:
        decorator_kwargs: Any number of keyword arguments used to override the default
        `webpfield` settings.

    Returns:
        The decorator function.

    Example:
        @override_webpfield_settings(
            saving_kwargs={"quality": 90, "lossless": True},
            delete_original=True,
            enable_svg=False
        )
        def test_my_webp_function():
            # Test code that uses the `webpfield` library
            pass
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            settings = webp_settings.WEBP_FIELD_SETTINGS
            settings.update(tests_settings.WEBP_FIELD_SETTINGS)
            settings.update(decorator_kwargs)
            for key, val in settings.items():
                setattr(webp_storage, key, val)
                setattr(fields, key, val)

            func(*args, **kwargs)

        return wrapper

    return decorator
