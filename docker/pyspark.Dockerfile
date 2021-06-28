FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y default-jdk wget python3.7 python3-pip curl unzip && \
    apt-get clean

RUN wget https://archive.apache.org/dist/spark/spark-3.0.1/spark-3.0.1-bin-hadoop3.2.tgz && \
    tar xvf spark-3.0.1-bin-hadoop3.2.tgz && \
    mv spark-3.0.1-bin-hadoop3.2/ /usr/local/spark && \
    ln -s /usr/local/spark spark

WORKDIR app
COPY . /app
RUN pip3 install cython==0.29.21 numpy==1.18.5 && pip3 install pytest pytest-mock pyspark pandas==1.0.5
ENV PYSPARK_PYTHON=python3
