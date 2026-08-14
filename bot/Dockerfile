FROM python:3.9.6-slim
WORKDIR /bot

COPY requirements.txt /bot/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /bot/

CMD [ "python", "bot.py" ]