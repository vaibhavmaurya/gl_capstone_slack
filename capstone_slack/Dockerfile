FROM python:bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python", "/app/slack/bot_event.py"]

# docker run -it --rm --env-file slack/.env -p 3010:3010 -v /home/guddi/learn/slack/capstone_slack/slack/responses:/app/responses --name capstone_slack capstone_slack:latest