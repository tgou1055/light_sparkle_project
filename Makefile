## Cluster management

build:
	docker compose build spark-master

docker-up:
	docker compose up --build -d --scale spark-worker=2

up: build docker-up

rm-logs:
	docker volume rm -f light_sparkle_tpch-data light_sparkle_spark-logs

down:
	docker compose down

restart: down rm-logs build up

sh:
	docker exec -ti spark-master bash

## Data generation
## 0.1: 100 MB of data

datagen:
	docker exec -ti spark-master bash -c 'cd tpch-dbgen && make && ./dbgen -s 0.1'  

upstream:
	PGPASSWORD=sdepassword pgcli -h localhost -p 5432 -U sdeuser -d upstreamdb

## Create tables

create-buckets:
	docker exec spark-master bash -c "python3 /opt/spark/work-dir/create_buckets.py"

upload-data-to-s3a:
	docker exec spark-master bash -c "python3 /opt/spark/work-dir/upload_data_to_s3a.py"

create-tables:
	docker exec spark-master spark-sql --master spark://spark-master:7077 --deploy-mode client -f ./setup.sql

count-tables:
	docker exec spark-master spark-sql --master spark://spark-master:7077 --deploy-mode client -f ./count.sql

setup: datagen create-buckets create-tables upload-data-to-s3a

## setup: datagen fake-datagen create-buckets create-tables upload-data-to-s3a

## Spark UIs: master UI, Spark application UI & History Server UI

hserver-ui:
	open http://localhost:18080

ui:
	open http://localhost:4040

master-ui:
	open http://localhost:9090
	
minio:
	open http://localhost:9000
	
rstudio:
	open http://localhost:8787

## Start Pyspark and Spark SQL REPL sessions

pyspark:
	docker exec -ti spark-master bash pyspark --master spark://spark-master:7077 

spark-sql:
	docker exec -ti spark-master spark-sql --master spark://spark-master:7077 

## Pyspark runner

cq: 
	@read -p "Enter .sql relative path:" sql_path; docker exec -ti spark-master spark-sql --master spark://spark-master:7077 -f $$sql_path

cr: 
	@read -p "Enter pyspark relative path:" pyspark_path; docker exec -ti spark-master spark-submit --master spark://spark-master:7077 $$pyspark_path

## Jupyter server

notebook:
	docker exec spark-master bash -c "jupyter notebook --ip=0.0.0.0 --port=3000 --allow-root"