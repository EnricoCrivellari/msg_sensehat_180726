FROM resin/raspberry-pi3-debian:jessie

RUN apt-get update && apt-get install -yq \
   python sense-hat raspberrypi-bootloader && pip install paho-mqtt && \
   apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY . .

ENV INITSYSTEM on

CMD ["python", "/usr/src/app/src/thread_sense.py"]
