

build:
	docker build . -t tarasenkoas/iqass:build

test:
	python3 test.py

install:
	./install.sh

run: build
	docker run -it --link iqass-db:postgres tarasenkoas/iqass:build

feed:
	docker run -it --link iqass-db:postgres tarasenkoas/iqass:build python3 /iqass/feed.py > /var/www/html/index.html

deploy: build
	docker push tarasenkoas/iqass


