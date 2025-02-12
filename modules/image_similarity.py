import subprocess

import google.auth.transport.requests
import google.oauth2.id_token
import httpx

from modules.utils import is_running_on_cloudrun


class ImageSimilarityAPIRequest:
    def __init__(self) -> None:
        self.url = "https://image-similarity-backend-cle7fyzzsq-uc.a.run.app/"

    def get_id_token(self) -> str:
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

    def get_image_similarity(self, body: dict) -> dict:
        try:
            response = httpx.post(
                self.url,
                json=body,
                headers={"Authorization": f"Bearer {self.get_id_token()}"},
                timeout=None,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return e.json()
