
import argparse, os

from planutils import settings


def setup():

    assert not_setup_yet(), "Error: planutils is already setup. Remove ~/.planutils to reset (warning: all cached packages will be lost)."

    CUR_DIR = os.path.dirname(os.path.abspath(__file__))

    print("\nCreating ~/.planutils...")
    os.mkdir(os.path.join(os.path.expanduser('~'), '.planutils'))
    os.mkdir(os.path.join(os.path.expanduser('~'), '.planutils', 'bin'))

    settings.save({
        'installed': []
    })

    os.symlink(os.path.join(CUR_DIR, 'packages'),
               os.path.join(os.path.expanduser('~'), '.planutils', 'packages'))

    print("Adding bin folder to path (assuming ~/.bashrc exists)...")
    os.system("echo 'export PLANUTILS_PREFIX=\"~/.planutils\"' >> ~/.bashrc")
    os.system("echo 'export PATH=\"$PLANUTILS_PREFIX/bin:$PATH\"' >> ~/.bashrc")

    print("Installing package scripts...")
    from planutils.package_installation import PACKAGES
    for p in PACKAGES:
        script  = "#!/bin/bash\n"
        script += "if [ \"$(planutils --check_installed %s)\" == \"True\" ]\n" % p
        script += "then\n"
        script += "  ~/.planutils/packages/%s/run $@\n" % p
        script += "else\n"
        script += "  echo\n"
        script += "  echo 'Package not installed!'\n"
        script += "  read -p \"Download & install? [y/n] \" varchoice\n"
        script += "  if [ $varchoice == \"y\" ]\n"
        script += "  then\n"
        script += "    planutils --install " + p + "\n"
        script += "  fi\n"
        script += "  echo\n"
        script += "fi"
        with open(os.path.join(os.path.expanduser('~'), '.planutils', 'bin', p), 'w') as f:
            f.write(script)
        os.chmod(os.path.join(os.path.expanduser('~'), '.planutils', 'bin', p), 0o0755)


    print("\nAll set! Be sure to start a new bash session or update your PATH variable to include ~/.planutils/bin\n")

def not_setup_yet():
    return not os.path.exists(os.path.join(os.path.expanduser('~'), '.planutils'))

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--install",
                        help="install an individual package such as a planner ('list' shows the options)",
                        metavar="{package name}")
    
    parser.add_argument("-u", "--uninstall",
                        help="uninstall a package, and any dependencies that are no longer required ('list' shows those that are installed)",
                        metavar="{package name}")
    
    parser.add_argument("--check_installed", help="check if a package is installed")
    
    parser.add_argument("-s", "--setup", help="setup planutils for current user", action="store_true")
    
    args = parser.parse_args()

    if args.setup:
        setup()
    elif not_setup_yet():
        print("\nPlease run 'planutils --setup' before using utility.\n")
        exit()
    
    if args.check_installed:
        from planutils.package_installation import check_installed
        print(check_installed(args.check_installed))

    if args.install:
        from planutils.package_installation import install
        install(args.install)
    
    if args.uninstall:
        from planutils.package_installation import uninstall
        uninstall(args.uninstall)
