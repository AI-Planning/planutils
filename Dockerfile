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
	wget

# install python and related
RUN apt-get install -y python3 python3-dev python3-pip python3-venv
RUN pip3 install --upgrade pip

# get a recent version of singularity
RUN wget -O- http://neuro.debian.net/lists/bionic.us-nh.full | tee /etc/apt/sources.list.d/neurodebian.sources.list
RUN apt-key adv --recv-keys --keyserver hkp://pool.sks-keyservers.net:80 0xA5D32F012649A5A9
RUN apt-get update && apt-get install -y singularity-container

# install the planutils
RUN pip3 install planutils

# default command to execute when container starts
CMD /bin/bash
