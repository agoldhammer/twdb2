FROM alpine:3.7
# modified from
# https://medium.com/@greut/minimal-python-deployment-on-docker-with-uwsgi-bc5aa89b3d35

EXPOSE 3031

RUN apk add --no-cache \
	uwsgi-python3 \
	python3

COPY testeudkr.conf .

COPY requirements.txt .

RUN pip install -r requirements.txt

# to revise topics in db, run maketopics in container
# env TWDBCONF=/testeudkr.conf

COPY eutopics.txt .
COPY euauthors.txt .

COPY dist/twdb2-0.1.tar.gz /twdb2-0.1.tar.gz

RUN pip install twdb2-0.1.tar.gz

RUN mkdir -p /var/log/twdb2

RUN touch /var/log/twdb2/testeu.log

# to update db, run readfeed
# to query db run query -d 1 querytext
