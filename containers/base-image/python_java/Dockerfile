FROM almond/base-java

MAINTAINER Caio Cominato <caiopetrellicominato@gmail.com>

# Create and switch to user
RUN useradd -rm -d /home/almond -s /bin/bash -g root -G sudo -u 1001 almond
RUN chown -R almond /home/almond
USER almond
WORKDIR /home/almond

ENV HOME "/home/almond"
ENV SHELL=/bin/bash
SHELL ["/bin/bash", "-ec"]

RUN echo "JAVA_HOME=$(update-java-alternatives -l | awk '{print $3}')" >> ~/.profile
RUN echo "JAVA_HOME=$(update-java-alternatives -l | awk '{print $3}')" >> ~/.bashrc

# Args
ENV PYTHON_VERSION=3.7.10

USER root
RUN apt-get update && apt-get install -y nano
USER almond

# Install miniconda
RUN mkdir $HOME/.conda
RUN curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o $HOME/miniconda.sh
RUN bash $HOME/miniconda.sh -b && ls $HOME/miniconda3/bin && $HOME/miniconda3/bin/conda init
RUN rm -r miniconda.sh

# Install all stuff
RUN $HOME/miniconda3/bin/conda install python=${PYTHON_VERSION}