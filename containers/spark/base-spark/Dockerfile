FROM almond/base-java-python

MAINTAINER Caio Cominato <caiopetrellicominato@gmail.com>

ENV ENABLE_INIT_DAEMON false
ENV INIT_DAEMON_BASE_URI http://identifier/init-daemon
ENV INIT_DAEMON_STEP spark_master_init

ENV BASE_URL=https://archive.apache.org/dist/spark/
ENV SPARK_VERSION=3.3.0
ENV HADOOP_VERSION=3

USER root
RUN apt-get install curl libc6 coreutils procps -y \
    && ln -s /lib64/ld-linux-x86-64.so.2 /lib/ld-linux-x86-64.so.2

# Installing Spark 
ENV SPARK_VERSION=3.3.0 \
 HADOOP_VERSION=3 \
 SPARK_HOME=/opt/spark \
 ALMOND_HOME=/opt/almond

RUN curl https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -o /tmp/apache-spark.tgz\
    && mkdir -p $SPARK_HOME \
    && tar -xf /tmp/apache-spark.tgz -C $SPARK_HOME --strip-components=1 \
    && rm /tmp/apache-spark.tgz \
    && mkdir /tmp/spark-events


RUN mkdir $SPARK_HOME/scripts
RUN chown -R almond $SPARK_HOME

COPY wait-for-step.sh $SPARK_HOME/scripts/wait-for-step.sh
COPY execute-step.sh $SPARK_HOME/scripts/execute-step.sh
COPY finish-step.sh $SPARK_HOME/scripts/finish-step.sh

# Preparing grounds for development...
RUN mkdir $ALMOND_HOME
RUN chown -R almond $ALMOND_HOME

USER almond
#Give permission to execute scripts

ENV PYTHONHASHSEED 1

# Register libs, rough i know 
ENV PYTHONPATH "${PYTHONPATH}:/$ALMOND_HOME/python:/$SPARK_HOME/python"

RUN mkdir $HOME/.env/ && chown -R almond $HOME/.env/
ADD entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/bin/bash"]