FROM python:3.6

COPY . /iqass
CMD ["python3", "/iqass/iqass.py"]
