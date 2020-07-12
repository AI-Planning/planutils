# planutils

General library for setting up linux-based environments for developing, running, and evaluating planners.

## Usage

### Example of currently working functionality

```bash
$ lama domain.pddl problem.pddl

Package not installed!
  Download & install? [Y/n] y

About to install the following packages: downward (36M), lama (20K)
  Proceed? [Y/n] y
Installing downward...
INFO:    Downloading shub image
 35.88 MiB / 35.88 MiB [=======================================] 100.00% 3.99 MiB/s 8s
Finished installing downward (size: 36M)
Installing lama...
Finished installing lama (size: 20K)
Successfully installed lama!

Original command: lama
  Re-run command? [Y/n] y

Parsing...
$
```

### Example of upcoming functionality

```bash
$ planutils install ipc-2018
Installing planners
This will require 3Gb of storage. Proceed? [Y/n]
Fetching all of the planners from IPC-2018 for use on the command line...

$ planutils install server-environment
Setting up a webserver to call the installed planners...

$ planutils install development-environment
Installing common dependencies for building planners...
Installing common planning libraries...

$ planutils install planning-domains
Installing the command-line utilities...
Installing the python library...
Fetching default benchmarks...

$ planutils setup-evaluation configuration.json
Installing Lab...
Configuring Lab...
Ready!
Run eval.py to evaluate

$
```

### Docker

The included Docker file will come with planutils pre-installed. Note that in order to
run a number of the planners (all those that are based on singularity), you will need
to run the docker with the `--privileged` option.
