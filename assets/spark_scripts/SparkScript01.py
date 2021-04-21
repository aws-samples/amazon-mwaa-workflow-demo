# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import argparse


def transform_data(spark, source_bucket, destination_bucket):
    movies = (spark.read.option("header", "true")
              .option("delimiter", ",")
              .option("inferSchema", "true")
              .csv(f"{source_bucket}"))

    movies.write.mode('overwrite').parquet(f"{destination_bucket}")


def parse_arguments():
    spark_job_parser = argparse.ArgumentParser(description='PySpark Job Arguments')
    spark_job_parser.add_argument('--source_bucket', action='store', type=str, required=True)
    spark_job_parser.add_argument('--destination_bucket', action='store', type=str, required=True)
    spark_job_parser.add_argument('--app_name', action='store', type=str, required=True)
    pyspark_args = spark_job_parser.parse_args()
    pyspark_args.app_name
    return pyspark_args


def main():
    pyspark_args = parse_arguments()

    spark = SparkSession.builder.appName(pyspark_args.app_name).getOrCreate()

    transform_data(spark,
                   source_bucket=pyspark_args.source_bucket,
                   destination_bucket=pyspark_args.destination_bucket
                   )


if __name__ == '__main__':
    main()
