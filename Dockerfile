FROM ubuntu:16.04

MAINTAINER modoojunko

RUN apt-get update && apt-get -y install python3 python3-dev python3-pip

RUN mkdir /opt/Centimani/cloc -p

COPY . /opt/Centimani/cloc/

RUN pip3 install -r /opt/Centimani/cloc/requirements.txt

WORKDIR /opt/Centimani/cloc/

CMD ["python3", "run.py"]