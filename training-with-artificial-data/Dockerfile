FROM ubuntu:18.04

ARG DATA_DIR=data-dir

RUN apt update && \
    apt install -y software-properties-common && \
    apt install -y default-jre && \
    apt install -y python3-pip

RUN mkdir data-mining

COPY requirements.txt data-mining/
RUN pip3 install -r /data-mining/requirements.txt

COPY $DATA_DIR/* data-mining/data_dir/
COPY *.ipynb data-mining/

WORKDIR /data-mining

CMD jupyter notebook --ip 0.0.0.0 --port 8000 --no-browser --allow-root
