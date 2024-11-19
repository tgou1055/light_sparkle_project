"""
Replicate IF.ELSE logic with CASE statements
"""
from pyspark.sql import SparkSession # type: ignore # pylint: disable=import-error
from pyspark.sql.functions import col, when # type: ignore # pylint: disable=import-error

def run_code(spark_obj):
    """
    Spark code runner

    params:
        :param spark: sparkSession object

    returns:

    """
    print("============================================")
    print("Replicate IF.ELSE logic with CASE statements")
    print("============================================")

    # Use tpch database;
    spark_obj.sql("USE tpch")
    # Read the 'orders' table
    orders = spark_obj.table("orders")

    # Apply the CASE statement using PySpark DateFrame API
    result = orders.select(
        col("orderkey"),
        col("totalprice"),
        when(col("totalprice") > 100000, "high")
        .when(
            (col("totalprice") >= 25000) & (col("totalprice") <= 100000),
            "medium",
        )
        .otherwise("low")
        .alias("order_price_bucket"),
    ).limit(20)

    # Show the result
    result.show()

if __name__ == '__main__':
    spark = (
        SparkSession.builder.appName("efficient-spark-data-processing")
        .enableHiveSupport()
        .getOrCreate()
    )
    # enable the hive support to query the table with meta data stored in metadata_db

    # Set the log level
    spark.sparkContext.setLogLevel("ERROR")
    run_code(spark_obj=spark)
    spark.stop()
