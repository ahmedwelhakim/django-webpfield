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
    from webp_field.fields import WebPField


    class MyModel(models.Model):
        my_image = WebPField(upload_to="images/")


Documentation
-------------

For more detailed information on how to use the library, please refer to the documentation at [Not Yet Available].

Contributing
------------

Contributions to the library are welcome! If you find a bug, have a feature request, or would like to contribute code,
please open an issue or pull request on the GitHub repo.

License
-------

This library is licensed under the MIT license. See the LICENSE file for more information.
