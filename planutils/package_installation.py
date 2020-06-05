
import json, os, glob, subprocess
from collections import defaultdict

from planutils import settings

PACKAGES = {}

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

for conf_file in glob.glob(os.path.join(CUR_DIR, 'packages', '*')):
    base = os.path.basename(conf_file)
    if base not in ['README.md', 'TEMPLATE']:
        with open(os.path.join(conf_file, 'manifest.json'), 'r') as f:
            config = json.load(f)
        assert base not in PACKAGES, "Error: Duplicate package config -- %s" % base
        PACKAGES[base] = config
        PACKAGES[base]['runnable'] = os.path.exists(os.path.join(conf_file, 'run'))


def check_installed(target):
    return target in settings.load()['installed']


def uninstall(target):

    if target not in PACKAGES:
        print("Error: Package not found -- %s" % target)
        return

    if not check_installed(target):
        print("%s isn't installed." % target)
    else:
        print ("Uninstalling %s..." % target)
        s = settings.load()
        # map a package to all those that depend on it
        dependency_mapping = defaultdict(set)
        for p in s['installed']:
            for dep in PACKAGES[p]['dependencies']:
                dependency_mapping[dep].add(p)

        if target in dependency_mapping and len(dependency_mapping[target]) > 0:
            print("Error: Package is required for the following: %s" % ', '.join(dependency_mapping[target]))
            return
        subprocess.call('./uninstall', cwd=os.path.join(CUR_DIR, 'packages', target))
        s['installed'].remove(target)
        settings.save(s)

def package_list():
    print("\nPackages:")
    for p in PACKAGES:
        print(" - %s: %s (installed: %s)" % \
                (p, PACKAGES[p]['name'], str(check_installed(p))))
    print()

def install(target):

    if target not in PACKAGES:
        print("Error: Package not found -- %s" % target)
        return

    # Compute all those that will need to be installed
    done = set()
    to_check = [target]
    to_install = []
    while to_check:
        check = to_check.pop(0)
        if check not in done:
            done.add(check)
            if not check_installed(check):
                to_install.append(check)
                to_check.extend(PACKAGES[check]['dependencies'])

    to_install.reverse()

    if to_install:
        print("\nAbout to install the following packages: %s" % ', '.join(to_install))
        if input("  Proceed? [Y/n] ").lower() in ['', 'y', 'yes']:
            installed = []
            for package in to_install:
                print("Installing %s..." % package)
                try:
                    installed.append(package)
                    subprocess.call('./install', cwd=os.path.join(CUR_DIR, 'packages', package))
                except subprocess.CalledProcessError:
                    print("Error installing %s. Rolling back changes..." % package)
                    for p in installed:
                        subprocess.call('./uninstall', cwd=os.path.join(CUR_DIR, 'packages', p))
                    return

            s = settings.load()
            s['installed'].extend(installed)
            settings.save(s)
        else:
            print("Aborting installation.")
    else:
        print("%s is already installed." % target)

