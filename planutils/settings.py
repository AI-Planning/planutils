
import json, os

from planutils import manifest_converter

# This should eventually be changed once the prefix is customizable
PLANUTILS_PREFIX = os.path.join(os.path.expanduser('~'), '.planutils')

SETTINGS_FILE = os.path.join(PLANUTILS_PREFIX, 'settings.json')

def load():
    with open(SETTINGS_FILE, 'r') as f:
        settings = json.loads(f.read())
    return settings

def save(s):
    with open(SETTINGS_FILE, 'w') as f:
        f.write(json.dumps(s))
    manifest_converter.generate_manifest()
