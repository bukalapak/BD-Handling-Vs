# Copyright (c) 2018 PT Bukalapak.com
# Distributed under the terms of the MIT License.
ARG BASE_CONTAINER=jupyter/base-notebook
FROM $BASE_CONTAINER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

USER root

# Install Kafka
RUN apt-get update && apt-get install -yq --no-install-recommends \
    python-dev \
    librdkafka-dev \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch back to jovyan to avoid accidental container runs as root
USER $NB_UID

# Install pip packages
RUN pip install --upgrade confluent-kafka

