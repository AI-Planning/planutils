
import argparse, os


def setup():

    assert not_setup_yet(), "Error: planning-utils is already setup. Remove ~/.planning-utils to reset (warning: all cached planners will be lost)."

    print("\nCreating ~/.planning-utils...")
    os.mkdir(os.path.join(os.path.expanduser('~'), '.planning-utils'))
    os.mkdir(os.path.join(os.path.expanduser('~'), '.planning-utils', 'bin'))

    print("Adding bin folder to path (assuming ~/.bashrc exists)...")
    os.system('echo \'export PATH="$HOME/.planning-utils/bin:$PATH"\' >> ~/.bashrc')

    print("Installing planner scripts...")
    from planning_utils.planner_installation import PLANNERS
    for p in PLANNERS:
        script  = "#!/bin/bash\n"
        script += "echo\n"
        script += "echo 'Planner not installed!'\n"
        script += "read -p \"Download & install? [y/n] \" varchoice\n"
        script += "if [ $varchoice == \"y\" ]\n"
        script += "then\n"
        script += "  planning-utils --install " + p + "\n"
        script += "fi\n"
        script += "echo"
        with open(os.path.join(os.path.expanduser('~'), '.planning-utils', 'bin', p), 'w') as f:
            f.write(script)
        os.chmod(os.path.join(os.path.expanduser('~'), '.planning-utils', 'bin', p), 0o0755)


    print("\nAll set! Be sure to start a new bash session or update your PATH variable to include ~/.planning-utils/bin\n")

def not_setup_yet():
    return not os.path.exists(os.path.join(os.path.expanduser('~'), '.planning-utils'))

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
        print("\nPlease run 'planning-utils --setup' before using utility.\n")
        exit()

    if args.install:
        from planning_utils.planner_installation import install
        install(args.install)
