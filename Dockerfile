# The build-stage image:
FROM continuumio/miniconda3:latest

WORKDIR /code

# Install necessary packages
RUN conda config --set always_yes yes --set changeps1 no
RUN conda update --all -y 
RUN conda config --add channels conda-forge
RUN conda install -c conda-forge conda-pack
    
# Install libmamba and set it as default solver
RUN conda install -n base conda-libmamba-solver
RUN conda config --set solver libmamba

# Install the package as normal:
# the environment.yaml file is downloaded from the git repo by the azure pipeline. 
# If this fails, then the repo is specified before this build doesn't have the environment.yaml at its top level
COPY prod_environment.yaml .
RUN conda env create -f prod_environment.yaml

COPY . ./

ENTRYPOINT ["/bin/bash", "run_server.sh"]