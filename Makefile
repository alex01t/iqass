

build:
    docker build -t tarasenkoas/iqass

test:
    docker run tarasenkoas/iqass:latest python3 /iqass/test.py

run:
    docker run tarasenkoas/iqass:latest

deploy: build
    docker push tarasenkoas/iqass


