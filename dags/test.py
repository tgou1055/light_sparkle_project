from datetime import datetime, timedelta

from airflow import DAG

from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
#from airflow.operators.postgres_operator import PostgresOperator
#from airflow.operators.python import PythonOperator
#from airflow.providers.amazon.aws.hooks.s3 import S3Hook
#from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.ssh.operators.ssh import SSHOperator

# DAG definition
default_args = {
    "owner": "airflow",
    "depends_on_past": True,
    "wait_for_downstream": True,
    "start_date": datetime(2024, 11, 15),  # Consider changing this to a past date
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,  
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

# DAG creation

dag = DAG(
    "test",
    default_args=default_args,
    schedule_interval="0 12 * * *",  # This runs the DAG daily at midnight
    max_active_runs=1,
)


# SSH command to run on the remote machine
ssh_command = 'bash -c "export JAVA_HOME=/usr/local/openjdk-11 && cd /opt/spark/work-dir && spark-submit --master spark://spark-master:7077 data-processing-spark/case_new.py"'
ssh_command_2 = 'bash -c "echo Hello from Airflow!; ls /opt/spark/work-dir"'

# Define the SSHOperator to execute the command
ssh_task = SSHOperator(
    task_id='run_remote_command',
    ssh_conn_id='ssh_conn',  # Use the connection ID configured above
    command=ssh_command ,  # The command to execute
    cmd_timeout=600,  # Increase the specific command timeout
    dag=dag
)

end_of_data_pipeline = DummyOperator(
                            task_id="end_of_data_pipeline",
                            dag=dag
                        )


ssh_task >> end_of_data_pipeline # pylint: disable=pointless-statement
