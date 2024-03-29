# Get parent image
FROM continuumio/miniconda3

# Set working directory 
WORKDIR /workspace

# Copy the list of required dependencies to /tmp
COPY /environment.yml /tmp/environment.yml

# Create the environment with these dependencies:
RUN conda env create -f /tmp/environment.yml

# Pull the environment name out of the environment.yml and add to bashrc
RUN echo "source activate $(head -1 /tmp/environment.yml | cut -d' ' -f2)" > ~/.bashrc

ENV PATH /opt/conda/envs/$(head -1 /tmp/environment.yml | cut -d' ' -f2)/bin:$PATH
