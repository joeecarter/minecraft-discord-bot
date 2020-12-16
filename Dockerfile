FROM python:3.8

WORKDIR /usr/src/po3-server-discord-bot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

CMD [ "python", "./main.py" ]
