FROM ubuntu

RUN apt-get update && apt-get install -y git python3
RUN git clone https://github.com/alex01t/iqass.git -b develop
CMD ["python3", "/iqass/iqass.py"]
