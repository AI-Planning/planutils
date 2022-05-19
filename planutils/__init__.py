
import argparse, os
from pathlib import Path

from planutils import settings
from planutils.package_installation import PACKAGES


def minimal_setup():
    script_dir = Path(__file__).resolve().parent
    planutils_dir = Path(settings.PLANUTILS_PREFIX)
    if not planutils_dir.is_dir():
        print(f"Creating {planutils_dir}...")
        planutils_dir.mkdir()
        os.symlink(script_dir / "packages", planutils_dir / "packages")
        settings.save({'installed': []})


def setup():

    if setup_done():
        print("\nError: planutils is already setup. Setting up again will wipe all cached packages and settings.")
        if input("  Proceed? [y/N] ").lower() in ['y', 'yes']:
            os.system("rm -rf %s" % os.path.join(os.path.expanduser('~'), '.planutils'))
        else:
            return

    minimal_setup()
    os.mkdir(os.path.join(os.path.expanduser('~'), '.planutils', 'bin'))

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


    print("\nAll set! Use \"planutils activate\" to activate the environment, or run through \"planutils\" directly.\n")


def setup_done():
    return os.path.exists(os.path.join(os.path.expanduser('~'), '.planutils'))


def main():
    parser = argparse.ArgumentParser(prog="planutils")
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')

    parser_install = subparsers.add_parser('install', help='install package(s) such as a planner')
    parser_install.add_argument('-f', '--force', help='force reinstallation if the package is already installed', action='store_true')
    parser_install.add_argument('-y', '--yes', help='Answer yes to all user queries automatically', action='store_true')
    parser_install.add_argument('package', help='package name', nargs='+')

    parser_uninstall = subparsers.add_parser('uninstall', help='uninstall package(s)')
    parser_uninstall.add_argument('package', help='package name', nargs='+')

    parser_run = subparsers.add_parser('run', help='run package')
    parser_run.add_argument('package', help='package name')
    parser_run.add_argument('options', help='commandline options for the package', nargs="*")

    parser_checkinstalled = subparsers.add_parser('check-installed', help='check if a package is installed')
    parser_checkinstalled.add_argument('package', help='package name')

    parser_list = subparsers.add_parser('list', help='list the available packages')
    parser_setup = subparsers.add_parser('setup', help='setup planutils for current user')
    parser_upgrade = subparsers.add_parser('upgrade', help='upgrade all of the installed packages')

    args = parser.parse_args()

    if 'setup' == args.command:
        setup()
        return
    else:
        minimal_setup()

    if 'check-installed' == args.command:
        from planutils.package_installation import check_installed
        exit({True:0, False:1}[check_installed(args.package)])

    elif 'install' == args.command:
        from planutils.package_installation import install
        exit({True:0, False:1}[install(args.package, args.force, args.yes)])

    elif 'uninstall' == args.command:
        from planutils.package_installation import uninstall
        uninstall(args.package)

    elif 'run' == args.command:
        from planutils.package_installation import run
        run(args.package, args.options)

    elif 'list' == args.command:
        from planutils.package_installation import package_list
        package_list()

    elif 'upgrade' == args.command:
        from planutils.package_installation import upgrade
        upgrade()

    else:
        parser.print_help()
