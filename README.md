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
export ENVIRONMENT=staging
gcloud config set project $PROJECT
gcloud auth configure-docker $REGION
docker build --platform linux/amd64 -t $REGION/$PROJECT/murmuration-image-similarity/$ENVIRONMENT:latest .
docker push $REGION/$PROJECT/murmuration-image-similarity/$ENVIRONMENT:latest
```

### Production

```
export PROJECT=data-intelligence-216907
export REGION=asia-northeast1-docker.pkg.dev
export ENVIRONMENT=production
gcloud config set project $PROJECT
gcloud auth configure-docker $REGION
docker build --platform linux/amd64 -t $REGION/$PROJECT/murmuration-image-similarity/$ENVIRONMENT:latest .
docker push $REGION/$PROJECT/murmuration-image-similarity/$ENVIRONMENT:latest
```
