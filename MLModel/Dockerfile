# FROM bitnami/scikit-learn-intel

# docker run --env-file [path-toenv-file]

FROM python:bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python", "test_model.py"]

# /home/guddi/learn/slack/MLModel

# docker run -it --rm --env-file .env -p 5010:5010 -v /home/guddi/learn/slack/MLModel/data:/app/data -v /home/guddi/learn/slack/MLModel/training_artefacts:/app/training_artefacts --name capstone_nlp capstone_nlp:latest