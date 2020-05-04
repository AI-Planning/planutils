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
    libssl-dev \
    uuid-dev \
    libgpgme11-dev \
    squashfs-tools \
    libseccomp-dev \
	ca-certificates \
    pkg-config \
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
RUN export VERSION=1.12 OS=linux ARCH=amd64 && \
    wget https://dl.google.com/go/go$VERSION.$OS-$ARCH.tar.gz && \
    tar -C /usr/local -xzvf go$VERSION.$OS-$ARCH.tar.gz && \
    rm go$VERSION.$OS-$ARCH.tar.gz
ENV GOPATH="${HOME}/go"
ENV PATH="/usr/local/go/bin:${PATH}:${GOPATH}/bin"

RUN export VERSION=3.2.0 && \
    wget https://github.com/sylabs/singularity/releases/download/v${VERSION}/singularity-${VERSION}.tar.gz && \
    tar -xzf singularity-${VERSION}.tar.gz

WORKDIR /singularity
RUN ./mconfig && make -C ./builddir && make -C ./builddir install

RUN echo '. /usr/local/etc/bash_completion.d/singularity' >> ~/.bashrc

# install & setup the planutils
RUN pip3 install planutils --trusted-host pypi.org --trusted-host files.pythonhosted.org
RUN planutils --setup

WORKDIR /root

# default command to execute when container starts
CMD /bin/bash
