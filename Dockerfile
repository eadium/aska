FROM ubuntu:18.04

ENV WORK /opt/aska
WORKDIR $WORK

ENV DEBIAN_FRONTEND 'noninteractive'
RUN echo 'Europe/Moscow' > '/etc/timezone'


RUN apt-get -y update
RUN apt-get -y install wget python3-pip

RUN pip3 install Django==2.2.3
RUN pip3 install django-dynamic-fixture --upgrade
RUN pip3 install Pillow

ADD . $WORK/

EXPOSE 8000

CMD python3 /opt/aska/manage.py migrate &&\
    python3 /opt/aska/manage.py runserver 0.0.0.0:8000
