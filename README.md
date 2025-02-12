# マーマレーション - 類似度ツール

## Getting Started

```
pipenv install
pipenv shell
streamlit run app.py
```

## Deploy

```
export PROJECT=data-intelligence-216907
gcloud config set project $PROJECT
gcloud auth configure-docker asia-northeast1-docker.pkg.dev
docker build --platform linux/amd64 -t asia-northeast1-docker.pkg.dev/$PROJECT/murmuration-image-similarity/front:latest .
docker push asia-northeast1-docker.pkg.dev/$PROJECT/murmuration-image-similarity/front:latest
```
