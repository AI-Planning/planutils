

# Instructions to build and deploy the docker image:
# docker build -t aiplanning/cpor .
# docker push aiplanning/cpor

# Building it locally if apptainer is installed:
# apptainer build cpor.sif docker-daemon://aiplanning/cpor:latest



# This file has been modified from the FastDownward version

# The recipe below implements a Docker multi-stage build:
# <https://docs.docker.com/develop/develop-images/multistage-build/>

###############################################################################
# A first image to build the planner
###############################################################################
FROM ubuntu:22.04 AS builder


RUN apt-get update && apt-get -y install locales
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata

RUN apt-get update && apt-get install --no-install-recommends -y \
    ca-certificates \
    build-essential \
    cmake           \
    make            \
    g++             \
    git             \
    libgmp3-dev     \
    make            \
    python3         \
    wget            \
    time            \
    graphviz        \
    time            \
    bc              \
    zlib1g-dev

RUN apt-get install -y mono-complete mono-devel mono-xbuild

# install python and related
RUN apt-get install -y python3 python3-dev python3-pip python3-venv python-is-python3
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade graphviz
RUN pip3 install --upgrade networkx
RUN pip3 install --upgrade pydot

# fetch all the code and build the project
WORKDIR /workspace
RUN git clone https://github.com/aiplan4eu/up-cpor.git
WORKDIR /workspace/up-cpor/CPORLib
RUN mono-csc -recurse:*.cs -r:../TestCPORLib/bin/Debug/net6.0/Microsoft.Solver.Foundation.dll


###############################################################################
# The final image to run the planner
###############################################################################
FROM ubuntu:22.04 AS runner

RUN apt-get update && apt-get install --no-install-recommends -y \
    python3 time python-is-python3 mono-runtime \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace/cpor/

# Copy the relevant files from the previous docker build into this build.
COPY --from=builder /workspace/up-cpor/CPORLib/Run.exe .

RUN echo "#!/bin/bash" > /workspace/cpor/run.sh
RUN echo "mono /workspace/cpor/Run.exe \$@" >> /workspace/cpor/run.sh
RUN chmod a+x /workspace/cpor/run.sh

ENTRYPOINT ["/workspace/cpor/run.sh"]

