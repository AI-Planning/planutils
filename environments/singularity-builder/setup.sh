#!/bin/bash

[ "$UID" -eq 0 ] || (echo "installation requires root access"; exec sudo "$0" "$@")

echo "Setting up your environment for building singularity containers requires the following:"
echo " - Installing curl and ca-certificates from apt"
echo " - Installing docker given the quickstart script at get.docker.com"
echo " - Creating an 'example' directory to house starter Dockerfile and Singularity files"
read -r -p "Proceed? [y/N]" varchoice
varchoice=${varchoice,,}
if ! [[ "$varchoice" =~ ^(yes|y)$ ]]
then
    echo "Cancelling setup."
    exit 0
else
    echo "Setting up environment..."
fi


apt update
apt install curl ca-certificates

# Install docker
curl -fsSL https://get.docker.com | sh
docker service start


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


WORKDIR /DEV/

# Set up some environment variables.
ENV CXX g++
ENV BUILD_COMMIT_ID 1234zxcv


# Fetch the code at the right commit ID from the Github repo
RUN curl -L https://github.com/whoever/whatever/archive/${BUILD_COMMIT_ID}.tar.gz | tar xz --strip=1

# Invoke the build script with appropriate options (this works with FD-based planners)
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

WORKDIR /DEV/

# Copy the relevant files from the previous docker build into this build.
COPY --from=builder /DEV/fast-downward.py .
COPY --from=builder /DEV/builds/release64/bin/ ./builds/release64/bin/
COPY --from=builder /DEV/driver ./driver

# ENTRYPOINT ["/usr/bin/python3", "/DEV/fast-downward.py", "--build", "release64"]
CMD /bin/bash
EOM

cat > example/Singularity <<- EOM
Bootstrap: docker-daemon
From: planner:latest

%setup
    # Just for diagnosis purposes
    hostname -f > $SINGULARITY_ROOTFS/etc/build_host

%runscript
    # This will be called whenever the Singularity container is invoked
    DOMAINFILE=$1
    PROBLEMFILE=$2
    PLANFILE=$3
    NUMPLANS=$4

    python3 /DEV/fast-downward.py --build release64 --plan-file $PLANFILE $DOMAINFILE $PROBLEMFILE --search "whatever(blind())"


%labels
Name        YourAwesomePlanner
Description Your very own awesome description.
Authors     Whoever <whoever@whatever.com>
EOM

echo
echo "Setup complete."
echo " - See example/ for the template Dockerfile and Singularity image."
echo " - It roughly corresponds to instructions for a FastDownward planner."
echo " - Once ready, build the docker image with 'docker build . -t planner'"
echo " - Once the docker builds, do the singularity with 'singularity build planner.sif Singularity'"
echo " - planner.sif can now be uploaded anywhere that is publicly accessible."
echo
