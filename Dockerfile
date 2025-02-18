FROM python:3.13-slim

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y git python3-pip python-dev-is-python3 libgl1-mesa-dev

RUN pip install -U pip

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["streamlit", "run", "app.py", "--server.port", "8080"]

EXPOSE 8080