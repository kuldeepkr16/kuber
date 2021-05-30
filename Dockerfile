FROM python:3
WORKDIR /kuber
COPY requirements.txt main.py ./
RUN pip install -r requirements.txt
COPY holdings.csv my_stocks.csv
ENV GMAIL_APP_S_USER="<senders emailID>" GMAIL_APP_R_USER="<reveivers emailID>" GMAIL_APP_PASSWORD="<password>"
CMD python3 main.py