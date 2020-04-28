
import json, os, glob


PLANNERS = {}

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

for conf_file in glob.glob(os.path.join(CUR_DIR, 'planner_configs', '*')):
    with open(conf_file, 'r') as f:
        config = json.load(f)
    assert config['shortname'] not in PLANNERS, "Error: Duplicate planner config -- %s" % config['shortname']
    PLANNERS[config['shortname']] = config

# TODO: Pull in the collection configs and setup the dict
COLLECTIONS = {}

def install(target):
    if 'list' == target:
        print("\nCollections:")
        for c in COLLECTIONS:
            print(" - %s" % c)

        print("\nPlanners:")
        for p in PLANNERS:
            print(" - %s: %s" % (p, PLANNERS[p]['name']))
        
        print()

    elif target in PLANNERS:
        install_planner(target)

    elif target in COLLECTIONS:
        install_planners(target)
    

# singularity pull --name downward.simg shub://aibasel/downward
# singularity run downward.simg --alias lama-first $BENCHMARKS/gripper/prob01.pddl


def binary_path(planner):
    return os.path.join('~', '.planning-utils', 'bin')

def install_planners(planner_set):
    raise NotImplementedError

def install_planner(planner):

    assert planner in PLANNERS, "Error: Planner not found -- %s" % planner
    
    if PLANNERS[planner]['method'] == 'proxy':
        install_planner(PLANNERS[planner]['details']['base'])
        cmd = "%s %s" % (PLANNERS[planner]['details']['base'], PLANNERS[planner]['details']['suffix'])
    
    elif PLANNERS[planner]['method'] == 'singularity':
        os.system("singularity pull --name %s %s" % \
            (PLANNERS[planner]['details']['name'], PLANNERS[planner]['details']['shub']))
        cmd = "singularity run %s" % PLANNERS[planner]['details']['name']
    
    script = "#!/bin/bash\n"
    script = "%s $@\n"

    with open(binary_path(planner), 'w') as f:
        f.write(script)
