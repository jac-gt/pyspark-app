# Demo Pyspark app

This pyspark app is to anonymize first_name, last_name, address, date_of_birth of an input(people.csv) CSV file.
The first_name and last_name is anonymized using soundex function and the address is replaced with xxxxx.

##Configuration
The application needs a config file(config.json) which gives the location of the input CSV file and the output location for the anonymized file
```
{
"app_name": "Anonymizer App",
"source_data_path": "data/input",
"output_data_path": "data/output"
}
```
##Running the code in a docker container
A docker container is used to run the code and test it. To create it the make tool is used. The docker container will have pyspark and pytest. The host folder dist is mapped to the docker container folder /app

```
$make
rm -rf ./dist && mkdir ./dist
cp ./main.py ./dist
cp ./config.json ./dist
cp -r ./jobs  ./dist/jobs
cp -r ./tests  ./dist/tests
cp conftest.py ./dist
cp -r ./data  ./dist/data
zip -r dist/jobs.zip jobs
  adding: jobs/ (stored 0%)
  adding: jobs/anonymize.py (deflated 59%)
  adding: jobs/__pycache__/ (stored 0%)
  adding: jobs/__pycache__/anonymize.cpython-38.pyc (deflated 40%)
  adding: jobs/__pycache__/anonymize.cpython-36.pyc (deflated 41%)
docker-compose --file docker/docker-compose.yml up
Starting <container_name> ... done
Attaching to <container_name>
```

##Running Tests
Pytest is used to test the code. To run the test cases first run the docker container by running make. This will build the docker image with pyspark and pytest. It will then create the docker container

Connect to the docker container by running 
```
docker exec -it <container_name> bash
```
To execute the test cases type pytest and it should run the tests and display the results

```
root@f3d569460a90:/app# pytest
================================================================ test session starts =================================================================
platform linux -- Python 3.6.9, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: /app
plugins: mock-3.6.1
collected 3 items

tests/test_anonymizer.py ...                                                                                                                   [100%]

================================================================== warnings summary ==================================================================
tests/test_anonymizer.py::test_all_rows_must_be_present_in_output
/usr/lib/python3.6/importlib/_bootstrap.py:219: RuntimeWarning: numpy.ufunc size changed, may indicate binary incompatibility. Expected 192 from C header, got 216 from PyObject
return f(*args, **kwds)

-- Docs: https://docs.pytest.org/en/stable/warnings.html
=========================================================== 3 passed, 1 warning in 14.34s ============================================================
```
##Running the anonymizer

To run the anonymizer in the container you can use the following:
```
$spark-submit --master local[8] --py-files jobs.zip --files config.json main.py
```

To submit it to a cluster give the proper master url and other options

## Important

Please note that the host folder and docker folder /app is mapped using docker volume. To delete the files which are created from the docker container you will need sudo access.