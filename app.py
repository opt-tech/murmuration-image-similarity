from textwrap import shorten

import streamlit as st
from streamlit import session_state as ss
from streamlit.runtime.uploaded_file_manager import UploadedFile

from modules import ImageSimilarityAPIRequest, is_image_size_matched


def display_sort_selectbox(
    images: list[UploadedFile], similarities: list[float]
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

        is_descending = ss.sort_selectbox == "高い順に並び替え"
        sorted_pairs = sorted(
            zip(images, similarities), key=lambda x: x[1], reverse=is_descending
        )
        sorted_images, sorted_similarities = zip(*sorted_pairs)
        images = list(sorted_images)
        similarities = list(sorted_similarities)

        display_gallery(images, similarities)


def display_gallery(images: list[UploadedFile], similarities: list[float]) -> None:
    num_cols = 3
    image_cols = st.columns(num_cols, gap="medium")
    for i in range(len(images)):
        with image_cols[i % num_cols]:
            caption = shorten(images[i].name, width=30, placeholder="...")
            st.image(images[i], caption=caption, use_container_width=True)
            st.html(f"<center>Similarity = {similarities[i]:.3f}</center>")


def init() -> None:
    if "similarities" not in ss:
        ss.similarities = []

    if "new_images" not in ss:
        ss.new_images = []


def main() -> None:
    st.set_page_config("マーマレーション類似度ツール")

    with st.sidebar:
        st.markdown("## マーマレーション類似度ツール")
        ss.old_image = st.file_uploader(
            "入稿済みCRをアップロード",
            type=["png", "jpg"],
            accept_multiple_files=False,
            help="画像ファイルを一枚だけアップロードすることができます。",
        )

        ss.new_images = st.file_uploader(
            "新規CRsをアップロード",
            type=["png", "jpg"],
            accept_multiple_files=True,
            help="画像ファイルを複数枚アップロードすることができます。",
        )

        calculated = st.button("Calculate", type="primary")

    if calculated:
        if ss.old_image and ss.new_images:
            if is_image_size_matched(ss.old_image, ss.new_images):
                st.warning("入稿済みCRと新規CRsの画像サイズが一致していません。")
                st.stop()

            image_similarity = ImageSimilarityAPIRequest()
            ss.similarities = image_similarity.get_image_similarity(
                ss.old_image, ss.new_images
            ).get("values")
        else:
            st.warning("入稿済みCRと新規CRsの両方を1件以上アップロードしてください。")
            st.stop()

    display_sort_selectbox(ss.new_images, ss.similarities)


if __name__ == "__main__":
    init()
    main()
