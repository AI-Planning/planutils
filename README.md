# planutils

General library for setting up linux-based environments for developing, running, and evaluating planners.


## 1. Docker

The included Docker file will come with planutils pre-installed. Note that in order to
run a number of the planners (all those that are based on singularity), you will need
to run the docker with the `--privileged` option.

**Build planutils images**
`docker build -t planutils:latest .`

**Run the plautils container**
`docker run -it --privileged planutils bash`

**Active the planutils environment**
`planutils activate`


## 2. Usage

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



## 3. Add a new package
### Package Configuration
1. Create a folder for new pacakeg, the package name will be the used to call the planner later
2. Set up the `install`, `run`,  `uninstall`, and manifest file. You can find the template files under packages/TEMPLATE folder

### Write Manifest file

Please create a manifest file named `manifest_compact.json` if you want to use predefined templates in the packages/TEMPLATE/SERVICE_TEMPLATE folder. The full `manifest.json` will be generated at the run time. You can overwrite the dafult template by restating the value of json fields. 

You can also create a `manifest.json` file directly if you don't need the template.

**Manifest Example**
```
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

There are four types of Args: `file`, `int`, `string` and,`categorical`. You can add default value for `int`,`string`, and `categorical` arguments

```
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

There are three types of return data: `generic`, `json` and `log`. The `generic` type should be used for all the text based result, the `log` type should be used for planner like Optic and Tfd which didn't generate a proper plan, and the type `json` should used for plan in JSON format.

For the value of `files`, you will have to write a [glob](https://docs.python.org/3/library/glob.html) pattern. Planning-as-service backend uses `glob` libary to find and return all the files that matched. 
```
"return": {
                    "type": "generic/log/json",
                    "files": "*plan*"
                }
```
