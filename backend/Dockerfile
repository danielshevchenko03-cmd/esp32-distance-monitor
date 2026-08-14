FROM python:3.9.6-slim
WORKDIR /backend

RUN apt-get update && apt-get install -y tzdata && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /backend/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /backend/

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]