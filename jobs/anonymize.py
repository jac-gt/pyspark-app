from pyspark.sql.functions import soundex, trim, when


def anonymize_columns(input_df):
    # This function uses soundex to anonymize the first_name and last_name columns.
    # The address column is replaced with xxxxx if it has some value otherwise it's left as such
    return input_df.select(soundex(trim(input_df["first_name"])).alias("first_name"),
                           soundex(trim(input_df["last_name"])).alias("last_name"),
                           when(input_df["address"].isNull(), input_df["address"]).otherwise('xxxxx').alias("address"),
                           input_df["date_of_birth"]
                           )


def save_output(config, output_df):
    output_df.write.option("header", True).mode("overwrite").csv(f"{config.get('output_data_path')}/people")


def load_data(spark, config):
    return (
        spark.read.format("csv").option("header", True).load(f"{config.get('source_data_path')}/people.csv")
    )


def run_job(spark, config):
    save_output(config, anonymize_columns(load_data(spark, config)))
