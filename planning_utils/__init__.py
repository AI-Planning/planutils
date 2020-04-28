
import argparse


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--install",
                        help="install an individual or collection of planners ('list' shows the options)",
                        metavar="{planner or collection or list}")
    
    args = parser.parse_args()

    if args.install:
        from planning_utils.planner_installation import install
        install(args.install)
