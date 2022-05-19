# planutils packages

Each package must contain the files `manifest.json`, `install`, and `uninstall`. Optionally, `run` can be included if the package installs a command-line executable (e.g., planners). An example of all four files can be found in the `TEMPLATE` directory, and a description of each follows. The directory name will correspond to how the package is run from the command line.

## manifest.json

Details on the package. Must include:

1. **name**: Long-form name of the package.
2. **description**: General description of the package.
3. **install-size**: Size of the package (estimated by `planutils` after you install it)
4. **dependencies**: List of shortnames for other `planutils` packages that are required.

## install

Script to install the package along with any dependencies not part of `planutils`.

## uninstall

Cleanup script to remove the package installation.

## run

(optional) Script to run the installed package. `shortname` specified in the `manifest.json` file will be used for the command-line invocation of this script.
