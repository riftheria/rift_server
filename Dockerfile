FROM python:3.11.0-bullseye
ENV ALLOWED_HOSTS='["server", "localhost"]'
ENV DJANGO_DEBUG="0"
WORKDIR /rift_servers
ADD . ./
RUN pip install -r requirements.txt
RUN python3 manage.py migrate