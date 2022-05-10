FROM python:3.10-slim
RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -r requirements.txt
VOLUME /tmp
#ENV API_ENDPOINT_FACEID="http://170.84.17.2:8001"
#ENV API_DATABASE_URL="postgresql://faceid:teste3@192.168.5.165/faceid"

#ENV API_DATABASE_URL="sqlite:////tmp/sql_app.db"
EXPOSE 5000
CMD ["python","main.py"]
