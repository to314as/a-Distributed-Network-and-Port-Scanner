FROM python:3.7
MAINTAINER group4
WORKDIR ./
ADD ./ ./
COPY requirements.txt ./
ENTRYPOINT [""]
RUN pip install -r requirements.txt
RUN apt-get update && \
      apt-get -y install sudo

RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo
USER docker
EXPOSE 5000
EXPOSE 8000