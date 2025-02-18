import os
from io import BytesIO
from tempfile import NamedTemporaryFile

import cv2
from PIL import Image
from streamlit.runtime.uploaded_file_manager import UploadedFile


def on_cloudrun() -> bool:
    return os.getenv("K_SERVICE") is not None


def is_image_size_matched(image: UploadedFile, images: list[UploadedFile]) -> bool:
    return any([Image.open(img).size != Image.open(image).size for img in images])


def convert_video_to_image(video: UploadedFile) -> BytesIO:
    with NamedTemporaryFile(delete=False) as tmp:
        tmp.write(video.read())
        tmp_path = tmp.name

    cap = cv2.VideoCapture(tmp_path)
    _, first_frame = cap.read()
    cap.release()

    os.remove(tmp_path)

    _, encoded_frame = cv2.imencode(".png", first_frame)
    encoded_frame_bytes = BytesIO(encoded_frame.tobytes())
    encoded_frame_bytes.name = video.name
    encoded_frame_bytes.type = "image/png"

    return encoded_frame_bytes
