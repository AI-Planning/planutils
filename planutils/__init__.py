
import argparse, os


def setup():

    assert not_setup_yet(), "Error: planutils is already setup. Remove ~/.planutils to reset (warning: all cached planners will be lost)."

    print("\nCreating ~/.planutils...")
    os.mkdir(os.path.join(os.path.expanduser('~'), '.planutils'))
    os.mkdir(os.path.join(os.path.expanduser('~'), '.planutils', 'bin'))

    print("Adding bin folder to path (assuming ~/.bashrc exists)...")
    os.system('echo \'export PATH="$HOME/.planutils/bin:$PATH"\' >> ~/.bashrc')

    print("Installing planner scripts...")
    from planutils.planner_installation import PLANNERS
    for p in PLANNERS:
        script  = "#!/bin/bash\n"
        script += "echo\n"
        script += "echo 'Planner not installed!'\n"
        script += "read -p \"Download & install? [y/n] \" varchoice\n"
        script += "if [ $varchoice == \"y\" ]\n"
        script += "then\n"
        script += "  planutils --install " + p + "\n"
        script += "fi\n"
        script += "echo"
        with open(os.path.join(os.path.expanduser('~'), '.planutils', 'bin', p), 'w') as f:
            f.write(script)
        os.chmod(os.path.join(os.path.expanduser('~'), '.planutils', 'bin', p), 0o0755)


    print("\nAll set! Be sure to start a new bash session or update your PATH variable to include ~/.planutils/bin\n")

def not_setup_yet():
    return not os.path.exists(os.path.join(os.path.expanduser('~'), '.planutils'))

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--install",
                        help="install an individual or collection of planners ('list' shows the options)",
                        metavar="{planner or collection or list}")
    
    parser.add_argument("-s", "--setup", help="setup planutils for current user", action="store_true")
    
    args = parser.parse_args()

    if args.setup:
        setup()
    elif not_setup_yet():
        print("\nPlease run 'planutils --setup' before using utility.\n")
        exit()

    if args.install:
        from planutils.planner_installation import install
        install(args.install)
