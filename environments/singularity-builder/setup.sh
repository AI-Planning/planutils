#!/bin/bash

[ "$UID" -eq 0 ] || (echo "installation requires root access"; exec sudo "$0" "$@")

apt update
apt install curl

# Install docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh



# Write the example Docker and Singularity files.
mkdir example

cat > example/Dockerfile <<- EOM
# The recipe below implements a Docker multi-stage build:
# <https://docs.docker.com/develop/develop-images/multistage-build/>

###############################################################################
## First stage: an image to build the planner.
## 
## We'll install here all packages we need to build the planner
###############################################################################
FROM ubuntu:18.04 AS builder

RUN apt-get update && apt-get install --no-install-recommends -y \
    cmake           \
    ca-certificates \
    curl            \
    g++             \
    make            \
    python3
    

WORKDIR /workspace/kstar/

# Set up some environment variables.
ENV CXX g++
ENV BUILD_COMMIT_ID 1d4647d


# Fetch the code at the right commit ID from the Github repo
RUN curl -L https://github.com/ctpelok77/kstar/archive/${BUILD_COMMIT_ID}.tar.gz | tar xz --strip=1

# Invoke the build script with appropriate options
RUN python3 ./build.py -j4 release64

# Strip the main binary to reduce size
RUN strip --strip-all builds/release64/bin/downward

###############################################################################
## Second stage: the image to run the planner
## 
## This is the image that will be distributed, we will simply copy here
## the files that we fetched and compiled in the previous image and that 
## are strictly necessary to run the planner
###############################################################################
FROM ubuntu:18.04

# Install any package needed to *run* the planner
RUN apt-get update && apt-get install --no-install-recommends -y \
    python3  \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace/kstar/

# Copy the relevant files from the previous docker build into this build.
COPY --from=builder /workspace/kstar/fast-downward.py .
COPY --from=builder /workspace/kstar/builds/release64/bin/ ./builds/release64/bin/
COPY --from=builder /workspace/kstar/driver ./driver

# ENTRYPOINT ["/usr/bin/python3", "/workspace/kstar/fast-downward.py", "--build", "release64"]
CMD /bin/bash
EOM

cat > example/Singularity <<- EOM
Bootstrap: docker-daemon
From: ctpelok77/kstar:latest

%setup
    # Just for diagnosis purposes
    hostname -f > $SINGULARITY_ROOTFS/etc/build_host

%runscript
    # This will be called whenever the Singularity container is invoked
    DOMAINFILE=$1
    PROBLEMFILE=$2
    PLANFILE=$3
    NUMPLANS=$4

    python3 /workspace/kstar/fast-downward.py --build release64 --plan-file $PLANFILE $DOMAINFILE $PROBLEMFILE --search "kstar(blind(),k=$NUMPLANS)"


%labels
Name        K*
Description The K* planner
Authors     Michael Katz <michael.katz1@ibm.com>, Shirin Sohrabi <ssohrab@us.ibm.com>, Octavian Udrea <udrea@us.ibm.com> and Dominik Winterer <dominik_winterer@gmx.de>
EOM