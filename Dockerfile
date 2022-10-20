FROM python:3.10-slim
RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -r requirements.txt
VOLUME /tmp
EXPOSE 8080
CMD uvicorn main:app --port 8080 --host 0.0.0.0
