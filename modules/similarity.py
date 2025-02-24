import subprocess
from base64 import b64encode
from io import BytesIO

import google.auth.transport.requests
import google.oauth2.id_token
import httpx

from modules.utils import on_cloudrun


class ImageSimilarity:
    def __init__(self) -> None:
        self.url = "https://image-similarity-backend-cle7fyzzsq-uc.a.run.app/"

    def authorize_post_request(self) -> str:
        if on_cloudrun():
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

    def get_image_similarity(
        self, old_image: BytesIO, new_images: list[BytesIO]
    ) -> dict:
        id_token = self.authorize_post_request()

        body = {}
        body["image"] = b64encode(old_image.getvalue()).decode()
        body["images"] = [b64encode(img.getvalue()).decode() for img in new_images]

        response = httpx.post(
            self.url,
            json=body,
            headers={"Authorization": f"Bearer {id_token}"},
            timeout=None,
        )

        return response.json()[0]
