FROM ubuntu:18.04

RUN apt update && \
    apt install -y software-properties-common && \
    apt install -y default-jre && \
    apt install -y python3-pip

RUN mkdir data-mining

COPY data_0408_0 data-mining/data_0408_0
COPY *.ipynb data-mining/
COPY requirements.txt data-mining/

RUN pip3 install -r /data-mining/requirements.txt

WORKDIR /data-mining

CMD jupyter notebook --ip 0.0.0.0 --port 8000 --no-browser --allow-root
