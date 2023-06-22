from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

from .settings import DELETE_ORIGINAL
from .utils import convert_to_webp


class WebPStorage(FileSystemStorage):
    def save(self, name, content, max_length=None):
        # In case of the image is already webP nothing extra need to be done
        if name.endswith(".webp") or name.endswith(".svg") or name.endswith(".gif"):
            return super().save(name, content, max_length=max_length)

        image_bytes = convert_to_webp(content)
        webp_content = ContentFile(image_bytes)
        webp_name = f"{name.split('.')[0]}.webp"
        if not DELETE_ORIGINAL:
            original_image_name = super().save(name, content, max_length=max_length)
        else:
            return super().save(webp_name, webp_content, max_length=max_length)

        webp_name = f"{original_image_name.split('.')[0]}.webp"
        return super().save(webp_name, webp_content, max_length=max_length)
