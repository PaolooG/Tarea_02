FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Instalar Java y utilidades necesarias
RUN apt-get update && apt-get install -y \
    openjdk-8-jdk \
    wget \
    curl \
    unzip \
    python3 \
    python3-pip \
    git \
    && apt-get clean

# Configurar variables de entorno
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV HADOOP_HOME=/opt/hadoop
ENV PIG_HOME=/opt/pig
ENV PATH=$PATH:$HADOOP_HOME/bin:$PIG_HOME/bin

# Instalar Hadoop pseudo-distribuido
RUN wget https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz && \
    tar -xvzf hadoop-3.3.6.tar.gz -C /opt && \
    mv /opt/hadoop-3.3.6 /opt/hadoop && \
    rm hadoop-3.3.6.tar.gz

# Instalar Apache Pig
RUN wget https://downloads.apache.org/pig/pig-0.17.0/pig-0.17.0.tar.gz && \
    tar -xvzf pig-0.17.0.tar.gz -C /opt && \
    mv /opt/pig-0.17.0 /opt/pig && \
    rm pig-0.17.0.tar.gz

# Copiar scripts de trabajo
WORKDIR /opt/pigjob
COPY ./data /opt/pigjob/data
COPY ./pig /opt/pigjob/pig

CMD ["pig"]
