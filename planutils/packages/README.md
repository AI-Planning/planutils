# planutils packages

Each package must contain the files `manifest.json`, `install`, and `uninstall`. Optionally, `run` can be included if the package installs a command-line executable (e.g., planners). An example of all four files can be found in the `TEMPLATE` directory, and a description of each follows.

## manifest.json

Details on the package. Must include:

1. **name**: Long-form name of the package.
2. **shortname**: Short-form name that will be used for installation, running, etc.
3. **description**: General description of the package.
4. **dependencies**: List of shortnames for other `planutils` packages that are required.

## install

Script to install the package along with any dependencies not part of `planutils`.

## uninstall

Cleanup script to remove the package installation.

## run

(optional) Script to run the installed package. `shortname` specified in the `manifest.json` file will be used for the command-line invocation of this script.
