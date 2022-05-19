FROM ubuntu
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get upgrade -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y curl build-essential libssl-dev libpcre3-dev zlib1g-dev
WORKDIR /ats
RUN curl -L https://dlcdn.apache.org/trafficserver/trafficserver-9.1.2.tar.bz2 > ats.tar.bz2 && \
    tar xf ats.tar.bz2 && \
    cd trafficserver-9.1.2 && \
    ./configure --prefix=/opt/ts && \
    make && \
    make install
COPY records.config /opt/ts/etc/trafficserver/records.config
COPY remap.config /opt/ts/etc/trafficserver/remap.config

CMD ["/opt/ts/bin/traffic_manager"]