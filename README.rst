=============================
Welcome to Django WebP Field
=============================

This is a library for Django that provides a custom model field for storing WebP images.
The `WebPField` model field allows you to store WebP images in your Django models
and provides convenient methods for converting between WebP and other image formats.

Installation
------------

To install the library, simply add it to your project's dependencies using pip:

.. code-block:: bash

    pip install django-webpfield

Usage
-----

To use the `WebPField` model field, simply import it from the library and add it to your Django model:

.. code-block:: python

    from django.db import models
    from webpfield.fields import WebPField


    class MyModel(models.Model):
        my_image = WebPField(upload_to="images/")


Settings
--------
The default settings are:

.. code-block:: python

    WEBP_FIELD_SETTINGS = {
        "saving_kwargs": {
            "quality": 75,
            "lossless": False,
        },
        "delete_original": False,
        "enable_svg": True,
        "image_field_class": {"module": "django.db.models", "class_name": "ImageField"},
    }

- saving_kwargs: are the kwargs passed to pillow when saving the new image
- enable_svg: if True you can upload and svg and it will remain svg as original, this achieved by updating the formfield kwargs of WebPField to file field instead of image field
- image_field_class: The default parent class of WebPField is django ImageField, but you can override it with yours

Contributing
------------

Contributions to the library are welcome! If you find a bug, have a feature request, or would like to contribute code,
please open an issue or pull request on the GitHub repo.

License
-------

This library is licensed under the MIT license. See the LICENSE file for more information.
