FROM ubuntu:22.04

LABEL maintainer="Christian Muise (christian.muise@queensu.ca)"

# Install required packages
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
        bash-completion \
        ca-certificates \
        git \
        libseccomp-dev \
        python3 \
        python3-pip \
        python3-venv \
        squashfs-tools \
        tzdata \
        unzip \
        vim \
        wget \
        build-essential \
        gcc-x86-64-linux-gnu \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/apptainer/apptainer/releases/download/v1.0.2/apptainer_1.0.2_amd64.deb \
    && dpkg -i apptainer_1.0.2_amd64.deb \
    && rm apptainer_1.0.2_amd64.deb

RUN pip3 install --upgrade pip
RUN pip3 install setuptools

# Install & setup the planutils
RUN pip3 install planutils --trusted-host pypi.org --trusted-host files.pythonhosted.org
RUN planutils setup

WORKDIR /root

# default command to execute when container starts
CMD /bin/bash
