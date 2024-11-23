FROM deltaio/delta-docker:latest
# latest is at 1.0.0_3.0.0, 

USER root

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy SQL DDL and DML to SPARK_HOME dir
COPY ./sql/setup.sql ./
COPY ./sql/count.sql ./
COPY ./scripts/create_buckets.py ./
COPY ./scripts/upload_data_to_s3a.py ./
COPY ./scripts/explore_imba_data_pandas.ipynb ./

# Copy tpch data generator into the container
COPY ./tpch-dbgen ./tpch-dbgen/

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    rsync && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Setup SSH server
RUN apt-get update && apt-get install -y openssh-server
RUN mkdir /var/run/sshd
# Set root password for SSH access (change 'your_password' to your desired password)
RUN echo 'root:password' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
#RUN service ssh restart

COPY ./conf/spark-defaults.conf "$SPARK_HOME/conf/spark-defaults.conf"
COPY ./conf/metrics.properties "$SPARK_HOME/conf/metrics.properties"
ENV SPARK_CONF_DIR="$SPARK_HOME/conf"
ENV SPARK_MASTER="spark://spark-master:7077"
ENV SPARK_MASTER_HOST spark-master
ENV SPARK_MASTER_PORT 7077
ENV PYSPARK_PYTHON python3

# Create and event logging directory to store job logs
RUN mkdir /tmp/spark-events

RUN chmod u+x /opt/spark/sbin/* && \
    chmod u+x /opt/spark/bin/*

ENV PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH

COPY entrypoint.sh .

ENTRYPOINT ["./entrypoint.sh"]
