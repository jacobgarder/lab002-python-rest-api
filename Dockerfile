FROM python:3.9 

ENV FLASK_APP=network_request
ENV TACACS_APP_NAME=network-request
ENV TACACS_HOST=tacacs_server
ENV TACACS_SECRET=tacacs_secret
# ENV LOAD_SAMPLE_DATA

WORKDIR /app

COPY network_request /app/network_request
COPY setup.py /app/
COPY setup.cfg /app/

RUN pip install -e .

ENTRYPOINT ["flask", "run", "-h", "0.0.0.0"]