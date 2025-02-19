from io import BytesIO
from uuid import uuid4

import streamlit as st
from streamlit import session_state as ss
from streamlit.runtime.uploaded_file_manager import UploadedFile

from modules import (
    ImageSimilarity,
    ThemeConfig,
    convert_video_to_image,
    is_image_size_matched,
)


def display_gallery(
    images: list[UploadedFile | BytesIO], similarities: list[float]
) -> None:
    num_cols = 3
    image_cols = st.columns(num_cols, gap="medium")
    for i in range(len(images)):
        with image_cols[i % num_cols]:
            caption = images[i].name[:15] + "..."
            st.image(images[i], caption=caption, use_container_width=True)
            st.html(f"<center>{similarities[i]}</center>")


def display_sort_selectbox(
    images: list[UploadedFile | BytesIO], similarities: list[float]
) -> None:
    if len(similarities) != 0 and len(images) != 0:
        num_cols = 3
        selectbox_cols = st.columns(num_cols, gap="small")
        with selectbox_cols[2]:
            st.selectbox(
                "並び替え",
                ["低い順に並び替え", "高い順に並び替え"],
                key="sort_selectbox",
                label_visibility="collapsed",
            )

        sorted_pairs = sorted(
            zip(images, similarities),
            key=lambda x: x[1],
            reverse=(ss.sort_selectbox == "高い順に並び替え"),
        )
        sorted_images, sorted_similarities = zip(*sorted_pairs)
        images = list(sorted_images)
        similarities = list(sorted_similarities)

        display_gallery(images, similarities)


def init() -> None:
    if "old_image_clear_key" not in ss:
        ss.old_image_clear_key = str(uuid4())

    if "old_image" not in ss:
        ss.old_image = None

    if "new_images_clear_key" not in ss:
        ss.new_images_clear_key = str(uuid4())

    if "new_images" not in ss:
        ss.new_images = []

    if "similarities" not in ss:
        ss.similarities = []


def main() -> None:
    st.set_page_config("Murmuration Sequential Generator")
    st.logo(ThemeConfig().get_theme_logo_path(), size="large")
    st.header("検証用")

    with st.sidebar:
        ss.old_image = st.file_uploader(
            "入稿済みCRをアップロード",
            type=["png", "jpg", "mp4"],
            accept_multiple_files=False,
            key=ss.old_image_clear_key,
            help="画像や動画ファイルを一枚アップロードすることができます。",
        )

        if ss.old_image:
            if ss.old_image.type in ["video/mp4", "video/mpeg4"]:
                ss.old_image = convert_video_to_image(ss.old_image)

            if ss.old_image.type == "image/png":
                old_image_col, _, _ = st.columns(3)
                old_image_col.image(ss.old_image)

        ss.new_images = st.file_uploader(
            "新規CRsをアップロード",
            type=["png", "jpg", "mp4"],
            accept_multiple_files=True,
            key=ss.new_images_clear_key,
            help="画像や動画ファイルを複数枚アップロードすることができます。",
        )

        if ss.new_images:
            for i, img in enumerate(ss.new_images):
                if img.type in ["video/mp4", "video/mpeg4"]:
                    ss.new_images[i] = convert_video_to_image(img)

        clear_col, calc_col = st.columns(2)
        cleared = clear_col.button("Clear", use_container_width=True)
        submitted = calc_col.button("Run", type="primary", use_container_width=True)

    if cleared:
        ss.clear()
        st.rerun()

    if submitted:
        if not (ss.old_image and ss.new_images):
            st.warning("入稿済みCRと新規CRsの両方を1件以上アップロードしてください。")
            st.stop()

        if is_image_size_matched(ss.old_image, ss.new_images):
            st.toast(
                "入稿済みCRと新規CRsの縦横サイズが一致していません。正しく測定できない場合があります。",
                icon="⚠️",
            )

        image_similarity = ImageSimilarity()
        ss.similarities = image_similarity.get_image_similarity(
            ss.old_image, ss.new_images
        ).get("values")

    display_sort_selectbox(ss.new_images, ss.similarities)


if __name__ == "__main__":
    init()
    main()
