import os

from PIL import Image
from streamlit.runtime.uploaded_file_manager import UploadedFile


def is_running_on_cloudrun() -> bool:
    return os.getenv("K_SERVICE") is not None


def is_image_size_matched(image: UploadedFile, images: list[UploadedFile]) -> bool:
    return any([Image.open(img).size != Image.open(image).size for img in images])
