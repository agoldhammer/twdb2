FROM python:latest

COPY testeudkr.conf .

COPY requirements.txt .

# to revise topics in db, run maketopics in container
# env TWDBCONF=/testeudkr.conf
COPY eutopics.txt .
COPY euauthors.txt .

COPY dist/twdb-0.1.tar.gz /twdb2-0.1.tar.gz

RUN pip install -r requirements.txt

RUN pip install twdb2-0.1.tar.gz

RUN mkdir -p /var/log/twdb2

RUN touch /var/log/twdb/testeu.log

# to update db, run readfeed
# to query db run query -d 1 querytext
