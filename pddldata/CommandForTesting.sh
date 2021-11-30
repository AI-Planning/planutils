#!/bin/sh
# This is a comment!

# 1. Build docker image
docker build -t planutils:latest .
# 2. Start Docker container
docker run -it --privileged planutils bash

# 3. In the container terminal, type the following command to update the planutils

git clone https://github.com/AI-Planning/planutils.git
cd planutils
git checkout manifest-new-version
pip uninstall planutils
python3 setup.py install --old-and-unmanageable
planutils setupy

# 4.Install the package and test it
planutils install bfws
# 5.Test the planner, here are some pddl file in pddldata folder
cd pddldata
bfws domain.pddl problem.pddl

# You can find all the pacakges in this folder in the docker
/usr/local/lib/python3.6/dist-packages/planutils/packages/