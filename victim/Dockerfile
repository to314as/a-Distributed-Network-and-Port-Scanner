FROM ubuntu:18.04
#FROM python:3.7
MAINTAINER group4
ADD ./ ./
RUN apt-get update -y
RUN apt-get install -y python3-pip
RUN apt-get install python3
RUN apt-get install ufw -y
RUN pip3 install -r requirements.txt
WORKDIR ./

