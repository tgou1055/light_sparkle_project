FROM apache/airflow:2.9.2
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

#COPY quarto.sh /
#RUN cd / && bash /quarto.sh

# $AIRFLOW_HOME /opt/airflow
COPY setup_conn.py /opt/airflow 

User root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    default-jdk procps iputils-ping

# Setup connection with spark-master
RUN python3 /opt/airflow/setup_conn.py

ENV JAVA_HOME='/usr/lib/jvm/java-17-openjdk-amd64'
ENV PATH=$PATH:$JAVA_HOME/bin



