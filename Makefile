

build:
	docker build . -t tarasenkoas/iqass:build

test:
	python3 test.py

install:
    ./install.sh

run: build
	docker run -it tarasenkoas/iqass:build

deploy: build
	docker push tarasenkoas/iqass


