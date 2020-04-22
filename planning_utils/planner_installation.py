
import json, os

def install_planners(planner_set):
    raise NotImplementedError

def install_planner(planner):
    
    with open(os.path.join(os.path.abspath(__file__), 'planner_configs', planner), 'r') as f:
        details = json.loads(f.read())
    
    raise NotImplementedError
