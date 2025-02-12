import base64

import streamlit as st
from PIL import Image
from streamlit import session_state as ss
from streamlit.runtime.uploaded_file_manager import UploadedFile

from modules import ImageSimilarityAPIRequest


def display_sort_selectbox(
    images: list[UploadedFile], similarities: list[float]
) -> None:
    if len(similarities) != 0:
        _, _, col = st.columns(3)
        with col:
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
            st.image(images[i], caption=images[i].name, use_container_width=True)
            st.html(f"<center>Similarity = {similarities[i]:.3f}</center>")


def init() -> None:
    if "similarities" not in ss:
        ss.similarities = []

    if "new_images" not in ss:
        ss.new_images = []


def main() -> None:
    st.set_page_config("類似度ツール")

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
            if any(
                Image.open(img).size != Image.open(ss.old_image).size
                for img in ss.new_images
            ):
                st.warning("入稿済みCRと新規CRsの画像サイズが一致していません。")
                st.stop()

            body = {}
            body["image"] = base64.b64encode(ss.old_image.getvalue()).decode()
            body["images"] = [
                base64.b64encode(image.getvalue()).decode() for image in ss.new_images
            ]

            image_similarity = ImageSimilarityAPIRequest()
            ss.similarities = image_similarity.get_image_similarity(body)[0].get(
                "values"
            )

    display_sort_selectbox(ss.new_images, ss.similarities)


if __name__ == "__main__":
    init()
    main()
