FROM ubuntu:20.04

# set timezone
ENV TZ=Europe/Zurich
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    apt-get --yes install \
        python3 \
        python3-pip \
        libgdal-dev \
        && \
    rm -rf /var/cache/apt/archives/

WORKDIR cm-raster-statistics
COPY cm_raster_statistics/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY base /tmp/base
RUN cd /tmp/base && pip3 install . && python3 test.py
COPY cm_raster_statistics .
RUN python3 test.py
CMD ["python3", "worker.py"]