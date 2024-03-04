ARG REDIS_HOST
ARG REDIS_PORT
ARG REDIS_PASS
ARG POSTGRESQL_URL
ARG SECRET_KEY

FROM python:3.12.2-bookworm

ENV REDIS_HOST=$REDIS_HOST
ENV REDIS_PORT=$REDIS_PORT
ENV REDIS_PASS=$REDIS_PASS
ENV POSTGRESQL_URL=$POSTGRESQL_URL
ENV SECRET_KEY=$SECRET_KEY

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py makemigrations tictactoe --noinput

RUN python manage.py migrate --noinput

RUN python manage.py collectstatic --noinput

RUN apt-get update && apt-get install -y nginx
COPY nginx.conf /etc/nginx/nginx.conf

RUN apt-get update && apt-get install -y redis-server

EXPOSE 80

COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

CMD ["/usr/local/bin/entrypoint.sh"]