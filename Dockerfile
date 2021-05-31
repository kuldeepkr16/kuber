FROM python:3.9-slim-buster
WORKDIR /kuber
COPY requirements.txt main.py ./
RUN pip install -r requirements.txt
COPY my_stocks.csv my_stocks.csv
CMD python3 main.py