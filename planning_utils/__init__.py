
import argparse

from planning_utils.planner_installation import install_planner, install_planners


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--install_planners", help="install a collection of planners ('list' shows the options)")
    
    args = parser.parse_args()

    if args.install_planners:
        install_planners(args.install_planners)
