FROM python:3.10-slim

RUN mkdir /telegram_bot_prozorro_v2

WORKDIR /telegram_bot_prozorro_v2

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh
