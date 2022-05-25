
import json, os, glob, subprocess, sys, requests, time
from collections import defaultdict
from pathlib import Path

from planutils import settings

PACKAGES = {}

CUR_DIR = os.path.dirname(os.path.abspath(__file__))


def check_package(target, manifest):
    assert os.path.exists(manifest), "Error: Manifest must be defined for %s" % target
    with open(manifest, 'r') as f:
        config = json.load(f)
    for key in ['name', 'description', 'dependencies', 'install-size']:
        assert key in config, "Error: Manifest for %s must include '%s'" % (base, key)


for conf_file in glob.glob(os.path.join(CUR_DIR, 'packages', '*')):
    base = os.path.basename(conf_file)
    if base not in ['README.md', 'TEMPLATE']:
        assert base not in PACKAGES, "Error: Duplicate package config -- %s" % base
        check_package(base, os.path.join(conf_file, 'manifest.json'))
        with open(os.path.join(conf_file, 'manifest.json'), 'r') as f:
            config = json.load(f)
        PACKAGES[base] = config
        PACKAGES[base]['runnable'] = os.path.exists(os.path.join(conf_file, 'run'))


def check_installed(target):
    return target in settings.load()['installed']


def uninstall(targets):

    for target in targets:
        if target not in PACKAGES:
            print("Error: Package not found -- %s" % target)
            return

    to_check = []
    for target in targets:
        if check_installed(target):
            to_check.append(target)
        else:
            print("%s isn't installed." % target)

    if not to_check:
        return

    s = settings.load()
    # map a package to all those that depend on it
    dependency_mapping = defaultdict(set)
    for p in s['installed']:
        for dep in PACKAGES[p]['dependencies']:
            dependency_mapping[dep].add(p)

    # compute all the packages that will be removed
    to_remove = set()
    while to_check:
        check = to_check.pop(0)
        to_remove.add(check)
        to_check.extend(list(dependency_mapping[check]))

    print("\nAbout to remove the following packages: %s" % ', '.join(to_remove))
    if input("  Proceed? [y/N] ").lower() in ['y', 'yes']:
        for package in to_remove:
            print ("Uninstalling %s..." % package)
            subprocess.call('./uninstall', cwd=os.path.join(CUR_DIR, 'packages', package))
            print ("Finished uninstalling %s" % package)
            s['installed'].remove(package)

    # Search for any packages that may be no longer required
    dependency_mapping = defaultdict(set)
    for p in PACKAGES:
        for dep in PACKAGES[p]['dependencies']:
            dependency_mapping[dep].add(p)

    possible_deletions = [d for p in to_remove for d in PACKAGES[p]['dependencies']]
    while possible_deletions:
        package = possible_deletions.pop(0)
        # Consider removing if (1) it's installed; and (2) nothing that requires this is installed
        if (package in s['installed']) and (not any([p in s['installed'] for p in dependency_mapping[package]])):
            print("\nPackage may no longer be required: %s" % package)
            if input("  Remove? [y/N] ").lower() in ['y', 'yes']:
                print ("Uninstalling %s..." % package)
                subprocess.call('./uninstall', cwd=os.path.join(CUR_DIR, 'packages', package))
                print ("Finished uninstalling %s" % package)
                s['installed'].remove(package)
                possible_deletions.extend(PACKAGES[package]['dependencies'])

    settings.save(s)


def package_list():
    print("\nInstalled:")
    installed = set(settings.load()['installed'])
    for p in installed:
        print("  %s: %s" % (p, PACKAGES[p]['name']))

    print("\nAvailable:")
    for p in PACKAGES:
        if p not in installed:
            print("  %s: %s" % (p, PACKAGES[p]['name']))
    print()

def upgrade():
    s = settings.load()
    for package in s['installed']:
        print("Upgrading %s..." % package)
        subprocess.call('./uninstall', cwd=os.path.join(CUR_DIR, 'packages', package))
        subprocess.call('./install', cwd=os.path.join(CUR_DIR, 'packages', package))

