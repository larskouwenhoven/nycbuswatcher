FROM continuumio/miniconda3:latest

RUN apt-get update -y; apt-get upgrade -y

COPY environment.yml environment.yml

RUN conda env create -f environment.yml
RUN echo "alias l='ls -lah'" >> ~/.bashrc
RUN echo "source activate nycbuswatcher" >> ~/.bashrc

# Setting these environmental variables is the functional equivalent of running 'source activate my-conda-env'
ENV CONDA_EXE /opt/conda/bin/conda
ENV CONDA_PREFIX /opt/conda/envs/nycbuswatcher
ENV CONDA_PYTHON_EXE /opt/conda/bin/python
ENV CONDA_PROMPT_MODIFIER (nycbuswatcher)
ENV CONDA_DEFAULT_ENV nycbuswatcher
ENV PATH /opt/conda/envs/nycbuswatcher/bin:/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# copy repo
WORKDIR /
COPY . .
