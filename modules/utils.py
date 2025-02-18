import os

from io import BytesIO

from PIL import Image
from streamlit.runtime.uploaded_file_manager import UploadedFile


def on_cloudrun() -> bool:
    return os.getenv("K_SERVICE") is not None


def is_image_size_matched(image: UploadedFile, images: list[UploadedFile]) -> bool:
    return any([Image.open(img).size != Image.open(image).size for img in images])


def encode_image(image: UploadedFile) -> str:
    image = Image.open(image)
    image_bytes = BytesIO()
    image.save(image_bytes, format="PNG")
    return 
