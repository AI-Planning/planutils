
import argparse, os


def setup():
    
    assert not_setup_yet(), "Error: planning-utils is already setup."

    print("Creating ~/.planning-utils...")
    os.mkdir(os.path.join('~', '.planning-utils'))
    os.mkdir(os.path.join('~', '.planning-utils', 'bin'))

    print("Adding bin folder to path (assuming ~/.bashrc exists)...")
    os.system('echo "export PATH=\\"$HOME/.planning-utils/bin:$PATH\\" >> ~/.bashrc')

def not_setup_yet():
    return not os.path.exists(os.path.join('~', '.planning-utils'))

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--install",
                        help="install an individual or collection of planners ('list' shows the options)",
                        metavar="{planner or collection or list}")
    
    parser.add_argument("-s", "--setup", help="setup planning-utils for current user", action="store_true")
    
    args = parser.parse_args()

    if args.setup:
        setup()
    elif not_setup_yet():
        print("Please run 'planning-utils --setup' before using utility.")
        exit()

    if args.install:
        from planning_utils.planner_installation import install
        install(args.install)
