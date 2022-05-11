FROM python:3.10-slim
RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -r requirements.txt
VOLUME /tmp
ENV \
    SECRET_KEY="fybrCkEEkQI09QgIKTN6NhR46DVDEqKzIx6H1+34DV4=" \
    API_DATABASE_URL="sqlite:///sql_tmp.db" \
    PORT=5000

EXPOSE 5000
CMD uvicorn main:app --port $PORT --host 0.0.0.0
