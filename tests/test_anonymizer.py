import pytest
import shutil
import os
from jobs import anonymize
from pathlib import Path

@pytest.mark.usefixtures("spark_session")
def test_all_rows_must_be_present_in_output(spark_session):
    test_df = spark_session.createDataFrame(
        [('Michael', 'Smith', '10 London', '2000-Jan-20'),
         ('Andy', 'Scott', '30 London', '1990-Oct-20')],
        ['first_name', 'last_name', 'address', 'date_of_birth']
    )
    output_df = anonymize.anonymize_columns(test_df)
    assert output_df.count() == 2


@pytest.mark.usefixtures("spark_session")
def test_first_name_last_name_address_is_anaonymized(spark_session):
    test_df = spark_session.createDataFrame(
        [('Michael', 'Smith', '10 London', '2000-Jan-20'),
         ('Andy', 'Scott', '30 London', '1990-Oct-20')],
        ['first_name', 'last_name', 'address', 'date_of_birth']
    )
    output_df = anonymize.anonymize_columns(test_df)

    output_df.createOrReplaceTempView("output")

    sql_df = spark_session.sql("Select * from output "
                               " where lower(first_name) in ('michael', 'andy')"
                               " or lower(last_name) in ('smith', 'scott')"
                               " or lower(address) like '%london%' ")
    assert sql_df.count() == 0


@pytest.mark.usefixtures("spark_session")
def test_run_job(spark_session, mocker):
    test_config = {"output_data_path": "test_data_output"}
    output_path = Path(test_config.get("output_data_path"))
    if output_path.exists() and output_path.is_dir():
        shutil.rmtree(test_config.get("output_data_path"))
    test_df = spark_session.createDataFrame(
        [('Michael', 'Smith', '10 London', '2000-Jan-20'),
         ('Scott', 'Philip', '20 Munich', '2000-Jan-20'),
         ('Andy', 'Scott', '30 London', '1990-Oct-20')],
        ['first_name', 'last_name', 'address', 'date_of_birth']
    )
    mocker.patch.object(anonymize, "load_data")
    anonymize.load_data.return_value = test_df
    anonymize.run_job(spark_session, test_config)
    assert os.path.exists(test_config.get("output_data_path"))
