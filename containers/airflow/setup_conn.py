"""
Setup connections from Airflow webserver to other services
"""
import subprocess


def airflow_connection_aws_minio():
    """
    Add SSH connection to transfer files to Minio

    :param

    :return
    """

    # Define connection details
    conn_id = "aws_default"
    conn_type = "aws"
    access_key = "minio"
    secret_key = "minio123"
    region_name = "us-east-1"
    endpoint_url = "http://minio:9000"
    # Construct the extra JSON
    extra = {
        "aws_access_key_id": access_key,
        "aws_secret_access_key": secret_key,
        "region_name": region_name,
        "host": endpoint_url,
    }
    # Convert to JSON string
    extra_json = str(extra).replace("'", '"')
    # Define the CLI command
    cmd = [
        "airflow",
        "connections",
        "add",
        conn_id,
        "--conn-type",
        conn_type,
        "--conn-extra",
        extra_json,
    ]
    # Execute the command
    result = subprocess.run(cmd, capture_output=True, text=True) # pylint: disable=W1510
    if result.returncode == 0:
        print(f"Successfully added {conn_id} connection")
    else:
        print(f"Failed to add {conn_id} connection: {result.stderr}")



def airflow_connection_ssh_spark():
    """
    Add SSH connection to submit spark job to standalone spark cluster

    :param

    :return
    """
    conn_id = "ssh_conn"
    conn_type = "ssh"
    host = "spark-master"
    login = "root"
    password = "password"
    port = "22"
    cmd = [
        "airflow",
        "connections",
        "add",
        conn_id,
        "--conn-type",
        conn_type,
        "--conn-host",
        host,
        "--conn-login",
        login,
        "--conn-password",
        password,
        "--conn-port",
        port,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True) # pylint: disable=W1510
    if result.returncode == 0:
        print(f"Successfully added {conn_id} connection")
    else:
        print(f"Failed to add {conn_id} connection: {result.stderr}")

if __name__ == "__main__":
    # Add connections
    airflow_connection_ssh_spark()
    airflow_connection_aws_minio()
