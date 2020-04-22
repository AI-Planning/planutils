# planning-utils
General library for setting up linux-based environments for developing, running, and evaluating planners.


## Usage
This doesn't work yet, but gives a general sense of where the project may be headed.

```
$ planning-utils --install-planners ipc-2018
This will require 3Gb of storage. Proceed? [Y/n] 
Fetching all of the planners from IPC-2018 for use on the command line...

$ planning-utils --setup-server-environment
Setting up a webserver to call the installed planners...

$ planning-utils --setup-development-environment
Installing common dependencies for building planners...
Installing common planning libraries...

$ planning-utils install-planning-domains
Installing the command-line utilities...
Installing the python library...
Fetching default benchmarks...

$ planning-utils --setup-evaluation configuration.json
Installing Lab...
Configuring Lab...
Ready!
Run eval.py to evaluate

$ lama domain.pddl problem.pddl
The lama planner requires the FastDownward to be installed. Install now (30Mb)? [Y/n] Y
Installing FastDownward...
Ready! Please try running the planner again.

$ lama domain.pddl problem.pddl
Parsing...
```