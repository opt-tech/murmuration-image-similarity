from dataclasses import dataclass


@dataclass(frozen=True)
class ImagePathConfig:
    dark_logo_path: str = "assets/dark_logo.png"
    light_logo_path: str = "assets/light_logo.png"
    favicon_path: str = "assets/favicon.jpg"