from io import BytesIO

from django.core.files.images import ImageFile
from PIL import Image

from .settings import SAVING_KWARGS


def convert_to_webp(image_data):
    # Create an ImageFile object to represent the image data
    image_file = ImageFile(image_data)
    # Open the image using Pillow
    with Image.open(image_file) as image:
        # Create an in-memory buffer to store the converted image data
        buffer = BytesIO()
        # Save the WebP image to the buffer
        image.save(buffer, "webp", **SAVING_KWARGS)
        # Get the byte string representation of the buffer
        webp_data = buffer.getvalue()
    # Return the converted image data as a byte string
    return webp_data
