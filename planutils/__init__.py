
import argparse, os

from planutils import settings
from planutils.package_installation import PACKAGES


def setup():

    if setup_done():
        print("\nError: planutils is already setup. Setting up again will wipe all cached packages and settings.")
        if input("  Proceed? [y/N] ").lower() in ['y', 'yes']:
            os.system("rm -rf %s" % os.path.join(os.path.expanduser('~'), '.planutils'))
        else:
            return

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
    with open(os.path.join(os.path.expanduser('~'), '.bashrc'), "a+") as f:
        f.write("export PLANUTILS_PREFIX=\"~/.planutils\"\n")
        f.write("export PATH=\"$PLANUTILS_PREFIX/bin:$PATH\"\n")

    print("Installing package scripts...")
    for p in PACKAGES:
        if PACKAGES[p]['runnable']:
            script  = "#!/bin/bash\n"
            script += "if $(planutils check-installed %s)\n" % p
            script += "then\n"
            script += "  ~/.planutils/packages/%s/run $@\n" % p
            script += "else\n"
            script += "  echo\n"
            script += "  echo 'Package not installed!'\n"
            script += "  read -r -p \"  Download & install? [Y/n] \" varchoice\n"
            script += "  varchoice=${varchoice,,}\n" # tolower
            script += "  if ! [[ \"$varchoice\" =~ ^(no|n)$ ]]\n"
            script += "  then\n"
            script += "    if planutils install %s;\n" % p
            script += "    then\n"
            script += "      echo 'Successfully installed %s!'\n" % p
            script += "      echo\n"
            script += "      echo \"Original command: %s $@\"\n" % p
            script += "      read -r -p \"  Re-run command? [Y/n] \" varchoice\n"
            script += "      varchoice=${varchoice,,}\n" # tolower
            script += "      if ! [[ \"$varchoice\" =~ ^(no|n)$ ]]\n"
            script += "      then\n"
            script += "        ~/.planutils/packages/%s/run $@\n" % p
            script += "      fi\n"
            script += "    fi\n"
            script += "  fi\n"
            script += "  echo\n"
            script += "fi\n"
            with open(os.path.join(os.path.expanduser('~'), '.planutils', 'bin', p), 'w') as f:
                f.write(script)
            os.chmod(os.path.join(os.path.expanduser('~'), '.planutils', 'bin', p), 0o0755)


    print("\nAll set! Be sure to start a new bash session or update your PATH variable to include ~/.planutils/bin\n")

def setup_done():
    return os.path.exists(os.path.join(os.path.expanduser('~'), '.planutils'))


def main():
    parser = argparse.ArgumentParser(prog="planutils")
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')

    parser_install = subparsers.add_parser('install', help='install package(s) such as a planner')
    parser_install.add_argument('-f', '--force', help='force installation', action='store_true')
    parser_install.add_argument('package', help='package name', nargs='+')

    parser_uninstall = subparsers.add_parser('uninstall', help='uninstall package(s)')
    parser_uninstall.add_argument('package', help='package name', nargs='+')

    parser_checkinstalled = subparsers.add_parser('check-installed', help='check if a package is installed')
    parser_checkinstalled.add_argument('package', help='package name')

    parser_list = subparsers.add_parser('list', help='list the available packages')
    parser_setup = subparsers.add_parser('setup', help='setup planutils for current user')
    parser_upgrade = subparsers.add_parser('upgrade', help='upgrade all of the installed packages')

    args = parser.parse_args()

    if 'setup' == args.command:
        setup()
    elif not setup_done():
        print("\nPlease run 'planutils setup' before using utility.\n")

    elif 'check-installed' == args.command:
        from planutils.package_installation import check_installed
        exit({True:0, False:1}[check_installed(args.package)])

    elif 'install' == args.command:
        from planutils.package_installation import install
        exit({True:0, False:1}[install(args.package, args.force)])

    elif 'uninstall' == args.command:
        from planutils.package_installation import uninstall
        uninstall(args.package)

    elif 'list' == args.command:
        from planutils.package_installation import package_list
        package_list()

    elif 'upgrade' == args.command:
        from planutils.package_installation import upgrade
        upgrade()

    else:
        parser.print_help()
