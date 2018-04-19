

build:
	docker build . -t tarasenkoas/iqass

test: build
	docker run tarasenkoas/iqass:latest python3 /iqass/test.py

run: build
	docker run -it tarasenkoas/iqass:latest

deploy: build
	docker push tarasenkoas/iqass


