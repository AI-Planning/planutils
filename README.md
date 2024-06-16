# planutils

A general library for setting up Linux-based environments for developing, running, and evaluating planners.

There are several ways to use planutils.
The easiest ones, based on the provided Docker image, are explained below.
If you use planutils for a publication, please cite the following paper:

```
@InProceedings{muise-et-al-icaps2022systemdemos,
  author       = "Christian Muise and Florian Pommerening and Jendrik Seipp and Michael Katz",
  title        = "Planutils: Bringing Planning to the Masses",
  booktitle    = "{ICAPS} 2022 System Demonstrations",
  year         = "2022"
}
```

## 1. Running the latest Docker release

The released Docker image comes with the latest planutils pre-installed.
This means that in order to run the latest release, it is not necessary to clone this repository.
Note that in order to run some of the planners (all those that are based on singularity), you will need to run Docker with the `--privileged` option.

**Run the planutils container**
```sh
docker run -it --privileged aiplanning/planutils:latest bash
```

**Active the planutils environment**
```sh
planutils activate
```

## 2. Making your own image with desired solvers

Below is an example for creating your own Dockerfile based on the latest release, with pre-installed solvers.
```sh
FROM aiplanning/planutils:latest

# Install solvers and tools
RUN planutils install -y val
RUN planutils install -y planning.domains
RUN planutils install -y popf
RUN planutils install -y optic
RUN planutils install -y smtplan
```

## 3. Running planutils from source
You can also run the latest unreleased version. For this, clone this repository and run
```sh
docker build . -t planutils-dev:latest
```

## 4. Usage

### Example of current functionality

```
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

```
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



## 5. Add a new package
### Package Configuration
1. Create a folder for the new package, the folder name will be the used to call the planner later.
2. Set up the `install`, `run`,  `uninstall`, and `manifest.json` files. You can find the template files under `packages/TEMPLATE`.

### Write Manifest file

Create a manifest file named `manifest_compact.json` if you want to use predefined templates in the `packages/TEMPLATE/SERVICE_TEMPLATE` folder. The full `manifest.json` will be generated at run time. You can overwrite the default template by restating the value of some JSON fields.

You can also create a `manifest.json` file directly if you don't need the template.

**Manifest Example**
```json
{
    "name": "LAMA-FIRST",
    "description": "http://fast-downward.org/",
    "install-size": "20K",
    "dependencies": [
        "downward"
    ],
    "endpoint": {
        "services": {
            "solve": {
                "args": [
                    {
                        "name": "domain",
                        "type": "file",
                        "description": "domain file"
                    },
                    {
                        "name": "problem",
                        "type": "file",
                        "description": "problem file"
                    }
                ],
                "call": "lama-first {domain} {problem}",
                "return": {
                    "type": "generic",
                    "files": "*plan*"
                }
            }
        }
    }
}
```
**Define Args**

There are four types of Args: `file`, `int`, `string` and,`categorical`. You can add default values for `int`,`string`, and `categorical` arguments.

```json
 "args": [
    {
        "name": "domain",
        "type": "file",
        "description": "domain file"
    },
    {
        "name": "number_of_plans",
        "type": "int",
        "description": "Number of Plans",
        "default":3
    },
    {
        "name": "custom_search_algorithm",
        "type": "string",
        "description": "Custom Search Algorithm",
        "default":"kstar(blind(),k=1)"
    },
    {
        "name": "search_algorithm",
        "type": "categorical",
        "description": "Search Algorithm",
        "choices":[
          {
            "display_value":"Kstar Blind k=1",
            "value":"kstar(blind(),k=1)"
          },
          {
            "display_value":"Kstar Blind k=2",
            "value":"kstar(blind(),k=2)"
          }
        ],
        "default":"kstar(blind(),k=1)"
    }
]
```
**Define Return Types**

There are three types of return data: `generic`, `json` and `log`. The `generic` type should be used for all text based results, the `log` type should be used for planners like Optic and Tfd which don't generate "proper" plans, and the `json` type should be used for plans in JSON format.

For the value of `files`, you will have to write a [glob](https://docs.python.org/3/library/glob.html) pattern. The planning-as-service backend uses the `glob` library to find and return all the files that matched.
```json
"return": {
                    "type": "generic/log/json",
                    "files": "*plan*"
                }
```
