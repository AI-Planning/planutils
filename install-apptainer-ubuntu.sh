#!/usr/bin/env bash

# exit when any command fails
set -e

APPTAINER_VERSION=$1
GO_VERSION=$2

# Install apptainer from release package on amd64
ARCH=$(arch)
if [ $ARCH == "x86_64" ]; then
  DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y wget
  DEBIAN_PACKAGE_NAME=apptainer_$APPTAINER_VERSION_amd64.deb
  wget https://github.com/apptainer/apptainer/releases/download/v$APPTAINER_VERSION/$DEBIAN_PACKAGE_NAME
  dpkg -i $DEBIAN_PACKAGE_NAME
  rm $DEBIAN_PACKAGE_NAME
  exit
fi

# Else, build it from source.
# Install build dependencies.
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
  build-essential \
  libssl-dev \
  uuid-dev \
  libgpgme11-dev \
  squashfs-tools \
  libseccomp-dev \
  wget \
  pkg-config \
  git \
  cryptsetup \
  curl \
  ca-certificates \
  squashfs-tools

# Install Golang
# $2: GOLANG_VERSION
if [ "$ARCH" == "aarch64" ]; then
  GO_ARCH="arm64" # go uses "arm64" whereas ubuntu uses "aarch64", but it is the same.
fi
GO_ARCHIVE_NAME=go$GO_VERSION.linux-$GO_ARCH.tar.gz
wget -qO - https://go.dev/dl/$GO_ARCHIVE_NAME | tar -C /usr/local -xzv
export PATH=/usr/local/go/bin:$PATH
echo 'export PATH=/usr/local/go/bin:$PATH' >>~/.bashrc
go version

# Install Apptainer
# $1: APPTAINER_VERSION
APPTAINER_BASE_NAME=apptainer-$APPTAINER_VERSION
wget -qO - https://github.com/apptainer/apptainer/releases/download/v$APPTAINER_VERSION/$APPTAINER_BASE_NAME.tar.gz | tar -xzv
cd $APPTAINER_BASE_NAME
./mconfig
make -C builddir
make -C builddir install
cd ..
rm -rf $APPTAINER_BASE_NAME
