from webpfield.webp_storage import WebPStorage

from .settings import IMAGE_FIELD_CLASS


class WebPField(IMAGE_FIELD_CLASS):
    def __init__(self, *args, **kwargs):
        kwargs.update({"storage": WebPStorage()})
        super().__init__(*args, **kwargs)
