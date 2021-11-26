
import sys
from planutils.package_installation import install, run

def entrypoint(name):
    install(name)
    run(name, sys.argv[1:])

import functools
import glob
import os.path

class Entrypoints():
    pass

entrypoints = Entrypoints()

for d in glob.glob(os.path.join(os.path.dirname(__file__),"packages","*")):
    if not os.path.isdir(d):
        continue

    name = os.path.basename(d)
    if name == "TEMPLATE":
        continue

    name2 = name.replace("-","_")
    setattr(entrypoints, name2, functools.partial(entrypoint, name))
