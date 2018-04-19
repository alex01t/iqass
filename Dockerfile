FROM ubuntu

RUN apt-get update && apt-get install -y git python3
COPY . /iqass
CMD ["python3", "/iqass/iqass.py"]
