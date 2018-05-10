

build:
	docker build . -t tarasenkoas/iqass:build

test:
	python3 test.py

install:
	./install.sh

run: build
	docker run --rm --link iqass-db:postgres tarasenkoas/iqass:build

daemon: build
	docker stop iq || true
	docker rm iq || true
	docker run -dit --restart unless-stopped --name iq --link iqass-db:postgres tarasenkoas/iqass:build

feed:
	date && docker run --rm --link iqass-db:postgres tarasenkoas/iqass:build python3 /iqass/feed.py > /var/www/html/index.html

deploy: build
	docker push tarasenkoas/iqass


