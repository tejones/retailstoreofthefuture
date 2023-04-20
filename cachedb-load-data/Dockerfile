# from python
FROM python:3.9.1-slim-buster

ENV POSTGRES_USR="cachedb_user"
ENV POSTGRES_DB="cachedb"
ENV POSTGRES_PW="cachedb_pass"
ENV POSTGRES_HST="localhost"
ENV DATA_PATH="data"

COPY requirements.txt create_db.py load_data.py script.sh /loader/
COPY data/ /loader/data/
# set working directory
WORKDIR /loader

# install python requirements
RUN pip install -r requirements.txt
RUN chmod +x script.sh

# run the scripts
ENTRYPOINT ["bash", "-c", "/loader/script.sh"]
