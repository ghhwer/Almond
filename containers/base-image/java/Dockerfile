FROM debian:buster-slim

MAINTAINER Caio Cominato <caiopetrellicominato@gmail.com>

# Install all dependencies
RUN mkdir -p /usr/share/man/man1
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    default-jdk \
    git \
    scala \ 
    mlocate \
    gnupg \
    netcat \
    net-tools \
    libsnappy-dev

# If you got an error after building, stating that java home was not found, maybe default-jdk was updated? (update-java-alternatives -l)

ENV JAVA_HOME=/usr/lib/jvm/java-1.11.0-openjdk-amd64