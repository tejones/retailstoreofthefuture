FROM intelpython/intelpython3_core

RUN conda install notebook pandas scikit-learn && \
	conda install -c conda-forge imbalanced-learn

RUN mkdir data-mining

COPY original_data data-mining/original_data
COPY *.ipynb data-mining/

WORKDIR /data-mining

CMD jupyter notebook --ip 0.0.0.0 --port 8000 --no-browser --allow-root

