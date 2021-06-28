build_dev:
	rm -rf ./dist && mkdir ./dist
	cp ./main.py ./dist
	cp ./config.json ./dist
	cp -r ./jobs  ./dist/jobs
	cp -r ./tests  ./dist/tests
	cp conftest.py ./dist
	cp -r ./data  ./dist/data
	zip -r dist/jobs.zip jobs
 	docker build -f docker/pyspark.Dockerfile -t pyspark-image .
	docker-compose --file docker/docker-compose.yml up
