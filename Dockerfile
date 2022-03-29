FROM python:3.10.0-alpine3.15

# ARG server_ip
# ARG server_port

EXPOSE 8000
WORKDIR /python
RUN pip install prometheus_client flask

COPY client.py ./

ENTRYPOINT ["python", "client.py"]