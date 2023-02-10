FROM ubuntu:22.04

LABEL maintainer="Christian Muise (christian.muise@queensu.ca)"

# Install required packages
WORKDIR /root/install
COPY install-apptainer-ubuntu.sh .
RUN bash install-apptainer-ubuntu.sh 1.0.3 1.18.3 \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    bash-completion \
    ca-certificates \
    git \
    libseccomp-dev \
    python3 \
    python3-pip \
    python3-venv \
    tzdata \
    unzip \
    vim \
    wget \
    build-essential \
    gcc-x86-64-linux-gnu \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip
RUN pip3 install setuptools

# Copy files and install
COPY . .
RUN python3 setup.py install

# Remove files
WORKDIR /root
RUN rm -rf install

# Setup the planutils
RUN planutils setup

# default command to execute when container starts
CMD /bin/bash
