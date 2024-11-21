# Install the latest Airflow and required python environment 
FROM apache/airflow:2.9.2
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

# Copy the connection file for SSH connection
COPY setup_conn.py /opt/airflow 

User root

# Install tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    default-jdk procps iputils-ping

# Setup the Environment
ENV JAVA_HOME='/usr/lib/jvm/java-17-openjdk-amd64'
ENV PATH=$PATH:$JAVA_HOME/bin



