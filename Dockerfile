FROM python:3.9

WORKDIR /WIADVANCE.AUTH

ADD . /WIADVANCE.AUTH

RUN pip3 install -r requirements.txt

CMD ["flask","run"]