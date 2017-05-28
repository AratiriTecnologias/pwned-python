FROM python:2.7.13

ADD requirements.txt app.py helper.py /app/
WORKDIR /app/

RUN pip install -r requirements.txt && mkdir /app/downloads

ENV DOWNLOADS_LOCATION /app/downloads

EXPOSE 8080
ENTRYPOINT ["python", "/app/app.py"]