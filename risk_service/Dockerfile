FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

RUN pip3 install pika 
RUN pip3 install mysql-connector-python

WORKDIR /risk-engine

COPY . /risk-engine

ENTRYPOINT [ "python3" ]

ENV PYTHONUNBUFFERED=0

CMD ["risk_engine_application.py"]
