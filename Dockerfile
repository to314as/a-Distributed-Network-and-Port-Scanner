FROM python:3.7
MAINTAINER group4
WORKDIR ./
ADD /network ./
COPY requirements.txt ./
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python","./job_processor.py &"]