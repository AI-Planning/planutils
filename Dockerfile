FROM ubuntu:18.04

#maintainer information
LABEL maintainer="Christian Muise (christian.muise@queensu.ca)"

# update the apt package manager
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN apt-get update && apt-get -y install locales

# Install required packages
RUN apt-get update && apt-get install --no-install-recommends -y \
	build-essential \
	ca-certificates \
	curl \
	scons \
	gcc-multilib \
	flex \
	bison \
    vim \
    git \
	cmake \
	unzip \
	g++-multilib \
    singularity-container

# install python and related
RUN apt-get install -y python3 python3-dev python3-pip python3-venv
RUN pip3 install --upgrade pip

# install the planning-utils
RUN pip3 install planning-utils

# default command to execute when container starts
CMD /bin/bash
