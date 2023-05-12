# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

from webpfield import __version__

setup(
    name="django-webpfield",
    packages=find_packages(),
    version=__version__,
    author="Ahmed Elhakim",
    author_email="ahmed.w.elhakim@gmail.com",
    url="https://github.com/ahmedwelhakim/django-webpfield/",
    license="MIT License, see LICENSE",
    description="A simple library that convert any user uploaded images to webP format",
    long_description=open("README.rst").read(),
    zip_safe=False,
    install_requires=[
        "Pillow>=9.5.0",
        "Django>=4.2",
    ],
    include_package_data=True,
    keywords=[
        "django",
        "webp",
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Graphics :: Presentation",
    ],
)
