# マーマレーション - 類似度ツール

## Getting Started

```
pipenv install
pipenv shell
streamlit run app.py
```

## Deploy（Staging）

### Staging

```
export PROJECT=data-intelligence-216907
export REGION=asia-northeast1-docker.pkg.dev
gcloud config set project $PROJECT
gcloud auth configure-docker $REGION
docker build --platform linux/amd64 -t $REGION/$PROJECT/murmuration-image-similarity/staging:latest .
docker push $REGION/$PROJECT/murmuration-image-similarity/staging:latest
```

### Production

```
export PROJECT=data-intelligence-216907
export REGION=asia-northeast1-docker.pkg.dev
gcloud config set project $PROJECT
gcloud auth configure-docker $REGION
docker build --platform linux/amd64 -t $REGION/$PROJECT/murmuration-image-similarity/production:latest .
docker push $REGION/$PROJECT/murmuration-image-similarity/production:latest
```
