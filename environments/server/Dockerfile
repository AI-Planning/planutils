
# Build the Planutils image and install the selected packages
FROM aiplanning/planutils:latest

# Needed for the server
RUN pip3 install flask

# FD Planner
RUN planutils install -f -y lama-first

# Satisficing classical planning
RUN planutils install -f -y dual-bfws-ffparser

# Optimal classical planning
RUN planutils install -f -y delfi

# top-k classical planning
RUN planutils install -f -y forbiditerative-topk

# numeric planning
RUN planutils install -f -y enhsp-2020

# PDDL3 support
RUN planutils install -f -y optic

# Temporal planning
RUN planutils install -f -y tfd

EXPOSE 5555

CMD planutils server --port 5555 --host 0.0.0.0