def install(targets, forced=False, always_yes=False):
    for target in targets:
        if target not in PACKAGES:
            print("Error: Package not found -- %s" % target)
            return False

    # Compute all those that will need to be installed
    to_check = []
    for target in targets:
        if check_installed(target):
            if forced:
                to_check.append(target)
                print("%s is present, will be re-installed (forced installation)." % target)
            else:
                print("%s is present, not installed." % target)
        else:
            to_check.append(target)
            print("%s will be installed." % target)

    done = set()
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
        to_install_desc = ["%s (%s)" % (pkg, PACKAGES[pkg]['install-size']) for pkg in to_install]
        print("\nAbout to install the following packages: %s" % ', '.join(to_install_desc))

        if always_yes:
            user_response = True
        else:
            user_response = input("  Proceed? [Y/n] ").lower() in ['', 'y', 'yes']

        if user_response:
            installed = []
            for package in to_install:
                package_path = os.path.join(CUR_DIR, 'packages', package)
                print("Installing %s..." % package)
                try:
                    installed.append(package)
                    subprocess.check_call('./install', cwd=package_path, shell=True)
                    size = subprocess.check_output('du -sh .',
                                                   cwd=package_path,
                                                   shell=True,
                                                   encoding='utf-8').split('\t')[0]
                    print("Finished installing %s (size: %s)" % (package, size))
                except subprocess.CalledProcessError:
                    print("\nError installing %s. Rolling back changes..." % package)
                    for p in installed:
                        subprocess.call('./uninstall', cwd=os.path.join(CUR_DIR, 'packages', p))
                    return False

            s = settings.load()
            s['installed'].extend(installed)
            settings.save(s)
            return True
        else:
            print("Aborting installation.")
    else:
        print("Nothing left to install.")

    return False


def run(target, options):
    if target not in PACKAGES:
        sys.exit(f"Package {target} not found")
    if not check_installed(target):
        sys.exit(f"Package {target} is not installed")
    if not PACKAGES[target]["runnable"]:
        sys.exit(f"Package {target} is not executable")
    subprocess.run([Path(settings.PLANUTILS_PREFIX) / "packages" / target / "run"] + options)


def remote(target, options):

    # 1. check if the target is deployed

    package_url = settings.PAAS_SERVER + "/package"
    r = requests.get(package_url)
    remote_packages = r.json()

    remote_package = None
    for p in remote_packages:
        if p['package_name'] == target:
            remote_package = p
            break

    if (remote_package is None) or ('solve' not in remote_package['endpoint']['services']):
        sys.exit(f"Package {target} is not remotely deployed")


    # 2. unpack the options and target to the right json

    json_options = {}
    remote_call = remote_package['endpoint']['services']['solve']['call']
    call_parts = remote_call.split(' ')

    args = {arg['name']: arg for arg in remote_package['endpoint']['services']['solve']['args']}

    if len(options) != len(args):
        sys.exit(f"Call string does not match the remote call: {remote_package['endpoint']['services']['solve']['call']}")

    call_map = {}
    for i, step in enumerate(call_parts[1:]):
        if '{' == step[0] and '}' == step[-1]:
            option = step[1:-1]
            call_map[option] = options[i]
            if option not in args:
                sys.exit(f"Option {option} from call string is not defined in the remote call: {remote_call}")
            if args[option]['type'] == 'file':
                with open(options[i], 'r') as f:
                    json_options[option] = f.read()
            else:
                json_options[option] = options[i]

    rcall = remote_call
    for k, v in call_map.items():
        rcall = rcall.replace('{' + k + '}', v)
    print("\nMaking remote call: %s" % rcall)


    # 3. run the remote command

    solve_url = '/'.join([settings.PAAS_SERVER, 'package', target, 'solve'])
    r = requests.post(solve_url, json=json_options)
    if r.status_code != 200:
        sys.exit(f"Error running remote call: {r.text}")

    result_url = f"{settings.PAAS_SERVER}/{r.json()['result']}"

    # call every 0.5s until the result is ready
    result = None
    for _ in range(settings.PAAS_SERVER_LIMIT):
        r = requests.get(result_url)
        if (r.status_code == 200) and ('status' in r.json()) and (r.json()['status'] == 'ok'):
            result = r.json()['result']
            break
        time.sleep(0.5)

    if result is None:
        sys.exit(f"Error running remote call: {r.text}")


    # 4. unpack the results back to the client, including any new files

    result = r.json()['result']
    for fn in result['output']:
        with open(fn, 'w') as f:
            f.write(result['output'][fn])

    print("\n\t{stdout}\n")
    print(result['stdout'])
    print("\n\t{stderr}\n")
    print(result['stderr'])
