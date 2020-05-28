
import json, os, glob, subprocess


PACKAGES = {}

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

for conf_file in glob.glob(os.path.join(CUR_DIR, 'packages', '*')):
    base = os.path.basename(conf_file)
    if base not in ['README.md', 'TEMPLATE']:
        with open(os.path.join(conf_file, 'manifest.json'), 'r') as f:
            config = json.load(f)
        assert base not in PACKAGES, "Error: Duplicate package config -- %s" % base
        PACKAGES[base] = config


def install(target):
    if 'list' == target:
        print("\nPackages:")
        for p in PACKAGES:
            print(" - %s: %s" % (p, PACKAGES[p]['name']))
        print()
        return

    assert target in PACKAGES, "Error: Package not found -- %s" % target

    for dep in PACKAGES[target]['dependencies']:
        install(dep)
    
    subprocess.Popen('./install', cwd=os.path.join(CUR_DIR, 'packages', target))
