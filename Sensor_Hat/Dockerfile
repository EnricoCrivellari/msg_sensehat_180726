FROM resin/raspberry-pi3-debian:jessie

RUN apt-get update && apt-get install -yq \
   python sense-hat raspberrypi-bootloader  && \
   apt-get clean && rm -rf /var/lib/apt/lists/*
RUN set -xe \
    && apt-get update \
    && apt-get install python-pip
RUN pip install --upgrade pip
RUN pip install paho-mqtt

WORKDIR /usr/src/app

COPY . .

ENV INITSYSTEM on

CMD ["python", "/usr/src/app/src/thread_sense.py"]
