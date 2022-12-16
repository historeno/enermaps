FROM ubuntu:20.04
# SET TZ for GDAL
ENV TZ=Europe/Zurich
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN chmod 1777 /tmp # needed since July 2021 to be run on an Ubuntu 20.04.3 LTS server
RUN apt-get update &&\
    apt-get --yes install python3 python3-pip git \
    postgresql-client \
    gdal-bin \
    proj-bin \
    libgdal-dev &&\
    rm -rf /var/cache/apt/archives/

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

COPY requirements.txt /data-integration/requirements.txt
WORKDIR data-integration
RUN pip3 install -r requirements.txt

COPY *.py /data-integration/
# COPY data/fake_data/ /data-integration/data/fake_data/
COPY data/ch_data/ /data-integration/data/ch_data/
COPY data/fake_data/ /data-integration/data/fake_data/
COPY inputs/ /data-integration/inputs/

# Make pipelines executable
RUN chmod u+x *.py

# should be a cront job in the production phase
CMD ["python3", "integrate.py"]
