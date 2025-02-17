from streamlit_theme import st_theme


class ThemeConfig:
    def __init__(self):
        self.dark_logo_path = "assets/msg_logo_w.png"
        self.light_logo_path = "assets/msg_logo_b.png"

    def get_theme_logo_path(self):
        theme = st_theme()

        if theme is None or theme.get("base") == "dark":
            return self.dark_logo_path
        else:
            return self.light_logo_path
