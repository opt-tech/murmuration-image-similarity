import subprocess

import google.auth.transport.requests
import google.oauth2.id_token
import httpx
from streamlit.runtime.uploaded_file_manager import UploadedFile

from modules.utils import encode_image, is_running_on_cloudrun


class ImageSimilarityAPIRequest:
    def __init__(self) -> None:
        self.url = "https://image-similarity-backend-cle7fyzzsq-uc.a.run.app/"

    def authorize_post_request(self) -> str:
        if is_running_on_cloudrun():
            audience = "/".join(self.url.split("/")[:-1])
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, audience)
        else:
            id_token = subprocess.run(
                ["gcloud", "auth", "print-identity-token"],
                encoding="utf-8",
                stdout=subprocess.PIPE,
            ).stdout.strip()

        return id_token

    def get_post_request_body(
        self, old_image: UploadedFile, new_images: list[UploadedFile]
    ) -> dict:
        body = {}
        body["image"] = encode_image(old_image)
        body["images"] = [encode_image(img) for img in new_images]

        return body

    def get_image_similarity(
        self, old_image: UploadedFile, new_images: list[UploadedFile]
    ) -> dict:
        id_token = self.authorize_post_request()
        body = self.get_post_request_body(old_image, new_images)

        response = httpx.post(
            self.url,
            json=body,
            headers={"Authorization": f"Bearer {id_token}"},
            timeout=None,
        )

        return response.json()[0]
