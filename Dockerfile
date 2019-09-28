FROM python:3.7
MAINTAINER TobiasO
ADD . /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD exec gunicorn networkscanner.wsgi:application --bind 0.0.0.0:8000 --workers 3
