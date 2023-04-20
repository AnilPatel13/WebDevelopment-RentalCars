FROM --platform=linux/amd64 python:3.10-slim-buster as build

COPY . /app

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

EXPOSE 80:80

RUN pip install --no-cache-dir -r requirements.txt

CMD exec gunicorn --bind :80 --workers 1 --threads 8 --timeout 0 main:app

#ENTRYPOINT ["sh", "./gunicorn_starter.sh"]