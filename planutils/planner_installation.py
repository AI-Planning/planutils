
import json, os, glob


PLANNERS = {}

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

for conf_file in glob.glob(os.path.join(CUR_DIR, 'planner_configs', '*.json')):
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
    

def binary_path(planner):
    return os.path.join(os.path.expanduser('~'), '.planutils', 'bin', planner)

def install_planners(planner_set):
    raise NotImplementedError

def install_planner(planner):

    assert planner in PLANNERS, "Error: Planner not found -- %s" % planner
    
    if PLANNERS[planner]['method'] == 'proxy':
        install_planner(PLANNERS[planner]['details']['base'])
        cmd = "%s %s" % (PLANNERS[planner]['details']['base'], PLANNERS[planner]['details']['suffix'])
    
    elif PLANNERS[planner]['method'] == 'singularity':
        image_path = os.path.join(binary_path(planner), 'images', PLANNERS[planner]['details']['name'])
        os.system("singularity pull --name %s %s" % \
            (PLANNERS[planner]['details']['name'], PLANNERS[planner]['details']['shub']))
        os.system("mv %s %s" % (PLANNERS[planner]['details']['name'], image_path))
        cmd = "singularity run %s" % image_path
    
    script  = "#!/bin/bash\n"
    script += "%s $@\n" % cmd

    with open(binary_path(planner), 'w') as f:
        f.write(script)
