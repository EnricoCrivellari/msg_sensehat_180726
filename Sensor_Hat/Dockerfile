FROM resin/raspberry-pi3-debian:jessie


RUN apt-get update && apt-get install -yq \
   python3 python sense-hat raspberrypi-bootloader python-pip python3-pip && \
   pip install paho-mqtt && \
   apt-get upgrade && \
   apt-get clean && rm -rf /var/lib/apt/lists/*


WORKDIR /usr/src/app

COPY . .

ENV INITSYSTEM on

CMD ["python", "/usr/src/app/src/thread_sense.py"]
