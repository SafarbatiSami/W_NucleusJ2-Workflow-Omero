# Image de base officielle de PyTorch
FROM pytorch/pytorch:latest

# Mise à jour et installation des dépendances nécessaires
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    python3-pip \
    git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------------------
# Install Cytomine python client
RUN git clone https://github.com/cytomine-uliege/Cytomine-python-client.git && \
    cd Cytomine-python-client/ && git checkout tags/v2.7.3 && pip install . && \
    rm -rf /Cytomine-python-client

# ------------------------------------------------------------------------------
# Install BIAFLOWS utilities (annotation exporter, compute metrics, helpers,...)
RUN apt-get update && apt-get install libgeos-dev -y && apt-get clean
RUN git clone https://github.com/Neubias-WG5/biaflows-utilities.git && \
    cd biaflows-utilities/ && git checkout tags/v0.9.2 && pip install . --no-deps

# install utilities binaries
RUN chmod +x biaflows-utilities/bin/*
RUN cp biaflows-utilities/bin/* /usr/bin/ && \
    rm -r biaflows-utilities/

# ------------------------------------------------------------------------------

# Installation de biom3d 
RUN pip install biom3d

# Ajout des fichiers de l'application
ADD wrapper.py /app/wrapper.py
ADD descriptor.json /app/descriptor.json

ENTRYPOINT ["python3.7","/app/wrapper.py"]
