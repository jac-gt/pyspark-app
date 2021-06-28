import json
from pyspark.sql import SparkSession
from jobs import anonymize


def main():
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    spark = SparkSession.builder.appName(config.get("app_name")).getOrCreate()
    anonymize.run_job(spark, config)


if __name__ == "__main__":
    main()
